#!/usr/bin/env python3
"""Validate the static site artifact without adding a build dependency."""

from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
SITE_BASE_PATH = "/AI_ONBOARD/"
REQUIRED_IDS = {"main", "problem", "lifecycle", "router", "catalog", "result"}


class SiteParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.references: list[str] = []
        self.errors: list[str] = []
        self._title_depth = 0
        self.title = ""

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        values = dict(attrs)
        element_id = values.get("id")
        if element_id:
            if element_id in self.ids:
                self.errors.append(f"duplicate id {element_id!r}")
            self.ids.add(element_id)
        for attr in ("href", "src"):
            if values.get(attr):
                self.references.append(values[attr] or "")
        if tag == "title":
            self._title_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._title_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._title_depth:
            self.title += data


def local_target(source: Path, reference: str) -> Path | None:
    parsed = urlsplit(reference)
    if parsed.scheme or parsed.netloc or reference.startswith(("mailto:", "tel:", "#")):
        return None
    path = unquote(parsed.path)
    if not path:
        return source
    if path == SITE_BASE_PATH.rstrip("/"):
        path = SITE_BASE_PATH
    if path.startswith(SITE_BASE_PATH):
        return SITE / path.removeprefix(SITE_BASE_PATH)
    if path.startswith("/"):
        return SITE / path.removeprefix("/")
    return source.parent / path


def validate_html(path: Path) -> list[str]:
    parser = SiteParser()
    parser.feed(path.read_text(encoding="utf-8"))
    errors = [f"{path.relative_to(ROOT)}: {error}" for error in parser.errors]
    if path.name == "index.html":
        missing = REQUIRED_IDS - parser.ids
        if missing:
            errors.append(f"site/index.html: missing required ids: {sorted(missing)}")
        if not parser.title.strip():
            errors.append("site/index.html: missing document title")

    for reference in parser.references:
        target = local_target(path, reference)
        if target is None:
            continue
        target = target.resolve()
        if target.is_dir():
            target /= "index.html"
        if not target.exists():
            errors.append(
                f"{path.relative_to(ROOT)}: broken local reference {reference!r}"
            )
    return errors


def validate_catalog() -> list[str]:
    path = SITE / "data" / "catalog.json"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"site/data/catalog.json: {exc}"]

    errors: list[str] = []
    skills = payload.get("skills", [])
    agents = payload.get("agents", [])
    categories = payload.get("categories", [])
    counts = payload.get("counts", {})
    expected = {
        "skills": len(skills),
        "agents": len(agents),
        "categories": len(categories),
        "mechanisms": 3,
    }
    for key, value in expected.items():
        if counts.get(key) != value:
            errors.append(
                f"site/data/catalog.json: count {key!r} is {counts.get(key)!r}, "
                f"expected {value}"
            )

    names = [skill.get("name") for skill in skills]
    duplicates = sorted({name for name in names if names.count(name) > 1})
    if duplicates:
        errors.append(f"site/data/catalog.json: duplicate skills: {duplicates}")

    category_names = {category.get("name") for category in categories}
    for skill in skills:
        if skill.get("category") not in category_names:
            errors.append(
                f"site/data/catalog.json: {skill.get('name')!r} has unknown category"
            )
        source = ROOT / str(skill.get("path", ""))
        if not source.is_file():
            errors.append(
                f"site/data/catalog.json: missing source for {skill.get('name')!r}"
            )

    return errors


def validate_route_skills() -> list[str]:
    """Catch route labels that look like skill names but do not exist."""
    catalog = json.loads((SITE / "data" / "catalog.json").read_text(encoding="utf-8"))
    skill_names = {skill["name"] for skill in catalog["skills"]}
    agent_names = {agent["name"] for agent in catalog["agents"]}
    allowed = {
        "AGENTS.md",
        "project instructions",
        "brand evidence",
        "release boundary",
        "existing system",
        "user evidence",
        "Xcode project",
        "deployment targets",
        "data flows",
        "deployment model",
        "wrangler config",
        "Cloudflare resources",
        "decision owner",
        "scope",
        "rules of engagement",
        "source quality",
        "public-source boundary",
        "legitimate purpose",
        "stopping condition",
        "git diff",
        "test commands",
        "responsive",
        "keyboard",
        "links",
        "runtime",
        "task scenarios",
        "state coverage",
        "instrumentation",
        "Swift Testing",
        "official Apple source",
        "closest sample",
        "adaptation record",
        "keyboard/VoiceOver",
        "performance",
        "dependency scan",
        "secret scan",
        "regression tests",
        "asset ledger",
        "retest evidence",
        "monitoring plan",
        "wrangler checks",
        "smoke test",
        "observability",
        "citations",
        "assumptions",
        "decision criteria",
        "evidence ledger",
        "source provenance",
        "contradiction and gaps",
        "tests",
        "diff review",
        "PR checks",
        "release notes",
    }
    text = (SITE / "app.js").read_text(encoding="utf-8")
    items = re.findall(r'items:\s*\[([^\]]+)\]', text)
    labels = {
        match
        for item in items
        for match in re.findall(r'"([^"]+)"', item)
    }
    unknown = sorted(labels - skill_names - agent_names - allowed)
    if unknown:
        return [f"site/app.js: unknown route items: {', '.join(unknown)}"]
    return []


def validate_harness_support() -> list[str]:
    text = (SITE / "index.html").read_text(encoding="utf-8")
    missing = [
        harness for harness in ("Codex", "Claude Code", "OpenCode")
        if harness not in text
    ]
    if missing:
        return [
            "site/index.html: missing first-class harness support: "
            + ", ".join(missing)
        ]
    return []


def validate_managed_lifecycle() -> list[str]:
    text = (SITE / "index.html").read_text(encoding="utf-8")
    app = (SITE / "app.js").read_text(encoding="utf-8")
    required_copy = (
        "ai-onboard.json",
        ".ai-onboard.lock.json",
        "upgrade --check",
        "uninstall --dry-run",
    )
    missing = [value for value in required_copy if value not in text]
    if "scripts/ai_onboard.py" not in app or "--profile core" not in app:
        missing.append("managed quickstart")
    if "--global install" not in app or "--profile apple" not in app:
        missing.append("global Apple quickstart")
    if missing:
        return [
            "site: missing managed lifecycle explanation: " + ", ".join(missing)
        ]
    return []


def main() -> int:
    errors: list[str] = []
    for path in (SITE / "index.html", SITE / "404.html"):
        errors.extend(validate_html(path))
    errors.extend(validate_catalog())
    errors.extend(validate_route_skills())
    errors.extend(validate_harness_support())
    errors.extend(validate_managed_lifecycle())

    if errors:
        print("site validation failed:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    print("site validation passed: HTML references, catalog, counts, and routes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
