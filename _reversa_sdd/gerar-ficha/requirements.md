# Gerar Ficha

> Gerado pelo **Writer** (Reversa) em 2026-07-20. Unit: `gerar-ficha` (feature central).
> Escala: 🟢 CONFIRMADO · 🟡 INFERIDO · 🔴 LACUNA

## Visão Geral

Caso de uso central do PreceptorIA: recebe uma `Entrada` (áudio, texto colado ou caso demo), obtém a transcrição (chamando o serviço de transcrição apenas quando a origem é áudio), aplica o prompt canônico SNAPPS-OMP via serviço de análise e devolve uma `Ficha` de feedback formativo em Markdown. Opcionalmente grava a ficha no histórico local. 🟢

## Responsabilidades

- Validar a entrada na construção do objeto — nenhuma `Entrada` inválida circula. 🟢
- Orquestrar o pipeline ingestão → transcrição condicional → análise → entrega. 🟢
- Garantir que resposta vazia da análise jamais vire ficha. 🟢
- Descartar o áudio após a transcrição (não-retenção). 🟢
- Delegar a gravação de histórico apenas quando o repositório foi injetado. 🟢

## Regras de Negócio

- Entrada de texto/demo exige transcrição não-vazia após `strip()`; mensagem: `"Entrada de texto vazia: cole a transcrição da passagem de caso."` 🟢
- Entrada de áudio exige nome de arquivo **e** conteúdo; extensão ∈ {`.ogg`, `.mp3`, `.m4a`, `.wav`} (case-insensitive); tamanho ≤ 25 MB (26.214.400 bytes). 🟢
- A transcrição de origens `TEXTO`/`DEMO` é o próprio texto fornecido, com `strip()`. 🟢
- Resposta da análise vazia/whitespace → `ErroRespostaAnalise` (o sistema prefere falhar a inventar — RN-03). 🟢
- A `Ficha` guarda o Markdown com `strip()` aplicado, a origem da entrada e `gerada_em = datetime.now()` (horário local). 🟢
- O áudio não é retido após a transcrição; somente o texto circula dali em diante (RN-07). 🟢
- Gravação no histórico ocorre **antes** do log de entrega e não tem isolamento de falha: erro de IO aborta a entrega da ficha já gerada. 🟡 (comportamento real, intencionalidade não documentada)

## Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de Aceite |
|----|-----------|-----------|-------------------|
| RF-GF-01 | Gerar ficha a partir de áudio válido (formato e tamanho aceitos) | Must | `executar(Entrada(AUDIO,...))` devolve `Ficha` com markdown não-vazio |
| RF-GF-02 | Gerar ficha a partir de transcrição colada | Must | `executar(Entrada(TEXTO,...))` devolve `Ficha` sem chamar o serviço de transcrição |
| RF-GF-03 | Gerar ficha a partir do caso demo | Must | Igual a RF-GF-02 com origem `DEMO` |
| RF-GF-04 | Rejeitar entrada inválida antes de qualquer chamada externa | Must | Construção de `Entrada` inválida levanta `ErroEntradaInvalida`; nenhum serviço é invocado |
| RF-GF-05 | Rejeitar resposta de análise vazia | Must | `ErroRespostaAnalise` com mensagem `"O serviço de análise devolveu resposta vazia; a ficha não foi gerada."` |
| RF-GF-06 | Gravar ficha no histórico quando o repositório foi injetado | Should | `historico.gravar(ficha)` chamado exatamente uma vez por ficha gerada |

## Requisitos Não Funcionais

| Tipo | Requisito inferido | Evidência no código | Confiança |
|------|--------------------|---------------------|-----------|
| Privacidade | Áudio descartado após transcrição; logs só de metadados (origem, tamanho, nome) — nunca conteúdo clínico | `application/gerar_ficha.py:30-57` | 🟢 |
| Observabilidade | Log estruturado chave=valor por etapa: `etapa=ingestao/transcricao/analise/entrega` | `application/gerar_ficha.py:30,33,44,51` | 🟢 |
| Confiabilidade | Execução atômica: ou devolve `Ficha`, ou levanta erro nomeado; sem retry, sem estado intermediário | `application/gerar_ficha.py:29-45` | 🟢 |

## Critérios de Aceitação

```gherkin
Dado uma Entrada de origem TEXTO com transcrição não-vazia
Quando GerarFicha.executar é chamado
Então o serviço de análise recebe (prompt_canonico, texto_com_strip)
E o serviço de transcrição NÃO é chamado
E o retorno é uma Ficha com markdown = resposta.strip() e origem_entrada = TEXTO

Dado uma Entrada de origem AUDIO válida
Quando GerarFicha.executar é chamado
Então o serviço de transcrição recebe (conteudo_audio, nome_arquivo)
E o texto transcrito (com strip) segue para a análise
E o áudio não é referenciado após a transcrição

Dado que o serviço de análise devolve string vazia ou whitespace
Quando GerarFicha.executar é chamado
Então ErroRespostaAnalise é levantado e nenhuma Ficha é criada

Dado um arquivo "gravacao.xyz" (extensão não suportada)
Quando Entrada(AUDIO, nome_arquivo="gravacao.xyz", conteudo_audio=b"...") é construída
Então ErroEntradaInvalida é levantado citando os formatos aceitos
E nenhuma chamada externa ocorre

Dado historico injetado e uma execução bem-sucedida
Quando a ficha é criada
Então historico.gravar(ficha) é chamado uma única vez
```

## Prioridade (MoSCoW)

| Requisito | MoSCoW | Justificativa |
|-----------|--------|---------------|
| Pipeline de geração (RF-GF-01..03) | Must | Caminho crítico — é o produto inteiro |
| Validação na construção (RF-GF-04) | Must | Barreira de privacidade: falha antes de dados saírem da máquina |
| Recusa de resposta vazia (RF-GF-05) | Must | Regra pedagógica central (não inventar ficha) |
| Histórico (RF-GF-06) | Should | Opt-in, desligado por padrão |

## Rastreabilidade de Código

| Arquivo | Função / Classe | Cobertura |
|---------|-----------------|-----------|
| `src/preceptor_ia/application/gerar_ficha.py` | `GerarFicha.executar`, `_obter_transcricao` | 🟢 |
| `src/preceptor_ia/application/factory.py` | `montar_gerar_ficha` | 🟢 |
| `src/preceptor_ia/domain/models.py` | `Entrada`, `Ficha`, `Transcricao`, `OrigemEntrada`, hierarquia de erros | 🟢 |
| `src/preceptor_ia/domain/ports.py` | `ServicoTranscricao`, `ServicoAnalise`, `RepositorioHistorico` | 🟢 |
| `src/preceptor_ia/domain/prompt.py` | `carregar_prompt`, `ErroPromptCanonico` | 🟢 |
| `tests/test_gerar_ficha.py`, `tests/test_domain.py` | Suítes com dublês | 🟢 |
