# Análise LLM (Ficha SNAPPS-OMP)

> Gerado pelo **Writer** (Reversa) em 2026-07-20. Unit: `analise-llm`.
> Escala: 🟢 CONFIRMADO · 🟡 INFERIDO · 🔴 LACUNA

## Visão Geral

Adaptador que aplica o prompt canônico SNAPPS-OMP à transcrição da passagem de caso, consumindo `/chat/completions` de provedor OpenAI-compatible (default: Groq com `llama-3.3-70b-versatile`), e o **prompt canônico** em si (`prompts/prompt-snapps-omp.md`) — o comportamento pedagógico como dado. A unit cobre os dois artefatos porque um só existe em função do outro. 🟢

## Responsabilidades

- Enviar prompt canônico (system) + transcrição (user) ao LLM com `temperature=0.2`. 🟢
- Fazer parse defensivo da resposta e recusar conteúdo vazio/malformado. 🟢
- Definir, via prompt, o formato exato da ficha e as regras de fidelidade pedagógica. 🟢

## Regras de Negócio

### No código

- `temperature=0.2`: fidelidade acima de criatividade (RN-03). 🟢
- Mensagens: `system` = prompt canônico íntegro; `user` = transcrição — sem interpolação no template (RN-P8). 🟢
- Resposta malformada (`KeyError`/`IndexError`/`ValueError` ao ler `choices[0].message.content`) → `ErroRespostaAnalise`. 🟢
- Conteúdo vazio/whitespace → `ErroRespostaAnalise`. 🟢
- Timeout 120 s; mapeamento HTTP idêntico ao da transcrição (etapa nomeada "análise"). 🟢

### No prompt canônico (comportamento pedagógico)

- Ficha estruturada em SNAPPS (6 elementos do residente) + OMP (5 microhabilidades do preceptor). 🟢
- Nada é inferido além do dito: campo não identificável recebe o literal `"Não identificado na transcrição"` (RN-F1). 🟢
- Cada elemento identificado exige citação literal da transcrição como evidência (RN-F2). 🟢
- Sugestões de melhoria para ambos os papéis — residente e preceptor (RN-F3). 🟢
- Campos administrativos ausentes → `"A preencher"`. 🟢
- ⚠️ O template termina com `{{transcricao}}`, que o código **não interpola** — o LLM recebe o placeholder literal no system prompt (RN-F4). 🔴 Lacuna L2, ver `questions.md`.

## Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de Aceite |
|----|-----------|-----------|-------------------|
| RF-AL-01 | Gerar Markdown da ficha a partir de (prompt, transcrição) | Must | `analisar(prompt, texto)` devolve string não-vazia no formato da ficha |
| RF-AL-02 | Enviar exatamente 2 mensagens (system + user) com `temperature=0.2` | Must | Payload JSON conforme `contracts.md` |
| RF-AL-03 | Recusar resposta malformada ou vazia | Must | `ErroRespostaAnalise` nos dois casos, com mensagens distintas |
| RF-AL-04 | Carregar o prompt canônico de `prompts/prompt-snapps-omp.md`, falhando alto se ausente/vazio | Must | `ErroPromptCanonico` com mensagem citando o caminho |
| RF-AL-05 | Manter o comportamento pedagógico integralmente no arquivo de prompt (editável sem código) | Must | Alterar o `.md` muda a ficha gerada sem redeploy |

## Requisitos Não Funcionais

| Tipo | Requisito inferido | Evidência no código | Confiança |
|------|--------------------|---------------------|-----------|
| Performance | Timeout 120 s, sem retry | `infra/analise_openai.py:12,36` | 🟢 |
| Segurança | Bearer `LLM_API_KEY`; conteúdo clínico nunca logado pelo adaptador | `infra/analise_openai.py:27` | 🟢 |
| Determinismo relativo | `temperature=0.2` reduz variância entre gerações | `infra/analise_openai.py:13` | 🟢 |

## Critérios de Aceitação

```gherkin
Dado um provedor que responde 200 com choices[0].message.content = "# Ficha..."
Quando analisar(prompt, transcricao) é chamado
Então o retorno é o content (sem strip nesta camada — o strip é do caso de uso)

Dado um provedor que responde 200 com JSON sem "choices"
Quando analisar é chamado
Então ErroRespostaAnalise é levantado ("Resposta malformada do serviço de análise: ...")

Dado um provedor que responde 200 com content = ""
Quando analisar é chamado
Então ErroRespostaAnalise é levantado ("Serviço de análise devolveu conteúdo vazio.")

Dado o arquivo prompts/prompt-snapps-omp.md ausente
Quando carregar_prompt() é chamado
Então ErroPromptCanonico é levantado citando o caminho esperado

Dado uma transcrição em que o residente não formulou perguntas
Quando a ficha é gerada
Então o campo correspondente do SNAPPS recebe "Não identificado na transcrição"
E nenhum conteúdo é inventado
```

## Prioridade (MoSCoW)

| Requisito | MoSCoW | Justificativa |
|-----------|--------|---------------|
| Chamada de análise (RF-AL-01/02) | Must | Coração do produto — toda ficha passa aqui |
| Parse defensivo (RF-AL-03) | Must | Regra "não inventar ficha" sem fallback |
| Prompt-as-data (RF-AL-04/05) | Must | ADR-0003; o prompt É o produto |

## Rastreabilidade de Código

| Arquivo | Função / Classe | Cobertura |
|---------|-----------------|-----------|
| `src/preceptor_ia/infra/analise_openai.py` | `AnaliseOpenAICompat.analisar` | 🟢 |
| `src/preceptor_ia/domain/prompt.py` | `carregar_prompt`, `CAMINHO_PROMPT_PADRAO` | 🟢 |
| `prompts/prompt-snapps-omp.md` | Prompt canônico (artefato de dado) | 🟢 |
| `tests/test_adaptadores.py`, `tests/test_domain.py` | Transporte mockado + validação do prompt | 🟢 |
