# ADR-0005 — Não-retenção por padrão; histórico local opt-in

> Retroativo, gerado pelo Detective (Reversa) em 2026-07-20. Status: **aceita** (implementada). Confiança: 🟢

## Contexto

Passagens de caso reais contêm dados de pacientes (LGPD). A ferramenta envia conteúdo a um provedor de IA externo — o risco de privacidade é o principal passivo do produto, e o autor é médico (responsabilidade profissional direta).

## Decisão

Privacidade por arquitetura, em três camadas:

1. **Não-retenção**: áudio e transcrição circulam apenas em memória; após a transcrição, o áudio é descartado (RN-07, `gerar_ficha.py:57`).
2. **Histórico opt-in**: `HISTORICO_ATIVO=false` por padrão; quando desligado, o repositório nem é injetado (`factory.py:19`). Quando ligado, grava fora do repositório git (`~/.preceptor-ia/historico`).
3. **Responsabilização informada**: aviso permanente na UI — casos simulados em demos públicas; anonimização de casos reais é responsabilidade do preceptor (`ui/app.py:27-34`).

Complementos: logs registram só metadados (nunca conteúdo clínico), e o modo demo usa caso inteiramente simulado.

## Consequências

- O passivo LGPD é reduzido ao trânsito pelo provedor de IA — explicitado ao usuário, não escondido. 🟢
- Sem histórico ativo não há qualquer rastro local das fichas além do download manual. 🟢
- A responsabilidade residual é deliberadamente transferida ao preceptor via aviso — decisão de produto, não de código. 🟢
- 🔴 LACUNA: não há termo de uso/consentimento formal além do aviso; se o produto for institucionalizado (curso/hospital), validar se o aviso basta juridicamente.
