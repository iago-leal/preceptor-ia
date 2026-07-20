# User Stories — Fluxo Gerar Ficha

> Gerado pelo **Writer** (Reversa) em 2026-07-20. Persona única: **Preceptor** (operador local — ver [../permissions.md](../permissions.md)).
> Escala: 🟢 CONFIRMADO · 🟡 INFERIDO · 🔴 LACUNA

## US-01 — Ficha a partir de áudio 🟢

**Como** preceptor de MFC, **quero** enviar a gravação da passagem de caso e receber uma ficha SNAPPS-OMP estruturada, **para** transformar a conversa em feedback formativo documentado sem trabalho manual.

**Critérios de aceite:**
- Formatos `.ogg/.mp3/.m4a/.wav` até 25 MB; fora disso, mensagem clara antes de qualquer envio.
- Progresso visível (ingestão → transcrição → análise).
- Ficha com evidências citadas da própria conversa; campos não identificáveis marcados "Não identificado na transcrição".
- Unit de referência: `interface-streamlit/` (RF-UI-01), `transcricao-audio/`, `analise-llm/`, `gerar-ficha/`.

## US-02 — Ficha a partir de transcrição colada 🟢

**Como** preceptor que já possui a transcrição (ex.: gerada por outro app), **quero** colá-la e gerar a ficha diretamente, **para** não depender de áudio nem repetir a transcrição.

**Critérios de aceite:**
- Texto vazio é rejeitado com orientação ("cole a transcrição da passagem de caso").
- Nenhuma chamada de transcrição ocorre; a análise recebe o texto como colado (com strip).
- Unit de referência: `interface-streamlit/` (RF-UI-02), `gerar-ficha/` (RF-GF-02).

## US-03 — Demonstração com caso simulado 🟢

**Como** preceptor apresentando a ferramenta (aula, banca do curso), **quero** gerar a ficha de um caso inteiramente simulado embutido, **para** demonstrar o produto sem expor nenhum dado real de paciente.

**Critérios de aceite:**
- Caso demo (hipertenso com má adesão, UBS) embutido no repositório; um clique gera a ficha real via provedor.
- Aviso explícito de que o caso é simulado.
- Unit de referência: `interface-streamlit/` (RF-UI-03).

## US-04 — Contingência offline da demonstração 🟢

**Como** preceptor demonstrando a ferramenta sem rede (ou com o provedor fora do ar), **quero** exibir uma ficha de exemplo pré-gerada, **para** que a demonstração nunca fique na mão do provedor de IA.

**Critérios de aceite:**
- Botão disponível apenas quando `demo/ficha-exemplo.md` existe; exibição sem nenhuma chamada externa.
- Unit de referência: `interface-streamlit/` (RF-UI-04), ADR-0006.

## US-05 — Download da ficha 🟢

**Como** preceptor, **quero** baixar a ficha em Markdown com nome datestampado, **para** arquivá-la ou anexá-la ao processo formativo do residente.

**Critérios de aceite:**
- Nome `{YYYYMMDDHHmm}-ficha-snapps-omp.md`; conteúdo idêntico ao exibido.
- Unit de referência: `interface-streamlit/` (RF-UI-07).

## US-06 — Histórico local opt-in 🟢

**Como** preceptor que decidiu guardar as fichas geradas, **quero** ativar o histórico local via configuração, **para** manter um arquivo das passagens de caso sem depender de download manual — sabendo que por padrão nada é retido.

**Critérios de aceite:**
- `HISTORICO_ATIVO=true` no `.env`; fichas gravadas em `~/.preceptor-ia/historico` (configurável), fora do repositório.
- Com a flag desligada (default), nenhuma persistência ocorre.
- Unit de referência: `historico-local/`.

## US-07 — Erros que orientam a ação 🟢

**Como** preceptor sem suporte técnico à mão, **quero** que toda falha me diga o que fazer (configurar chave, aguardar limite, checar rede), **para** resolver sozinho sem ler logs.

**Critérios de aceite:**
- Configuração ausente → "⚙️" citando `LLM_API_KEY` e o `.env.example`; falhas de provedor → "❌" nomeando a etapa e a ação sugerida; nunca stack trace. (Exceção conhecida: textarea vazio — ver risco 🔴 em `interface-streamlit/design.md`.)
- Unit de referência: `interface-streamlit/` (RF-UI-06), `configuracao/`, contratos das units de infra.

---

**Fora de escopo (não existem no código, não inventadas):** login/perfis, consulta ao histórico pela UI, edição da ficha na página, envio da ficha ao residente. 🟢
