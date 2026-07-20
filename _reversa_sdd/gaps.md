# Lacunas Remanescentes — PreceptorIA

> Gerado pelo **Reviewer** (Reversa) em 2026-07-20, após a sessão de validação com o autor.
> Das 7 perguntas de `questions.md`, 3 foram resolvidas (Q2 sufixar, Q5 rastreabilidade fechada, Q6 escopo local confirmado). As 4 abaixo receberam "não sei" e permanecem 🔴 — nenhuma bloqueia a reimplementação, mas as duas primeiras afetam decisões de código.

## G1 — Placeholder `{{transcricao}}` não interpolado (ex-Q1 · L2 · DT-1)

O template do prompt canônico termina com `## Transcrição recebida` + `{{transcricao}}` (`prompts/prompt-snapps-omp.md:102-104`), mas o adaptador envia a transcrição como mensagem `user` separada — o placeholder chega literal ao LLM. Provável resíduo do fluxo n8n (a spec de origem confirma que o prompt veio intacto do legado, RF-04 "o prompt não muda"). 🟡

**Estado:** autor indeciso. **Default recomendado para reimplementação:** remover as linhas 102-104 (opção de menor risco; registrar micro-ADR ao decidir). **Afeta:** `analise-llm/tasks.md` T-01.

## G2 — Falha de IO do histórico aborta a entrega (ex-Q3 · DT-2)

`gerar_ficha.py:41-42` grava o histórico sem isolamento de falha; um `OSError` impede a entrega de ficha já gerada e vaza como exceção crua até a UI (fora da hierarquia `ErroPreceptorIA`).

**Estado:** autor indeciso. **Default recomendado:** best-effort (capturar, logar `etapa=historico erro=...`, entregar a ficha) — coerente com o caráter opcional/Could do histórico (RF-07). **Afeta:** `gerar-ficha/tasks.md` T-07, `historico-local/tasks.md`.

## G3 — `Entrada` construída fora do try/except na UI (ex-Q4 · achado do Writer)

Textarea vazio na aba de texto produz `ErroEntradaInvalida` na construção da `Entrada` (`ui/app.py:77`), fora do bloco protegido (`app.py:97-102`) — stack trace na página em vez de mensagem "❌", contrariando RF-06 da spec de origem ("mensagem clara com a etapa que falhou").

**Estado:** autor indeciso sobre classificar como bug do legado. **Avaliação do Reviewer:** é divergência objetiva de RF-06 (Must na spec de origem) — recomenda-se registrá-la via `/reversa-debugger` quando o autor decidir. Na reimplementação, a construção deve ocorrer em fluxo protegido (`interface-streamlit/tasks.md` T-03 já prevê). **Afeta:** `interface-streamlit/`.

## G4 — Modelos homologados para a análise (ex-Q7)

Apenas o default `llama-3.3-70b-versatile` está implicitamente homologado pelo uso; nenhum outro modelo foi testado e nada valida a qualidade pedagógica da ficha por modelo.

**Estado:** autor não sabe. **Severidade baixa:** documentação de operação; não bloqueia nada. **Sugestão:** anotar no README que o default é o único testado.
