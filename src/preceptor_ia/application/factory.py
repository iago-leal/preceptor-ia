"""Composition root: único ponto que conhece configuração e infraestrutura ao mesmo tempo."""

from preceptor_ia.application.gerar_ficha import GerarFicha
from preceptor_ia.config import Settings, carregar_settings
from preceptor_ia.domain.prompt import carregar_prompt
from preceptor_ia.infra.analise_openai import AnaliseOpenAICompat
from preceptor_ia.infra.historico import HistoricoFilesystem
from preceptor_ia.infra.transcricao_openai import TranscricaoOpenAICompat


def montar_gerar_ficha(settings: Settings | None = None) -> GerarFicha:
    cfg = settings or carregar_settings()
    return GerarFicha(
        prompt_sistema=carregar_prompt(),
        transcricao=TranscricaoOpenAICompat(
            cfg.llm_base_url, cfg.llm_api_key, cfg.transcricao_model
        ),
        analise=AnaliseOpenAICompat(cfg.llm_base_url, cfg.llm_api_key, cfg.llm_model),
        historico=HistoricoFilesystem(cfg.historico_dir) if cfg.historico_ativo else None,
    )
