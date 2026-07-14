import pytest

from preceptor_ia.application.gerar_ficha import GerarFicha
from preceptor_ia.domain.models import (
    Entrada,
    ErroRespostaAnalise,
    ErroServicoExterno,
    Ficha,
    OrigemEntrada,
    Transcricao,
)

FICHA_MD = "# 📋 Ficha de Feedback Estruturado — SNAPPS-OMP\n..."


class FakeServicoTranscricao:
    def __init__(self, texto="paciente de 58 anos, hipertenso"):
        self.texto = texto
        self.chamadas = []

    def transcrever(self, conteudo, nome_arquivo):
        self.chamadas.append(nome_arquivo)
        return Transcricao(texto=self.texto, origem_servico="fake")


class FakeServicoAnalise:
    def __init__(self, resposta=FICHA_MD):
        self.resposta = resposta
        self.chamadas = []

    def analisar(self, prompt_sistema, transcricao):
        self.chamadas.append((prompt_sistema, transcricao))
        return self.resposta


class FakeHistorico:
    def __init__(self):
        self.gravadas: list[Ficha] = []

    def gravar(self, ficha):
        self.gravadas.append(ficha)


class ServicoQueFalha:
    def transcrever(self, conteudo, nome_arquivo):
        raise ErroServicoExterno("falha na etapa de transcrição")

    def analisar(self, prompt_sistema, transcricao):
        raise ErroServicoExterno("falha na etapa de análise")


def caso_de_uso(transcricao=None, analise=None, historico=None):
    return GerarFicha(
        prompt_sistema="PROMPT CANÔNICO",
        transcricao=transcricao or FakeServicoTranscricao(),
        analise=analise or FakeServicoAnalise(),
        historico=historico,
    )


def test_fluxo_audio_transcreve_e_analisa():
    transcricao = FakeServicoTranscricao()
    analise = FakeServicoAnalise()
    ficha = caso_de_uso(transcricao, analise).executar(
        Entrada(OrigemEntrada.AUDIO, nome_arquivo="caso.m4a", conteudo_audio=b"audio")
    )
    assert transcricao.chamadas == ["caso.m4a"]
    assert analise.chamadas[0] == ("PROMPT CANÔNICO", "paciente de 58 anos, hipertenso")
    assert ficha.markdown == FICHA_MD
    assert ficha.origem_entrada is OrigemEntrada.AUDIO


@pytest.mark.parametrize("origem", [OrigemEntrada.TEXTO, OrigemEntrada.DEMO])
def test_fluxos_texto_e_demo_pulam_transcricao(origem):
    transcricao = FakeServicoTranscricao()
    analise = FakeServicoAnalise()
    ficha = caso_de_uso(transcricao, analise).executar(
        Entrada(origem, texto_transcricao="  transcrição colada  ")
    )
    assert transcricao.chamadas == []
    assert analise.chamadas[0][1] == "transcrição colada"
    assert ficha.origem_entrada is origem


def test_erro_de_transcricao_propaga_nomeado():
    with pytest.raises(ErroServicoExterno, match="transcrição"):
        caso_de_uso(transcricao=ServicoQueFalha()).executar(
            Entrada(OrigemEntrada.AUDIO, nome_arquivo="caso.mp3", conteudo_audio=b"x")
        )


def test_erro_de_analise_propaga_nomeado():
    with pytest.raises(ErroServicoExterno, match="análise"):
        caso_de_uso(analise=ServicoQueFalha()).executar(
            Entrada(OrigemEntrada.TEXTO, texto_transcricao="caso")
        )


def test_resposta_vazia_da_analise_nao_vira_ficha():
    with pytest.raises(ErroRespostaAnalise):
        caso_de_uso(analise=FakeServicoAnalise(resposta="   ")).executar(
            Entrada(OrigemEntrada.TEXTO, texto_transcricao="caso")
        )


def test_historico_recebe_ficha_quando_presente():
    historico = FakeHistorico()
    caso_de_uso(historico=historico).executar(
        Entrada(OrigemEntrada.TEXTO, texto_transcricao="caso")
    )
    assert len(historico.gravadas) == 1


def test_sem_historico_nada_e_gravado():
    ficha = caso_de_uso(historico=None).executar(
        Entrada(OrigemEntrada.TEXTO, texto_transcricao="caso")
    )
    assert ficha.markdown  # apenas confirma o fluxo completo sem repositório
