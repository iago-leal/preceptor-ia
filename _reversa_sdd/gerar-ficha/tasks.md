# Gerar Ficha, Tarefas de Implementação

> Gerado pelo **Writer** (Reversa) em 2026-07-20.
> Sequência para reimplementar a unit a partir das specs, sem acesso ao código original.

## Pré-requisitos

- [ ] Python ≥ 3.12 (usa `StrEnum`, sintaxe `X | None`)
- [ ] Prompt canônico disponível em `prompts/prompt-snapps-omp.md` (ver unit `analise-llm`)
- [ ] Nenhuma dependência externa nesta unit — domínio e aplicação usam somente stdlib

## Tarefas

- [ ] T-01, Criar hierarquia de erros: `ErroPreceptorIA(Exception)` raiz e subclasses `ErroEntradaInvalida`, `ErroCredencial`, `ErroLimiteProvedor`, `ErroServicoExterno`, `ErroRespostaAnalise`
  - Origem no legado: `src/preceptor_ia/domain/models.py:11-32`
  - Critério de pronto: `except ErroPreceptorIA` captura todas as subclasses
  - Confiança: 🟢

- [ ] T-02, Criar `OrigemEntrada(StrEnum)` com valores `audio`, `texto`, `demo`
  - Origem no legado: `src/preceptor_ia/domain/models.py:35-38`
  - Critério de pronto: `OrigemEntrada.AUDIO.value == "audio"`
  - Confiança: 🟢

- [ ] T-03, Criar dataclass frozen `Entrada` com validação no `__post_init__`: texto/demo exigem `texto_transcricao` não-vazio (strip); áudio exige `nome_arquivo` + `conteudo_audio`, extensão ∈ {`.ogg`, `.mp3`, `.m4a`, `.wav`} (case-insensitive, via `rsplit(".", 1)`), tamanho ≤ `25 * 1024 * 1024` bytes
  - Origem no legado: `src/preceptor_ia/domain/models.py:41-72`
  - Critério de pronto: cenários Gherkin de entrada inválida do `requirements.md` passam; mensagens de erro orientadas ao usuário (citam formatos aceitos / limite de 25 MB)
  - Confiança: 🟢

- [ ] T-04, Criar dataclasses frozen `Transcricao(texto, origem_servico)` e `Ficha(markdown, origem_entrada, contexto=None, gerada_em=datetime.now via default_factory)`
  - Origem no legado: `src/preceptor_ia/domain/models.py:75-88`
  - Critério de pronto: `Ficha` sem `gerada_em` explícito recebe o horário de construção
  - Confiança: 🟢

- [ ] T-05, Criar Protocols `ServicoTranscricao.transcrever(conteudo: bytes, nome_arquivo: str) -> Transcricao`, `ServicoAnalise.analisar(prompt_sistema: str, transcricao: str) -> str`, `RepositorioHistorico.gravar(ficha: Ficha) -> None`
  - Origem no legado: `src/preceptor_ia/domain/ports.py`
  - Critério de pronto: dublês de teste satisfazem os Protocols sem herança
  - Confiança: 🟢

- [ ] T-06, Criar `carregar_prompt(caminho=CAMINHO_PROMPT_PADRAO) -> str` com `ErroPromptCanonico` (subclasse de `ErroPreceptorIA`) para arquivo ausente ou vazio; retorno com `strip()`
  - Origem no legado: `src/preceptor_ia/domain/prompt.py`
  - Critério de pronto: caminho padrão resolve `prompts/prompt-snapps-omp.md` a partir da raiz do repositório
  - Confiança: 🟢

- [ ] T-07, Implementar `GerarFicha` (construtor com 4 dependências, `executar`, `_obter_transcricao`) seguindo o fluxo numerado do `design.md`, incluindo os 4 logs `etapa=...`
  - Origem no legado: `src/preceptor_ia/application/gerar_ficha.py`
  - Critério de pronto: cenários Gherkin do `requirements.md` passam com dublês; áudio não referenciado após transcrição
  - Confiança: 🟢

- [ ] T-08, Implementar `montar_gerar_ficha(settings=None)`: carrega settings e prompt, instancia adaptadores com `(base_url, api_key, modelo)` e injeta histórico somente se `historico_ativo`
  - Origem no legado: `src/preceptor_ia/application/factory.py`
  - Critério de pronto: com `historico_ativo=False`, o caso de uso recebe `historico=None`
  - Confiança: 🟢

## Tarefas de Teste

- [ ] TT-01, Happy path texto/demo com dublês (análise devolve Markdown; transcrição não chamada)
- [ ] TT-02, Happy path áudio (transcrição chamada com bytes+nome; texto transcrito vai à análise)
- [ ] TT-03, Resposta de análise vazia → `ErroRespostaAnalise`
- [ ] TT-04, Matriz de entradas inválidas (texto vazio, áudio sem arquivo, extensão errada, > 25 MB)
- [ ] TT-05, Histórico: chamado quando injetado, ausente quando `None`
  - Referência do legado: `tests/test_gerar_ficha.py`, `tests/test_domain.py`

## Ordem Sugerida

1. T-01 → T-04 (domínio puro, sem dependências entre si além dos erros).
2. T-05 e T-06 (contratos e prompt) — desbloqueiam T-07.
3. T-07 (caso de uso) com testes TT-01..05 em paralelo.
4. T-08 por último: exige as units `configuracao`, `transcricao-audio`, `analise-llm` e `historico-local` prontas.

## Lacunas Pendentes (🔴)

- Decidir se a falha de IO do histórico deve abortar a entrega da ficha (comportamento atual) ou ser isolada com log de aviso — ver `historico-local/questions.md`.
