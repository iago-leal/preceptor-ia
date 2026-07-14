"""Caso de uso central: entrada → (transcrição) → análise → Ficha."""

import logging

from preceptor_ia.domain.models import (
    Entrada,
    ErroRespostaAnalise,
    Ficha,
    OrigemEntrada,
)
from preceptor_ia.domain.ports import RepositorioHistorico, ServicoAnalise, ServicoTranscricao

logger = logging.getLogger("preceptor_ia")


class GerarFicha:
    def __init__(
        self,
        prompt_sistema: str,
        transcricao: ServicoTranscricao,
        analise: ServicoAnalise,
        historico: RepositorioHistorico | None = None,
    ) -> None:
        self._prompt = prompt_sistema
        self._transcricao = transcricao
        self._analise = analise
        self._historico = historico

    def executar(self, entrada: Entrada) -> Ficha:
        logger.info("etapa=ingestao origem=%s", entrada.origem.value)
        texto = self._obter_transcricao(entrada)

        logger.info("etapa=analise tamanho_transcricao=%d", len(texto))
        markdown = self._analise.analisar(self._prompt, texto)
        if not (markdown or "").strip():
            raise ErroRespostaAnalise(
                "O serviço de análise devolveu resposta vazia; a ficha não foi gerada."
            )

        ficha = Ficha(markdown=markdown.strip(), origem_entrada=entrada.origem)
        if self._historico is not None:
            self._historico.gravar(ficha)

        logger.info("etapa=entrega origem=%s", entrada.origem.value)
        return ficha

    def _obter_transcricao(self, entrada: Entrada) -> str:
        if entrada.origem is not OrigemEntrada.AUDIO:
            return (entrada.texto_transcricao or "").strip()
        assert entrada.conteudo_audio is not None and entrada.nome_arquivo is not None
        logger.info(
            "etapa=transcricao arquivo=%s bytes=%d",
            entrada.nome_arquivo,
            len(entrada.conteudo_audio),
        )
        resultado = self._transcricao.transcrever(entrada.conteudo_audio, entrada.nome_arquivo)
        # RN-07: o áudio não é retido; daqui em diante só a transcrição circula.
        return resultado.texto.strip()
