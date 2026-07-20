# Interface Streamlit, Design Técnico

> Gerado pelo **Writer** (Reversa) em 2026-07-20.
> Escala: 🟢 CONFIRMADO · 🟡 INFERIDO · 🔴 LACUNA

## Interface

Script Streamlit top-level (sem função `main`), executado por `uv run streamlit run src/preceptor_ia/ui/app.py`. Símbolos internos:

| Símbolo | Assinatura | Papel |
|---------|-----------|-------|
| `_caso_de_uso` | `() -> GerarFicha`, decorada com `@st.cache_resource` | Fábrica cacheada por processo |
| `_gerar` | `(entrada: Entrada) -> None` | Dedup + execução + gravação do resultado em `session_state` |

Constantes de caminho: `RAIZ = Path(__file__).resolve().parents[3]`; `TRANSCRICAO_DEMO = RAIZ/"demo"/"transcricao-simulada.md"`; `FICHA_CONTINGENCIA = RAIZ/"demo"/"ficha-exemplo.md"`. 🟢

Chaves de `st.session_state`:

| Chave | Tipo | Papel |
|---|---|---|
| `entrada_pendente` | `Entrada \| ausente` | Fila de 1 elemento entre o clique e o processamento |
| `chave_resultado` | `str (SHA-256) \| None` | Identidade da última entrada processada (dedup) |
| `ficha` | `Ficha \| None` | Resultado exibido |

## Fluxo Principal (por rerun do script)

1. `st.set_page_config` (título "PreceptorIA", ícone 🩺, layout centered) + título + caption + `st.warning` LGPD (`app.py:19-34`).
2. Três abas (`st.tabs`): áudio (`st.file_uploader` com `type=["ogg","mp3","m4a","wav"]`), texto (`st.text_area` height 220), demo (markdown explicativo + botões). Cada botão "Gerar ficha..." apenas grava `st.session_state["entrada_pendente"] = Entrada(...)` (`app.py:60-93`).
3. Fora das abas: `entrada_pendente = st.session_state.pop("entrada_pendente", None)`; se presente, `_gerar(entrada)` dentro de try/except (`app.py:95-102`).
4. `_gerar`: calcula `chave = sha256((origem.value + (texto or "")).encode() + (audio or b"")).hexdigest()`; se igual a `chave_resultado`, retorna sem efeito. Senão abre `st.status("Gerando ficha…")`, escreve as etapas (2 para áudio, 1 para texto/demo), chama `_caso_de_uso().executar(entrada)`, escreve "▸ análise concluída", marca `state="complete"` e grava `chave_resultado` + `ficha` (`app.py:42-57`).
5. Render final: se `ficha` presente, separador + `st.markdown(ficha.markdown)` + `st.download_button` com `data=ficha.markdown + "\n"`, `file_name={%Y%m%d%H%M}-ficha-snapps-omp.md`, `mime="text/markdown"` (`app.py:104-113`).

## Fluxos Alternativos

- **`ErroConfiguracao`** → `st.error(f"⚙️ {exc}")`; **`ErroPreceptorIA`** → `st.error(f"❌ {exc}")` (`app.py:99-102`). Exceções fora dessas duas famílias (ex.: `OSError` do histórico) vazam para o handler default do Streamlit. 🟡
- **`ErroEntradaInvalida` no clique:** a construção `Entrada(...)` acontece dentro do bloco da aba, **fora** do try/except — entrada inválida (ex.: textarea vazio) vaza como exceção do Streamlit em vez de virar "❌". 🟡 Na prática o file_uploader e o botão mitigam o caso de áudio, mas o textarea vazio reproduz o problema. 🔴 validar se é aceitável
- **Contingência offline:** botão condicional (`FICHA_CONTINGENCIA.is_file()`) zera `ficha`/`chave_resultado` e renderiza o arquivo direto na aba, fora do fluxo de geração (`app.py:89-93`).

## Dependências

- `streamlit` (confinado a esta unit), `hashlib`, `logging`, `pathlib`.
- `application/factory.montar_gerar_ficha`, `config.ErroConfiguracao`, `domain.models.{Entrada, ErroPreceptorIA, OrigemEntrada}`.

## Decisões de Design Identificadas

| Decisão | Evidência no código | Confiança |
|---------|---------------------|-----------|
| Padrão fila-de-1 + `pop` no fim do script: desacopla o clique (dentro da aba) do processamento (fora), sobrevivendo ao modelo de rerun do Streamlit | `app.py:70-72,95-96` | 🟢 |
| Dedup por hash de conteúdo, não por flag booleana — resiste a reruns múltiplos | `app.py:43-48` | 🟢 |
| `@st.cache_resource` na composição inteira (settings + prompt + adaptadores) | `app.py:37-39` | 🟢 |
| `logging.basicConfig` no entry point (nível INFO, formato com timestamp) | `app.py:13` | 🟢 |
| Aviso LGPD como `st.warning` sempre visível, não como modal dispensável | `app.py:27-34` | 🟢 |

## Estado Interno

Todo em `st.session_state` (3 chaves) + cache de recurso do processo. Máquina de estados da sessão documentada em [../state-machines.md](../state-machines.md) §2. 🟢

## Observabilidade

A UI não loga por conta própria; habilita (basicConfig) os logs `etapa=...` das camadas internas no stdout do processo Streamlit. 🟢

## Riscos e Lacunas

- 🔴 `Entrada` construída fora do try/except: `ErroEntradaInvalida` (ex.: texto vazio) vira stack trace na página em vez de "❌" — divergência do padrão RF-UI-06. Reproduzir: aba texto, textarea vazio, clicar gerar. Corrigir movendo a construção para dentro do fluxo protegido (ou try local na aba).
- 🟡 `st.cache_resource` segura configuração antiga até restart (documentar no README).
- 🟡 Sem teste automatizado de UI (AppTest do Streamlit existe e caberia aqui).
- 🟡 A ficha exibida não sobrevive à contingência offline (estado zerado) — comportamento deliberado, mas surpreende.
