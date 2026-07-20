# Domínio — PreceptorIA

> Gerado pelo **Detective** (Reversa) em 2026-07-20.
> Escala de confiança: 🟢 CONFIRMADO (extraído do código) · 🟡 INFERIDO (padrões, pode estar errado) · 🔴 LACUNA (requer validação humana).

## 1. Propósito do sistema

Ferramenta de **feedback formativo estruturado** para preceptoria em Medicina de Família e Comunidade (MFC). Recebe uma passagem de caso entre residente e preceptor (áudio, transcrição colada ou caso demo), transcreve quando necessário, aplica o prompt pedagógico SNAPPS-OMP via LLM e devolve uma ficha de feedback em Markdown com evidências citadas da própria conversa. 🟢 (`README.md:5`, `src/preceptor_ia/ui/app.py:22-25`)

Produto técnico do Curso de Especialização em Preceptoria em MFC (Hospital Moinhos de Vento / PROADI-SUS), tipologia CAPES TIC. 🟢 (`README.md:7`)

## 2. Glossário de domínio

| Termo | Definição | Confiança |
|---|---|---|
| **Passagem de caso** | Conversa clínico-pedagógica em que o residente apresenta um caso ao preceptor; é o insumo bruto do sistema (áudio ou texto). | 🟢 |
| **Preceptor** | Médico que supervisiona o residente; usuário-alvo da ferramenta e responsável legal pelo conteúdo enviado ao provedor de IA (LGPD). | 🟢 (`ui/app.py:27-34`) |
| **Residente** | Médico em formação que apresenta o caso; sujeito avaliado na ficha. | 🟢 |
| **SNAPPS** | Modelo de apresentação do residente em 6 passos: Sumarizar, Narrowing, Analisar, Perguntar, Planejar, Selecionar. | 🟢 (`prompts/prompt-snapps-omp.md:6-13`) |
| **One-Minute Preceptor (OMP)** | Modelo do feedback do preceptor em 5 microhabilidades: comprometimento, sondagem de evidências, ensino de regras gerais, reforço positivo, correção de erros. | 🟢 (`prompts/prompt-snapps-omp.md:15-20`) |
| **Ficha (de Feedback Estruturado)** | Documento Markdown gerado pelo LLM no formato SNAPPS-OMP; entidade central de saída (`Ficha`). | 🟢 (`domain/models.py:81-88`) |
| **Prompt canônico** | Arquivo `prompts/prompt-snapps-omp.md`; fonte única do comportamento pedagógico — editá-lo muda a ferramenta sem tocar em código ("prompt-as-data"). | 🟢 (`domain/prompt.py`, `README.md:16`) |
| **Entrada** | Pedido de geração de ficha; três origens: `AUDIO`, `TEXTO`, `DEMO`. | 🟢 (`domain/models.py:35-48`) |
| **Transcrição** | Texto da passagem de caso, obtido via serviço Whisper (áudio) ou fornecido diretamente (texto/demo). | 🟢 |
| **Histórico** | Persistência local opcional das fichas em `.md` datestampado; desligada por padrão. | 🟢 (`infra/historico.py`) |
| **Contingência offline** | Ficha de exemplo pré-gerada (`demo/ficha-exemplo.md`) exibível sem nenhuma chamada externa; rede de segurança para demonstrações. | 🟢 (`ui/app.py:89-93`) |
| **APS / UBS** | Atenção Primária à Saúde / Unidade Básica de Saúde; contexto clínico típico dos casos (justifica o idioma fixo `pt` na transcrição). | 🟢 (`infra/transcricao_openai.py:34`) |

## 3. Regras de negócio

Os códigos `RF-NN`/`RN-NN`/`RD-NN`/`D-NN` aparecem em comentários do código e referenciam a spec da feature `001-migracao-python-streamlit` no repositório `preceptoria-mfc`. 🟢 **[Revisão 2026-07-20] Rastreabilidade fechada:** com autorização do autor, a spec foi lida em `~/dev/preceptoria-mfc/_reversa_forward/001-migracao-python-streamlit/` — RF-01..RF-09 e RN-01..RN-08 em `requirements.md`, RD-01..RD-05 herdados da extração do legado n8n, e D-07 em `roadmap.md` (decisão: histórico opcional como Markdown datestampado, desligado por padrão). Todos os códigos citados no código conferem com a spec de origem.

### Validação de entrada (antes de qualquer chamada externa)

