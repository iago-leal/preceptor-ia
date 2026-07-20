# Flowchart — módulo `application`

> Archaeologist (Reversa), 2026-07-20. 🟢 CONFIRMADO a partir de `application/gerar_ficha.py` e `factory.py`.

## Caso de uso `GerarFicha.executar`

```mermaid
flowchart TD
    A[executar entrada] --> B[log etapa=ingestao]
    B --> C{origem == AUDIO?}
    C -- não --> D[texto = texto_transcricao.strip]
    C -- sim --> E[log etapa=transcricao] --> F[transcricao.transcrever bytes, nome]
    F --> G[texto = resultado.texto.strip<br/>áudio descartado — RN-07]
    D --> H[log etapa=analise]
    G --> H
    H --> I[markdown = analise.analisar prompt, texto]
    I --> J{markdown vazio?}
    J -- sim --> E1[ErroRespostaAnalise — RN-03]
    J -- não --> K[Ficha markdown.strip, origem]
    K --> L{historico injetado?}
    L -- sim --> M[historico.gravar ficha]
    L -- não --> N[log etapa=entrega]
    M --> N
    N --> R[retorna Ficha]
```

## Composition root `montar_gerar_ficha`

```mermaid
flowchart TD
    A[montar_gerar_ficha settings?] --> B{settings fornecido?}
    B -- não --> C[carregar_settings — pode levantar ErroConfiguracao]
    B -- sim --> D[usa o recebido]
    C --> E[carregar_prompt — pode levantar ErroPromptCanonico]
    D --> E
    E --> F[TranscricaoOpenAICompat base_url, key, transcricao_model]
    F --> G[AnaliseOpenAICompat base_url, key, llm_model]
    G --> H{historico_ativo?}
    H -- sim --> I[HistoricoFilesystem historico_dir]
    H -- não --> J[historico = None]
    I --> K[GerarFicha prompt, transcricao, analise, historico]
    J --> K
```
