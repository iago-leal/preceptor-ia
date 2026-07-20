# Configuração, Tarefas de Implementação

> Gerado pelo **Writer** (Reversa) em 2026-07-20.

## Pré-requisitos

- [ ] `pydantic-settings` 2.14.2 (pinada em `pyproject.toml`)
- [ ] Nenhuma dependência de outras units (esta é a unit mais independente — boa candidata a primeira)

## Tarefas

- [ ] T-01, Criar `ErroConfiguracao(RuntimeError)` — fora da hierarquia `ErroPreceptorIA`, por design
  - Origem no legado: `src/preceptor_ia/config.py:9-10`
  - Critério de pronto: `except ErroPreceptorIA` NÃO captura `ErroConfiguracao`
  - Confiança: 🟢

- [ ] T-02, Criar `Settings(BaseSettings)` com os 6 campos, defaults e `SettingsConfigDict(env_file=".env", extra="ignore")` conforme tabela do `design.md`
  - Origem no legado: `src/preceptor_ia/config.py:13-21`
  - Critério de pronto: RF-CF-01/03/04 verificados por teste com `monkeypatch` de ambiente
  - Confiança: 🟢

- [ ] T-03, Criar `carregar_settings()` envelopando qualquer exceção em `ErroConfiguracao` com a mensagem exata do `design.md` (incluindo `from exc`)
  - Origem no legado: `src/preceptor_ia/config.py:24-32`
  - Critério de pronto: cenários Gherkin do `requirements.md` passam
  - Confiança: 🟢

- [ ] T-04, Criar `.env.example` documentando as 6 variáveis (obrigatória sinalizada; defaults comentados)
  - Origem no legado: `.env.example`
  - Critério de pronto: copiar para `.env` + preencher a chave é suficiente para rodar
  - Confiança: 🟢

## Tarefas de Teste

- [ ] TT-01, Só `LLM_API_KEY` definida → defaults corretos nos 5 campos restantes
- [ ] TT-02, Ambiente vazio → `ErroConfiguracao` com a mensagem acionável
- [ ] TT-03, `LLM_API_KEY=""` → `ErroConfiguracao` (min_length)
- [ ] TT-04, Coerção: `HISTORICO_ATIVO=true` → `bool`; `HISTORICO_DIR=/x/y` → `Path`
  - Referência do legado: cobertura distribuída nas suítes existentes 🟡 (não há `test_config.py` dedicado no legado)

## Ordem Sugerida

1. T-01 → T-02 → T-03 → T-04, linear (cada uma depende da anterior).

## Lacunas Pendentes (🔴)

- Nenhuma. Itens 🟡 do `design.md` (mensagem fixa citando `LLM_API_KEY`; `.env` relativo ao cwd) são melhorias opcionais a decidir na reimplementação.
