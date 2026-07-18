#!/usr/bin/env python3
"""Generate the website catalog and keep README inventory blocks synchronized."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE_CATALOG = ROOT / "site" / "data" / "catalog.json"
SITE_INDEX = ROOT / "site" / "index.html"

CATEGORIES = {
    "Manual workflow foundations": {
        "goal-contract",
        "grill-requirements",
    },
    "Product & experience": {
        "design-and-build-website",
        "design-product-interface",
        "conduct-user-research",
        "shape-product-opportunity",
        "define-brand-foundation",
        "design-product-content",
        "evolve-design-system",
        "audit-accessibility",
        "measure-product-experiments",
        "coordinate-data-views",
    },
    "Apple engineering": {
        "develop-apple-platform-app",
        "swift-api-design-guidelines",
        "swift-architecture",
        "swift-concurrency",
        "swift-testing-expert",
        "swiftui-ui-patterns",
        "swiftui-accessibility-auditor",
        "appkit-accessibility-auditor",
        "swiftui-performance-audit",
        "swiftdata-expert",
        "core-data-expert",
    },
    "Security & trust": {
        "map-attack-surface",
        "threat-model",
        "secure-coding",
        "input-sanitization",
        "identity-management",
        "secret-management",
        "vulnerability-hardening",
        "security-audit",
        "manage-vulnerability-risk",
        "assess-security-controls",
        "dependency-vuln-scan",
        "secret-scan",
        "automated-security-review",
    },
    "Cloudflare platform": {
        "agents-sdk",
        "cloudflare-email-service",
        "cloudflare-one",
        "durable-objects",
        "sandbox-sdk",
        "turnstile-spin",
        "workers-best-practices",
        "wrangler",
    },
    "Engineering & delivery": {
        "agents-md-init",
        "component-scaffold",
        "cobra-command",
        "prisma-migrate",
        "conventional-commit",
        "pr-description",
        "changelog",
        "gh-issue",
        "gh-pr",
        "gh-release",
        "develop-test-first",
        "debug-systematically",
        "simplify-code-safely",
        "test-browser-workflows",
    },
    "Research & communication": {
        "conduct-open-source-investigation",
        "market-research",
        "competitive-intel",
        "analytical-frameworks",
        "data-storytelling",
        "dataviz",
        "obsidian",
        "preserve-web-evidence",
        "retrieve-technical-docs",
    },
}

ORCHESTRATORS = {
    "design-and-build-website",
    "design-product-interface",
    "develop-apple-platform-app",
    "conduct-open-source-investigation",
    "map-attack-surface",
    "security-audit",
    "wrangler",
}

README_BLOCKS = {
    ROOT / "README.md": (
        "project-inventory",
        lambda skill_count, agent_count, category_count: (
            f"- **{skill_count}** portable skills across **{category_count}** capability groups\n"
            f"- **{agent_count}** independent reference subagents for research, review, and verification\n"
            "- **3** composable mechanisms: project context, on-demand skills, and isolated subagents"
        ),
    ),
    ROOT / "skills" / "README.md": (
        "skills-inventory",
        lambda skill_count, _agent_count, category_count: (
            f"**{skill_count} portable skills · {category_count} capability groups · one shared format.**"
        ),
    ),
    ROOT / "agents" / "README.md": (
        "agents-inventory",
        lambda _skill_count, agent_count, _category_count: (
            f"**{agent_count} reference subagents · research, review, verification, security, design, and accessibility.**"
        ),
    ),
}


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{path.relative_to(ROOT)} has no YAML frontmatter")
    try:
        raw = text.split("---", 2)[1]
    except IndexError as exc:
        raise ValueError(f"{path.relative_to(ROOT)} has incomplete frontmatter") from exc

    values: dict[str, str] = {}
    for line in raw.splitlines():
        if not line or line[0].isspace() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        values[key.strip()] = value
    return values


def category_for(name: str) -> str:
    matches = [category for category, names in CATEGORIES.items() if name in names]
    if len(matches) != 1:
        raise ValueError(f"skill {name!r} must belong to exactly one category; found {matches}")
    return matches[0]


def collect_skills() -> list[dict[str, str]]:
    skills: list[dict[str, str]] = []
    for path in sorted((ROOT / "skills").rglob("SKILL.md")):
        metadata = parse_frontmatter(path)
        name = metadata.get("name", "")
        description = metadata.get("description", "")
        if not name or not description:
            raise ValueError(f"{path.relative_to(ROOT)} needs name and description")
        if path.parent.name != name:
            raise ValueError(f"{path.relative_to(ROOT)} name does not match folder")
        skills.append(
            {
                "name": name,
                "description": description,
                "category": category_for(name),
                "kind": (
                    "foundation"
                    if category_for(name) == "Manual workflow foundations"
                    else "orchestrator"
                    if name in ORCHESTRATORS
                    else "specialist"
                ),
                "path": path.relative_to(ROOT).as_posix(),
            }
        )

    names = [skill["name"] for skill in skills]
    duplicates = sorted({name for name in names if names.count(name) > 1})
    if duplicates:
        raise ValueError(f"duplicate skill names: {', '.join(duplicates)}")
    return skills


def collect_agents() -> list[dict[str, str]]:
    agents: list[dict[str, str]] = []
    for path in sorted((ROOT / "agents").glob("*.md")):
        if path.name == "README.md":
            continue
        metadata = parse_frontmatter(path)
        agents.append(
            {
                "name": metadata["name"],
                "description": metadata["description"],
                "path": path.relative_to(ROOT).as_posix(),
            }
        )
    return agents


def render_catalog(skills: list[dict[str, str]], agents: list[dict[str, str]]) -> str:
    payload = {
        "repository": "K95M65/AI_ONBOARD",
        "counts": {
            "skills": len(skills),
            "agents": len(agents),
            "categories": len(CATEGORIES),
            "mechanisms": 3,
        },
        "categories": [
            {
                "name": category,
                "count": sum(skill["category"] == category for skill in skills),
            }
            for category in CATEGORIES
        ],
        "skills": skills,
        "agents": agents,
    }
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def replace_block(text: str, marker: str, content: str) -> str:
    start = f"<!-- generated:{marker}:start -->"
    end = f"<!-- generated:{marker}:end -->"
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    replacement = f"{start}\n{content}\n{end}"
    if not pattern.search(text):
        raise ValueError(f"missing generated block {marker!r}")
    return pattern.sub(replacement, text)


def sync_site_counts(text: str, skill_count: int) -> str:
    pattern = re.compile(r'(data-count="skills">)\d+(</)')
    updated, replacements = pattern.subn(rf"\g<1>{skill_count}\g<2>", text)
    if replacements == 0:
        raise ValueError("site/index.html has no static skill counts to synchronize")
    return updated


def expected_outputs(
    skills: list[dict[str, str]], agents: list[dict[str, str]]
) -> dict[Path, str]:
    outputs = {
        SITE_CATALOG: render_catalog(skills, agents),
        SITE_INDEX: sync_site_counts(
            SITE_INDEX.read_text(encoding="utf-8"), len(skills)
        ),
    }
    for path, (marker, renderer) in README_BLOCKS.items():
        outputs[path] = replace_block(
            path.read_text(encoding="utf-8"),
            marker,
            renderer(len(skills), len(agents), len(CATEGORIES)),
        )
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail when generated website data or README inventory blocks are stale.",
    )
    args = parser.parse_args()

    try:
        skills = collect_skills()
        agents = collect_agents()
        outputs = expected_outputs(skills, agents)
    except (KeyError, ValueError) as exc:
        print(f"sync error: {exc}", file=sys.stderr)
        return 1

    stale: list[Path] = []
    for path, expected in outputs.items():
        current = path.read_text(encoding="utf-8") if path.exists() else ""
        if current == expected:
            continue
        stale.append(path)
        if not args.check:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(expected, encoding="utf-8")

    if args.check and stale:
        print("generated documentation is stale:", file=sys.stderr)
        for path in stale:
            print(f"  - {path.relative_to(ROOT)}", file=sys.stderr)
        print("run: python3 scripts/sync_project_docs.py", file=sys.stderr)
        return 1

    verb = "checked" if args.check else "updated"
    print(
        f"{verb}: {len(skills)} skills, {len(agents)} agents, "
        f"{len(CATEGORIES)} capability groups"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
