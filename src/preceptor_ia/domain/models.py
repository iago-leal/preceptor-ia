"""Modelos e erros do domínio. Camada pura: sem framework, sem HTTP, sem filesystem."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum

EXTENSOES_AUDIO = {".ogg", ".mp3", ".m4a", ".wav"}
TAMANHO_MAXIMO_AUDIO_BYTES = 25 * 1024 * 1024  # limite do contrato de transcrição (RF-01)


class ErroPreceptorIA(Exception):
    """Raiz de todos os erros nomeados da aplicação."""


class ErroEntradaInvalida(ErroPreceptorIA):
    """Entrada rejeitada antes de qualquer chamada externa (RD-01/RN-01)."""


class ErroCredencial(ErroPreceptorIA):
    """Credencial ausente ou recusada pelo provedor (401)."""


class ErroLimiteProvedor(ErroPreceptorIA):
    """Limite de uso do provedor atingido (429)."""


class ErroServicoExterno(ErroPreceptorIA):
    """Falha de serviço externo (5xx/timeout); a mensagem nomeia a etapa."""


class ErroRespostaAnalise(ErroPreceptorIA):
    """Resposta do serviço de análise vazia ou malformada (RN-03: não inventar ficha)."""


class OrigemEntrada(StrEnum):
    AUDIO = "audio"
    TEXTO = "texto"
    DEMO = "demo"


@dataclass(frozen=True)
class Entrada:
    """Pedido de geração de ficha: áudio enviado, transcrição colada ou caso demo."""

    origem: OrigemEntrada
    nome_arquivo: str | None = None
    conteudo_audio: bytes | None = None
    texto_transcricao: str | None = None

    def __post_init__(self) -> None:
        if self.origem is OrigemEntrada.AUDIO:
            self._validar_audio()
        elif not (self.texto_transcricao or "").strip():
            raise ErroEntradaInvalida(
                "Entrada de texto vazia: cole a transcrição da passagem de caso."
            )

    def _validar_audio(self) -> None:
        if not self.nome_arquivo or not self.conteudo_audio:
            raise ErroEntradaInvalida("Entrada de áudio sem arquivo: envie uma gravação.")
        sufixo = (
            "." + self.nome_arquivo.rsplit(".", 1)[-1].lower() if "." in self.nome_arquivo else ""
        )
        if sufixo not in EXTENSOES_AUDIO:
            aceitos = ", ".join(sorted(EXTENSOES_AUDIO))
            raise ErroEntradaInvalida(
                f"Formato não suportado ({self.nome_arquivo!r}). Formatos aceitos: {aceitos}."
            )
        if len(self.conteudo_audio) > TAMANHO_MAXIMO_AUDIO_BYTES:
            raise ErroEntradaInvalida(
                "Áudio acima de 25 MB. Grave trechos menores ou comprima o arquivo."
            )


@dataclass(frozen=True)
class Transcricao:
    texto: str
    origem_servico: str


@dataclass(frozen=True)
class Ficha:
    """Ficha de Feedback Estruturado SNAPPS-OMP, como devolvida pelo serviço de análise."""

    markdown: str
    origem_entrada: OrigemEntrada
    contexto: str | None = None
    gerada_em: datetime = field(default_factory=datetime.now)
