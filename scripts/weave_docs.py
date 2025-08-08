import argparse
from pathlib import Path
import re

BEGIN = "<!-- BEGIN:AUTO:API -->"
END = "<!-- END:AUTO:API -->"


def upsert_block(md: str, new_block: str) -> str:
    pattern = re.compile(re.escape(BEGIN) + r"[\s\S]*?" + re.escape(END), re.MULTILINE)
    replacement = f"{BEGIN}\n{new_block}\n{END}"
    if pattern.search(md):
        # Use function replacement to avoid backslash escapes in replacement string
        return pattern.sub(lambda _m: replacement, md)
    # append at end with a separator
    md = md.rstrip() + "\n\n" + replacement + "\n"
    return md


def derive_api_summary(src_dir: Path) -> str:
    items: list[str] = []
    for py in src_dir.rglob("*.py"):
        rel = py.relative_to(src_dir.parent)
        items.append(f"- `{rel}`: {sum(1 for _ in py.open('r', encoding='utf-8', errors='ignore'))} linhas")
    if not items:
        return "(sem ficheiros Python detectados)"
    return "\n".join(items)


def main() -> None:
    parser = argparse.ArgumentParser(description="Atualizar blocos AUTO nos Markdown")
    parser.add_argument("--file", default="README.md")
    parser.add_argument("--src", default="src")
    args = parser.parse_args()

    md_path = Path(args.file)
    src_dir = Path(args.src)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    content = md_path.read_text(encoding="utf-8") if md_path.exists() else "# Documentação\n\n"

    api_summary = derive_api_summary(src_dir if src_dir.exists() else Path("."))
    new_block = f"Resumo automático dos ficheiros Python em `{src_dir}`:\n\n{api_summary}"
    updated = upsert_block(content, new_block)
    md_path.write_text(updated, encoding="utf-8")
    print(f"Bloco AUTO atualizado em: {md_path}")


if __name__ == "__main__":
    main()


