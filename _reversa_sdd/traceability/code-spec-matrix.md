# Code/Spec Matrix — PreceptorIA

> Gerado pelo **Writer** (Reversa) em 2026-07-20. Mapeia cada arquivo do legado à unit de spec que o cobre.
> Cobertura: 🟢 coberto integralmente · 🟡 coberto parcialmente · n/a sem unit (candidato a análise adicional)

## Código-fonte

| Arquivo do legado | Unit correspondente | Cobertura |
|---|---|---|
| `src/preceptor_ia/domain/models.py` | `gerar-ficha/` | 🟢 |
| `src/preceptor_ia/domain/ports.py` | `gerar-ficha/` | 🟢 |
| `src/preceptor_ia/domain/prompt.py` | `gerar-ficha/` (carga) + `analise-llm/` (conteúdo) | 🟢 |
| `src/preceptor_ia/application/gerar_ficha.py` | `gerar-ficha/` | 🟢 |
| `src/preceptor_ia/application/factory.py` | `gerar-ficha/` (T-08) + injeção condicional em `historico-local/` | 🟢 |
| `src/preceptor_ia/infra/transcricao_openai.py` | `transcricao-audio/` | 🟢 |
| `src/preceptor_ia/infra/analise_openai.py` | `analise-llm/` | 🟢 |
| `src/preceptor_ia/infra/historico.py` | `historico-local/` | 🟢 |
| `src/preceptor_ia/config.py` | `configuracao/` | 🟢 |
| `src/preceptor_ia/ui/app.py` | `interface-streamlit/` | 🟢 |
| `src/preceptor_ia/__init__.py` e `__init__.py` de subpacotes | — (vazios, estruturais) | n/a |

## Artefatos de comportamento e dados

| Arquivo do legado | Unit correspondente | Cobertura |
|---|---|---|
| `prompts/prompt-snapps-omp.md` | `analise-llm/` (estrutura no design, contrato de saída, Q1) | 🟢 |
| `demo/transcricao-simulada.md` | `interface-streamlit/` (RF-UI-03) | 🟢 |
| `demo/ficha-exemplo.md` | `interface-streamlit/` (RF-UI-04) | 🟢 |
| `.env.example` | `configuracao/` (T-04) | 🟢 |

## Testes

| Arquivo do legado | Unit correspondente | Cobertura |
|---|---|---|
| `tests/test_domain.py` | `gerar-ficha/` (TT-04) + `analise-llm/` (TT-06) | 🟢 |
| `tests/test_gerar_ficha.py` | `gerar-ficha/` (TT-01..05) | 🟢 |
| `tests/test_adaptadores.py` | `transcricao-audio/` + `analise-llm/` (TT-01..05 de cada) | 🟢 |
| `tests/test_historico.py` | `historico-local/` (TT-01..04) | 🟢 |

## Configuração de projeto e infraestrutura

| Arquivo do legado | Unit correspondente | Cobertura |
|---|---|---|
| `pyproject.toml`, `uv.lock` | — (documentados em [../dependencies.md](../dependencies.md)) | 🟡 |
| `.github/workflows/ci.yml` | — (documentado em [../inventory.md](../inventory.md); sem unit própria) | 🟡 |
| `.pre-commit-config.yaml` | — (idem) | 🟡 |
| `README.md`, `AGENTS.md`, `CLAUDE.md` | — (documentação, não comportamento) | n/a |

## Síntese de cobertura

- **Código executável:** 10/10 arquivos com unit correspondente — **100%**. 🟢
- **Artefatos de comportamento (prompt, demo, .env.example):** 4/4 — 100%. 🟢
- **Sem unit própria (aceito):** manifestos de build/CI/qualidade — cobertos por artefatos transversais (inventory, dependencies), não por specs de feature; `__init__.py` vazios.
- Nenhum arquivo de comportamento ficou sem spec; não há candidatos pendentes a análise adicional.
