# Flowchart — módulo `config`

> Archaeologist (Reversa), 2026-07-20. 🟢 CONFIRMADO a partir de `config.py`.

```mermaid
flowchart TD
    A[carregar_settings] --> B[Settings lê ambiente + .env<br/>extra=ignore]
    B -- validação ok --> R[Settings com defaults Groq]
    B -- falha ex.: LLM_API_KEY ausente --> E[ErroConfiguracao<br/>mensagem nomeia variável e aponta .env.example]
```

Precedência: variáveis de ambiente > `.env` > defaults de código (comportamento padrão do pydantic-settings). Único campo obrigatório: `LLM_API_KEY`.
