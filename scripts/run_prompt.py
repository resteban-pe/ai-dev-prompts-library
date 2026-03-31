#!/usr/bin/env python3
"""
run_prompt.py — Ejecuta un prompt Markdown contra la Claude API.

Uso:
    python scripts/run_prompt.py --prompt prompts/code_review/review_java_class.md
    python scripts/run_prompt.py --prompt prompts/code_review/review_java_class.md \
        --var class_name=UserService \
        --var java_code="$(cat UserService.java)" \
        --model claude-opus-4-6 \
        --output examples/outputs/review_output.md
"""

import argparse
import re
import sys
from pathlib import Path

import anthropic
from dotenv import load_dotenv

load_dotenv()

DEFAULT_MODEL = "claude-sonnet-4-6"
DEFAULT_MAX_TOKENS = 4096

SYSTEM_BLOCK_RE = re.compile(
    r"##\s+Contexto del sistema.*?```\n(.*?)```", re.DOTALL
)
USER_BLOCK_RE = re.compile(
    r"##\s+Template del mensaje.*?```\n(.*?)```", re.DOTALL
)


def parse_prompt_file(path: Path) -> tuple[str, str]:
    """Extrae system prompt y user template de un archivo .md de prompt."""
    content = path.read_text(encoding="utf-8")

    system_match = SYSTEM_BLOCK_RE.search(content)
    user_match = USER_BLOCK_RE.search(content)

    if not system_match:
        raise ValueError(f"No se encontró bloque '## Contexto del sistema' en {path}")
    if not user_match:
        raise ValueError(f"No se encontró bloque '## Template del mensaje' en {path}")

    return system_match.group(1).strip(), user_match.group(1).strip()


def apply_variables(template: str, variables: dict[str, str]) -> str:
    """Reemplaza {{variable}} en el template con los valores provistos."""
    for key, value in variables.items():
        template = template.replace(f"{{{{{key}}}}}", value)
    return template


def run_prompt(
    prompt_path: Path,
    variables: dict[str, str],
    model: str = DEFAULT_MODEL,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    output_path: Path | None = None,
) -> str:
    system_prompt, user_template = parse_prompt_file(prompt_path)
    user_message = apply_variables(user_template, variables)

    remaining = re.findall(r"\{\{(\w+)\}\}", user_message)
    if remaining:
        print(f"[ADVERTENCIA] Variables sin reemplazar: {remaining}", file=sys.stderr)

    client = anthropic.Anthropic()

    print(f"Modelo: {model}", file=sys.stderr)
    print(f"Prompt: {prompt_path}", file=sys.stderr)
    print("Enviando a Claude API...", file=sys.stderr)

    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )

    response_text = message.content[0].text

    print(
        f"Tokens usados — input: {message.usage.input_tokens}, "
        f"output: {message.usage.output_tokens}",
        file=sys.stderr,
    )

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(response_text, encoding="utf-8")
        print(f"Output guardado en: {output_path}", file=sys.stderr)

    return response_text


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ejecuta un prompt Markdown contra la Claude API."
    )
    parser.add_argument(
        "--prompt", required=True, type=Path, help="Ruta al archivo .md del prompt"
    )
    parser.add_argument(
        "--var",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="Variable para el template (puede repetirse): --var key=value",
    )
    parser.add_argument(
        "--model", default=DEFAULT_MODEL, help=f"Modelo Claude (default: {DEFAULT_MODEL})"
    )
    parser.add_argument(
        "--max-tokens", type=int, default=DEFAULT_MAX_TOKENS, help="Máximo de tokens en la respuesta"
    )
    parser.add_argument(
        "--output", type=Path, default=None, help="Archivo donde guardar el output"
    )

    args = parser.parse_args()

    variables: dict[str, str] = {}
    for var_str in args.var:
        if "=" not in var_str:
            print(f"[ERROR] Formato inválido para --var: '{var_str}'. Usa KEY=VALUE.", file=sys.stderr)
            sys.exit(1)
        key, _, value = var_str.partition("=")
        variables[key.strip()] = value

    if not args.prompt.exists():
        print(f"[ERROR] Archivo de prompt no encontrado: {args.prompt}", file=sys.stderr)
        sys.exit(1)

    result = run_prompt(
        prompt_path=args.prompt,
        variables=variables,
        model=args.model,
        max_tokens=args.max_tokens,
        output_path=args.output,
    )

    print(result)


if __name__ == "__main__":
    main()
