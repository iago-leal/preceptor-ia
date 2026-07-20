# Spec Impact Matrix — PreceptorIA

> Gerado pelo **Architect** (Reversa) em 2026-07-20.
> Lê-se por linha: alterar o artefato da linha **impacta** os componentes marcados nas colunas.
> Escala: 🟢 CONFIRMADO (import/uso direto no código) · 🟡 INFERIDO (impacto comportamental, sem import)

## Matriz

| Alterar ↓ impacta → | domain/models | domain/ports | domain/prompt | application/gerar_ficha | application/factory | infra/transcricao | infra/analise | infra/historico | config | ui/app | prompts/*.md | tests |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| **domain/models.py** | — | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | | 🟢 | | 🟢 |
| **domain/ports.py** | | — | | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | | | | 🟢 |
| **domain/prompt.py** | | | — | | 🟢 | | | | | | 🟡 | 🟢 |
| **application/gerar_ficha.py** | | | | — | 🟢 | | | | | 🟢 | | 🟢 |
| **application/factory.py** | | | | | — | | | | | 🟢 | | 🟢 |
| **infra/transcricao_openai.py** | | | | | 🟢 | — | 🟢 | | | | | 🟢 |
| **infra/analise_openai.py** | | | | | 🟢 | | — | | | | | 🟢 |
| **infra/historico.py** | | | | | 🟢 | | | — | | | | 🟢 |
| **config.py** | | | | | 🟢 | 🟡 | 🟡 | 🟡 | — | 🟢 | | 🟢 |
| **ui/app.py** | | | | | | | | | | — | | 🟡 |
| **prompts/prompt-snapps-omp.md** | | | | | | | 🟡 | | | | — | 🟡 |
| **.env / variáveis de ambiente** | | | | | | 🟡 | 🟡 | 🟡 | 🟢 | 🟡 | | |

## Leituras de maior alcance (hubs)

| Artefato | Alcance | Por quê |
|---|---|---|
| `domain/models.py` | **10 componentes** — o hub do sistema | Todas as camadas importam os modelos e a hierarquia de erros; qualquer mudança de assinatura ou de erro reverbera em tudo. |
| `domain/ports.py` | 6 componentes | Mudar um Protocol quebra os 3 adaptadores, o caso de uso e a fábrica ao mesmo tempo. |
| `config.py` | 6 componentes | Campos novos exigem fábrica + `.env.example`; a UI depende do `ErroConfiguracao`. |
| `prompts/prompt-snapps-omp.md` | 2 componentes, **impacto máximo no produto** | Nenhum import — mas altera o comportamento pedagógico inteiro (formato da ficha, regras de fidelidade). É o artefato com maior razão impacto/visibilidade: muda o produto sem falhar nenhum teste. 🟡 |

## Casos de impacto notáveis (não óbvios pela matriz)

1. **`infra/transcricao_openai.py` → `infra/analise_openai.py`** 🟢 — o segundo importa `_levantar_erro_nomeado` do primeiro (DT-4 em [architecture.md](architecture.md)); renomear ou mover o helper quebra o adaptador de análise.
2. **`domain/prompt.py` → `prompts/`** 🟡 — o caminho padrão (`CAMINHO_PROMPT_PADRAO`, resolvido por `parents[3]`) acopla o código à posição física do arquivo; mover `prompts/` ou reorganizar `src/` quebra a resolução silenciosamente até o primeiro run.
3. **`prompts/prompt-snapps-omp.md` → demo/ficha-exemplo.md** 🟡 — a ficha de contingência foi gerada pelo prompt atual; mudar o formato da ficha no prompt desatualiza o exemplo offline (nada valida essa coerência).
4. **`config.py` → adaptadores** 🟡 — sem import direto (a fábrica repassa valores), mas defaults de modelo/base URL alteram o comportamento efetivo dos adaptadores.
5. **`ui/app.py` → testes** 🟡 — a UI não tem teste próprio (as 4 suítes cobrem domain, application, infra); mudanças ali só são verificadas manualmente.
