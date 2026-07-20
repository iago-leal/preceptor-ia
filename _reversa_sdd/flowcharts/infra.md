# Flowchart — módulo `infra`

> Archaeologist (Reversa), 2026-07-20. 🟢 CONFIRMADO a partir de `infra/transcricao_openai.py`, `analise_openai.py`, `historico.py`.

## `TranscricaoOpenAICompat.transcrever`

```mermaid
flowchart TD
    A[transcrever bytes, nome] --> B[POST /audio/transcriptions<br/>multipart, language=pt, timeout 120s]
    B -- httpx.HTTPError --> E1[ErroServicoExterno: falha de rede]
    B --> C{status HTTP}
    C -- 401 --> E2[ErroCredencial]
    C -- 429 --> E3[ErroLimiteProvedor]
    C -- ">=400" --> E4[ErroServicoExterno]
    C -- 2xx --> D["texto = json().text.strip()"]
    D --> F{texto vazio?}
    F -- sim --> E5[ErroServicoExterno: texto vazio]
    F -- não --> R["Transcricao(texto, base_url#modelo)"]
```

## `AnaliseOpenAICompat.analisar`

```mermaid
flowchart TD
    A[analisar prompt, transcricao] --> B[POST /chat/completions<br/>temperature=0.2, system+user, timeout 120s]
    B -- httpx.HTTPError --> E1[ErroServicoExterno: falha de rede]
    B --> C{status HTTP}
    C -- 401 --> E2[ErroCredencial]
    C -- 429 --> E3[ErroLimiteProvedor]
    C -- ">=400" --> E4[ErroServicoExterno]
    C -- 2xx --> D["conteudo = choices[0].message.content"]
    D -- KeyError/IndexError/ValueError --> E5[ErroRespostaAnalise: malformada]
    D --> F{conteúdo vazio?}
    F -- sim --> E6[ErroRespostaAnalise: vazio]
    F -- não --> R[retorna markdown]
```

Ambos os adaptadores compartilham `_levantar_erro_nomeado` (mapa status → erro de domínio), definida em `transcricao_openai.py:49`.

## `HistoricoFilesystem.gravar`

```mermaid
flowchart TD
    A[gravar ficha] --> B[mkdir -p historico_dir]
    B --> C[slug = contexto ou origem, normalizado a-z0-9-]
    C --> D[nome = YYYYMMDDHHmm-ficha-slug.md]
    D --> E[write_text markdown + \n]
    E --> F[log etapa=historico]
```