| ID | Regra | Evidência | Confiança |
|---|---|---|---|
| RN-V1 (RD-01/RN-01) | Entrada de texto ou demo deve ter transcrição não-vazia (strip). | `domain/models.py:53-56` | 🟢 |
| RN-V2 (RF-01) | Áudio aceito apenas em `.ogg`, `.mp3`, `.m4a`, `.wav` (extensão case-insensitive). | `domain/models.py:7,64-68` | 🟢 |
| RN-V3 (RF-01) | Áudio limitado a 25 MB (limite do contrato de transcrição). | `domain/models.py:8,69-72` | 🟢 |
| RN-V4 | Entrada de áudio exige nome de arquivo **e** conteúdo. | `domain/models.py:59-60` | 🟢 |
| RN-V5 | A validação ocorre na construção do objeto (`__post_init__` de dataclass congelada): não existe `Entrada` inválida em circulação. | `domain/models.py:50-56` | 🟢 |

### Pipeline de geração

| ID | Regra | Evidência | Confiança |
|---|---|---|---|
| RN-P1 (RN-02) | Transcrição com idioma fixo `pt` — jargões da APS brasileira. | `infra/transcricao_openai.py:34` | 🟢 |
| RN-P2 (RN-03) | Análise com `temperature=0.2`: fidelidade, não criatividade. | `infra/analise_openai.py:13` | 🟢 |
| RN-P3 (RN-03) | Resposta de análise vazia ou malformada **não** vira ficha (`ErroRespostaAnalise`): o sistema prefere falhar a inventar. | `application/gerar_ficha.py:35-38`, `infra/analise_openai.py:43-50` | 🟢 |
| RN-P4 (RN-07) | O áudio não é retido após a transcrição; daqui em diante só o texto circula. | `application/gerar_ficha.py:57` | 🟢 |
| RN-P5 (RF-04/RN-06) | Prompt canônico é fonte única e obrigatória; ausência ou vazio é falha fatal (`ErroPromptCanonico`). | `domain/prompt.py:14-23` | 🟢 |
| RN-P6 | Transcrição que devolve texto vazio é erro de serviço externo (não segue para análise). | `infra/transcricao_openai.py:44-45` | 🟢 |
| RN-P7 | Timeout de 120 s por chamada externa (transcrição e análise). | `infra/transcricao_openai.py:16`, `infra/analise_openai.py:12` | 🟢 |
| RN-P8 | A transcrição vai ao LLM como mensagem `user` separada; o prompt de sistema vai íntegro. | `infra/analise_openai.py:31-34` | 🟢 |

### Regras pedagógicas (vivem no prompt, não no código)

| ID | Regra | Evidência | Confiança |
|---|---|---|---|
| RN-F1 | Nada é inferido além do dito: campo não identificável recebe "Não identificado na transcrição". | `prompts/prompt-snapps-omp.md:26,32` | 🟢 |
| RN-F2 | Cada elemento encontrado exige citação literal da transcrição como evidência. | `prompts/prompt-snapps-omp.md:27` | 🟢 |
| RN-F3 | A ficha sugere pontos de melhoria para **ambos** os papéis (residente e preceptor). | `prompts/prompt-snapps-omp.md:28` | 🟢 |
| RN-F4 | ⚠️ O template termina com `## Transcrição recebida\n{{transcricao}}`, mas o código **não interpola** esse placeholder (a transcrição vai como mensagem `user`). O LLM recebe o placeholder literal no prompt de sistema. Comportamento provavelmente acidental — ou o placeholder é resíduo do fluxo n8n anterior. | `prompts/prompt-snapps-omp.md:102-104` vs. `infra/analise_openai.py:31-34` | 🟡 |

### Configuração e operação

