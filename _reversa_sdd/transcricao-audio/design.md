# Transcrição de Áudio, Design Técnico

> Gerado pelo **Writer** (Reversa) em 2026-07-20.
> Escala: 🟢 CONFIRMADO · 🟡 INFERIDO · 🔴 LACUNA

## Interface

| Símbolo | Assinatura | Retorno | Observação |
|---------|-----------|---------|------------|
| `TranscricaoOpenAICompat.__init__` | `(base_url: str, api_key: str, modelo: str)` | — | `base_url` recebe `rstrip("/")` |
| `TranscricaoOpenAICompat.transcrever` | `(conteudo: bytes, nome_arquivo: str)` | `Transcricao` | Satisfaz o Protocol `ServicoTranscricao` |
| `_levantar_erro_nomeado` | `(resposta: httpx.Response, etapa: str)` | `None` | Função de módulo; também usada por `analise_openai.py` |

Constantes: `TIMEOUT_SEGUNDOS = 120.0`, `ETAPA = "transcrição"`. 🟢

## Fluxo Principal

1. `httpx.post(f"{base_url}/audio/transcriptions", ...)` com header `Authorization: Bearer {api_key}`, `files={"file": (nome_arquivo, conteudo)}`, `data={"model": modelo, "language": "pt", "response_format": "json"}`, `timeout=120.0` (`transcricao_openai.py:27-38`).
2. `_levantar_erro_nomeado(resposta, "transcrição")` — retorna silenciosamente em 2xx/3xx (`transcricao_openai.py:42`).
3. Extrai `resposta.json().get("text")`, aplica `or ""` + `strip()`; vazio → `ErroServicoExterno` (`transcricao_openai.py:43-45`).
4. Retorna `Transcricao(texto=texto, origem_servico=f"{base_url}#{modelo}")` (`transcricao_openai.py:46`).

## Fluxos Alternativos

- **`httpx.HTTPError` no POST** (timeout, DNS, conexão): capturada e reempacotada em `ErroServicoExterno` com `from exc` (`transcricao_openai.py:39-40`).
- **HTTP 401 / 429 / ≥400:** ver mapeamento em `contracts.md`; a função levanta antes de qualquer parse do corpo.

## Dependências

- `httpx` — cliente HTTP síncrono, chamada module-level `httpx.post` (sem client reutilizado). 🟢
- `domain/models.py` — `Transcricao` e os erros nomeados.

## Decisões de Design Identificadas

| Decisão | Evidência no código | Confiança |
|---------|---------------------|-----------|
| `response_format="json"` e leitura de `.json()["text"]` (não texto puro) | `transcricao_openai.py:35,43` | 🟢 |
| Sem retry/backoff: uma tentativa por chamada; resiliência delegada ao usuário (mensagens acionáveis) | `transcricao_openai.py:26-46` | 🟢 |
| `httpx.post` sem `httpx.Client` persistente — sem pool de conexões (chamadas raras, custo aceitável) | `transcricao_openai.py:28` | 🟡 (interpretação do porquê) |
| Tradutor de erros como função de módulo compartilhada entre adaptadores | `transcricao_openai.py:49-62` | 🟢 |

## Estado Interno

Nenhum além dos três parâmetros imutáveis do construtor. Sem cache, sem sessão HTTP. 🟢

## Observabilidade

O módulo define `logger = logging.getLogger("preceptor_ia")` mas **não emite nenhum log próprio** — a telemetria da etapa (`etapa=transcricao arquivo=... bytes=...`) é emitida pelo caso de uso antes da chamada. 🟢

## Riscos e Lacunas

- 🟡 `_levantar_erro_nomeado` é "privada" por convenção mas importada por `analise_openai.py` — mover para módulo próprio (ex.: `infra/_http_erros.py`) em reimplementação (DT-4).
- 🟡 Sem validação de `content-type` da resposta: um 200 com corpo não-JSON levantaria exceção de parse do httpx (não capturada como erro nomeado nesta etapa — divergência sutil do adaptador de análise, que captura `ValueError`).
