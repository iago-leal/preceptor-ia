# Análise LLM, Contrato Externo

> Gerado pelo **Writer** (Reversa) em 2026-07-20. Contrato HTTP **consumido**.
> Escala: 🟢 CONFIRMADO · 🟡 INFERIDO · 🔴 LACUNA

## Endpoint consumido

`POST {LLM_BASE_URL}/chat/completions` — padrão OpenAI Chat Completions; default `https://api.groq.com/openai/v1`. 🟢

### Requisição

| Elemento | Valor | Evidência |
|---|---|---|
| Header | `Authorization: Bearer {LLM_API_KEY}` | `analise_openai.py:27` |
| Corpo | JSON | `analise_openai.py:28-35` |
| `model` | `Settings.llm_model` (default `llama-3.3-70b-versatile`) | idem |
| `temperature` | `0.2` (constante, não configurável) | `analise_openai.py:13` |
| `messages[0]` | `{"role": "system", "content": <prompt canônico íntegro>}` | `analise_openai.py:32` |
| `messages[1]` | `{"role": "user", "content": <transcrição>}` | `analise_openai.py:33` |
| Timeout | 120 s | `analise_openai.py:12,36` |

Parâmetros **ausentes** deliberadamente (defaults do provedor): `max_tokens`, `top_p`, `stream`, penalidades. 🟢

### Resposta esperada (2xx)

```json
{ "choices": [ { "message": { "content": "<ficha SNAPPS-OMP em Markdown>" } } ] }
```

Somente `choices[0].message.content` é lido. 🟢

### Mapeamento de erros → domínio

| Condição | Exceção | Mensagem (exata) |
|---|---|---|
| `httpx.HTTPError` | `ErroServicoExterno` | `Falha de rede na etapa de análise: {exc}` |
| HTTP 401 | `ErroCredencial` | `Credencial recusada na etapa de análise: confira LLM_API_KEY no .env.` |
| HTTP 429 | `ErroLimiteProvedor` | `Limite do provedor atingido na etapa de análise: aguarde alguns minutos ou configure outro provedor (LLM_BASE_URL).` |
| HTTP ≥ 400 (demais) | `ErroServicoExterno` | `Falha na etapa de análise (HTTP {status}): {corpo[:300]}` |
| Parse falho (`choices`/`message`/`content` ausentes ou JSON inválido) | `ErroRespostaAnalise` | `Resposta malformada do serviço de análise: {corpo[:300]}` |
| `content` vazio/whitespace | `ErroRespostaAnalise` | `Serviço de análise devolveu conteúdo vazio.` |

🟢 (`analise_openai.py:38-49`, tradutor em `transcricao_openai.py:49-62`)

## Contrato de saída (a ficha)

O Markdown devolvido deve seguir o template do prompt canônico: cabeçalho administrativo (Data/Preceptor/Residente/Contexto clínico, com "A preencher" quando ausentes), Seção 1 SNAPPS (6 subitens), Seção 2 OMP (5 subitens), Seção 3 Plano de aprendizado (4 listas). Cumprimento garantido **apenas por instrução ao modelo** — não há validação estrutural no código além de "não-vazio". 🟡