| ID | Regra | Evidência | Confiança |
|---|---|---|---|
| RN-C1 (RF-05) | Única variável obrigatória é `LLM_API_KEY`; falta de configuração falha barulhento nomeando a variável. | `config.py:16,24-32` | 🟢 |
| RN-C2 (RF-05) | Provedor de IA trocável sem código: default Groq, qualquer endpoint OpenAI-compatible via `LLM_BASE_URL`. | `config.py:17-19`, `README.md:48` | 🟢 |
| RN-C3 (RF-07) | Histórico é **opt-in** (`HISTORICO_ATIVO=false` por padrão); quando desligado, o repositório nem é injetado no caso de uso. | `config.py:20`, `application/factory.py:19` | 🟢 |
| RN-C4 (D-07) | Ficha gravada como `<YYYYMMDDHHmm>-ficha-<slug>.md` fora do repositório (`~/.preceptor-ia/historico`). | `infra/historico.py:16-21`, `config.py:21` | 🟢 |
| RN-C5 | Duas fichas geradas no mesmo minuto com o mesmo contexto sobrescrevem o mesmo arquivo (sem sufixo de desambiguação). | `infra/historico.py:19-21` | 🟡 |
| RN-C6 | Erros HTTP mapeados em erros nomeados: 401→`ErroCredencial`, 429→`ErroLimiteProvedor`, ≥400→`ErroServicoExterno`; a mensagem sempre nomeia a etapa e sugere ação ao usuário. | `infra/transcricao_openai.py:49-62` | 🟢 |
| RN-C7 | Logging estruturado chave=valor por etapa (`etapa=ingestao/transcricao/analise/entrega/historico`); nunca loga conteúdo clínico, só metadados (origem, tamanho, nome de arquivo). | `application/gerar_ficha.py:30-53`, `infra/historico.py:22` | 🟢 |

### Interface e privacidade

| ID | Regra | Evidência | Confiança |
|---|---|---|---|
| RN-U1 | Deduplicação por SHA-256 (origem + texto + bytes do áudio): a mesma entrada na mesma sessão não repete chamadas externas. | `ui/app.py:43-48` | 🟢 |
| RN-U2 | Aviso de privacidade LGPD permanente: não-retenção, casos simulados em demos públicas, anonimização como responsabilidade do preceptor. | `ui/app.py:27-34` | 🟢 |
| RN-U3 | O caso demo é inteiramente simulado (hipertenso com má adesão, UBS) — nenhum dado real. | `ui/app.py:80-83`, `demo/transcricao-simulada.md` | 🟢 |
| RN-U4 | Contingência offline: botão que exibe `demo/ficha-exemplo.md` sem chamada externa alguma (o botão só aparece se o arquivo existir). | `ui/app.py:89-93` | 🟢 |
| RN-U5 | Erros de configuração (⚙️) e de domínio (❌) são exibidos com prefixos distintos; nenhum stack trace chega ao usuário. | `ui/app.py:99-102` | 🟢 |
| RN-U6 | Download da ficha como `.md` datestampado, espelhando a convenção do histórico. | `ui/app.py:108-113` | 🟢 |

## 4. Hierarquia de erros nomeados

```
ErroPreceptorIA (raiz)
├── ErroEntradaInvalida    — rejeição antes de qualquer chamada externa
├── ErroCredencial         — 401 do provedor
├── ErroLimiteProvedor     — 429 do provedor
├── ErroServicoExterno     — 5xx/timeout/rede; mensagem nomeia a etapa
├── ErroRespostaAnalise    — resposta vazia/malformada (não inventar ficha)
└── ErroPromptCanonico     — prompt canônico ausente ou vazio
ErroConfiguracao (RuntimeError, fora da hierarquia)
```
🟢 (`domain/models.py:11-32`, `domain/prompt.py:10-11`, `config.py:9-10`)

🟡 `ErroConfiguracao` herda de `RuntimeError`, não de `ErroPreceptorIA` — por isso a UI o captura em bloco separado (`ui/app.py:99-100`). Provável decisão deliberada (configuração precede o domínio), mas não documentada.

## 5. Lacunas 🔴

| # | Lacuna | Impacto |
|---|---|---|
| ~~L1~~ | ✅ **Resolvida (2026-07-20):** spec de origem lida e verificada em `~/dev/preceptoria-mfc/_reversa_forward/001-migracao-python-streamlit/` — todos os códigos conferem. | Rastreabilidade requisito→código completa. 🟢 |
| L2 | O placeholder `{{transcricao}}` do prompt não é interpolado (RN-F4): intencional ou resíduo? Autor respondeu "não sei" (2026-07-20) — permanece aberta em `gaps.md`. | Se residual, o prompt de sistema contém uma seção morta que pode confundir o LLM. |
| ~~L3~~ | ✅ **Resolvida (2026-07-20):** política decidida — **sufixar** em colisão; a sobrescrita do legado vira correção na reimplementação (`historico-local/tasks.md` T-02b). 🟢 | Nenhuma ficha perdida na política nova. |
| L4 | Não há logs de produção no repositório para análise (aplicação local, sem agregação). | Análise de logs do Detective sem objeto; eventos monitorados foram inferidos do código. |
