# Análise LLM, Design Técnico

> Gerado pelo **Writer** (Reversa) em 2026-07-20.
> Escala: 🟢 CONFIRMADO · 🟡 INFERIDO · 🔴 LACUNA

## Interface

| Símbolo | Assinatura | Retorno | Observação |
|---------|-----------|---------|------------|
| `AnaliseOpenAICompat.__init__` | `(base_url: str, api_key: str, modelo: str)` | — | `base_url` recebe `rstrip("/")` |
| `AnaliseOpenAICompat.analisar` | `(prompt_sistema: str, transcricao: str)` | `str` | Satisfaz o Protocol `ServicoAnalise`; devolve `content` cru (o `strip()` final é do caso de uso) |

Constantes: `TIMEOUT_SEGUNDOS = 120.0`, `TEMPERATURA = 0.2`, `ETAPA = "análise"`. 🟢

## Fluxo Principal

1. `httpx.post(f"{base_url}/chat/completions", ...)` com Bearer e corpo JSON `{model, temperature: 0.2, messages: [{role: system, content: prompt_sistema}, {role: user, content: transcricao}]}`, timeout 120 s (`analise_openai.py:25-37`).
2. `_levantar_erro_nomeado(resposta, "análise")` — importada de `transcricao_openai.py` (`analise_openai.py:8,41`).
3. Parse defensivo: `resposta.json()["choices"][0]["message"]["content"]`; `KeyError`/`IndexError`/`ValueError` → `ErroRespostaAnalise` com corpo truncado em 300 chars (`analise_openai.py:42-47`).
4. `content` vazio/whitespace → `ErroRespostaAnalise` (`analise_openai.py:48-49`).
5. Retorna `content` como recebido. 🟢

## Estrutura do prompt canônico (`prompts/prompt-snapps-omp.md`, 105 linhas)

| Bloco | Linhas | Conteúdo |
|---|---|---|
| Papel e tarefa | 1-3 | Assistente de educação médica; analisar transcrição e gerar ficha |
| Modelos de referência | 5-20 | SNAPPS (6 elementos) e OMP (5 microhabilidades) definidos item a item |
| Instruções | 22-28 | Registrar só o identificável; citar trechos como evidência; sugerir melhorias para ambos os papéis |
| Formato de saída | 30-99 | Template literal da ficha: cabeçalho administrativo ("A preencher" quando ausente), seção 1 SNAPPS, seção 2 OMP, seção 3 Plano de aprendizado |
| Seção residual | 102-104 | `## Transcrição recebida` + `{{transcricao}}` — **nunca interpolado pelo código** 🔴 |

## Fluxos Alternativos

- **`httpx.HTTPError`:** → `ErroServicoExterno` (`Falha de rede na etapa de análise: {exc}`).
- **HTTP 401/429/≥400:** mesmo tradutor da transcrição, etapa "análise" (ver `contracts.md`).
- **200 com corpo não-JSON:** `ValueError` do parse é capturada → `ErroRespostaAnalise` (diferente do adaptador de transcrição, onde vazaria). 🟢

## Dependências

- `httpx` — POST module-level, sem client persistente.
- `infra/transcricao_openai._levantar_erro_nomeado` — acoplamento interno entre adaptadores (DT-4). 🟡
- `domain/models.py` — `ErroRespostaAnalise`, `ErroServicoExterno`.

## Decisões de Design Identificadas

| Decisão | Evidência no código | Confiança |
|---------|---------------------|-----------|
| Transcrição como mensagem `user` separada, template íntegro como `system` | `analise_openai.py:31-34` | 🟢 |
| `temperature=0.2` fixa em constante, não configurável via `.env` | `analise_openai.py:13` | 🟢 |
| Sem `max_tokens`, `top_p` ou penalidades — defaults do provedor | `analise_openai.py:28-35` | 🟢 |
| Formato da ficha imposto por instrução ("Gere a ficha exatamente no formato abaixo"), sem structured output/JSON mode | `prompts/prompt-snapps-omp.md:32` | 🟢 |

## Estado Interno

Nenhum. Três parâmetros imutáveis no construtor. 🟢

## Observabilidade

Logger definido mas sem emissão própria (mesmo padrão do adaptador de transcrição); o caso de uso loga `etapa=analise tamanho_transcricao=...` antes da chamada. 🟢

## Riscos e Lacunas

- 🔴 **L2 / DT-1:** o placeholder `{{transcricao}}` chega literal ao LLM no fim do system prompt. Como a transcrição real vem na mensagem `user`, o modelo em geral ignora o resíduo — mas é divergência entre desenho do template e uso real, com risco de o modelo ecoar a seção "Transcrição recebida" vazia na ficha. Decisão pendente em `questions.md`.
- 🟡 Sem `max_tokens`: fichas muito longas dependem do limite default do provedor; transcrições enormes podem estourar contexto do modelo sem mensagem amigável (viraria HTTP 400 → `ErroServicoExterno` com corpo do provedor).
- 🟡 A qualidade pedagógica da ficha depende inteiramente do modelo configurado; trocar `LLM_MODEL` muda o produto sem qualquer teste que o detecte.
