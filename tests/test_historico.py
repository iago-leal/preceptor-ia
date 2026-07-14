from datetime import datetime

from preceptor_ia.domain.models import Ficha, OrigemEntrada
from preceptor_ia.infra.historico import HistoricoFilesystem


def ficha(contexto=None):
    return Ficha(
        markdown="# Ficha\nconteúdo",
        origem_entrada=OrigemEntrada.TEXTO,
        contexto=contexto,
        gerada_em=datetime(2026, 7, 14, 10, 30),
    )


def test_grava_markdown_datestampado(tmp_path):
    HistoricoFilesystem(tmp_path).gravar(ficha(contexto="UBS Central"))
    arquivos = list(tmp_path.iterdir())
    assert [a.name for a in arquivos] == ["202607141030-ficha-ubs-central.md"]
    assert arquivos[0].read_text(encoding="utf-8").startswith("# Ficha")


def test_contexto_ausente_usa_origem(tmp_path):
    HistoricoFilesystem(tmp_path).gravar(ficha())
    assert [a.name for a in tmp_path.iterdir()] == ["202607141030-ficha-texto.md"]


def test_cria_diretorio_se_nao_existir(tmp_path):
    destino = tmp_path / "aninhado" / "historico"
    HistoricoFilesystem(destino).gravar(ficha())
    assert destino.is_dir() and len(list(destino.iterdir())) == 1
