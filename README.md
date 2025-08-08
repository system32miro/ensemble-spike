# Ensemble Spike — CLIs de IA a colaborar sobre o mesmo repositório

Este mini‑projeto valida que é possível orquestrar múltiplos CLIs de IA para coding — Claude Code (Opus 4.1), Gemini CLI e Cursor CLI (GPT‑5) — a trabalhar em paralelo sobre o MESMO commit e com o MESMO contexto, escolhendo automaticamente o melhor diff com base em testes/lints.

- Claude Code: https://docs.anthropic.com/en/docs/claude-code/overview
- Gemini CLI: https://github.com/google-gemini/gemini-cli e https://blog.google/technology/developers/introducing-gemini-cli-open-source-ai-agent/
- Cursor CLI: https://docs.cursor.com/en/cli/overview

## O que valida
- Contexto único (ContextPack informal via `CONTEXT.md`/`PROMPT.md`) igual para todos.
- Estado partilhado via `git worktree` (cada agente edita a sua cópia do mesmo SHA).
- Seleção objetiva do melhor candidato por pipeline técnica (pytest + lints/SAST opcional).
- Integração automática numa branch de integração e PR com scoreboard.

## Estrutura principal
- `src/` e `tests/`: projeto mínimo (Python + pytest).
- `CONTEXT.md` e `PROMPT.md`: instruções e critérios de aceitação partilhados.
- `scripts/select_best.ps1`: avalia candidatos (pytest + diff shortstat), pontua e integra o melhor.
- `PLAN.md`: plano detalhado para evoluir isto para um MVP/Produto.
- `VALIDATION.md`: resumo da validação local.

## Requisitos
- Windows + PowerShell, Git e Python 3.10+.
- (Para uso dos CLIs) Ter `claude`, `gemini` e `cursor` instalados e autenticados.

## Como reproduzir rapidamente
1) Criar o spike e worktrees (se ainda não existir):
```powershell
# na pasta desejada
powershell -NoProfile -ExecutionPolicy Bypass -File .\spike.ps1 -ProjectName "ensemble-spike"
```
2) Em três consolas, executar cada CLI no respetivo worktree e colar `PROMPT.md` (cada CLI lê também `CONTEXT.md`).
3) Avaliar e integrar automaticamente o melhor candidato:
```powershell
# a partir de ensemble-spike
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\select_best.ps1 -Apply
```

## Critérios de aceitação (exemplo do spike)
- Melhorar `sum_numbers` e adicionar pelo menos 1 teste novo.
- Todos os testes a passar (`pytest`).
- Editar apenas `src/calc.py` e `tests/test_calc.py`.

## Resultados (exemplo)
- Três candidatos válidos; escolhido o Gemini por menor diff e testes a passar.
- PR aberto com scoreboard e alterações integradas na branch de integração.

## Próximos passos (produto)
- Formalizar `ContextPack` (JSON) e adaptadores não‑interativos para os CLIs.
- CI em matriz (GitHub Actions) a publicar scoreboard no PR e aplicar o melhor diff.
- Router “cost‑aware” (K pequeno, early‑stop) e políticas (paths editáveis, budgets, DLP).

---

Licença: experimental (spike). Use por sua conta e risco.
