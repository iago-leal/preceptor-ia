# Análise LLM, Tarefas de Implementação

> Gerado pelo **Writer** (Reversa) em 2026-07-20.

## Pré-requisitos

- [ ] Unit `gerar-ficha` (T-01, T-06): erros nomeados e `carregar_prompt` prontos
- [ ] Unit `transcricao-audio` (T-01): `_levantar_erro_nomeado` disponível (idealmente já extraído para módulo comum)
- [ ] `httpx` 0.28.1

## Tarefas

- [ ] T-01, Recriar o prompt canônico `prompts/prompt-snapps-omp.md` com os 4 blocos documentados no `design.md`: papel/tarefa, modelos SNAPPS + OMP, instruções de fidelidade e template literal da ficha (cabeçalho + 3 seções)
  - Origem no legado: `prompts/prompt-snapps-omp.md:1-99`
  - Critério de pronto: ficha gerada com caso demo reproduz todas as seções; campos ausentes viram "Não identificado na transcrição" / "A preencher"
  - Confiança: 🟢
  - **Atenção:** NÃO reproduzir as linhas 102-104 (`## Transcrição recebida` + `{{transcricao}}`) sem antes resolver a questão Q1 de `questions.md` 🔴

- [ ] T-02, Implementar `AnaliseOpenAICompat` com o fluxo do `design.md` (POST JSON, 2 mensagens, `temperature=0.2`, timeout 120 s, Bearer)
  - Origem no legado: `src/preceptor_ia/infra/analise_openai.py:17-37`
  - Critério de pronto: payload verificado por teste com `httpx.MockTransport` (modelo, temperatura, papéis das mensagens)
  - Confiança: 🟢

- [ ] T-03, Implementar parse defensivo: `choices[0].message.content` com captura de `KeyError`/`IndexError`/`ValueError` → `ErroRespostaAnalise` (corpo truncado em 300); conteúdo vazio → `ErroRespostaAnalise`
  - Origem no legado: `src/preceptor_ia/infra/analise_openai.py:41-50`
  - Critério de pronto: cenários Gherkin de resposta malformada/vazia do `requirements.md` passam
  - Confiança: 🟢

## Tarefas de Teste

- [ ] TT-01, Happy path com transporte mockado (200 + choices completo)
- [ ] TT-02, Parametrizado de status 401/429/500 → exceções nomeadas (etapa "análise")
- [ ] TT-03, JSON sem `choices` / lista vazia / content vazio → `ErroRespostaAnalise`
- [ ] TT-04, Falha de rede → `ErroServicoExterno`
- [ ] TT-05, Verificar payload: system = prompt, user = transcrição, `temperature == 0.2`
- [ ] TT-06, Prompt canônico: arquivo presente, não-vazio, contém os marcadores das 3 seções da ficha (teste de contrato do artefato de dado)
  - Referência do legado: `tests/test_adaptadores.py`, `tests/test_domain.py`

## Ordem Sugerida

1. T-01 (prompt) — independe de código e destrava validação manual ponta a ponta.
2. T-02 e T-03 juntos, com TT-01..05.

## Lacunas Pendentes (🔴)

- **Q1 (L2/DT-1):** destino do placeholder `{{transcricao}}` — remover a seção residual do template, ou passar a interpolá-la (e então enviar uma única mensagem system)? Ver `questions.md`. Bloqueia a forma final de T-01.
