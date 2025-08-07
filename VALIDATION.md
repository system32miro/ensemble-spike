# Validação do Spike (3 CLIs)

- Melhor candidato: Gemini (menor diff com testes a passar)
- Testes no base: PASS
- Scoreboard (linhas alteradas):
  - gemini: +7/-3 (3 ficheiros)
  - claude: +18/-3 (2 ficheiros)
  - cursor: +26/-5 (2 ficheiros)

Como reproduzir:
- Avaliar: `powershell -NoProfile -ExecutionPolicy Bypass -File ..\\scripts\\select_best.ps1`
- Aplicar: `powershell -NoProfile -ExecutionPolicy Bypass -File ..\\scripts\\select_best.ps1 -Apply`
