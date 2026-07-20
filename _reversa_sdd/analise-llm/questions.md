# Análise LLM, Questões para Validação Humana

> Gerado pelo **Writer** (Reversa) em 2026-07-20. Lacunas 🔴 desta unit que dependem do autor.

## Q1 — Placeholder `{{transcricao}}` não interpolado (L2 / DT-1 / RN-F4)

**Fato:** o template `prompts/prompt-snapps-omp.md` termina com:

```markdown
## Transcrição recebida

{{transcricao}}
```

mas `AnaliseOpenAICompat.analisar` envia o template íntegro como mensagem `system` e a transcrição como mensagem `user` separada — o placeholder nunca é substituído e chega literal ao modelo (`analise_openai.py:31-34`).

**Hipótese:** resíduo do fluxo n8n/Telegram anterior (ADR-0001), onde o template provavelmente era interpolado antes do envio. 🟡

**Impacto:** em geral inócuo (o modelo usa a mensagem `user`), mas o system prompt carrega uma seção morta que pode induzir o modelo a ecoar "Transcrição recebida" na ficha ou a tratar o placeholder como conteúdo.

**Decisão pendente — escolher uma:**
1. **Remover** as linhas 102-104 do template (mantém a arquitetura de 2 mensagens; mudança mínima). ← recomendação do Writer 🟡
2. **Interpolar** o placeholder e enviar uma única mensagem `system` (restaura o desenho original do template; muda o adaptador).
3. **Manter como está** e documentar como intencional (registrar ADR).

**Resposta do autor:** _(pendente)_

## Q2 — Sensibilidade ao modelo configurado

**Fato:** `LLM_MODEL` é livremente trocável via `.env` e nenhum teste valida a qualidade pedagógica da ficha resultante (o contrato de saída é garantido só por instrução — ver `contracts.md`).

**Pergunta:** existe um conjunto mínimo de modelos homologados para uso real (além do default `llama-3.3-70b-versatile`), ou a homologação é responsabilidade do usuário final? Vale registrar no README?

**Resposta do autor:** _(pendente)_
