# Perguntas para Validação — PreceptorIA

> Gerado pelo **Reviewer** (Reversa) em 2026-07-20.
> `answer_mode = chat`: as perguntas são feitas no chat; este arquivo é o registro consolidado.
> Respostas processadas atualizam as specs afetadas e o `confidence-report.md`.

---

## Pergunta 1 — Placeholder `{{transcricao}}` não interpolado

**Contexto:** `prompts/prompt-snapps-omp.md:102-104` termina com `## Transcrição recebida` + `{{transcricao}}`, mas `infra/analise_openai.py:31-34` envia o template íntegro como mensagem `system` e a transcrição como mensagem `user` — o placeholder chega literal ao modelo. (L2 / DT-1 / RN-F4)
**Spec afetada:** [`analise-llm/questions.md` Q1, `analise-llm/design.md`, `analise-llm/tasks.md` T-01]
**Pergunta:** O placeholder é resíduo do fluxo n8n anterior ou intencional? O que fazer: (a) remover as linhas 102-104, (b) interpolar e enviar mensagem única, ou (c) manter e documentar?
**Impacto:** Define a forma final do prompt canônico na reimplementação; se (a) ou (b), o template atual está formalmente incorreto.

**Resposta:** "Não sei" (autor, 2026-07-20). Permanece 🔴 — registrada em `gaps.md`.

---

## Pergunta 2 — Colisão de nome no histórico

**Contexto:** `infra/historico.py:19-21` — duas fichas de mesma origem no mesmo minuto geram o mesmo nome e a segunda sobrescreve a primeira sem aviso. (L3 / DT-3 / RN-C5)
**Spec afetada:** [`historico-local/questions.md` Q1, `historico-local/requirements.md`, `historico-local/tasks.md` TT-04]
**Pergunta:** Sobrescrever é aceitável para o volume esperado, ou a política deve ser sufixar (`-2`) / falhar barulhento?
**Impacto:** Muda RN e teste de colisão; se sobrescrita for aceita, vira decisão registrada (🟢) em vez de lacuna.

✅ Respondida
**Resposta:** **Sufixar** (autor, 2026-07-20). Política decidida: em colisão, acrescentar sufixo de desambiguação. O comportamento do legado (sobrescrita) fica registrado como divergência a corrigir na reimplementação. Specs atualizadas: `historico-local/requirements.md`, `historico-local/tasks.md`, `historico-local/questions.md`, `domain.md` (L3). 🔴→🟢

---

## Pergunta 3 — Falha de IO do histórico aborta a entrega

**Contexto:** `application/gerar_ficha.py:41-42` grava o histórico sem try/except; um `OSError` (permissão, disco cheio) aborta a entrega de ficha já gerada e, por estar fora da hierarquia `ErroPreceptorIA`, vaza como stack trace na UI — único ponto do sistema onde isso ocorre. (DT-2)
**Spec afetada:** [`historico-local/questions.md` Q2, `gerar-ficha/design.md`, `gerar-ficha/tasks.md`]
**Pergunta:** O histórico deve ser best-effort (loga aviso, entrega a ficha) ou a falha deve mesmo impedir a entrega (e então virar erro nomeado, ex.: `ErroHistorico`)?
**Impacto:** Altera o fluxo do caso de uso (passo 6) e a hierarquia de erros.

**Resposta:** "Não sei" (autor, 2026-07-20). Permanece 🔴 — registrada em `gaps.md`.

---

## Pergunta 4 — `Entrada` construída fora do try/except na UI

