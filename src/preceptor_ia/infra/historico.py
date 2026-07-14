"""Persistência opcional de fichas em arquivos Markdown datestampados (RF-07, D-07)."""

import logging
import re
from pathlib import Path

from preceptor_ia.domain.models import Ficha

logger = logging.getLogger("preceptor_ia")


class HistoricoFilesystem:
    def __init__(self, diretorio: Path) -> None:
        self._dir = diretorio.expanduser()

    def gravar(self, ficha: Ficha) -> None:
        self._dir.mkdir(parents=True, exist_ok=True)
        contexto = _slug(ficha.contexto or ficha.origem_entrada.value)
        nome = f"{ficha.gerada_em.strftime('%Y%m%d%H%M')}-ficha-{contexto}.md"
        destino = self._dir / nome
        destino.write_text(ficha.markdown + "\n", encoding="utf-8")
        logger.info("etapa=historico arquivo=%s", destino)


def _slug(texto: str) -> str:
    limpo = re.sub(r"[^a-z0-9]+", "-", texto.lower()).strip("-")
    return limpo or "sem-contexto"
