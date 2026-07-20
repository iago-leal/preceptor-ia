# Transcrição de Áudio, Tarefas de Implementação

> Gerado pelo **Writer** (Reversa) em 2026-07-20.

## Pré-requisitos

- [ ] Unit `gerar-ficha` (T-01..T-05): erros nomeados, `Transcricao` e Protocol `ServicoTranscricao` prontos
- [ ] `httpx` 0.28.1 disponível (pinada em `pyproject.toml`)
- [ ] Credencial de provedor OpenAI-compatible para teste manual (os testes automatizados usam transporte mockado)

## Tarefas

- [ ] T-01, Implementar `_levantar_erro_nomeado(resposta, etapa)`: 401 → `ErroCredencial`, 429 → `ErroLimiteProvedor`, ≥400 → `ErroServicoExterno` com `resposta.text[:300]`; mensagens exatas do `contracts.md`
  - Origem no legado: `src/preceptor_ia/infra/transcricao_openai.py:49-62`
  - Critério de pronto: tabela de mapeamento do `contracts.md` coberta por teste parametrizado
  - Confiança: 🟢
  - Nota de reimplementação: extrair para módulo próprio (`infra/_http_erros.py`) para eliminar o import cruzado entre adaptadores (DT-4) 🟡

- [ ] T-02, Implementar `TranscricaoOpenAICompat` com o fluxo do `design.md` (POST multipart, `language="pt"`, `response_format="json"`, timeout 120 s, Bearer)
  - Origem no legado: `src/preceptor_ia/infra/transcricao_openai.py:20-46`
  - Critério de pronto: cenários Gherkin do `requirements.md` passam com `httpx.MockTransport`
  - Confiança: 🟢

- [ ] T-03, Garantir semântica de resposta: `.json().get("text")` com `or ""` + `strip()`; vazio → `ErroServicoExterno`; `origem_servico = f"{base_url}#{modelo}"`
  - Origem no legado: `src/preceptor_ia/infra/transcricao_openai.py:43-46`
  - Critério de pronto: `{"text": "  "}` e `{}` são rejeitados; texto válido volta com strip
  - Confiança: 🟢

## Tarefas de Teste

- [ ] TT-01, Happy path com transporte mockado (200 + text)
- [ ] TT-02, Parametrizado de status: 401, 429, 500 → exceções corretas
- [ ] TT-03, Falha de rede (transporte que levanta `httpx.ConnectError`) → `ErroServicoExterno`
- [ ] TT-04, Resposta 200 com text vazio/ausente → `ErroServicoExterno`
- [ ] TT-05, Verificar payload enviado: `language=pt`, modelo e nome de arquivo corretos
  - Referência do legado: `tests/test_adaptadores.py`

## Ordem Sugerida

1. T-01 (o tradutor de erros é pré-requisito lógico do adaptador e da unit `analise-llm`).
2. T-02 e T-03 juntos, com TT-01..05.

## Lacunas Pendentes (🔴)

- Nenhuma lacuna bloqueante. Item 🟡 a decidir na reimplementação: capturar corpo 200 não-JSON como `ErroServicoExterno` (hoje vaza exceção de parse do httpx — ver Riscos do `design.md`).
