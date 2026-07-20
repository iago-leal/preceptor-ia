# Análise de Código — preceptor-ia

> Gerado pelo Archaeologist (Reversa) em 2026-07-20. Nível: **completo**.
> Escala: 🟢 CONFIRMADO · 🟡 INFERIDO · 🔴 LACUNA.

## Visão do fluxo central

O sistema tem um único caso de uso, executado de ponta a ponta em memória:

```
Entrada (áudio | texto | demo)
  → [se áudio] ServicoTranscricao.transcrever() → Transcricao
  → ServicoAnalise.analisar(prompt_canonico, texto) → Markdown
  → Ficha (validada não-vazia)
  → [se historico_ativo] RepositorioHistorico.gravar(ficha)
  → exibição/download na UI
```

---

## Módulo `domain` 🟢

**Arquivos:** `src/preceptor_ia/domain/models.py` (88 l), `ports.py` (23 l), `prompt.py` (23 l).
**Propósito:** regra de negócio pura — modelos imutáveis, hierarquia de erros nomeados, contratos (Protocols) e carregador do prompt canônico. Sem dependência externa (somente stdlib).

### Estruturas de dados

| Entidade | Tipo | Campos |
|---|---|---|
| `Entrada` | dataclass frozen | `origem: OrigemEntrada`, `nome_arquivo: str\|None`, `conteudo_audio: bytes\|None`, `texto_transcricao: str\|None` |
| `Transcricao` | dataclass frozen | `texto: str`, `origem_servico: str` |
| `Ficha` | dataclass frozen | `markdown: str`, `origem_entrada: OrigemEntrada`, `contexto: str\|None`, `gerada_em: datetime` (default `now()`) |
| `OrigemEntrada` | StrEnum | `AUDIO`, `TEXTO`, `DEMO` |

### Hierarquia de erros (models.py:11-32)

```
ErroPreceptorIA (raiz)
├── ErroEntradaInvalida    — rejeição antes de qualquer chamada externa
├── ErroCredencial         — 401 do provedor
├── ErroLimiteProvedor     — 429 do provedor
├── ErroServicoExterno     — 5xx/timeout/rede; mensagem nomeia a etapa
├── ErroRespostaAnalise    — resposta vazia/malformada da análise
└── ErroPromptCanonico     — prompt ausente/vazio (definido em prompt.py)
```

`ErroConfiguracao` (config.py) é `RuntimeError`, **fora** da hierarquia — a UI o captura separadamente. 🟢

### Validação em `Entrada.__post_init__` (models.py:50-72)

- Origem `AUDIO`: exige `nome_arquivo` e `conteudo_audio`; extensão ∈ {`.ogg`, `.mp3`, `.m4a`, `.wav`} (case-insensitive, extraída por `rsplit(".", 1)`); tamanho ≤ 25 MB (`TAMANHO_MAXIMO_AUDIO_BYTES = 25 * 1024 * 1024`).
- Origens `TEXTO`/`DEMO`: exige `texto_transcricao` não-vazio após `strip()`.
- Toda violação levanta `ErroEntradaInvalida` com mensagem orientada ao usuário. Referências RD-01/RN-01/RF-01 nos docstrings. 🟢

### Contratos (ports.py)

| Protocol | Método | Implementação em infra |
|---|---|---|
| `ServicoTranscricao` | `transcrever(conteudo: bytes, nome_arquivo: str) -> Transcricao` | `TranscricaoOpenAICompat` |
| `ServicoAnalise` | `analisar(prompt_sistema: str, transcricao: str) -> str` | `AnaliseOpenAICompat` |
| `RepositorioHistorico` | `gravar(ficha: Ficha) -> None` | `HistoricoFilesystem` |

### Prompt canônico (prompt.py)

`carregar_prompt(caminho)` resolve por padrão `prompts/prompt-snapps-omp.md` na raiz do repositório (`parents[3]` a partir do arquivo). Falha barulhenta (`ErroPromptCanonico`) se ausente ou vazio. Padrão *prompt-as-data*: o comportamento pedagógico mora no `.md`, não no código (RF-04/RN-06). 🟢

