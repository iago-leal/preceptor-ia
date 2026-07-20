# Relatório de Confiança — PreceptorIA

> Gerado pelo **Reviewer** (Reversa) em 2026-07-20, após a sessão de validação com o autor.
> Metodologia: contagem de marcadores 🟢/🟡/🔴 em todos os artefatos de `_reversa_sdd/` (excluídas as linhas de legenda). Marcações 🔴 remanescentes são majoritariamente referências cruzadas às **4 lacunas substantivas** de `gaps.md`.

---

## Resumo Geral

| Nível | Quantidade | Percentual |
|-------|-----------|------------|
| 🟢 CONFIRMADO | 402 | 75,3% |
| 🟡 INFERIDO   | 97  | 18,2% |
| 🔴 LACUNA     | 35  | 6,5% |
| **Total**     | 534 | 100% |

**Confiança geral: 84%** — (402 + 97×0,5) / 534.

Leitura qualitativa: projeto pequeno, recente e bem testado, com o próprio autor disponível — a extração alcançou rastreabilidade requisito→código **completa** (spec de origem verificada no repo `preceptoria-mfc`) e 100% do código executável coberto por specs. As lacunas abertas são 4, todas conhecidas, nenhuma bloqueante para reimplementação.

---

## Por Spec (units)

| Unit | 🟢 | 🟡 | 🔴 | Confiança |
|------|----|----|-----|-----------|
| `gerar-ficha/` | 37 | 4 | 2 | 91% |
| `transcricao-audio/` | 31 | 7 | 1 | 88% |
| `configuracao/` | 26 | 6 | 1 | 88% |
| `interface-streamlit/` | 35 | 8 | 4 | 83% |
| `analise-llm/` | 37 | 6 | 6 | 82% |
| `historico-local/` | 28 | 5 | 5 | 80% |

As units de menor confiança são exatamente as que carregam as lacunas G1 (prompt, em `analise-llm`) e G2 (IO, em `historico-local`) — coerente, não acidental.

---

## Lacunas Pendentes 🔴 (detalhes em [gaps.md](gaps.md))

| # | Lacuna | Spec afetada | Bloqueia reimplementação? |
|---|--------|--------------|---------------------------|
| G1 | Placeholder `{{transcricao}}` não interpolado (destino indefinido) | `analise-llm/` | Não — default recomendado: remover |
| G2 | Falha de IO do histórico aborta a entrega | `gerar-ficha/`, `historico-local/` | Não — default recomendado: best-effort |
| G3 | `Entrada` fora do try/except na UI (textarea vazio → traceback) | `interface-streamlit/` | Não — correção já prevista em T-03 |
| G4 | Modelos homologados além do default | `analise-llm/` (operação) | Não — nota de README basta |

---

## Recomendações

- [ ] **G3 é divergência objetiva de RF-06 (Must)** da spec de origem — registrar via `/reversa-debugger` quando decidir; correção trivial no legado.
- [ ] Ao decidir G1 e G2, registrar micro-ADR e atualizar `analise-llm/tasks.md` T-01 e `gerar-ficha/tasks.md` T-07.
- [ ] A reimplementação deve partir de `historico-local/tasks.md` T-02b (sufixo em colisão) — única divergência deliberada decidida em relação ao legado.
- [ ] `ui/app.py` segue sem teste automatizado — a spec sugere `streamlit.testing.v1.AppTest` (`interface-streamlit/tasks.md` TT-01).

---

## Sessão de Validação (2026-07-20)

7 perguntas apresentadas (`questions.md`): **3 resolvidas** — Q2 colisão→sufixar (🔴→🟢), Q5 rastreabilidade L1 fechada com leitura da spec de origem (🔴→🟢), Q6 escopo local single-user confirmado (🔴→🟢); **4 sem resposta** ("não sei") → `gaps.md`.

## Histórico de Reclassificações

| De | Para | Afirmação | Evidência |
|----|------|-----------|-----------|
| 🔴 | 🟢 | L1: códigos RF/RN/RD/D rastreáveis à spec de origem | `~/dev/preceptoria-mfc/_reversa_forward/001-migracao-python-streamlit/requirements.md` (RF-01..09, RN-01..08) e `roadmap.md` (D-07) |
| 🔴 | 🟢 | L3/DT-3: política de colisão do histórico | Decisão do autor (sufixar), 2026-07-20 → `historico-local/tasks.md` T-02b |
| 🔴 | 🟢 | P2: deploy multiusuário fora de escopo | Confirmação do autor (protótipo de instalação local), 2026-07-20 |
| 🟡 | 🟢 | `Ficha.contexto` nunca preenchido — propósito explicado | RF-07 da spec de origem ("data e identificação de contexto") |
| 🟢 | 🟢 | Correção de precisão: transcrição lê o campo `text` do JSON (não `resposta.text`) | `data-dictionary.md` corrigido contra `transcricao_openai.py:43` |

## Revisão Cruzada

Não realizada — engine externa (Codex) indisponível nesta sessão; revisão conduzida pelo próprio Reviewer com releitura integral do código-fonte e da suíte de testes.
