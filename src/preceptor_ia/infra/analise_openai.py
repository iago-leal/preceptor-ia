"""Adaptador de análise para endpoints OpenAI-compatible (/chat/completions)."""

import logging

import httpx

from preceptor_ia.domain.models import ErroRespostaAnalise, ErroServicoExterno
from preceptor_ia.infra.transcricao_openai import _levantar_erro_nomeado

logger = logging.getLogger("preceptor_ia")

TIMEOUT_SEGUNDOS = 120.0
TEMPERATURA = 0.2  # RN-03: fidelidade, não criatividade
ETAPA = "análise"


class AnaliseOpenAICompat:
    def __init__(self, base_url: str, api_key: str, modelo: str) -> None:
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key
        self._modelo = modelo

    def analisar(self, prompt_sistema: str, transcricao: str) -> str:
        try:
            resposta = httpx.post(
                f"{self._base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self._api_key}"},
                json={
                    "model": self._modelo,
                    "temperature": TEMPERATURA,
                    "messages": [
                        {"role": "system", "content": prompt_sistema},
                        {"role": "user", "content": transcricao},
                    ],
                },
                timeout=TIMEOUT_SEGUNDOS,
            )
        except httpx.HTTPError as exc:
            raise ErroServicoExterno(f"Falha de rede na etapa de {ETAPA}: {exc}") from exc

        _levantar_erro_nomeado(resposta, ETAPA)
        try:
            conteudo = resposta.json()["choices"][0]["message"]["content"]
        except (KeyError, IndexError, ValueError) as exc:
            raise ErroRespostaAnalise(
                f"Resposta malformada do serviço de {ETAPA}: {resposta.text[:300]}"
            ) from exc
        if not (conteudo or "").strip():
            raise ErroRespostaAnalise(f"Serviço de {ETAPA} devolveu conteúdo vazio.")
        return conteudo
