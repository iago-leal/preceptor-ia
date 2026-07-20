# Histórico Local

> Gerado pelo **Writer** (Reversa) em 2026-07-20. Unit: `historico-local`.
> Escala: 🟢 CONFIRMADO · 🟡 INFERIDO · 🔴 LACUNA

## Visão Geral

Persistência **opcional e desligada por padrão** das fichas geradas, como arquivos Markdown datestampados em diretório local fora do repositório (`~/.preceptor-ia/historico`). Implementa a porta `RepositorioHistorico`. Materializa a postura de não-retenção do produto (ADR-0005): guardar é decisão deliberada do usuário, nunca default. 🟢

## Responsabilidades

- Gravar o Markdown da ficha em arquivo nomeado por timestamp + slug. 🟢
- Criar o diretório de destino quando ausente. 🟢
- Registrar log da gravação (caminho do arquivo, sem conteúdo clínico). 🟢

## Regras de Negócio

- Opt-in: com `HISTORICO_ATIVO=false` (default), o repositório **nem é instanciado** — a fábrica injeta `None` (RN-C3). 🟢
- Nome do arquivo: `{gerada_em:%Y%m%d%H%M}-ficha-{slug}.md`; slug derivado de `ficha.contexto` ou, na ausência (fluxo atual sempre), do valor da origem (`audio`/`texto`/`demo`) (RN-C4). 🟢
- `_slug`: minúsculas, `[^a-z0-9]+` → `-`, strip de `-`; resultado vazio → `"sem-contexto"`. 🟢
- Conteúdo gravado: `ficha.markdown + "\n"`, UTF-8. 🟢
- Diretório criado com `mkdir(parents=True, exist_ok=True)`; `~` expandido no construtor. 🟢
- Colisão de nome (mesma origem/contexto no mesmo minuto): o legado **sobrescreve** o arquivo anterior sem aviso (RN-C5, comportamento confirmado 🟢). **Política decidida pelo autor (2026-07-20): sufixar** (`-2`, `-3`, ...) — a sobrescrita é divergência do legado a corrigir na reimplementação. 🟢 [Revisão]

## Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de Aceite |
|----|-----------|-----------|-------------------|
| RF-HL-01 | Gravar ficha como `.md` datestampado no diretório configurado | Must* | Arquivo existe com nome e conteúdo esperados (*Must dentro da feature; a feature em si é Should no produto) |
| RF-HL-02 | Criar diretório ausente (incl. pais) | Must | Gravação em diretório inexistente funciona |
| RF-HL-03 | Normalizar slug do nome | Must | `"Consulta HAS!"` → `consulta-has`; vazio → `sem-contexto` |
| RF-HL-04 | Não ser instanciado quando desativado | Must | `HISTORICO_ATIVO=false` → caso de uso recebe `historico=None` |

## Requisitos Não Funcionais

| Tipo | Requisito inferido | Evidência no código | Confiança |
|------|--------------------|---------------------|-----------|
| Privacidade | Persistência fora do repositório git; log só do caminho | `infra/historico.py:21-22`, `config.py:21` | 🟢 |
| Observabilidade | Log `etapa=historico arquivo=<destino>` | `infra/historico.py:22` | 🟢 |

## Critérios de Aceitação

```gherkin
Dado HISTORICO_ATIVO=true e uma Ficha(origem=TEXTO, gerada_em=2026-07-20 14:30)
Quando gravar(ficha) é chamado
Então existe {HISTORICO_DIR}/202607201430-ficha-texto.md
E o conteúdo é ficha.markdown + "\n" em UTF-8

Dado um diretório de histórico inexistente
Quando gravar é chamado
Então o diretório (e pais) é criado e a gravação conclui

Dado duas fichas de mesma origem geradas no mesmo minuto
Quando ambas são gravadas
Então a segunda sobrescreve a primeira (comportamento atual — ver questions.md)

Dado HISTORICO_ATIVO=false
Quando o caso de uso é montado pela fábrica
Então nenhum HistoricoFilesystem é criado e nada é gravado
```

## Prioridade (MoSCoW)

| Requisito | MoSCoW | Justificativa |
|-----------|--------|---------------|
| Opt-in via fábrica (RF-HL-04) | Must | Postura de privacidade do produto (ADR-0005) |
| Gravação datestampada (RF-HL-01/02/03) | Should | Feature opcional, desligada por padrão, com alternativa (download manual na UI) |

## Rastreabilidade de Código

| Arquivo | Função / Classe | Cobertura |
|---------|-----------------|-----------|
| `src/preceptor_ia/infra/historico.py` | `HistoricoFilesystem.gravar`, `_slug` | 🟢 |
| `src/preceptor_ia/application/factory.py` | Injeção condicional (linha 19) | 🟢 |
| `tests/test_historico.py` | Filesystem em tmp | 🟢 |
