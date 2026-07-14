"""Portas do domínio: contratos que a infraestrutura implementa (baixo acoplamento)."""

from typing import Protocol

from preceptor_ia.domain.models import Ficha, Transcricao


class ServicoTranscricao(Protocol):
    def transcrever(self, conteudo: bytes, nome_arquivo: str) -> Transcricao:
        """Converte áudio em texto (idioma fixado em português, RN-02)."""
        ...


class ServicoAnalise(Protocol):
    def analisar(self, prompt_sistema: str, transcricao: str) -> str:
        """Aplica o prompt canônico à transcrição e devolve o Markdown da ficha."""
        ...


class RepositorioHistorico(Protocol):
    def gravar(self, ficha: Ficha) -> None:
        """Persiste a ficha quando o histórico está ativo (RF-07, opt-in)."""
        ...
