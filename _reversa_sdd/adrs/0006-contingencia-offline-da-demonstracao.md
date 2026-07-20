# ADR-0006 — Contingência offline da demonstração

> Retroativo, gerado pelo Detective (Reversa) em 2026-07-20. Status: **aceita** (implementada). Confiança: 🟢

## Contexto

O produto será demonstrado ao vivo (curso de especialização — banca/colegas). Uma demo dependente de rede, chave válida e provedor no ar tem três pontos únicos de falha simultâneos no pior momento possível.

## Decisão

Commit dedicado (`971bad6`, 2026-07-14, o último do repositório: "ficha de exemplo gerada ponta a ponta (contingência offline da demo)") adiciona `demo/ficha-exemplo.md` — uma ficha real gerada previamente pelo pipeline completo a partir do caso simulado. A UI exibe um botão "Exibir ficha de exemplo (offline)" que renderiza o arquivo **sem nenhuma chamada externa**; o botão só aparece se o arquivo existir (`ui/app.py:89-93`).

## Consequências

- A demonstração degrada graciosamente: sem rede/chave/provedor, ainda se mostra o resultado final autêntico do produto. 🟢
- O artefato de contingência é saída genuína do pipeline (não mockup), preservando a honestidade da demo. 🟢
- Ao exibir a contingência, o estado da sessão (`ficha`, `chave_resultado`) é limpo — uma ficha recém-gerada some da tela. Aceitável no contexto de demo; surpreendente fora dele. 🟡
