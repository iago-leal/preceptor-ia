"""Adaptador de transcrição para endpoints OpenAI-compatible (/audio/transcriptions)."""

import logging

import httpx

from preceptor_ia.domain.models import (
    ErroCredencial,
    ErroLimiteProvedor,
    ErroServicoExterno,
    Transcricao,
)

logger = logging.getLogger("preceptor_ia")

TIMEOUT_SEGUNDOS = 120.0
ETAPA = "transcrição"


class TranscricaoOpenAICompat:
    def __init__(self, base_url: str, api_key: str, modelo: str) -> None:
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key
        self._modelo = modelo

    def transcrever(self, conteudo: bytes, nome_arquivo: str) -> Transcricao:
        try:
            resposta = httpx.post(
                f"{self._base_url}/audio/transcriptions",
                headers={"Authorization": f"Bearer {self._api_key}"},
                files={"file": (nome_arquivo, conteudo)},
                data={
                    "model": self._modelo,
                    "language": "pt",  # RN-02: idioma fixo, jargões da APS brasileira
                    "response_format": "json",
                },
                timeout=TIMEOUT_SEGUNDOS,
            )
        except httpx.HTTPError as exc:
            raise ErroServicoExterno(f"Falha de rede na etapa de {ETAPA}: {exc}") from exc

        _levantar_erro_nomeado(resposta, ETAPA)
        texto = (resposta.json().get("text") or "").strip()
        if not texto:
            raise ErroServicoExterno(f"Etapa de {ETAPA} devolveu texto vazio.")
        return Transcricao(texto=texto, origem_servico=f"{self._base_url}#{self._modelo}")


def _levantar_erro_nomeado(resposta: httpx.Response, etapa: str) -> None:
    if resposta.status_code == 401:
        raise ErroCredencial(
            f"Credencial recusada na etapa de {etapa}: confira LLM_API_KEY no .env."
        )
    if resposta.status_code == 429:
        raise ErroLimiteProvedor(
            f"Limite do provedor atingido na etapa de {etapa}: aguarde alguns minutos "
            "ou configure outro provedor (LLM_BASE_URL)."
        )
    if resposta.status_code >= 400:
        raise ErroServicoExterno(
            f"Falha na etapa de {etapa} (HTTP {resposta.status_code}): {resposta.text[:300]}"
        )
