# Configuração, Design Técnico

> Gerado pelo **Writer** (Reversa) em 2026-07-20.
> Escala: 🟢 CONFIRMADO · 🟡 INFERIDO · 🔴 LACUNA

## Interface

| Símbolo | Assinatura | Retorno | Observação |
|---------|-----------|---------|------------|
| `Settings` | `BaseSettings` com 6 campos | — | `model_config = SettingsConfigDict(env_file=".env", extra="ignore")` |
| `carregar_settings` | `()` | `Settings` | Envelopa qualquer exceção em `ErroConfiguracao` |
| `ErroConfiguracao` | `RuntimeError` | — | Fora da hierarquia `ErroPreceptorIA` (deliberado 🟡) |

Campos (nome interno → env var, tipo, default):

| Campo | Env var | Tipo | Default |
|---|---|---|---|
| `llm_api_key` | `LLM_API_KEY` | `str`, `Field(min_length=1)` | — (obrigatória) |
| `llm_base_url` | `LLM_BASE_URL` | `str` | `https://api.groq.com/openai/v1` |
| `llm_model` | `LLM_MODEL` | `str` | `llama-3.3-70b-versatile` |
| `transcricao_model` | `TRANSCRICAO_MODEL` | `str` | `whisper-large-v3-turbo` |
| `historico_ativo` | `HISTORICO_ATIVO` | `bool` | `False` |
| `historico_dir` | `HISTORICO_DIR` | `Path` | `Path.home() / ".preceptor-ia" / "historico"` |

🟢 (`config.py:13-21`; mapeamento env var por convenção case-insensitive do pydantic-settings)

## Fluxo Principal

1. `carregar_settings()` tenta `Settings()` (`config.py:27`).
2. Pydantic resolve, na ordem de precedência: argumentos > variáveis de ambiente > `.env` > defaults. 🟢
3. Qualquer exceção (`ValidationError` ou outra) → `ErroConfiguracao("Configuração incompleta: defina LLM_API_KEY no ambiente ou no arquivo .env (modelo em .env.example). Detalhe: " + str(exc))` com `from exc` (`config.py:28-32`).

## Fluxos Alternativos

- **`.env` ausente:** não é erro — pydantic-settings segue para variáveis de ambiente e defaults; só a falta de `LLM_API_KEY` falha. 🟢
- **Consumo pela fábrica:** `montar_gerar_ficha(settings=None)` chama `carregar_settings()`; testes injetam `Settings` construída manualmente. 🟢

## Dependências

- `pydantic` (`Field`) e `pydantic-settings` 2.14.2 — única unit com dependência externa fora de httpx/streamlit. 🟢

## Decisões de Design Identificadas

| Decisão | Evidência no código | Confiança |
|---------|---------------------|-----------|
| Mensagem de erro fixa cita sempre `LLM_API_KEY` (a única obrigatória), com o detalhe pydantic anexado para outros casos | `config.py:29-31` | 🟢 |
| `extra="ignore"`: `.env` pode conter variáveis de outros apps | `config.py:14` | 🟢 |
| Sem singleton: cada chamada de `carregar_settings()` relê o ambiente; o cache efetivo é o `st.cache_resource` da UI, uma camada acima | `config.py:24-27`, `ui/app.py:37-39` | 🟢 |

## Estado Interno

Nenhum (instância imutável na prática; pydantic BaseSettings). 🟢

## Observabilidade

Nenhum log próprio; a falha se manifesta como `ErroConfiguracao` exibido pela UI com prefixo ⚙️. 🟢

## Riscos e Lacunas

- 🟡 A mensagem cita `LLM_API_KEY` mesmo quando a falha for de outro campo (ex.: `HISTORICO_ATIVO=talvez` não coercível) — o detalhe pydantic esclarece, mas a primeira linha pode enganar.
- 🟡 `env_file=".env"` é relativo ao diretório de execução: rodar o Streamlit fora da raiz do repositório ignora o `.env` silenciosamente (mitigado pela instrução de execução no README).
