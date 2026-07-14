"""Carregador do prompt canônico SNAPPS-OMP (RF-04/RN-06: fonte única, prompt-as-data)."""

from pathlib import Path

from preceptor_ia.domain.models import ErroPreceptorIA

CAMINHO_PROMPT_PADRAO = Path(__file__).resolve().parents[3] / "prompts" / "prompt-snapps-omp.md"


class ErroPromptCanonico(ErroPreceptorIA):
    """Prompt canônico ausente ou vazio — a aplicação não funciona sem ele."""


def carregar_prompt(caminho: Path = CAMINHO_PROMPT_PADRAO) -> str:
    if not caminho.is_file():
        raise ErroPromptCanonico(
            f"Prompt canônico não encontrado em {caminho}. "
            "O arquivo prompts/prompt-snapps-omp.md é parte obrigatória do repositório."
        )
    texto = caminho.read_text(encoding="utf-8").strip()
    if not texto:
        raise ErroPromptCanonico(f"Prompt canônico vazio em {caminho}.")
    return texto
