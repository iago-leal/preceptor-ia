# Flowchart — módulo `domain`

> Archaeologist (Reversa), 2026-07-20. 🟢 CONFIRMADO a partir de `domain/models.py` e `domain/prompt.py`.

## Validação de `Entrada.__post_init__`

```mermaid
flowchart TD
    A[Entrada criada] --> B{origem == AUDIO?}
    B -- sim --> C{nome_arquivo e conteudo_audio presentes?}
    C -- não --> E1[ErroEntradaInvalida: áudio sem arquivo]
    C -- sim --> D{extensão em .ogg .mp3 .m4a .wav?}
    D -- não --> E2[ErroEntradaInvalida: formato não suportado]
    D -- sim --> F{tamanho <= 25 MB?}
    F -- não --> E3[ErroEntradaInvalida: acima de 25 MB]
    F -- sim --> OK[Entrada válida]
    B -- não --> G{texto_transcricao não-vazio após strip?}
    G -- não --> E4[ErroEntradaInvalida: texto vazio]
    G -- sim --> OK
```

## `carregar_prompt(caminho)`

```mermaid
flowchart TD
    A[carregar_prompt] --> B{arquivo existe?}
    B -- não --> E1[ErroPromptCanonico: não encontrado]
    B -- sim --> C[ler UTF-8 e strip]
    C --> D{texto vazio?}
    D -- sim --> E2[ErroPromptCanonico: vazio]
    D -- não --> R[retorna prompt canônico]
```
