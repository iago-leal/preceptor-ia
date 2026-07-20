# Dependências — preceptor-ia

> Gerado pelo Scout (Reversa) em 2026-07-20, a partir de `pyproject.toml` e `uv.lock`.
> Confiança: 🟢 CONFIRMADO.

## Runtime (pinadas em `pyproject.toml`)

| Pacote | Versão | Papel |
|---|---|---|
| streamlit | 1.59.2 | Interface web (camada `ui/`) |
| httpx | 0.28.1 | Cliente HTTP dos adaptadores OpenAI-compatible (camada `infra/`) |
| pydantic-settings | 2.14.2 | Configuração tipada via `.env` (`config.py`) |

## Desenvolvimento (`dependency-groups.dev`)

| Pacote | Versão | Papel |
|---|---|---|
| pytest | 9.1.1 | Testes |
| ruff | 0.15.21 | Lint + formatação (regras E, F, I, UP, B, SIM; linha 100) |

## Gestão

- **Gerenciador:** `uv`; `uv.lock` commitado → build determinístico (`uv sync --frozen` no CI).
- **Build backend:** hatchling; pacote em `src/preceptor_ia`.
- **Python:** >= 3.12.

## Observações de acoplamento

- A regra de negócio (`domain/`) não importa nenhuma dependência externa — apenas stdlib (`typing.Protocol`, dataclasses).
- `httpx` fica confinado a `infra/`; `streamlit` fica confinado a `ui/`.
- Trocar de provedor de IA não exige código: `LLM_BASE_URL` + `LLM_MODEL` + chave no `.env` (qualquer API OpenAI-compatible).
