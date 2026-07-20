# Histórico Local, Questões para Validação Humana

> Gerado pelo **Writer** (Reversa) em 2026-07-20. Lacunas 🔴 desta unit que dependem do autor.

## Q1 — Política de colisão de nome (L3 / DT-3 / RN-C5)

**Fato:** duas fichas com a mesma origem (ou mesmo `contexto`) geradas no mesmo minuto produzem o mesmo nome `{YYYYMMDDHHmm}-ficha-{slug}.md`; `write_text` sobrescreve a primeira sem aviso (`historico.py:19-21`).

**Impacto:** perda silenciosa de ficha em uso intenso (ex.: preceptor processa duas passagens de caso em sequência rápida). Contradiz o princípio de "erros barulhentos" do projeto, se não for deliberado.

**Decisão pendente — escolher uma:**
1. **Sufixar** em colisão (`-2`, `-3`, ... ou segundos no timestamp). ← recomendação do Writer 🟡
2. **Manter sobrescrita** e registrar como decisão aceita (volume esperado ≈ 1 ficha por passagem de caso; janela de 1 minuto improvável).
3. **Falhar barulhento** (`ErroHistorico` se o arquivo já existe).

✅ Respondida
**Resposta do autor (2026-07-20):** **Opção 1 — sufixar.** Política oficial: em colisão de nome, acrescentar sufixo de desambiguação (`-2`, `-3`, ...). O legado sobrescreve; a divergência vira correção obrigatória na reimplementação (`tasks.md` T-02b/TT-04). 🔴→🟢

## Q2 — Isolamento de falha de IO (DT-2)

**Fato:** `gravar` não tem tratamento de erro e o caso de uso chama `self._historico.gravar(ficha)` sem try/except (`gerar_ficha.py:41-42`). Uma falha de IO (permissão, disco cheio) aborta a entrega de uma ficha **já gerada** — e, por ser `OSError` (fora da hierarquia `ErroPreceptorIA`), vazaria como stack trace do Streamlit na UI, único ponto do sistema onde isso pode ocorrer.

**Pergunta:** o histórico deve ser best-effort (logar aviso e entregar a ficha mesmo assim) ou a falha de gravação deve mesmo impedir a entrega? A postura de "erros barulhentos" sugere ao menos converter em erro nomeado.

**Resposta do autor:** _(pendente)_
