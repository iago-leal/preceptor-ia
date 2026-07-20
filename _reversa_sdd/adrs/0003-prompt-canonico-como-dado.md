# ADR-0003 — Prompt canônico como arquivo de dados (prompt-as-data)

> Retroativo, gerado pelo Detective (Reversa) em 2026-07-20. Status: **aceita** (implementada). Confiança: 🟢

## Contexto

O comportamento pedagógico (estrutura SNAPPS-OMP da ficha, regras de fidelidade, exigência de citações) é o coração do produto e o que a orientação do curso mais tende a iterar — mais que o código.

## Decisão

Todo o comportamento pedagógico vive em `prompts/prompt-snapps-omp.md`, carregado em runtime por `domain/prompt.py`. O README declara: "Editar esse arquivo muda o comportamento da ferramenta sem tocar em código". A ausência ou vazio do arquivo é falha fatal (`ErroPromptCanonico`) — o app se recusa a operar sem sua fonte de verdade pedagógica (RF-04/RN-06).

## Consequências

- Iteração pedagógica desacoplada de deploy de código; o git versiona a evolução do prompt como documento. 🟢
- O prompt é enviado como mensagem `system` íntegra; a transcrição segue como mensagem `user` separada (`infra/analise_openai.py:31-34`). 🟢
- ⚠️ Efeito colateral: a seção final do template (`## Transcrição recebida` + `{{transcricao}}`) não é interpolada pelo código — o LLM recebe o placeholder literal. Provável resíduo do fluxo n8n (ADR-0001), onde a interpolação existia. Corrigir o prompt ou documentar a intenção. 🟡
- Risco aceito: qualquer pessoa com acesso ao filesystem altera o comportamento clínico sem passar por revisão de código (ver permissions.md, P3). 🟡
