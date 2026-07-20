# ADR-0002 — Arquitetura em camadas com portas e adaptadores

> Retroativo, gerado pelo Detective (Reversa) em 2026-07-20. Status: **aceita** (implementada). Confiança: 🟢

## Contexto

Validação conceitual de escopo pequeno (≈600 LOC), mas com dois serviços externos (transcrição e análise) e persistência opcional — pontos de variação previsíveis (trocar provedor, transcrição local, outro armazenamento).

## Decisão

Quatro camadas com dependências apontando para dentro: `domain/` (modelos imutáveis, erros nomeados, contratos `Protocol`, prompt), `application/` (caso de uso `GerarFicha` + composition root `factory.py`), `infra/` (adaptadores HTTP OpenAI-compatible e histórico filesystem), `ui/` (Streamlit). Contratos como `typing.Protocol` (duck typing estrutural, sem herança): `ServicoTranscricao`, `ServicoAnalise`, `RepositorioHistorico` (`domain/ports.py`).

## Consequências

- Testes rodam sem rede: dublês implementam os Protocols; o transporte httpx é mockado nos testes de adaptador. 🟢
- Trocar Groq por qualquer OpenAI-compatible é configuração (`LLM_BASE_URL`); trocar por transcrição local (mlx-whisper) é implementar um método, como o README anuncia. 🟢
- O único ponto que conhece config + infra simultaneamente é `factory.py` — dependências injetadas por construtor, histórico injetado como `None` quando desligado (ausência de capability em vez de flag interna). 🟢
- Custo: mais arquivos do que um script Streamlit monolítico teria; assumido conscientemente como investimento em longevidade. 🟡
