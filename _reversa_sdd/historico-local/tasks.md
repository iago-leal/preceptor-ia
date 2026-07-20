# Histórico Local, Tarefas de Implementação

> Gerado pelo **Writer** (Reversa) em 2026-07-20.

## Pré-requisitos

- [ ] Unit `gerar-ficha` (T-04, T-05): `Ficha` e Protocol `RepositorioHistorico` prontos
- [ ] Unit `configuracao`: `historico_ativo` e `historico_dir` disponíveis nas Settings
- [ ] Somente stdlib (`pathlib`, `re`)

## Tarefas

- [ ] T-01, Implementar `_slug(texto)`: lower → `[^a-z0-9]+` vira `-` → strip de `-` → fallback `"sem-contexto"`
  - Origem no legado: `src/preceptor_ia/infra/historico.py:25-27`
  - Critério de pronto: casos do `requirements.md` (RF-HL-03) passam, incluindo acentos e string vazia
  - Confiança: 🟢

- [ ] T-02, Implementar `HistoricoFilesystem` com o fluxo de 5 passos do `design.md` (expanduser no construtor, mkdir, nome datestampado, write_text UTF-8 com newline final, log)
  - Origem no legado: `src/preceptor_ia/infra/historico.py:12-22`
  - Critério de pronto: cenários Gherkin do `requirements.md` passam com `tmp_path`
  - Confiança: 🟢

- [ ] T-02b, [Revisão] Implementar desambiguação por sufixo em colisão de nome (`-2`, `-3`, ...) — decisão do autor de 2026-07-20; diverge deliberadamente do legado, que sobrescreve
  - Origem: `questions.md` Q1 (política decidida); comportamento legado em `src/preceptor_ia/infra/historico.py:19-21`
  - Critério de pronto: duas gravações no mesmo minuto e mesmo slug produzem dois arquivos distintos
  - Confiança: 🟢 (decisão registrada)

- [ ] T-03, Garantir a injeção condicional na fábrica: `HistoricoFilesystem(cfg.historico_dir) if cfg.historico_ativo else None`
  - Origem no legado: `src/preceptor_ia/application/factory.py:19`
  - Critério de pronto: RF-HL-04 verificado por teste da fábrica
  - Confiança: 🟢

## Tarefas de Teste

- [ ] TT-01, Gravação feliz em `tmp_path`: nome, conteúdo, encoding
- [ ] TT-02, Diretório inexistente criado automaticamente
- [ ] TT-03, `_slug` parametrizado (maiúsculas, pontuação, vazio, só símbolos)
- [ ] TT-04, [Revisão] Colisão de minuto: segunda gravação recebe sufixo `-2` e nenhum arquivo é perdido (política decidida em Q1; o legado sobrescrevia)
  - Referência do legado: `tests/test_historico.py`

## Ordem Sugerida

1. T-01 → T-02 (o slug é usado pelo nome do arquivo).
2. T-03 depois que a unit `configuracao` existir.

## Lacunas Pendentes (🔴)

- ~~**Q1 (L3/DT-3):** política de colisão~~ ✅ Resolvida (2026-07-20): **sufixar** — ver T-02b e TT-04.
- **Q2 (DT-2):** isolamento da falha de IO — decidir se a exceção deve virar erro nomeado (ex.: `ErroHistorico`) sem abortar a entrega. Afeta `gerar-ficha/T-07`. Autor respondeu "não sei" em 2026-07-20 — permanece aberta em `../gaps.md`.
