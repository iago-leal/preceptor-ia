# Transcrição de Áudio

> Gerado pelo **Writer** (Reversa) em 2026-07-20. Unit: `transcricao-audio`.
> Escala: 🟢 CONFIRMADO · 🟡 INFERIDO · 🔴 LACUNA

## Visão Geral

Adaptador que converte a gravação da passagem de caso em texto, consumindo o endpoint `/audio/transcriptions` de qualquer provedor OpenAI-compatible (default: Groq com `whisper-large-v3-turbo`). Implementa a porta `ServicoTranscricao` e traduz falhas HTTP em erros nomeados de domínio. 🟢

## Responsabilidades

- Enviar o áudio (multipart) ao provedor com idioma fixo `pt`. 🟢
- Validar que a resposta contém texto não-vazio. 🟢
- Traduzir erros de rede e HTTP em erros de domínio com mensagens que nomeiam a etapa. 🟢
- Registrar a procedência da transcrição (`origem_servico = "{base_url}#{modelo}"`). 🟢

## Regras de Negócio

- Idioma fixo `pt` — jargões da APS brasileira não podem ser autodetectados como outro idioma (RN-02). 🟢
- Texto vazio do provedor é falha (`ErroServicoExterno: "Etapa de transcrição devolveu texto vazio."`), não transcrição válida. 🟢
- Timeout de 120 s por chamada. 🟢
- `base_url` é normalizada com `rstrip("/")` na construção. 🟢
- Mapeamento HTTP → domínio: 401 → `ErroCredencial` (aponta `LLM_API_KEY`); 429 → `ErroLimiteProvedor` (sugere aguardar ou trocar `LLM_BASE_URL`); ≥ 400 → `ErroServicoExterno` (inclui corpo truncado em 300 chars). 🟢
- Exceção `httpx.HTTPError` (rede/timeout) → `ErroServicoExterno: "Falha de rede na etapa de transcrição: {exc}"`. 🟢

## Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de Aceite |
|----|-----------|-----------|-------------------|
| RF-TA-01 | Transcrever áudio válido em texto | Must | `transcrever(bytes, nome)` devolve `Transcricao` com texto não-vazio (strip) |
| RF-TA-02 | Fixar idioma `pt` na requisição | Must | Payload multipart contém `language="pt"` |
| RF-TA-03 | Traduzir 401/429/≥400 em erros nomeados | Must | Cada status levanta a exceção correspondente com mensagem em português |
| RF-TA-04 | Rejeitar resposta sem texto | Must | `{"text": ""}` ou campo ausente → `ErroServicoExterno` |
| RF-TA-05 | Registrar procedência do serviço | Should | `origem_servico == f"{base_url}#{modelo}"` |

## Requisitos Não Funcionais

| Tipo | Requisito inferido | Evidência no código | Confiança |
|------|--------------------|---------------------|-----------|
| Performance | Timeout de 120 s por chamada (sem retry) | `infra/transcricao_openai.py:16,37` | 🟢 |
| Segurança | Autenticação Bearer com `LLM_API_KEY`; chave nunca logada | `infra/transcricao_openai.py:30` | 🟢 |
| Portabilidade | Qualquer endpoint OpenAI-compatible via `base_url` injetada | `infra/transcricao_openai.py:21-29` | 🟢 |

## Critérios de Aceitação

```gherkin
Dado um provedor que responde 200 com {"text": " Bom dia... "}
Quando transcrever(conteudo, "caso.ogg") é chamado
Então o retorno é Transcricao(texto="Bom dia...", origem_servico="{base_url}#{modelo}")

Dado um provedor que responde 401
Quando transcrever é chamado
Então ErroCredencial é levantado com mensagem citando LLM_API_KEY e o .env

Dado um provedor que responde 429
Quando transcrever é chamado
Então ErroLimiteProvedor é levantado sugerindo aguardar ou configurar outro provedor

Dado um provedor inacessível (timeout ou falha de rede)
Quando transcrever é chamado
Então ErroServicoExterno é levantado com "Falha de rede na etapa de transcrição"

Dado um provedor que responde 200 com {"text": ""}
Quando transcrever é chamado
Então ErroServicoExterno é levantado ("texto vazio")
```

## Prioridade (MoSCoW)

| Requisito | MoSCoW | Justificativa |
|-----------|--------|---------------|
| Transcrição com idioma fixo (RF-TA-01/02) | Must | Único caminho de entrada por áudio |
| Erros nomeados (RF-TA-03/04) | Must | A UI depende deles para mensagens acionáveis |
| Procedência (RF-TA-05) | Should | Metadado informativo; nenhum consumidor atual o exibe 🟡 |

## Rastreabilidade de Código

| Arquivo | Função / Classe | Cobertura |
|---------|-----------------|-----------|
| `src/preceptor_ia/infra/transcricao_openai.py` | `TranscricaoOpenAICompat.transcrever`, `_levantar_erro_nomeado` | 🟢 |
| `tests/test_adaptadores.py` | Transporte httpx mockado | 🟢 |
