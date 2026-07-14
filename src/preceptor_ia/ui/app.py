"""Interface Streamlit do PreceptorIA — validação conceitual."""

import hashlib
import logging
from pathlib import Path

import streamlit as st

from preceptor_ia.application.factory import montar_gerar_ficha
from preceptor_ia.config import ErroConfiguracao
from preceptor_ia.domain.models import Entrada, ErroPreceptorIA, OrigemEntrada

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s | %(message)s")

RAIZ = Path(__file__).resolve().parents[3]
TRANSCRICAO_DEMO = RAIZ / "demo" / "transcricao-simulada.md"
FICHA_CONTINGENCIA = RAIZ / "demo" / "ficha-exemplo.md"

st.set_page_config(page_title="PreceptorIA", page_icon="🩺", layout="centered")

st.title("🩺 PreceptorIA")
st.caption(
    "Feedback formativo estruturado (SNAPPS + One-Minute Preceptor) para passagens de caso "
    "em Medicina de Família e Comunidade."
)

st.warning(
    "**Aviso de privacidade** — Áudios e transcrições são enviados ao provedor de IA "
    "configurado e **não são retidos** pela aplicação (o histórico local é opcional e "
    "desligado por padrão). Em demonstrações públicas, use **somente casos simulados**. "
    "O processamento de passagens de caso reais é de responsabilidade do preceptor: "
    "anonimize os dados do paciente antes de gravar.",
    icon="🔒",
)


@st.cache_resource
def _caso_de_uso():
    return montar_gerar_ficha()


def _gerar(entrada: Entrada) -> None:
    chave = hashlib.sha256(
        (entrada.origem.value + (entrada.texto_transcricao or "")).encode()
        + (entrada.conteudo_audio or b"")
    ).hexdigest()
    if st.session_state.get("chave_resultado") == chave:
        return  # mesma entrada já processada nesta sessão: não repete chamadas externas
    etapas = ["ingestão", "transcrição", "análise", "entrega"]
    with st.status("Gerando ficha…", expanded=True) as status:
        for etapa in etapas[: 2 if entrada.origem is OrigemEntrada.AUDIO else 1]:
            st.write(f"▸ {etapa}")
        ficha = _caso_de_uso().executar(entrada)
        st.write("▸ análise concluída")
        status.update(label="Ficha pronta", state="complete")
    st.session_state["chave_resultado"] = chave
    st.session_state["ficha"] = ficha


aba_audio, aba_texto, aba_demo = st.tabs(
    ["🎙️ Áudio da passagem de caso", "📄 Transcrição colada", "🎬 Demonstração"]
)

with aba_audio:
    arquivo = st.file_uploader(
        "Gravação da passagem de caso (.ogg, .mp3, .m4a, .wav — até 25 MB)",
        type=["ogg", "mp3", "m4a", "wav"],
    )
    if arquivo is not None and st.button("Gerar ficha a partir do áudio", type="primary"):
        st.session_state["entrada_pendente"] = Entrada(
            OrigemEntrada.AUDIO, nome_arquivo=arquivo.name, conteudo_audio=arquivo.getvalue()
        )

with aba_texto:
    texto = st.text_area("Cole aqui a transcrição da passagem de caso", height=220)
    if st.button("Gerar ficha a partir do texto", type="primary"):
        st.session_state["entrada_pendente"] = Entrada(OrigemEntrada.TEXTO, texto_transcricao=texto)

with aba_demo:
    st.markdown(
        "Caso **inteiramente simulado** (hipertenso com má adesão, UBS) para demonstração — "
        "nenhum dado real de paciente."
    )
    if st.button("Gerar ficha do caso simulado", type="primary"):
        st.session_state["entrada_pendente"] = Entrada(
            OrigemEntrada.DEMO,
            texto_transcricao=TRANSCRICAO_DEMO.read_text(encoding="utf-8"),
        )
    if FICHA_CONTINGENCIA.is_file() and st.button("Exibir ficha de exemplo (offline)"):
        st.session_state["ficha"] = None
        st.session_state["chave_resultado"] = None
        st.markdown("---")
        st.markdown(FICHA_CONTINGENCIA.read_text(encoding="utf-8"))

entrada_pendente = st.session_state.pop("entrada_pendente", None)
if entrada_pendente is not None:
    try:
        _gerar(entrada_pendente)
    except ErroConfiguracao as exc:
        st.error(f"⚙️ {exc}")
    except ErroPreceptorIA as exc:
        st.error(f"❌ {exc}")

ficha = st.session_state.get("ficha")
if ficha is not None:
    st.markdown("---")
    st.markdown(ficha.markdown)
    st.download_button(
        "⬇️ Baixar ficha (.md)",
        data=ficha.markdown + "\n",
        file_name=f"{ficha.gerada_em.strftime('%Y%m%d%H%M')}-ficha-snapps-omp.md",
        mime="text/markdown",
    )
