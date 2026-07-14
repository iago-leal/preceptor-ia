import httpx
import pytest

from preceptor_ia.domain.models import (
    ErroCredencial,
    ErroLimiteProvedor,
    ErroRespostaAnalise,
    ErroServicoExterno,
)
from preceptor_ia.infra.analise_openai import AnaliseOpenAICompat
from preceptor_ia.infra.transcricao_openai import TranscricaoOpenAICompat

BASE = "https://provedor.teste/v1"


@pytest.fixture
def transporte(monkeypatch):
    """Intercepta httpx.post com um MockTransport configurável por teste."""

    estado = {}

    def configurar(handler):
        transporte = httpx.MockTransport(handler)

        def post_falso(url, **kwargs):
            with httpx.Client(transport=transporte) as cliente:
                return cliente.post(url, **kwargs)

        monkeypatch.setattr("preceptor_ia.infra.transcricao_openai.httpx.post", post_falso)
        monkeypatch.setattr("preceptor_ia.infra.analise_openai.httpx.post", post_falso)
        estado["ultimo"] = None

    return configurar


def resposta_json(codigo, corpo):
    return lambda request: httpx.Response(codigo, json=corpo)


class TestTranscricao:
    def adaptador(self):
        return TranscricaoOpenAICompat(BASE, "chave", "whisper-large-v3-turbo")

    def test_sucesso_devolve_transcricao(self, transporte):
        capturado = {}

        def handler(request):
            capturado["url"] = str(request.url)
            return httpx.Response(200, json={"text": " transcrição ok "})

        transporte(handler)
        resultado = self.adaptador().transcrever(b"bytes", "caso.m4a")
        assert resultado.texto == "transcrição ok"
        assert capturado["url"] == f"{BASE}/audio/transcriptions"

    def test_401_vira_erro_credencial(self, transporte):
        transporte(resposta_json(401, {"error": "unauthorized"}))
        with pytest.raises(ErroCredencial, match="LLM_API_KEY"):
            self.adaptador().transcrever(b"x", "caso.mp3")

    def test_429_vira_erro_limite(self, transporte):
        transporte(resposta_json(429, {"error": "rate limit"}))
        with pytest.raises(ErroLimiteProvedor):
            self.adaptador().transcrever(b"x", "caso.mp3")

    def test_5xx_vira_erro_servico_com_etapa(self, transporte):
        transporte(resposta_json(503, {"error": "down"}))
        with pytest.raises(ErroServicoExterno, match="transcrição"):
            self.adaptador().transcrever(b"x", "caso.mp3")

    def test_timeout_vira_erro_servico(self, transporte):
        def handler(request):
            raise httpx.ConnectTimeout("timeout")

        transporte(handler)
        with pytest.raises(ErroServicoExterno, match="rede"):
            self.adaptador().transcrever(b"x", "caso.mp3")


class TestAnalise:
    def adaptador(self):
        return AnaliseOpenAICompat(BASE, "chave", "llama-3.3-70b-versatile")

    def test_sucesso_devolve_markdown(self, transporte):
        corpo = {"choices": [{"message": {"content": "# Ficha SNAPPS-OMP"}}]}
        transporte(resposta_json(200, corpo))
        assert self.adaptador().analisar("prompt", "caso") == "# Ficha SNAPPS-OMP"

    def test_401_vira_erro_credencial(self, transporte):
        transporte(resposta_json(401, {}))
        with pytest.raises(ErroCredencial):
            self.adaptador().analisar("prompt", "caso")

    def test_429_vira_erro_limite(self, transporte):
        transporte(resposta_json(429, {}))
        with pytest.raises(ErroLimiteProvedor):
            self.adaptador().analisar("prompt", "caso")

    def test_5xx_nomeia_etapa_analise(self, transporte):
        transporte(resposta_json(500, {}))
        with pytest.raises(ErroServicoExterno, match="análise"):
            self.adaptador().analisar("prompt", "caso")

    def test_resposta_malformada_nao_vira_ficha(self, transporte):
        transporte(resposta_json(200, {"inesperado": True}))
        with pytest.raises(ErroRespostaAnalise, match="malformada"):
            self.adaptador().analisar("prompt", "caso")

    def test_conteudo_vazio_nao_vira_ficha(self, transporte):
        transporte(resposta_json(200, {"choices": [{"message": {"content": "  "}}]}))
        with pytest.raises(ErroRespostaAnalise, match="vazio"):
            self.adaptador().analisar("prompt", "caso")
