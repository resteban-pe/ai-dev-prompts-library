#!/usr/bin/env python3
"""
batch_runner.py — Inventaría los prompts disponibles sin llamar a la API.

Uso:
    python scripts/batch_runner.py --dir prompts/
    python scripts/batch_runner.py --dir prompts/ --output examples/outputs/inventory.txt
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from run_prompt import SYSTEM_BLOCK_RE, USER_BLOCK_RE

TITLE_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)
PURPOSE_RE = re.compile(r"##\s+Propósito\s*\n(.*?)(?=\n##|\Z)", re.DOTALL)
VARIABLE_RE = re.compile(r"\{\{(\w+)\}\}")


def inspect_prompt(path: Path) -> dict:
    """Lee un .md y extrae: título, propósito, variables requeridas y validez."""
    content = path.read_text(encoding="utf-8")

    title_match = TITLE_RE.search(content)
    title = title_match.group(1).strip() if title_match else path.stem

    purpose_match = PURPOSE_RE.search(content)
    purpose = purpose_match.group(1).strip() if purpose_match else "(sin propósito)"

    user_match = USER_BLOCK_RE.search(content)
    variables: list[str] = []
    if user_match:
        variables = sorted(set(VARIABLE_RE.findall(user_match.group(1))))

    has_system = bool(SYSTEM_BLOCK_RE.search(content))

    return {
        "path": path,
        "title": title,
        "purpose": purpose,
        "variables": variables,
        "valid": has_system and user_match is not None,
    }


def format_inventory(prompts: list[dict], prompts_dir: Path) -> str:
    lines: list[str] = []
    lines.append("=" * 60)
    lines.append(f"INVENTARIO DE PROMPTS")
    lines.append(f"Directorio : {prompts_dir}")
    lines.append(f"Total      : {len(prompts)} prompt(s)")
    lines.append("=" * 60)

    for i, p in enumerate(prompts, 1):
        try:
            rel = p["path"].relative_to(prompts_dir.parent)
        except ValueError:
            rel = p["path"]

        purpose_first_line = p["purpose"].splitlines()[0] if p["purpose"] else ""
        vars_str = ", ".join(p["variables"]) if p["variables"] else "(ninguna)"
        valid_str = "OK" if p["valid"] else "INVALIDO — falta seccion requerida"

        lines.append(f"\n[{i}] {p['title']}")
        lines.append(f"    Archivo   : {rel}")
        lines.append(f"    Proposito : {purpose_first_line}")
        lines.append(f"    Variables : {vars_str}")
        lines.append(f"    Estado    : {valid_str}")

    lines.append("\n" + "=" * 60)
    lines.append("Para ejecutar un prompt:")
    lines.append("  python scripts/run_prompt.py --prompt <archivo> --var KEY=VALUE")
    lines.append("=" * 60)

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Inventaría prompts .md sin llamar a la API."
    )
    parser.add_argument(
        "--dir", required=True, type=Path, help="Directorio raiz con archivos .md de prompts"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("examples/outputs/inventory.txt"),
        help="Archivo donde guardar el inventario (default: examples/outputs/inventory.txt)",
    )
    args = parser.parse_args()

    if not args.dir.exists():
        print(f"[ERROR] Directorio no encontrado: {args.dir}", file=sys.stderr)
        sys.exit(1)

    md_files = sorted(args.dir.rglob("*.md"))
    if not md_files:
        print(f"[ADVERTENCIA] No se encontraron archivos .md en {args.dir}", file=sys.stderr)
        sys.exit(0)

    prompts = [inspect_prompt(f) for f in md_files]
    report = format_inventory(prompts, args.dir)

    print(report)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report, encoding="utf-8")
    print(f"\nInventario guardado en: {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
