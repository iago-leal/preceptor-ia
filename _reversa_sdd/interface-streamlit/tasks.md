# Interface Streamlit, Tarefas de Implementação

> Gerado pelo **Writer** (Reversa) em 2026-07-20.

## Pré-requisitos

- [ ] Todas as demais units prontas (esta é a última — consome a fábrica completa)
- [ ] `streamlit` 1.59.2
- [ ] Artefatos de demo: `demo/transcricao-simulada.md` (obrigatório para a aba demo) e `demo/ficha-exemplo.md` (opcional, habilita a contingência)

## Tarefas

- [ ] T-01, Montar o esqueleto da página: `set_page_config` (🩺, centered), título, caption e `st.warning` LGPD com o texto integral de `app.py:27-34`
  - Origem no legado: `src/preceptor_ia/ui/app.py:19-34`
  - Critério de pronto: aviso visível antes de qualquer interação
  - Confiança: 🟢

- [ ] T-02, Implementar `_caso_de_uso()` com `@st.cache_resource` chamando `montar_gerar_ficha()`
  - Origem no legado: `src/preceptor_ia/ui/app.py:37-39`
  - Critério de pronto: fábrica executa uma única vez por processo (verificável pelo log de carga)
  - Confiança: 🟢

- [ ] T-03, Implementar as três abas com o padrão fila-de-1: cada botão constrói `Entrada` e grava em `session_state["entrada_pendente"]`; aba áudio com `file_uploader(type=["ogg","mp3","m4a","wav"])`; aba demo lê `TRANSCRICAO_DEMO`; botão de contingência condicional a `FICHA_CONTINGENCIA.is_file()`
  - Origem no legado: `src/preceptor_ia/ui/app.py:60-93`
  - Critério de pronto: RF-UI-01..04 do `requirements.md`
  - Confiança: 🟢
  - Nota: avaliar corrigir aqui o risco 🔴 do `design.md` (construir `Entrada` dentro de fluxo protegido)

- [ ] T-04, Implementar `_gerar` com dedup SHA-256 e `st.status` (etapas condicionais por origem), gravando `chave_resultado` e `ficha` no sucesso
  - Origem no legado: `src/preceptor_ia/ui/app.py:42-57`
  - Critério de pronto: RF-UI-05; resubmissão idêntica não repete chamadas externas (verificar com dublê/mock)
  - Confiança: 🟢

- [ ] T-05, Implementar o consumo da fila (`pop`) com try/except: `ErroConfiguracao` → "⚙️", `ErroPreceptorIA` → "❌"
  - Origem no legado: `src/preceptor_ia/ui/app.py:95-102`
  - Critério de pronto: RF-UI-06; nenhum stack trace nos cenários Gherkin de erro
  - Confiança: 🟢

- [ ] T-06, Implementar render final: ficha em markdown + `download_button` (`{%Y%m%d%H%M}-ficha-snapps-omp.md`, `text/markdown`, conteúdo com newline final)
  - Origem no legado: `src/preceptor_ia/ui/app.py:104-113`
  - Critério de pronto: RF-UI-07
  - Confiança: 🟢

- [ ] T-07, Configurar `logging.basicConfig(level=INFO, format="%(asctime)s %(levelname)s %(name)s | %(message)s")` no topo do entry point
  - Origem no legado: `src/preceptor_ia/ui/app.py:13`
  - Critério de pronto: logs `etapa=...` visíveis no terminal do Streamlit
  - Confiança: 🟢

## Tarefas de Teste

- [ ] TT-01, Smoke com `streamlit.testing.v1.AppTest`: página carrega, 3 abas presentes, aviso LGPD visível 🟡 (não existe no legado — melhoria)
- [ ] TT-02, Fluxo texto com caso de uso mockado → ficha renderizada + download
- [ ] TT-03, Erro de configuração → mensagem "⚙️" sem traceback
- [ ] TT-04, Dedup: dois cliques com o mesmo texto → 1 chamada ao caso de uso

## Ordem Sugerida

1. T-01, T-02, T-07 (esqueleto e composição).
2. T-03 → T-04 → T-05 (fluxo de geração).
3. T-06 e testes por último.

## Lacunas Pendentes (🔴)

- Construção de `Entrada` fora do try/except (textarea vazio → traceback): corrigir na reimplementação ou registrar como aceito. Ver Riscos do `design.md`.
