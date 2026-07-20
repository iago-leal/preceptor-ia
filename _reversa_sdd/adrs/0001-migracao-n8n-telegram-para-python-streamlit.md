# ADR-0001 — Migração do fluxo n8n + Telegram para Python + Streamlit

> Retroativo, gerado pelo Detective (Reversa) em 2026-07-20. Status: **aceita** (implementada). Confiança: 🟢

## Contexto

A proposta original (UE2 do curso de Preceptoria em MFC) implementava o pipeline como workflow n8n acionado via Telegram. O commit inicial deste repositório (`4c37704`, 2026-07-14) declara explicitamente: "Migrado do fluxo n8n + Telegram (proposta UE2) — ver feature 001-migracao-python-streamlit no repo preceptoria-mfc".

## Decisão

Reimplementar como aplicação Python em camadas (domain/application/infra/ui) com interface Streamlit, testes sem rede, CI e dependências pinadas (`uv.lock`).

## Motivação aparente

🟡 Inferida do resultado: controle total do código (vs. workflow visual), testabilidade (35 testes sem rede no commit inicial), reprodutibilidade (uv + lock) e independência de plataforma de mensageria para a demonstração do produto ao curso. O racional completo vive na feature `001-migracao-python-streamlit` do repo `preceptoria-mfc`. 🔴 LACUNA: validar lá.

## Consequências

- Todo o comportamento é versionado e testável; o pipeline deixou de depender de infraestrutura n8n.
- A entrada por Telegram deixou de existir; a captura de áudio passou a ser upload manual na página.
- O placeholder `{{transcricao}}` no prompt canônico aparenta ser resíduo do fluxo anterior, onde o template provavelmente era interpolado (ver ADR-0003 e lacuna L2 do domain.md). 🟡
