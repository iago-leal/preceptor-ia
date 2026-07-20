# C4 — Nível 1: Contexto — PreceptorIA

> Gerado pelo **Architect** (Reversa) em 2026-07-20.
> Escala: 🟢 CONFIRMADO · 🟡 INFERIDO · 🔴 LACUNA

## Diagrama

```mermaid
C4Context
    title Contexto do Sistema — PreceptorIA

    Person(preceptor, "Preceptor", "Médico que supervisiona o residente. Opera a ferramenta localmente e responde pela anonimização do conteúdo (LGPD).")
    Person_Ext(residente, "Residente", "Papel de domínio: aparece na passagem de caso e é avaliado na ficha, mas nunca opera o sistema.")

    System(preceptoria, "PreceptorIA", "Página Streamlit local que transforma uma passagem de caso (áudio ou texto) em ficha de feedback formativo SNAPPS-OMP com evidências citadas.")

    System_Ext(provedor, "Provedor de IA OpenAI-compatible", "Default: Groq. Dois serviços consumidos: transcrição Whisper e chat completions. Trocável via .env sem código.")
    SystemDb_Ext(fs, "Filesystem local", "Histórico opcional de fichas (~/.preceptor-ia/historico), desligado por padrão. Protegido apenas pelas permissões do SO.")

    Rel(preceptor, preceptoria, "Envia áudio/transcrição da passagem de caso; recebe e baixa a ficha", "Browser → localhost:8501")
    Rel(residente, preceptor, "Apresenta o caso (fora do sistema)")
    Rel(preceptoria, provedor, "Transcreve áudio e solicita análise pedagógica", "HTTPS REST, Bearer LLM_API_KEY, timeout 120 s")
    Rel(preceptoria, fs, "Grava ficha .md datestampada (somente se HISTORICO_ATIVO=true)", "Escrita em arquivo")
```

## Leitura do diagrama

- **Um único usuário humano** 🟢 — o preceptor, papel único sem autenticação ([permissions.md](permissions.md)). O residente é ator de domínio, não de sistema.
- **Uma única integração externa** 🟢 — o provedor OpenAI-compatible, consumido por dois endpoints REST (`/audio/transcriptions` e `/chat/completions`). Não há webhooks, filas nem eventos.
- **Fronteira de privacidade** 🟢 — o conteúdo clínico sai do perímetro local apenas na chamada ao provedor; o app não retém áudio (RN-P4) e o histórico é opt-in (RN-C3). O aviso LGPD na UI rege essa relação de confiança.
- **Modo demo/contingência** 🟢 — com o caso simulado embutido e a ficha de exemplo offline, o sistema opera de ponta a ponta sem tocar o provedor, o que faz da integração externa uma dependência *evitável* em demonstração.
