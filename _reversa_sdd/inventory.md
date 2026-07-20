# Inventário — preceptor-ia

> Gerado pelo Scout (Reversa) em 2026-07-20.
> Confiança: 🟢 CONFIRMADO (extraído diretamente do código e dos manifestos).

## Visão geral

**PreceptorIA** é uma ferramenta de feedback formativo estruturado para preceptoria em Medicina de Família e Comunidade. Recebe o áudio (ou a transcrição colada) de uma passagem de caso entre residente e preceptor, transcreve via Whisper, aplica um prompt pedagógico baseado nos modelos SNAPPS e One-Minute Preceptor (OMP) e devolve uma ficha de feedback estruturada com evidências citadas da conversa. Produto técnico do Curso de Especialização em Preceptoria em MFC (Hospital Moinhos de Vento / PROADI-SUS).

## Estrutura de pastas

```
preceptor-ia/
├── .github/workflows/ci.yml        # CI: lint (ruff) + formato + pytest
├── demo/
│   ├── ficha-exemplo.md            # Ficha gerada ponta a ponta (contingência offline)
│   └── transcricao-simulada.md     # Caso simulado embutido no modo demonstração
├── prompts/
│   └── prompt-snapps-omp.md        # Prompt canônico — coração do produto
├── src/preceptor_ia/
│   ├── config.py                   # Settings (pydantic-settings), tudo via .env
│   ├── domain/                     # Camada de domínio — sem dependência de framework
│   │   ├── models.py               # Modelos e erros nomeados
│   │   ├── ports.py                # Protocols: ServicoTranscricao, ServicoAnalise, RepositorioHistorico
│   │   └── prompt.py               # Carregamento do prompt canônico
│   ├── application/                # Casos de uso
│   │   ├── gerar_ficha.py          # Caso de uso GerarFicha (orquestração)
│   │   └── factory.py              # Fábrica / composição de dependências
│   ├── infra/                      # Adaptadores
│   │   ├── transcricao_openai.py   # Whisper via API OpenAI-compatible (httpx)
│   │   ├── analise_openai.py       # LLM chat via API OpenAI-compatible (httpx)
│   │   └── historico.py            # Persistência opcional de fichas em filesystem
│   └── ui/
│       └── app.py                  # Página Streamlit (entry point)
├── tests/                          # 4 arquivos, rodam sem rede (dublês + HTTP mockado)
├── pyproject.toml                  # Manifesto (hatchling; deps pinadas)
├── uv.lock                         # Lock file commitado
├── .env.example                    # Modelo de configuração
└── .pre-commit-config.yaml         # Hooks de qualidade
```

## Linguagens

| Linguagem | Arquivos | Observação |
|---|---|---|
| Python | 19 (15 em `src/`, 4 em `tests/`) | ~861 linhas no total — projeto compacto |
| Markdown | 6 | README, prompt canônico, demo, docs de agente |
| TOML / YAML | 4 | pyproject, pre-commit, CI, lock |

**Linguagem principal:** Python (>= 3.12).

## Tecnologias e frameworks

- **Streamlit 1.59.2** — interface web (única página, `ui/app.py`).
- **httpx 0.28.1** — cliente HTTP dos adaptadores OpenAI-compatible.
- **pydantic-settings 2.14.2** — configuração via `.env`.
- **pytest 9.1.1** + **ruff 0.15.21** (dev).
- **Gerenciador de pacotes:** `uv` (lock file `uv.lock` commitado; build backend hatchling).

## Pontos de entrada

| Tipo | Caminho | Como executar |
|---|---|---|
| App (UI) | `src/preceptor_ia/ui/app.py` | `uv run streamlit run src/preceptor_ia/ui/app.py` |
| Configuração | `.env` (modelo em `.env.example`), `src/preceptor_ia/config.py` | variáveis `LLM_API_KEY` (obrigatória), `LLM_BASE_URL`, `LLM_MODEL`, `TRANSCRICAO_MODEL`, `HISTORICO_ATIVO`, `HISTORICO_DIR` |
| CI/CD | `.github/workflows/ci.yml` | push em `main` e PRs: `ruff check`, `ruff format --check`, `pytest` |
| Qualidade local | `.pre-commit-config.yaml` | hooks pre-commit |

Não há Dockerfile nem docker-compose.

## Integrações externas

| Integração | Adaptador | Protocolo |
|---|---|---|
| Groq (default) ou qualquer provedor OpenAI-compatible — chat completions | `infra/analise_openai.py` | HTTP REST via httpx |
| Groq/Whisper — transcrição de áudio | `infra/transcricao_openai.py` | HTTP REST via httpx |

## Banco de dados

Ausente. A única persistência é o histórico local opcional (`infra/historico.py`), gravado em filesystem fora do repositório (`~/.preceptor-ia/historico`), desligado por padrão. O Data Master não se aplica a este projeto.

## Testes

- **Framework:** pytest.
- **Arquivos:** `test_domain.py`, `test_gerar_ficha.py`, `test_adaptadores.py`, `test_historico.py` (4 arquivos, ~333 linhas).
- **Característica:** rodam sem rede — dublês para as portas e transporte httpx mockado.
- **Estimativa de cobertura:** alta em relação ao tamanho do código (razão testes/código ≈ 0,6); todas as camadas têm teste correspondente.

## Módulos identificados (para a Fase 2 — Escavação)

1. `domain` — modelos, erros, portas e prompt (regra de negócio pura).
2. `application` — caso de uso `GerarFicha` e fábrica.
3. `infra` — adaptadores de transcrição, análise e histórico.
4. `ui` — página Streamlit com três entradas (áudio, transcrição colada, demonstração).
5. `config` — settings via ambiente.
6. `prompts` — prompt canônico SNAPPS-OMP (artefato de comportamento, não código).
