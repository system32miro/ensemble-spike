import argparse
import json
import os
import subprocess
from pathlib import Path


def git(cmd: list[str], cwd: Path) -> str:
    result = subprocess.run(["git", *cmd], cwd=cwd, capture_output=True, text=True, check=True)
    return result.stdout.strip()


def read_file_lines(path: Path, start: int, end: int) -> str:
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
    start_idx = max(1, start) - 1
    end_idx = min(len(lines), end)
    return "".join(lines[start_idx:end_idx])


def build_context_pack(repo_dir: Path, task_id: str, objective: str, files: list[str]) -> dict:
    sha = git(["rev-parse", "HEAD"], repo_dir)
    # naive spans: include whole file
    focus_files = []
    evidence = []
    for rel in files:
        p = (repo_dir / rel).resolve()
        if not p.exists():
            continue
        # count lines
        try:
            with p.open("r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception:
            content = ""
        total_lines = content.count("\n") + (0 if content.endswith("\n") else 1)
        if total_lines <= 0:
            total_lines = 1
        focus_files.append({"path": rel, "spans": [[1, total_lines]]})
        # add first 200 lines as evidence (bounded)
        excerpt = read_file_lines(repo_dir / rel, 1, min(200, total_lines))
        evidence.append({"file": rel, "start": 1, "end": min(200, total_lines), "content": excerpt})

    pack = {
        "task_id": task_id,
        "repo": {"sha": sha, "branch": git(["rev-parse", "--abbrev-ref", "HEAD"], repo_dir)},
        "objective": objective,
        "acceptance_criteria": [
            "Todos os testes existentes passam",
            "Adicionar pelo menos 1 teste relevante",
            "Editar apenas paths permitidos",
        ],
        "policies": {
            "editable_paths": files,
            "blocked_paths": [".github/**", "infra/**"],
            "max_time_seconds": 600,
            "max_tokens": 200000,
        },
        "focus": {"files": focus_files, "symbols": []},
        "evidence": evidence,
        "style": {"language": "python", "linters": ["pytest"], "notes": "idiomático, simples"},
        "budgets": {"time_seconds": 300, "attempts": 1},
        "expected_output": {"requires_tests": True, "rationale": "brief", "format": "diff+tests"},
    }
    return pack


def main() -> None:
    parser = argparse.ArgumentParser(description="Gerar ContextPack v1 simples")
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--objective", required=True)
    parser.add_argument(
        "--files", nargs="+", required=True, help="Lista de ficheiros/paths a incluir como foco/editáveis"
    )
    parser.add_argument("--out", default=".context/context.json")
    args = parser.parse_args()

    repo_dir = Path.cwd()
    out_path = repo_dir / args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)

    pack = build_context_pack(repo_dir, args.task_id, args.objective, args.files)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(pack, f, ensure_ascii=False, indent=2)
    print(f"ContextPack gravado em: {out_path}")


if __name__ == "__main__":
    main()


