# Gerar Ficha, Design Técnico

> Gerado pelo **Writer** (Reversa) em 2026-07-20.
> Escala: 🟢 CONFIRMADO · 🟡 INFERIDO · 🔴 LACUNA

## Interface

| Símbolo | Assinatura | Retorno | Observação |
|---------|-----------|---------|------------|
| `GerarFicha.__init__` | `(prompt_sistema: str, transcricao: ServicoTranscricao, analise: ServicoAnalise, historico: RepositorioHistorico \| None = None)` | — | Dependências injetadas; `historico=None` significa opt-out |
| `GerarFicha.executar` | `(entrada: Entrada)` | `Ficha` | Levanta subclasses de `ErroPreceptorIA` em falha |
| `GerarFicha._obter_transcricao` | `(entrada: Entrada)` | `str` | Privado; despacha por origem |
| `montar_gerar_ficha` | `(settings: Settings \| None = None)` | `GerarFicha` | Composition root; `settings=None` → `carregar_settings()` |
| `Entrada` | `(origem: OrigemEntrada, nome_arquivo: str \| None = None, conteudo_audio: bytes \| None = None, texto_transcricao: str \| None = None)` | — | dataclass frozen; valida no `__post_init__` |
| `Ficha` | `(markdown: str, origem_entrada: OrigemEntrada, contexto: str \| None = None, gerada_em: datetime = now())` | — | dataclass frozen |
| `carregar_prompt` | `(caminho: Path = CAMINHO_PROMPT_PADRAO)` | `str` | Prompt com `strip()`; `ErroPromptCanonico` se ausente/vazio |

## Fluxo Principal

1. `executar` loga `etapa=ingestao origem=<valor>` (`gerar_ficha.py:30`).
2. `_obter_transcricao`: origem ≠ `AUDIO` → retorna `texto_transcricao.strip()`; origem `AUDIO` → loga `etapa=transcricao arquivo=<nome> bytes=<n>`, chama `transcricao.transcrever(conteudo, nome)` e retorna `resultado.texto.strip()` (`gerar_ficha.py:47-58`). O áudio não é usado após esse ponto (RN-07).
3. Loga `etapa=analise tamanho_transcricao=<len>` e chama `analise.analisar(prompt, texto)` (`gerar_ficha.py:33-34`).
4. Se `markdown` vazio/whitespace → `ErroRespostaAnalise` (`gerar_ficha.py:35-38`).
5. Constrói `Ficha(markdown=markdown.strip(), origem_entrada=entrada.origem)` — `contexto` fica `None` no fluxo atual (`gerar_ficha.py:40`).
6. Se `historico is not None` → `historico.gravar(ficha)` (`gerar_ficha.py:41-42`).
7. Loga `etapa=entrega origem=<valor>` e retorna a ficha (`gerar_ficha.py:44-45`).

## Fluxos Alternativos

- **Entrada inválida:** a exceção nasce no `__post_init__` da `Entrada` — `executar` nunca chega a rodar com entrada malformada (`models.py:50-72`).
- **Falha na transcrição/análise:** erros nomeados dos adaptadores (`ErroCredencial`, `ErroLimiteProvedor`, `ErroServicoExterno`, `ErroRespostaAnalise`) atravessam o caso de uso sem captura — propagação limpa até a UI. 🟢
- **Falha na gravação do histórico:** sem try/except — a exceção de IO aborta a entrega embora a ficha já exista em memória. 🟡

## Dependências

- `ServicoTranscricao` (porta) — somente para origem `AUDIO`.
- `ServicoAnalise` (porta) — sempre.
- `RepositorioHistorico` (porta, opcional) — injetado pela fábrica apenas se `historico_ativo=True`.
- `carregar_prompt` — a fábrica carrega o prompt uma vez e o injeta como string; o caso de uso não conhece filesystem.

## Decisões de Design Identificadas

| Decisão | Evidência no código | Confiança |
|---------|---------------------|-----------|
| Injeção de dependência manual via Protocols, sem container | `factory.py:11-20`, `ports.py` | 🟢 |
| Opt-out do histórico por injeção de `None` (decisão na fábrica, não no caso de uso) | `factory.py:19` | 🟢 |
| Validação como invariante de construção (dataclass frozen + `__post_init__`) | `models.py:41-72` | 🟢 |
| Prompt como parâmetro do construtor (string), não como dependência de arquivo | `gerar_ficha.py:17-24` | 🟢 |
| `assert` como guarda interna de tipo em `_obter_transcricao` (invariante já garantida pelo modelo) | `gerar_ficha.py:50` | 🟢 |

## Estado Interno

Nenhum estado mutável: os quatro atributos do caso de uso são fixados no construtor; modelos são frozen. Cada `executar` é independente. 🟢

## Observabilidade

Logger `preceptor_ia`, formato chave=valor: `etapa=ingestao origem=...` · `etapa=transcricao arquivo=... bytes=...` · `etapa=analise tamanho_transcricao=...` · `etapa=entrega origem=...`. Nunca loga conteúdo clínico. 🟢

## Riscos e Lacunas

- 🟡 Falha de IO do histórico aborta a entrega (sem isolamento); decidir se é intencional (DT-2 de [../architecture.md](../architecture.md)).
- 🟡 `Ficha.gerada_em` usa `datetime.now()` local sem timezone — nomes de arquivo e download dependem do relógio da máquina.
- 🔴 Códigos RF/RN/RD/D citados nos docstrings referenciam spec no repo `preceptoria-mfc` (feature `001-migracao-python-streamlit`), fora deste repositório (lacuna L1).
