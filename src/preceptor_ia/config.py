"""Configuração da aplicação — tudo vem do ambiente/.env, nada chumbado no código."""

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ErroConfiguracao(RuntimeError):
    """Configuração ausente ou inválida; a mensagem nomeia a variável faltante."""


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    llm_api_key: str = Field(min_length=1)
    llm_base_url: str = "https://api.groq.com/openai/v1"
    llm_model: str = "llama-3.3-70b-versatile"
    transcricao_model: str = "whisper-large-v3-turbo"
    historico_ativo: bool = False
    historico_dir: Path = Path.home() / ".preceptor-ia" / "historico"


def carregar_settings() -> Settings:
    """Carrega a configuração; falha barulhenta nomeando o que falta (RF-05)."""
    try:
        return Settings()  # type: ignore[call-arg]
    except Exception as exc:
        raise ErroConfiguracao(
            "Configuração incompleta: defina LLM_API_KEY no ambiente ou no arquivo .env "
            "(modelo em .env.example). Detalhe: " + str(exc)
        ) from exc
