#!/usr/bin/env python3
"""Validate portable skill structure, links, UI prompts, and obvious trigger duplication."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_PATTERN = re.compile(r"\[[^\]]*]\(([^)]+)\)")
STOP_WORDS = {
    "a",
    "an",
    "and",
    "for",
    "from",
    "in",
    "into",
    "it",
    "of",
    "on",
    "or",
    "the",
    "this",
    "to",
    "use",
    "using",
    "when",
    "with",
}


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing YAML frontmatter")
    parts = text.split("---", 2)
    if len(parts) != 3:
        raise ValueError("incomplete YAML frontmatter")

    values: dict[str, str] = {}
    for line in parts[1].splitlines():
        if not line or line[0].isspace() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        values[key.strip()] = value
    return values


def description_tokens(description: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", description.lower())) - STOP_WORDS


def validate_links(path: Path) -> list[str]:
    errors: list[str] = []
    for target in LINK_PATTERN.findall(path.read_text(encoding="utf-8")):
        target = target.strip()
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        relative = unquote(target.split("#", 1)[0])
        if relative and not (path.parent / relative).resolve().exists():
            errors.append(
                f"{path.relative_to(ROOT)}: broken local link {target!r}"
            )
    return errors


def main() -> int:
    errors: list[str] = []
    records: list[tuple[str, str, Path]] = []

    for path in sorted(SKILLS.rglob("SKILL.md")):
        try:
            metadata = parse_frontmatter(path)
        except ValueError as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")
            continue

        name = metadata.get("name", "")
        description = metadata.get("description", "")
        if not NAME_PATTERN.fullmatch(name):
            errors.append(f"{path.relative_to(ROOT)}: invalid skill name {name!r}")
        if path.parent.name != name:
            errors.append(
                f"{path.relative_to(ROOT)}: name {name!r} does not match folder"
            )
        if len(description) < 40:
            errors.append(f"{path.relative_to(ROOT)}: description is too short")
        if "TODO" in path.read_text(encoding="utf-8"):
            errors.append(f"{path.relative_to(ROOT)}: unresolved TODO")

        interface = path.parent / "agents" / "openai.yaml"
        if interface.is_file():
            interface_text = interface.read_text(encoding="utf-8")
            if f"${name}" not in interface_text:
                errors.append(
                    f"{interface.relative_to(ROOT)}: default prompt must mention ${name}"
                )

        records.append((name, description, path))

    names = [name for name, _description, _path in records]
    for name in sorted({name for name in names if names.count(name) > 1}):
        errors.append(f"duplicate skill name: {name}")

    descriptions: dict[str, list[str]] = {}
    for name, description, _path in records:
        descriptions.setdefault(description.casefold(), []).append(name)
    for duplicate_names in descriptions.values():
        if len(duplicate_names) > 1:
            errors.append(
                f"duplicate skill descriptions: {', '.join(sorted(duplicate_names))}"
            )

    for index, (left_name, left_description, _path) in enumerate(records):
        left = description_tokens(left_description)
        for right_name, right_description, _right_path in records[index + 1 :]:
            right = description_tokens(right_description)
            similarity = len(left & right) / len(left | right) if left | right else 0
            if similarity >= 0.72:
                errors.append(
                    "high lexical trigger overlap: "
                    f"{left_name} <> {right_name} ({similarity:.2f} token similarity)"
                )

    for path in sorted(SKILLS.rglob("*.md")):
        errors.extend(validate_links(path))

    if errors:
        print("skill validation failed:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    print(
        f"skill validation passed: {len(records)} unique skills, "
        "resolved links, UI prompts, and no high lexical trigger overlap"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
