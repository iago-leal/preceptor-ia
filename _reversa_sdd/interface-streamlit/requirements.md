# Interface Streamlit

> Gerado pelo **Writer** (Reversa) em 2026-07-20. Unit: `interface-streamlit`.
> Escala: 🟢 CONFIRMADO · 🟡 INFERIDO · 🔴 LACUNA

## Visão Geral

Página única Streamlit (`ui/app.py`, entry point do sistema) com três vias de entrada — upload de áudio, transcrição colada e caso demo — mais a contingência offline. Exibe aviso permanente de privacidade (LGPD), orquestra a chamada ao caso de uso com indicador de progresso, deduplica reprocessamentos por hash e oferece download da ficha. 🟢

## Responsabilidades

- Renderizar título, aviso de privacidade e as três abas de entrada. 🟢
- Construir a `Entrada` correta por aba e enfileirá-la em `st.session_state` (fila de 1). 🟢
- Processar a entrada pendente uma vez por rerun, com dedup por SHA-256. 🟢
- Traduzir erros em mensagens com prefixo ⚙️ (configuração) ou ❌ (domínio), sem stack trace. 🟢
- Exibir a ficha e o botão de download `.md` datestampado. 🟢
- Exibir a ficha de exemplo offline quando disponível (contingência de demo). 🟢

## Regras de Negócio

- Aviso LGPD fixo: não-retenção, casos simulados em demos públicas, anonimização é responsabilidade do preceptor (RN-U2). 🟢
- Upload restrito a `.ogg/.mp3/.m4a/.wav` já no widget (`type=[...]`), redundante com a validação de domínio (defesa em profundidade). 🟢
- Dedup de sessão: SHA-256 de `origem + texto_transcricao + conteudo_audio`; hash igual ao último processado → nenhuma chamada externa (RN-U1). 🟢
- Caso de uso montado uma única vez por processo (`@st.cache_resource`) — mudar `.env` exige restart (RN-U5 implícita). 🟡
- Caso demo lido de `demo/transcricao-simulada.md` (inteiramente simulado, RN-U3); contingência lê `demo/ficha-exemplo.md` e só aparece se o arquivo existir (RN-U4). 🟢
- Exibir a contingência offline zera `ficha` e `chave_resultado` — única ação que "desfaz" um resultado exibido. 🟢
- Download nomeado `{gerada_em:%Y%m%d%H%M}-ficha-snapps-omp.md`, espelhando a convenção do histórico (RN-U6). 🟢
- Progresso via `st.status`: áudio exibe "ingestão, transcrição"; texto/demo só "ingestão"; ambas fecham com "análise concluída". 🟢

## Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de Aceite |
|----|-----------|-----------|-------------------|
| RF-UI-01 | Gerar ficha via upload de áudio | Must | Aba 1: upload + botão → ficha renderizada |
| RF-UI-02 | Gerar ficha via transcrição colada | Must | Aba 2: textarea + botão → ficha renderizada |
| RF-UI-03 | Gerar ficha do caso demo embutido | Must | Aba 3: botão → ficha do caso simulado |
| RF-UI-04 | Exibir ficha de exemplo offline | Should | Botão presente só se `demo/ficha-exemplo.md` existe; exibição sem chamadas externas |
| RF-UI-05 | Dedup de resubmissão idêntica | Should | Mesmo conteúdo na mesma sessão não repete chamadas externas |
| RF-UI-06 | Erros amigáveis sem stack trace | Must | `ErroConfiguracao` → "⚙️ ..."; `ErroPreceptorIA` → "❌ ..." |
| RF-UI-07 | Download da ficha em Markdown | Must | Arquivo com nome datestampado e conteúdo + newline final |

## Requisitos Não Funcionais

| Tipo | Requisito inferido | Evidência no código | Confiança |
|------|--------------------|---------------------|-----------|
| Privacidade | Aviso LGPD permanente antes de qualquer interação | `ui/app.py:27-34` | 🟢 |
| Performance | Composição cacheada por processo (fábrica roda 1×) + dedup evita chamadas repetidas | `ui/app.py:37-39,43-48` | 🟢 |
| Usabilidade | Feedback de progresso por etapa durante a geração | `ui/app.py:49-55` | 🟢 |
| Observabilidade | `logging.basicConfig(level=INFO)` no entry point habilita os logs estruturados das camadas internas | `ui/app.py:13` | 🟢 |

## Critérios de Aceitação

```gherkin
Dado a aba de texto com transcrição válida colada
Quando o usuário clica "Gerar ficha a partir do texto"
Então a Entrada é enfileirada, processada no rerun, e a ficha aparece com botão de download

Dado uma entrada idêntica à última processada na sessão
Quando o usuário clica gerar novamente
Então nenhuma chamada externa ocorre e a ficha exibida permanece

Dado LLM_API_KEY ausente
Quando qualquer geração é acionada
Então a página exibe mensagem iniciada por "⚙️" e nenhum stack trace

Dado um provedor fora do ar
Quando a geração é acionada
Então a página exibe mensagem iniciada por "❌" com o texto do erro nomeado

Dado que demo/ficha-exemplo.md existe
Quando o usuário clica "Exibir ficha de exemplo (offline)"
Então a ficha de exemplo é renderizada sem chamadas externas
E o resultado anterior (se houver) é limpo
```

## Prioridade (MoSCoW)

| Requisito | MoSCoW | Justificativa |
|-----------|--------|---------------|
| Três vias de geração (RF-UI-01..03) | Must | Interface é o único ponto de acesso ao produto |
| Erros amigáveis (RF-UI-06) e download (RF-UI-07) | Must | Sem eles a ficha não chega ao usuário com segurança |
| Contingência offline (RF-UI-04) | Should | Rede de segurança de demo (ADR-0006); produto funciona sem ela |
| Dedup (RF-UI-05) | Should | Proteção contra reruns; sem ela o app funciona, com custo |

## Rastreabilidade de Código

| Arquivo | Função / Classe | Cobertura |
|---------|-----------------|-----------|
| `src/preceptor_ia/ui/app.py` | Página completa (`_caso_de_uso`, `_gerar`, abas, render) | 🟢 |
| `demo/transcricao-simulada.md`, `demo/ficha-exemplo.md` | Artefatos de demo/contingência | 🟢 |
| — | **Sem teste automatizado de UI no legado** | 🟡 |
