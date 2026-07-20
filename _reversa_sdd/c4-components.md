# C4 — Nível 3: Componentes — PreceptorIA

> Gerado pelo **Architect** (Reversa) em 2026-07-20. Container detalhado: **Aplicação Streamlit** (único container de código).
> Escala: 🟢 CONFIRMADO · 🟡 INFERIDO · 🔴 LACUNA

## Diagrama

```mermaid
C4Component
    title Componentes — Aplicação Streamlit (src/preceptor_ia)

    Person(preceptor, "Preceptor")

    Container_Boundary(app, "Aplicação Streamlit") {
        Component(ui, "ui/app.py", "Streamlit", "Página única: 3 abas (áudio, texto, demo), aviso LGPD, dedup por SHA-256, contingência offline, download da ficha.")
        Component(factory, "application/factory.py", "Python", "Composition root: carrega Settings + prompt, instancia adaptadores e injeta histórico apenas se ativo.")
        Component(usecase, "application/gerar_ficha.py", "Python", "Caso de uso GerarFicha: ingestão → transcrição condicional → análise → validação → entrega (+ histórico).")
        Component(models, "domain/models.py", "Python puro", "Entrada, Transcricao, Ficha (frozen) + hierarquia de erros nomeados. Validação no __post_init__.")
        Component(ports, "domain/ports.py", "typing.Protocol", "Contratos: ServicoTranscricao, ServicoAnalise, RepositorioHistorico.")
        Component(promptmod, "domain/prompt.py", "Python puro", "carregar_prompt(): resolve e valida o prompt canônico; falha barulhenta.")
        Component(config, "config.py", "pydantic-settings", "Settings via .env; ErroConfiguracao nomeando a variável faltante.")
        Component(transcricao, "infra/transcricao_openai.py", "httpx", "Adaptador Whisper: multipart, language=pt fixo, mapeamento HTTP→erros nomeados.")
        Component(analise, "infra/analise_openai.py", "httpx", "Adaptador chat completions: temperature=0.2, parse defensivo de choices[0].")
        Component(historico, "infra/historico.py", "pathlib", "Grava ficha .md datestampada com slug normalizado.")
    }

    System_Ext(provedor, "Provedor OpenAI-compatible")
    ContainerDb_Ext(fs, "Histórico local")

    Rel(preceptor, ui, "Usa")
    Rel(ui, factory, "monta caso de uso (st.cache_resource)")
    Rel(ui, usecase, "executar(entrada)")
    Rel(factory, config, "carregar_settings()")
    Rel(factory, promptmod, "carregar_prompt()")
    Rel(usecase, ports, "depende dos Protocols")
    Rel(usecase, models, "constrói Ficha, levanta erros")
    Rel(transcricao, provedor, "POST /audio/transcriptions")
    Rel(analise, provedor, "POST /chat/completions")
    Rel(historico, fs, "grava .md")
```

## Regras de dependência entre camadas

Direção das setas de import 🟢 (confirmada em [code-analysis.md](code-analysis.md) e [dependencies.md](dependencies.md)):

```
ui  →  application  →  domain  ←  infra
         ↓
       config
```

- `domain/` não importa nada externo (somente stdlib) — núcleo hexagonal puro (ADR-0002). 🟢
- `infra/` implementa os Protocols de `domain/ports.py`; `httpx` confinado ali. 🟢
- `ui/` conhece `application` e os erros de `domain`; `streamlit` confinado ali. 🟢
- `factory.py` é o único componente que conhece config + infra + domínio ao mesmo tempo (composition root). 🟢

## Pontos de atenção por componente

| Componente | Observação | Confiança |
|---|---|---|
| `gerar_ficha.py` | Gravação de histórico sem try/except próprio: falha de IO abortaria a entrega da ficha já gerada. | 🟡 |
| `transcricao_openai.py` | Abriga `_levantar_erro_nomeado`, importada também por `analise_openai.py` — helper "privado" compartilhado entre adaptadores; candidato a módulo próprio (`infra/_http_erros.py`). | 🟡 |
| `historico.py` | Colisão de nome no mesmo minuto sobrescreve silenciosamente. | 🟡 |
| `ui/app.py` | `st.cache_resource` congela Settings por processo: mudança no `.env` exige restart. | 🟡 |
| `ui/app.py` | Concentra 5 responsabilidades (layout, estado de sessão, dedup, tratamento de erro, download) em 113 linhas — aceitável no tamanho atual, primeiro candidato a split se a UI crescer. | 🟡 |
