# ADR-0004 — Provedor único OpenAI-compatible, default Groq

> Retroativo, gerado pelo Detective (Reversa) em 2026-07-20. Status: **aceita** (implementada). Confiança: 🟢

## Contexto

O pipeline precisa de dois serviços de IA (Whisper para transcrição, LLM para análise). Multiplicar provedores multiplicaria credenciais, SDKs e modos de falha — contra o perfil de manutenção do projeto (single maintainer intermitente).

## Decisão

Um único `LLM_BASE_URL` + `LLM_API_KEY` serve às duas etapas, sobre o padrão de API OpenAI-compatible (`/audio/transcriptions` e `/chat/completions`), com **Groq como default** (`https://api.groq.com/openai/v1`, `llama-3.3-70b-versatile`, `whisper-large-v3-turbo`). Chamadas via `httpx` puro — **sem SDK do provedor**; a regra de negócio não acopla a biblioteca externa.

## Motivação aparente

🟡 Groq oferece chave gratuita (o README instrui a obtê-la) e hospeda os dois modelos necessários atrás do mesmo endpoint — custo zero para a validação conceitual e um único segredo a gerenciar. O padrão OpenAI-compatible maximiza os substitutos possíveis (OpenAI, Together, Ollama local etc.) sem mudança de código.

## Consequências

- Troca de provedor = editar `.env` (RN-C2). Transcrição local possível via aba de texto ou implementando `ServicoTranscricao`. 🟢
- Limite de 25 MB por áudio herdado do contrato de transcrição, promovido a regra de domínio (`TAMANHO_MAXIMO_AUDIO_BYTES`). 🟢
- Erros do provedor traduzidos em erros nomeados acionáveis (401→conferir chave, 429→aguardar ou trocar provedor). 🟢
- Restrição implícita: um provedor que só ofereça LLM (sem Whisper) exigiria dois base_urls — não suportado hoje. 🟡
