# Arquitetura — PreceptorIA

> Gerado pelo **Architect** (Reversa) em 2026-07-20. Nível de documentação: **completo**.
> Escala: 🟢 CONFIRMADO · 🟡 INFERIDO · 🔴 LACUNA
>
> Artefatos-irmãos: [c4-context.md](c4-context.md) · [c4-containers.md](c4-containers.md) · [c4-components.md](c4-components.md) · [erd-complete.md](erd-complete.md) · [traceability/spec-impact-matrix.md](traceability/spec-impact-matrix.md)

## 1. Visão geral

PreceptorIA é um **monólito hexagonal compacto** (~861 linhas de Python) com um único caso de uso: transformar uma passagem de caso entre residente e preceptor em uma ficha de feedback formativo SNAPPS-OMP. A arquitetura segue portas-e-adaptadores de forma canônica (ADR-0002): domínio puro em stdlib, contratos como `typing.Protocol`, adaptadores HTTP confinados em `infra/`, UI Streamlit confinada em `ui/`, e um composition root manual (`factory.py`).

```
ui/app.py ──► application/gerar_ficha.py ──► domain (models, ports, prompt)
   │                    ▲                          ▲
   │            application/factory.py ────────────┤ implementa Protocols
   │                    │                          │
   └── erros de domínio │              infra/ (transcricao, analise, historico)
                     config.py
```

O traço arquitetural mais distintivo é o **prompt-as-data** (ADR-0003): o comportamento pedagógico — os modelos SNAPPS e OMP, as regras de fidelidade, o formato exato da ficha — vive em `prompts/prompt-snapps-omp.md`, não no código. O código é o encanamento; o prompt é o produto.

## 2. Decisões estruturais (síntese dos ADRs)

| ADR | Decisão | Efeito arquitetural |
|---|---|---|
| 0001 | Migração de n8n+Telegram para Python+Streamlit | Sistema local single-user; elimina infraestrutura de bot |
| 0002 | Arquitetura hexagonal | Domínio testável sem rede; adaptadores substituíveis |
| 0003 | Prompt canônico como dado | Comportamento pedagógico editável sem deploy |
| 0004 | Provedor OpenAI-compatible, default Groq | Troca de provedor via `.env`, zero acoplamento a SDK |
| 0005 | Não-retenção por padrão; histórico opt-in | Postura LGPD: áudio descartado, persistência só deliberada |
| 0006 | Contingência offline da demonstração | Demo funciona sem rede (caso simulado + ficha pré-gerada) |

## 3. Estilo e qualidades

| Qualidade | Como é atendida | Confiança |
|---|---|---|
| **Testabilidade** | Portas como Protocol + dublês; 4 arquivos de teste sem rede, razão teste/código ≈ 0,6 | 🟢 |
| **Substituibilidade** | Provedor de IA trocável por `.env`; qualquer adaptador substituível pelo contrato | 🟢 |
| **Erros barulhentos** | Hierarquia `ErroPreceptorIA` com 6 erros nomeados + `ErroConfiguracao`; mensagens orientadas ao usuário; nenhum stack trace na UI | 🟢 |
| **Privacidade** | Validação antes de qualquer chamada externa; áudio não retido; logs só de metadados; histórico opt-in fora do repo | 🟢 |
| **Reprodutibilidade** | `uv.lock` commitado, deps pinadas, CI com `uv sync --frozen` | 🟢 |
| **Observabilidade** | Logging estruturado chave=valor por etapa do pipeline | 🟢 |

## 4. Integrações externas

Uma única integração, com dois endpoints ([data-dictionary.md](data-dictionary.md) detalha os payloads):

| Endpoint | Adaptador | Formato | Particularidades |
|---|---|---|---|
| `POST {LLM_BASE_URL}/audio/transcriptions` | `TranscricaoOpenAICompat` | multipart | `language="pt"` fixo (RN-P1); timeout 120 s |
| `POST {LLM_BASE_URL}/chat/completions` | `AnaliseOpenAICompat` | JSON | `temperature=0.2` (RN-P2); system=prompt canônico, user=transcrição |

Erros HTTP são traduzidos centralmente em erros de domínio (401→`ErroCredencial`, 429→`ErroLimiteProvedor`, ≥400→`ErroServicoExterno`). Não há API produzida, webhook, fila nem evento. 🟢

## 5. Dados

Sem banco de dados. Três dataclasses imutáveis em memória (`Entrada`, `Transcricao`, `Ficha`) e um formato de persistência opcional (arquivo `.md` datestampado). ERD conceitual completo em [erd-complete.md](erd-complete.md). 🟢

## 6. Dívidas técnicas

Nenhuma dependência desatualizada, nenhum módulo sem teste, nenhum código duplicado relevante no tamanho atual. As dívidas reais são pontuais e pequenas:

| # | Dívida | Onde | Severidade | Confiança |
|---|---|---|---|---|
| DT-1 | Placeholder `{{transcricao}}` do prompt nunca interpolado — o LLM recebe o placeholder literal no system prompt (lacuna L2; possível resíduo do fluxo n8n) | `prompts/prompt-snapps-omp.md:102-104` vs `infra/analise_openai.py:31-34` | média (risco de confundir o modelo; divergência template×uso) | 🔴 validar intenção |
| DT-2 | Gravação de histórico sem isolamento de falha: IO quebrado aborta a entrega de ficha já gerada | `application/gerar_ficha.py:41-42` | baixa (histórico é opt-in) | 🟡 |
| DT-3 | Colisão de nome no histórico no mesmo minuto sobrescreve silenciosamente | `infra/historico.py:19-21` | baixa — **política decidida (2026-07-20): sufixar**; correção mapeada em `historico-local/tasks.md` T-02b | 🟢 [Revisão] |
| DT-4 | `_levantar_erro_nomeado` "privada" de um adaptador importada pelo outro — acoplamento interno entre módulos de infra | `infra/analise_openai.py` ← `infra/transcricao_openai.py:49-62` | baixa (extrair para módulo próprio) | 🟡 |
| DT-5 | `st.cache_resource` congela Settings por processo: mudar `.env` exige restart, sem aviso na UI | `ui/app.py:37-39` | baixa (documentar no README basta) | 🟡 |
| DT-6 | Rastreabilidade RF/RN/RD/D aponta para spec em outro repositório (`preceptoria-mfc`, feature `001-migracao-python-streamlit`) | comentários em todo o código | resolvida como lacuna: spec lida e verificada (L1 fechada em 2026-07-20); permanece a observação de manutenção — a fonte vive fora deste repo | 🟢 [Revisão] |

## 7. Riscos de evolução

- **Deploy multiusuário** 🟢 [Revisão 2026-07-20] — fora de escopo por decisão do autor: o produto é protótipo técnico para instalação local por cada preceptor (P2 de [permissions.md](permissions.md), resolvida). Se o escopo mudar, gate de acesso e isolamento de histórico viram Must.
- **Crescimento da UI** 🟡 — `ui/app.py` concentra 5 responsabilidades; é o primeiro arquivo a dividir se ganhar telas.
- **Prompt sem validação de procedência** 🟡 — quem edita o `.md` muda o comportamento clínico-pedagógico sem que o app valide nada (P3); aceitável localmente, relevante em cenário compartilhado.