---

## Módulo `application` 🟢

**Arquivos:** `application/gerar_ficha.py` (58 l), `factory.py` (20 l).
**Propósito:** orquestração do caso de uso e composition root.

### `GerarFicha.executar(entrada) -> Ficha` (gerar_ficha.py:29-45)

1. Log estruturado `etapa=ingestao origem=...`.
2. `_obter_transcricao`: se origem ≠ `AUDIO`, usa `texto_transcricao.strip()`; se `AUDIO`, chama a porta de transcrição e **descarta o áudio** dali em diante (comentário RN-07: não-retenção).
3. Chama `analise.analisar(prompt, texto)`; resposta vazia/whitespace → `ErroRespostaAnalise` (RN-03: não inventar ficha).
4. Constrói `Ficha(markdown.strip(), origem)`; grava no histórico **somente se** o repositório foi injetado (opt-in decidido na fábrica).
5. Log `etapa=entrega` e retorno.

Observação: a gravação do histórico não tem try/except próprio — uma falha de IO do histórico abortaria a entrega da ficha. 🟡 (comportamento implícito, não documentado como intencional)

### `montar_gerar_ficha(settings=None)` (factory.py:11-20)

Único ponto que conhece configuração + infraestrutura: carrega `Settings`, o prompt canônico, instancia os dois adaptadores HTTP com `(base_url, api_key, modelo)` e injeta `HistoricoFilesystem` apenas quando `historico_ativo=True`. Injeção de dependência manual, sem container. 🟢

---

## Módulo `infra` 🟢

**Arquivos:** `infra/transcricao_openai.py` (62 l), `analise_openai.py` (50 l), `historico.py` (27 l).
**Propósito:** adaptadores concretos das três portas.

### `TranscricaoOpenAICompat.transcrever`

- `POST {base_url}/audio/transcriptions` (multipart: `file`, `model`, `language="pt"`, `response_format="json"`), timeout 120 s.
- `language="pt"` fixo — RN-02: jargões da APS brasileira. 🟢
- Erros de rede → `ErroServicoExterno`; HTTP mapeado por `_levantar_erro_nomeado` (ver abaixo); `text` vazio → `ErroServicoExterno`.
- `Transcricao.origem_servico = "{base_url}#{modelo}"`.

### `AnaliseOpenAICompat.analisar`

- `POST {base_url}/chat/completions` com `temperature=0.2` (RN-03: fidelidade > criatividade) e mensagens `system` (prompt canônico) + `user` (transcrição), timeout 120 s.
- Parse defensivo de `choices[0].message.content`: `KeyError/IndexError/ValueError` → `ErroRespostaAnalise`; conteúdo vazio → `ErroRespostaAnalise`.

### `_levantar_erro_nomeado(resposta, etapa)` (transcricao_openai.py:49-62)

Tradução centralizada de status HTTP em erros de domínio: 401 → `ErroCredencial`, 429 → `ErroLimiteProvedor`, ≥400 → `ErroServicoExterno` (com corpo truncado em 300 chars). Compartilhada pelos dois adaptadores (import cruzado de função "privada" entre módulos de infra — funcional, mas acoplamento interno digno de nota). 🟡

### `HistoricoFilesystem.gravar`

- Cria o diretório (`mkdir parents=True exist_ok=True`), nomeia `{YYYYMMDDHHmm}-ficha-{slug}.md` (slug de `contexto` ou da origem; `_slug` normaliza para `[a-z0-9-]`, fallback `"sem-contexto"`), grava o Markdown com newline final.
- Colisão de nome no mesmo minuto sobrescreve o arquivo anterior. 🟡 (não tratado; janela improvável em uso real)

---

## Módulo `config` 🟢

**Arquivo:** `config.py` (32 l).

