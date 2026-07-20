# Flowchart — módulo `ui`

> Archaeologist (Reversa), 2026-07-20. 🟢 CONFIRMADO a partir de `ui/app.py`.

## Ciclo de página Streamlit

```mermaid
flowchart TD
    A[render: título + aviso de privacidade] --> B[3 abas]
    B --> B1[🎙️ Áudio: file_uploader + botão]
    B --> B2[📄 Texto: text_area + botão]
    B --> B3[🎬 Demo: caso simulado + botão<br/>+ botão ficha de exemplo offline]
    B1 -- clique --> C1[session_state.entrada_pendente = Entrada AUDIO]
    B2 -- clique --> C2[session_state.entrada_pendente = Entrada TEXTO]
    B3 -- clique --> C3[session_state.entrada_pendente = Entrada DEMO]
    B3 -- clique offline --> C4[exibe demo/ficha-exemplo.md<br/>sem chamada externa]
    C1 & C2 & C3 --> D[pop entrada_pendente]
    D --> E[_gerar entrada]
    E -- ErroConfiguracao --> F1[st.error ⚙️]
    E -- ErroPreceptorIA --> F2[st.error ❌]
    E -- sucesso --> G[session_state.ficha]
    G --> H[render markdown + download .md]
```

## `_gerar` — deduplicação e progresso

```mermaid
flowchart TD
    A[_gerar entrada] --> B[chave = sha256 origem + texto + bytes]
    B --> C{chave == última processada?}
    C -- sim --> R1[retorna sem reprocessar<br/>proteção contra rerun]
    C -- não --> D[st.status Gerando ficha]
    D --> E[_caso_de_uso cache_resource .executar]
    E --> F[status = Ficha pronta]
    F --> G[salva chave e ficha no session_state]
```

Notas:
- `Entrada` inválida levanta `ErroEntradaInvalida` já na construção (dentro do handler das abas → capturado no bloco externo).
- `@st.cache_resource` congela fábrica e settings pelo tempo de vida do processo 🟡.
