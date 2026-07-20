# Permissões e Papéis — PreceptorIA

> Gerado pelo **Detective** (Reversa) em 2026-07-20.
> Escala: 🟢 CONFIRMADO · 🟡 INFERIDO · 🔴 LACUNA

## Conclusão central

**Não existe RBAC/ACL no código.** 🟢 A aplicação não tem autenticação, cadastro, sessão de usuário nem qualquer verificação de identidade: é uma página Streamlit local de papel único. A varredura não encontrou nenhum símbolo de auth (`login`, `user`, `role`, `permission`, `token` de sessão) fora do `Bearer` da API do provedor.

## Papéis

| Papel | Natureza | Acesso |
|---|---|---|
| **Preceptor (operador local)** | Único papel humano; quem roda `streamlit run` e abre `localhost:8501`. | Total: todas as abas, geração, download e (se ativo) histórico. 🟢 |
| **Residente** | Papel de domínio, não de sistema — aparece na transcrição e na ficha, mas nunca opera a ferramenta. | Nenhum. 🟢 |
| **Provedor de IA (Groq ou compatível)** | Ator externo técnico; recebe áudio/transcrição para processar. | Autenticado via `LLM_API_KEY` (Bearer); a relação de confiança é regida pelo aviso LGPD, não por controle de acesso do app. 🟢 |

## Matriz de capacidades (papel único)

| Capacidade | Preceptor local | Guarda existente |
|---|---|---|
| Gerar ficha por áudio | ✅ | Validação de formato/tamanho, não de identidade (`domain/models.py:58-72`) |
| Gerar ficha por texto | ✅ | Texto não-vazio |
| Gerar ficha demo | ✅ | — |
| Exibir contingência offline | ✅ | Só se `demo/ficha-exemplo.md` existir (`ui/app.py:89`) |
| Baixar ficha `.md` | ✅ | — |
| Ler histórico gravado | ✅ (via filesystem) | Permissões do SO em `~/.preceptor-ia/historico`; o app não lê o histórico, só grava 🟢 |
| Alterar comportamento pedagógico | ✅ (editar `prompts/prompt-snapps-omp.md`) | Nenhuma — o prompt é dado, não código 🟢 |
| Trocar provedor/modelos | ✅ (editar `.env`) | Nenhuma |

## Fronteiras de segurança efetivas

O controle de acesso real é **delegado ao ambiente de execução**, não implementado no app: 🟢

1. **Rede** — Streamlit servindo em localhost por padrão; quem alcança a porta usa o app. Não há binding configurado no repositório (nem `--server.address`), portanto exposição pública dependeria de decisão de deploy externa ao código. 🟡
2. **Filesystem** — histórico fora do repositório, protegido só pelas permissões do usuário do SO. 🟢
3. **Segredo** — `LLM_API_KEY` vive no `.env` (ignorado pelo git via `.gitignore`) e nunca é logado. 🟢

## Avaliação e lacunas

| # | Observação | Confiança |
|---|---|---|
| P1 | A ausência de auth é **coerente com o escopo** (validação conceitual, uso local pelo próprio preceptor); não é dívida hoje. | 🟡 |
| P2 | 🟢 **[Revisão 2026-07-20] Resolvida:** o autor confirmou que o produto é técnico, estilo protótipo, para **instalação local pelo próprio preceptor** (cada usuário roda a sua instância) — coerente com o RNF de Distribuição da spec de origem (repo público + manual de implantação). Deploy multiusuário hospedado está fora de escopo; a ausência de auth é decisão de escopo, não lacuna. Se o escopo mudar um dia, gate de acesso e isolamento de histórico viram requisitos Must. | 🟢 |
| P3 | A "permissão" mais sensível do sistema é implícita: qualquer pessoa com acesso ao filesystem edita o prompt canônico e muda o comportamento clínico-pedagógico da ferramenta sem deixar rastro no app (o git rastreia, o app não valida procedência). Aceitável localmente; relevante em qualquer cenário compartilhado. | 🟡 |
