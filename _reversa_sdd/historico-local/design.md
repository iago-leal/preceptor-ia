# Histórico Local, Design Técnico

> Gerado pelo **Writer** (Reversa) em 2026-07-20.
> Escala: 🟢 CONFIRMADO · 🟡 INFERIDO · 🔴 LACUNA

## Interface

| Símbolo | Assinatura | Retorno | Observação |
|---------|-----------|---------|------------|
| `HistoricoFilesystem.__init__` | `(diretorio: Path)` | — | Aplica `expanduser()` e guarda em `self._dir` |
| `HistoricoFilesystem.gravar` | `(ficha: Ficha)` | `None` | Satisfaz o Protocol `RepositorioHistorico` |
| `_slug` | `(texto: str)` | `str` | Função de módulo; normaliza para `[a-z0-9-]` |

## Fluxo Principal

1. `self._dir.mkdir(parents=True, exist_ok=True)` (`historico.py:17`).
2. `contexto = _slug(ficha.contexto or ficha.origem_entrada.value)` (`historico.py:18`).
3. `nome = f"{ficha.gerada_em.strftime('%Y%m%d%H%M')}-ficha-{contexto}.md"` (`historico.py:19`).
4. `destino.write_text(ficha.markdown + "\n", encoding="utf-8")` (`historico.py:21`).
5. `logger.info("etapa=historico arquivo=%s", destino)` (`historico.py:22`).

`_slug`: `re.sub(r"[^a-z0-9]+", "-", texto.lower()).strip("-")`, fallback `"sem-contexto"` (`historico.py:25-27`).

## Fluxos Alternativos

- **Erro de IO** (permissão, disco cheio): nenhuma captura local — a exceção sobe crua para o caso de uso, que também não a captura, abortando a entrega da ficha (DT-2). Note que **não** é um `ErroPreceptorIA`: a UI a deixaria vazar como exceção não tratada do Streamlit. 🟡
- **Colisão de nome no mesmo minuto:** `write_text` sobrescreve sem verificação de existência (DT-3). 🟢 (comportamento) / 🔴 (intenção)

## Dependências

- `pathlib`, `re` (stdlib) — nenhuma dependência externa. 🟢
- `domain/models.Ficha` — entidade gravada.

## Decisões de Design Identificadas

| Decisão | Evidência no código | Confiança |
|---------|---------------------|-----------|
| Arquivo Markdown puro, sem índice/metadados/rotação — legível por humanos e versionável manualmente | `historico.py:16-22` | 🟢 |
| Timestamp com resolução de minuto (`%Y%m%d%H%M`), espelhando o nome do download da UI | `historico.py:19`, `ui/app.py:111` | 🟢 |
| Diretório default fora do repositório (`~/.preceptor-ia/historico`), configurável via `HISTORICO_DIR` | `config.py:21` | 🟢 |
| Escrita direta (sem arquivo temporário + rename): gravação não-atômica, risco teórico de arquivo truncado em falha no meio da escrita | `historico.py:21` | 🟡 |

## Estado Interno

Somente `self._dir` (Path imutável na prática). Sem cache nem buffer. 🟢

## Observabilidade

Log único `etapa=historico arquivo=<caminho completo>` por gravação; conteúdo clínico nunca logado. 🟢

## Riscos e Lacunas

- 🔴 **L3/DT-3:** sobrescrita silenciosa na colisão de minuto — contradiz o princípio de erros barulhentos se for acidental (ver `questions.md`).
- 🟡 **DT-2:** falha de IO aborta a entrega e vaza exceção não-nomeada até a UI (única rota de exceção crua do sistema).
- 🟡 O app só grava; nunca lê o histórico — não há feature de consulta, e nada limita o crescimento do diretório.