**Contexto:** Achado novo do Writer: em `ui/app.py:74-77`, o clique em "Gerar ficha a partir do texto" constrói `Entrada(...)` dentro do bloco da aba, fora do try/except de `app.py:97-102`. Com o textarea vazio, `ErroEntradaInvalida` vira stack trace na página em vez de mensagem "❌" — contradiz RF-UI-06 e RN-U5.
**Spec afetada:** [`interface-streamlit/design.md` (Riscos), `interface-streamlit/tasks.md` T-03]
**Pergunta:** Confirma que é bug (a corrigir movendo a construção para o fluxo protegido) ou comportamento aceito para a validação conceitual?
**Impacto:** Se bug, entra como correção obrigatória na reimplementação (e candidato a fix imediato no legado); se aceito, a spec registra a exceção à regra.

**Resposta:** "Não sei" (autor, 2026-07-20). Permanece 🔴 — registrada em `gaps.md`. Sugestão do Reviewer: registrável via `/reversa-debugger` para triagem formal quando decidir.

---

## Pergunta 5 — Spec de origem dos códigos RF/RN/RD/D

**Contexto:** Comentários no código citam RF-01, RN-02, RN-03, RN-06, RN-07, RF-04, RF-05, RF-07, RD-01, D-07 — referências à spec da feature `001-migracao-python-streamlit` no repositório `preceptoria-mfc`, fora deste repo. (L1)
**Spec afetada:** [rastreabilidade de todas as units; `domain.md` §3]
**Pergunta:** Você pode disponibilizar aquela spec (cópia ou caminho local em `~/dev/preceptoria-mfc`) para fechar a rastreabilidade requisito→código?
**Impacto:** Com acesso, os códigos citados podem ser verificados e a rastreabilidade sobe de 🔴 para 🟢; sem, permanece lacuna documentada.

✅ Respondida
**Resposta:** Autorizada a leitura (autor, 2026-07-20). Spec localizada em `~/dev/preceptoria-mfc/_reversa_forward/001-migracao-python-streamlit/` e verificada: RF-01..RF-09, RN-01..RN-08 (requirements.md), RD-01..RD-05 (extração do legado n8n) e D-07 (roadmap.md, decisão do histórico Markdown datestampado) — todos os códigos citados no código conferem. Rastreabilidade L1 fechada. `domain.md` §3 atualizado. 🔴→🟢

---

## Pergunta 6 — Horizonte de deploy multiusuário

**Contexto:** `permissions.md` P2 — não há autenticação nem isolamento de histórico; aceitável localmente, bloqueante para qualquer publicação (ex.: Streamlit Cloud para a banca do curso).
**Spec afetada:** [`permissions.md`, `architecture.md` §7]
**Pergunta:** Existe intenção de publicar a ferramenta (mesmo temporariamente) para terceiros? Em que horizonte?
**Impacto:** Se sim, gate de acesso e isolamento de dados entram como requisitos Must de uma próxima feature; se não, o risco fica registrado como fora de escopo.

✅ Respondida
**Resposta:** É produto técnico (estilo protótipo) para a pessoa instalar no próprio computador (autor, 2026-07-20). Modelo de distribuição: cada preceptor roda a sua instância local — coerente com o RNF de Distribuição da spec de origem (repo público + manual de implantação). Deploy multiusuário hospedado está **fora de escopo**; a ausência de auth deixa de ser lacuna e vira decisão de escopo. `permissions.md` (P2) e `architecture.md` (§7) atualizados. 🔴→🟢

---

## Pergunta 7 — Modelos homologados para a análise

**Contexto:** `LLM_MODEL` é livremente trocável via `.env`; a qualidade pedagógica da ficha depende do modelo e nada a valida. (Q2 de `analise-llm/questions.md`)
**Spec afetada:** [`analise-llm/contracts.md`, README (recomendação)]
**Pergunta:** Além do default `llama-3.3-70b-versatile`, há modelos homologados/testados que valha registrar? A homologação é responsabilidade do usuário final?
**Impacto:** Documentação de operação; não bloqueia reimplementação.

**Resposta:** "Não sei" (autor, 2026-07-20). Permanece 🔴 — registrada em `gaps.md` (severidade baixa: só o default está implicitamente homologado pelo uso).
