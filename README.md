# 🩺 PreceptorIA

[![ci](https://github.com/iago-leal/preceptor-ia/actions/workflows/ci.yml/badge.svg)](https://github.com/iago-leal/preceptor-ia/actions/workflows/ci.yml)

Ferramenta de **feedback formativo estruturado** para preceptoria em Medicina de Família e Comunidade. Você grava (ou cola a transcrição de) uma **passagem de caso** entre residente e preceptor; a aplicação transcreve o áudio, aplica um prompt pedagógico baseado nos modelos **SNAPPS** e **One-Minute Preceptor (OMP)** e devolve uma **ficha de feedback estruturada**, com evidências citadas da própria conversa.

Produto técnico do Curso de Especialização em Preceptoria em MFC (Hospital Moinhos de Vento / PROADI-SUS), tipologia CAPES **TIC — Desenvolvimento de Tecnologias de Informação e Comunicação**.

## Como funciona

```
áudio da passagem de caso ──► transcrição (Whisper) ──► análise por LLM ──► ficha SNAPPS-OMP
        ou transcrição colada ───────────────────────────┘
```

O coração do produto é o **prompt canônico** em [`prompts/prompt-snapps-omp.md`](prompts/prompt-snapps-omp.md): ele define o que a ficha contém, as regras de fidelidade (nada é inferido além do que foi dito; lacunas viram "Não identificado na transcrição") e a exigência de citações literais como evidência. Editar esse arquivo muda o comportamento da ferramenta sem tocar em código.

## Instalação (≈ 5 minutos)

Pré-requisitos: [`uv`](https://docs.astral.sh/uv) e uma chave de API gratuita da [Groq](https://console.groq.com/keys).

```bash
git clone https://github.com/iago-leal/preceptor-ia.git
cd preceptor-ia
uv sync

cp .env.example .env
# edite .env e preencha LLM_API_KEY=<sua chave>

uv run streamlit run src/preceptor_ia/ui/app.py
```

O app abre em `http://localhost:8501` com três entradas: **áudio** (`.ogg`, `.mp3`, `.m4a`, `.wav`, até 25 MB), **transcrição colada** e **demonstração** (caso simulado embutido — útil para conhecer a ferramenta sem gravar nada).

## Configuração

Tudo via `.env` (modelo em [`.env.example`](.env.example)):

| Variável | Default | Função |
|----------|---------|--------|
| `LLM_API_KEY` | — (obrigatória) | Chave do provedor de IA |
| `LLM_BASE_URL` | endpoint OpenAI-compatible da Groq | Trocar de provedor sem tocar em código |
| `LLM_MODEL` | `llama-3.3-70b-versatile` | Modelo de análise |
| `TRANSCRICAO_MODEL` | `whisper-large-v3-turbo` | Modelo de transcrição |
| `HISTORICO_ATIVO` | `false` | Liga a gravação local das fichas geradas |
| `HISTORICO_DIR` | `~/.preceptor-ia/historico` | Onde o histórico é gravado (fora do repositório) |

Qualquer provedor com API compatível com o padrão OpenAI serve: basta ajustar `LLM_BASE_URL`, `LLM_MODEL` e a chave. Para **transcrição local** (privacidade máxima, sem enviar áudio a terceiros), ferramentas como [mlx-whisper](https://github.com/ml-explore/mlx-examples) (Apple Silicon) ou [whisper.cpp](https://github.com/ggml-org/whisper.cpp) podem alimentar a aba "Transcrição colada" — ou implementar o contrato `ServicoTranscricao` (uma classe com um método) para integração direta.

## Privacidade

- Áudios e transcrições **não são retidos**: circulam apenas em memória durante a geração da ficha.
- O histórico local é **opcional e desligado por padrão**; quando ativo, grava fora do repositório.
- Em demonstrações públicas, use **somente casos simulados**. Com passagens de caso reais, anonimize os dados do paciente antes de gravar — a responsabilidade pelo conteúdo enviado ao provedor de IA é do preceptor (LGPD).

## Arquitetura (resumo)

Camadas com portas e adaptadores: `domain/` (modelos, erros nomeados, prompt e contratos — sem dependência de framework), `application/` (caso de uso `GerarFicha` e fábrica), `infra/` (adaptadores HTTP OpenAI-compatible e histórico em filesystem), `ui/` (página Streamlit). Testes em `tests/` rodam sem rede (dublês e transporte HTTP mockado): `uv run pytest`.

## Fundamentação pedagógica

- SNAPPS: Wolpaw TM, Wolpaw DR, Papp KK. *Acad Med.* 2003.
- One-Minute Preceptor: Neher JO et al. *J Am Board Fam Pract.* 1992.
- Eficácia: Jain V, Rao S, Jinadani M. *BMC Med Educ.* 2019; Machado JLM, Medeiros ML. 2021.
- Avaliação longitudinal (horizonte de evolução): modelo CRAFT — Lawrence K et al. 2018.

## Licença

MIT.
