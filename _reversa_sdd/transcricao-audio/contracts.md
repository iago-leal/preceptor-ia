# Transcrição de Áudio, Contrato Externo

> Gerado pelo **Writer** (Reversa) em 2026-07-20. Contrato HTTP **consumido** (o sistema não expõe API própria).
> Escala: 🟢 CONFIRMADO · 🟡 INFERIDO · 🔴 LACUNA

## Endpoint consumido

`POST {LLM_BASE_URL}/audio/transcriptions` — padrão OpenAI Audio API; default `https://api.groq.com/openai/v1`. 🟢

### Requisição

| Elemento | Valor | Evidência |
|---|---|---|
| Header | `Authorization: Bearer {LLM_API_KEY}` | `transcricao_openai.py:30` |
| Corpo | `multipart/form-data` | `transcricao_openai.py:31-36` |
| Campo `file` | `(nome_arquivo, bytes do áudio)` | idem |
| Campo `model` | `Settings.transcricao_model` (default `whisper-large-v3-turbo`) | idem |
| Campo `language` | `"pt"` — fixo, nunca configurável (RN-02) | `transcricao_openai.py:34` |
| Campo `response_format` | `"json"` | `transcricao_openai.py:35` |
| Timeout | 120 s | `transcricao_openai.py:16,37` |

Pré-condições garantidas pelo domínio antes da chamada: extensão ∈ {`.ogg`, `.mp3`, `.m4a`, `.wav`}, tamanho ≤ 25 MB. 🟢

### Resposta esperada (2xx)

```json
{ "text": "<transcrição da passagem de caso>" }
```

Somente o campo `text` é lido; campos extras são ignorados. `text` vazio/ausente é tratado como falha. 🟢

### Mapeamento de erros → domínio

| Condição | Exceção | Mensagem (exata) |
|---|---|---|
| `httpx.HTTPError` (rede/timeout) | `ErroServicoExterno` | `Falha de rede na etapa de transcrição: {exc}` |
| HTTP 401 | `ErroCredencial` | `Credencial recusada na etapa de transcrição: confira LLM_API_KEY no .env.` |
| HTTP 429 | `ErroLimiteProvedor` | `Limite do provedor atingido na etapa de transcrição: aguarde alguns minutos ou configure outro provedor (LLM_BASE_URL).` |
| HTTP ≥ 400 (demais) | `ErroServicoExterno` | `Falha na etapa de transcrição (HTTP {status}): {corpo[:300]}` |
| 2xx com `text` vazio | `ErroServicoExterno` | `Etapa de transcrição devolveu texto vazio.` |

🟢 (`transcricao_openai.py:39-45,49-62`)

## Garantias de substituibilidade

Qualquer provedor que aceite este contrato (endpoint, multipart, campo `text` na resposta) funciona via `.env`, sem mudança de código — testado implicitamente pela suíte com transporte mockado. 🟢 Limitação: provedores cujo Whisper não aceite `language="pt"` ou `response_format="json"` quebrariam silenciosamente o contrato. 🟡
