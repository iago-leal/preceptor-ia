import pytest

from preceptor_ia.domain.models import (
    TAMANHO_MAXIMO_AUDIO_BYTES,
    Entrada,
    ErroEntradaInvalida,
    OrigemEntrada,
)
from preceptor_ia.domain.prompt import CAMINHO_PROMPT_PADRAO, ErroPromptCanonico, carregar_prompt


class TestEntradaAudio:
    def test_aceita_extensoes_suportadas(self):
        for nome in ["caso.ogg", "caso.mp3", "CASO.M4A", "caso.wav"]:
            entrada = Entrada(OrigemEntrada.AUDIO, nome_arquivo=nome, conteudo_audio=b"x")
            assert entrada.nome_arquivo == nome

    def test_rejeita_extensao_nao_suportada(self):
        with pytest.raises(ErroEntradaInvalida, match="Formatos aceitos"):
            Entrada(OrigemEntrada.AUDIO, nome_arquivo="caso.pdf", conteudo_audio=b"x")

    def test_rejeita_arquivo_sem_extensao(self):
        with pytest.raises(ErroEntradaInvalida):
            Entrada(OrigemEntrada.AUDIO, nome_arquivo="caso", conteudo_audio=b"x")

    def test_rejeita_audio_ausente(self):
        with pytest.raises(ErroEntradaInvalida, match="sem arquivo"):
            Entrada(OrigemEntrada.AUDIO)

    def test_rejeita_audio_acima_do_limite(self):
        grande = b"0" * (TAMANHO_MAXIMO_AUDIO_BYTES + 1)
        with pytest.raises(ErroEntradaInvalida, match="25 MB"):
            Entrada(OrigemEntrada.AUDIO, nome_arquivo="caso.mp3", conteudo_audio=grande)

    def test_aceita_audio_no_limite(self):
        exato = b"0" * TAMANHO_MAXIMO_AUDIO_BYTES
        Entrada(OrigemEntrada.AUDIO, nome_arquivo="caso.mp3", conteudo_audio=exato)


class TestEntradaTexto:
    def test_aceita_transcricao_colada(self):
        entrada = Entrada(OrigemEntrada.TEXTO, texto_transcricao="residente apresenta caso")
        assert entrada.texto_transcricao

    def test_rejeita_texto_vazio(self):
        for texto in [None, "", "   \n"]:
            with pytest.raises(ErroEntradaInvalida, match="vazia"):
                Entrada(OrigemEntrada.TEXTO, texto_transcricao=texto)

    def test_demo_usa_mesma_validacao_de_texto(self):
        with pytest.raises(ErroEntradaInvalida):
            Entrada(OrigemEntrada.DEMO, texto_transcricao="")


class TestPromptCanonico:
    def test_prompt_do_repositorio_carrega(self):
        texto = carregar_prompt()
        assert "SNAPPS" in texto
        assert "One-Minute Preceptor" in texto

    def test_caminho_padrao_aponta_para_prompts(self):
        assert CAMINHO_PROMPT_PADRAO.name == "prompt-snapps-omp.md"

    def test_arquivo_ausente_gera_erro_nomeado(self, tmp_path):
        with pytest.raises(ErroPromptCanonico, match="não encontrado"):
            carregar_prompt(tmp_path / "inexistente.md")

    def test_arquivo_vazio_gera_erro_nomeado(self, tmp_path):
        vazio = tmp_path / "vazio.md"
        vazio.write_text("  \n")
        with pytest.raises(ErroPromptCanonico, match="vazio"):
            carregar_prompt(vazio)
