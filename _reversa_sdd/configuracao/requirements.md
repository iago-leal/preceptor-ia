# Configuração

> Gerado pelo **Writer** (Reversa) em 2026-07-20. Unit: `configuracao`.
> Escala: 🟢 CONFIRMADO · 🟡 INFERIDO · 🔴 LACUNA

## Visão Geral

Camada de configuração tipada via `pydantic-settings`: tudo vem do ambiente ou do `.env` (modelo em `.env.example`), nada chumbado no código. Uma única variável obrigatória (`LLM_API_KEY`); falha de validação vira `ErroConfiguracao` com mensagem que nomeia o que falta e aponta o `.env.example` (RF-05: falha barulhenta). 🟢

## Responsabilidades

- Declarar e validar as 6 configurações do sistema com defaults seguros. 🟢
- Converter qualquer falha de validação em `ErroConfiguracao` acionável. 🟢
- Manter o segredo (`LLM_API_KEY`) fora do código e do git (`.env` no `.gitignore`). 🟢

## Regras de Negócio

- `llm_api_key`: obrigatória, `min_length=1` — string vazia é inválida. 🟢
- Defaults: `llm_base_url=https://api.groq.com/openai/v1`, `llm_model=llama-3.3-70b-versatile`, `transcricao_model=whisper-large-v3-turbo`, `historico_ativo=False`, `historico_dir=~/.preceptor-ia/historico`. 🟢
- Fonte: `.env` na raiz + variáveis de ambiente; `extra="ignore"` (variáveis desconhecidas não quebram). 🟢
- `ErroConfiguracao` herda de `RuntimeError`, **deliberadamente fora** da hierarquia `ErroPreceptorIA` — a configuração precede o domínio; a UI a captura em bloco separado com prefixo ⚙️. 🟡 (padrão consistente, intenção não documentada)
- Troca de provedor sem código: qualquer endpoint OpenAI-compatible via `LLM_BASE_URL` + modelos (RN-C2, ADR-0004). 🟢

## Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de Aceite |
|----|-----------|-----------|-------------------|
| RF-CF-01 | Carregar Settings de `.env`/ambiente com os 6 campos e defaults documentados | Must | `Settings()` com só `LLM_API_KEY` definida produz os 5 defaults |
| RF-CF-02 | Falhar barulhento sem `LLM_API_KEY` | Must | `carregar_settings()` levanta `ErroConfiguracao` citando a variável e o `.env.example` |
| RF-CF-03 | Ignorar variáveis extras do ambiente | Should | `.env` com chaves desconhecidas não causa erro |
| RF-CF-04 | Tipagem forte (`bool`, `Path`) com coerção do pydantic | Must | `HISTORICO_ATIVO=true` (string) vira `True`; `HISTORICO_DIR` vira `Path` |

## Requisitos Não Funcionais

| Tipo | Requisito inferido | Evidência no código | Confiança |
|------|--------------------|---------------------|-----------|
| Segurança | Segredo só em `.env` (git-ignored); nunca logado | `config.py:14-16`, `.gitignore` | 🟢 |
| Operabilidade | Mensagem de erro nomeia a variável e o modelo de arquivo | `config.py:29-31` | 🟢 |

## Critérios de Aceitação

```gherkin
Dado um ambiente com apenas LLM_API_KEY=abc
Quando carregar_settings() é chamado
Então Settings tem base_url Groq, modelos default, historico desativado

Dado um ambiente sem LLM_API_KEY (e sem .env)
Quando carregar_settings() é chamado
Então ErroConfiguracao é levantado com mensagem iniciando em
  "Configuração incompleta: defina LLM_API_KEY no ambiente ou no arquivo .env"

Dado LLM_API_KEY="" (vazia)
Quando carregar_settings() é chamado
Então ErroConfiguracao é levantado (min_length=1)
```

## Prioridade (MoSCoW)

| Requisito | MoSCoW | Justificativa |
|-----------|--------|---------------|
| Carga + validação (RF-CF-01/02/04) | Must | Pré-condição de todo o sistema; a fábrica depende dela |
| Tolerância a extras (RF-CF-03) | Should | Conveniência; evita quebra por `.env` compartilhado |

## Rastreabilidade de Código

| Arquivo | Função / Classe | Cobertura |
|---------|-----------------|-----------|
| `src/preceptor_ia/config.py` | `Settings`, `carregar_settings`, `ErroConfiguracao` | 🟢 |
| `.env.example` | Modelo documentado das variáveis | 🟢 |