`Settings(BaseSettings)` lê `.env` (`extra="ignore"`): `llm_api_key` (obrigatória, `min_length=1`), `llm_base_url` (default Groq), `llm_model` (`llama-3.3-70b-versatile`), `transcricao_model` (`whisper-large-v3-turbo`), `historico_ativo` (False), `historico_dir` (`~/.preceptor-ia/historico`). `carregar_settings()` converte qualquer falha de validação em `ErroConfiguracao` com mensagem que nomeia a variável e aponta o `.env.example` (RF-05: falha barulhenta).

---

## Módulo `ui` 🟢

**Arquivo:** `ui/app.py` (113 l). Página única Streamlit.

### Fluxo

1. `st.set_page_config` + título + **aviso de privacidade fixo** (LGPD: não-retenção, casos simulados em demo pública, responsabilidade do preceptor).
2. Três abas → três origens: upload de áudio (`type=["ogg","mp3","m4a","wav"]`), textarea, demo (lê `demo/transcricao-simulada.md`). Cada botão apenas deposita `Entrada` em `st.session_state["entrada_pendente"]`.
3. Fora das abas, o pendente é consumido (`pop`) e processado por `_gerar`; `ErroConfiguracao` → `st.error("⚙️ ...")`, `ErroPreceptorIA` → `st.error("❌ ...")`.
4. Ficha em `session_state` é renderizada com botão de download (`{timestamp}-ficha-snapps-omp.md`).

### Algoritmos notáveis

- **Deduplicação por hash** (`_gerar`, app.py:43-48): chave SHA-256 de `origem + texto + bytes do áudio`; se igual à última processada na sessão, não repete chamadas externas (proteção contra reruns do Streamlit). 🟢
- **Cache do caso de uso**: `@st.cache_resource` em `_caso_de_uso()` — a fábrica roda uma vez por processo; mudanças no `.env` exigem restart. 🟡 (implicação, não documentada)
- **Contingência offline**: botão extra na aba demo exibe `demo/ficha-exemplo.md` sem nenhuma chamada externa (plano B de demonstração). 🟢
- Indicador de progresso: `st.status` com etapas exibidas condicionalmente (áudio mostra "ingestão, transcrição"; texto só "ingestão").

---

## Artefato `prompts` 🟢

**Arquivo:** `prompts/prompt-snapps-omp.md` (105 l). Não é código: é o **comportamento pedagógico como dado**.

- Define os dois modelos de referência (SNAPPS com 6 elementos; OMP com 5 microhabilidades) e o formato exato da ficha de saída (cabeçalho, seções 1-3).
- Regras de fidelidade embutidas: registrar apenas o identificável na transcrição; campo não identificável recebe literal `"Não identificado na transcrição"`; exigência de citações literais como evidência; campos administrativos ausentes → `"A preencher"`.
- Termina com o placeholder `{{transcricao}}` — porém o código envia a transcrição como mensagem `user` separada e **não substitui o placeholder**; o template chega ao modelo com o `{{transcricao}}` literal no final do system prompt. 🔴 LACUNA: divergência entre o desenho do template e o uso real (inócua na prática, mas merece validação humana — ou remover o placeholder, ou interpolar).

---

## Testes (contexto para o Reviewer)

4 arquivos, ~333 linhas, sem rede: `test_domain.py` (validações de `Entrada` e prompt), `test_gerar_ficha.py` (caso de uso com dublês), `test_adaptadores.py` (httpx com transporte mockado), `test_historico.py` (filesystem em tmp). Razão teste/código ≈ 0,6. 🟢

## Síntese de complexidade

| Módulo | Complexidade | Risco |
|---|---|---|
| domain | baixa | — |
| application | baixa | histórico sem isolamento de falha 🟡 |
| infra | baixa-média | colisão de nome no histórico 🟡; helper compartilhado entre adaptadores 🟡 |
| ui | média (estado de sessão Streamlit) | cache resource segura config antiga 🟡 |
| config | baixa | — |
| prompts | n/a | placeholder `{{transcricao}}` não interpolado 🔴 |
