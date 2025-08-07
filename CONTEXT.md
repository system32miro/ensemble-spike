# Spike 3-CLI (Claude Code, Gemini CLI, Cursor CLI)

Objetivo: melhorar a funÃ§Ã£o sum_numbers em src/calc.py para:
- Lidar com entradas mistas (int/float) ignorando valores nÃ£o numÃ©ricos e tratando None como 0.
- Manter complexidade O(n) e sem dependÃªncias novas.
- Adicionar pelo menos 1 teste novo que cubra um caso de aresta (ex.: floats, None, valores muito grandes, lista longa).

CritÃ©rios de aceitaÃ§Ã£o:
- Todos os testes existentes passam (pytest).
- Pelo menos 1 teste novo Ã© adicionado e passa.
- Apenas os ficheiros permitidos podem ser editados: src/calc.py, 	ests/test_calc.py.
- NÃ£o modificar configs/projeto fora destes ficheiros.

Estilo/guia:
- CÃ³digo Python idiomÃ¡tico, legÃ­vel e simples (sem microâ€‘otimizaÃ§Ãµes prematuras).

EvidÃªncia atual:
- src/calc.py contÃ©m uma soma ingÃªnua que falha com None/strings.
- 	ests/test_calc.py tem casos bÃ¡sicos que devem permanecer a passar.

SaÃ­da esperada:
- EdiÃ§Ãµes aplicadas diretamente nos ficheiros permitidos.
- Testes existentes e novos a passar.
- Commit opcional: â€œspike: candidate <cli>â€.
