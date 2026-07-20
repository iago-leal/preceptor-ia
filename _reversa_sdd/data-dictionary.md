# Dicionário de Dados — preceptor-ia

> Gerado pelo Archaeologist (Reversa) em 2026-07-20. Confiança: 🟢 salvo indicação.
> Não há banco de dados; as estruturas vivem em memória (dataclasses) e, opcionalmente, em arquivos Markdown no histórico local.

## Enums

### `OrigemEntrada` (StrEnum) — `domain/models.py:35`

| Valor | Significado |
|---|---|
| `audio` | Gravação enviada pela aba de áudio |
| `texto` | Transcrição colada pelo usuário |
| `demo` | Caso simulado embutido (`demo/transcricao-simulada.md`) |

## Entidades

### `Entrada` — `domain/models.py:41` (dataclass frozen)

| Campo | Tipo | Obrigatório | Default | Regras |
|---|---|---|---|---|
| `origem` | `OrigemEntrada` | sim | — | — |
| `nome_arquivo` | `str \| None` | se origem=audio | `None` | precisa de extensão ∈ {.ogg, .mp3, .m4a, .wav}, case-insensitive |
| `conteudo_audio` | `bytes \| None` | se origem=audio | `None` | ≤ 25 MB (26.214.400 bytes) |
| `texto_transcricao` | `str \| None` | se origem≠audio | `None` | não-vazio após strip |

Validação em `__post_init__`; violação → `ErroEntradaInvalida` antes de qualquer chamada externa.

### `Transcricao` — `domain/models.py:75` (dataclass frozen)

| Campo | Tipo | Obrigatório | Regras |
|---|---|---|---|
| `texto` | `str` | sim | adaptador garante não-vazio |
| `origem_servico` | `str` | sim | formato `"{base_url}#{modelo}"` |

### `Ficha` — `domain/models.py:82` (dataclass frozen)

| Campo | Tipo | Obrigatório | Default | Regras |
|---|---|---|---|---|
| `markdown` | `str` | sim | — | conteúdo integral da ficha SNAPPS-OMP; validado não-vazio no caso de uso |
| `origem_entrada` | `OrigemEntrada` | sim | — | — |
| `contexto` | `str \| None` | não | `None` | usado só no slug do nome de arquivo do histórico; nunca preenchido pelo fluxo atual. 🟢 [Revisão] Explicação encontrada na spec de origem: RF-07 prevê ficha "com data e identificação de contexto" — o campo foi modelado para isso, mas a alimentação nunca foi implementada (feature Could parcialmente entregue) |
| `gerada_em` | `datetime` | não | `datetime.now()` | horário local; compõe nomes de arquivo (`%Y%m%d%H%M`) |

### `Settings` — `config.py:13` (pydantic BaseSettings, fonte `.env`)

| Campo | Env var | Tipo | Obrigatório | Default |
|---|---|---|---|---|
| `llm_api_key` | `LLM_API_KEY` | `str` (min_length=1) | **sim** | — |
| `llm_base_url` | `LLM_BASE_URL` | `str` | não | `https://api.groq.com/openai/v1` |
| `llm_model` | `LLM_MODEL` | `str` | não | `llama-3.3-70b-versatile` |
| `transcricao_model` | `TRANSCRICAO_MODEL` | `str` | não | `whisper-large-v3-turbo` |
| `historico_ativo` | `HISTORICO_ATIVO` | `bool` | não | `False` |
| `historico_dir` | `HISTORICO_DIR` | `Path` | não | `~/.preceptor-ia/historico` |

## Constantes de domínio

| Constante | Valor | Local | Papel |
|---|---|---|---|
| `EXTENSOES_AUDIO` | `{.ogg, .mp3, .m4a, .wav}` | `domain/models.py:7` | formatos aceitos (RF-01) |
| `TAMANHO_MAXIMO_AUDIO_BYTES` | `25 * 1024 * 1024` | `domain/models.py:8` | limite do contrato de transcrição |
| `CAMINHO_PROMPT_PADRAO` | `prompts/prompt-snapps-omp.md` | `domain/prompt.py:7` | fonte única do prompt |
| `TIMEOUT_SEGUNDOS` | `120.0` | ambos adaptadores | timeout HTTP |
| `TEMPERATURA` | `0.2` | `infra/analise_openai.py:13` | fidelidade > criatividade (RN-03) |

## Formato de persistência (histórico opcional)

Arquivo Markdown por ficha, em `HISTORICO_DIR`:

```
{YYYYMMDDHHmm}-ficha-{slug}.md      # slug: contexto ou origem, normalizado [a-z0-9-]
conteúdo: Ficha.markdown + "\n"
```

Sem índice, sem metadados adicionais, sem rotação. Colisões no mesmo minuto sobrescrevem 🟡.

## Contratos HTTP externos (payloads)

### Transcrição — `POST {base}/audio/transcriptions` (multipart)

| Campo | Valor |
|---|---|
| `file` | `(nome_arquivo, bytes)` |
| `model` | `Settings.transcricao_model` |
| `language` | `"pt"` (fixo, RN-02) |
| `response_format` | `"json"` — resposta lida do campo `text` do corpo JSON (`resposta.json().get("text")`) [Revisão: precisão corrigida] |

### Análise — `POST {base}/chat/completions` (JSON)

| Campo | Valor |
|---|---|
| `model` | `Settings.llm_model` |
| `temperature` | `0.2` |
| `messages` | `[{system: prompt canônico}, {user: transcrição}]` — resposta lida de `choices[0].message.content` |
