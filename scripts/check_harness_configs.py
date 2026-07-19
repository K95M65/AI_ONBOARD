#!/usr/bin/env python3
"""Validate the portable project configurations for Claude Code, Codex, and OpenCode."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUAL_SKILLS = {"goal-contract", "grill-requirements"}


def load_json(path: Path, errors: list[str]) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{path}: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{path}: top-level value must be an object")
        return {}
    return value


def load_toml(path: Path, errors: list[str]) -> dict:
    try:
        value = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        errors.append(f"{path}: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{path}: top-level value must be a table")
        return {}
    return value


def validate_agents_md(errors: list[str]) -> None:
    path = ROOT / "AGENTS.md"
    text = path.read_text(encoding="utf-8")
    placeholders = (
        "[One or two sentences:",
        "[# the exact commands",
        "[npm install]",
        "[what lives here]",
    )
    for placeholder in placeholders:
        if placeholder in text:
            errors.append(f"AGENTS.md: unresolved template placeholder {placeholder!r}")
    for required in (
        "scripts/check_harness_configs.py",
        "scripts/check_skills.py",
        "scripts/check_site.py",
        "scripts/ai_onboard.py --target . check-git",
    ):
        if required not in text:
            errors.append(f"AGENTS.md: missing required check {required!r}")


def validate_claude(path: Path, errors: list[str]) -> None:
    data = load_json(path, errors)
    overrides = data.get("skillOverrides", {})
    for name in MANUAL_SKILLS:
        if overrides.get(name) != "user-invocable-only":
            errors.append(
                f"{path}: {name} must be user-invocable-only for Claude Code"
            )
    denies = set(data.get("permissions", {}).get("deny", []))
    for rule in {"Read(./.env)", "Read(./.env.*)", "Read(./secrets/**)"}:
        if rule not in denies:
            errors.append(f"{path}: missing secret-protection rule {rule!r}")


def validate_codex(path: Path, errors: list[str]) -> None:
    data = load_toml(path, errors)
    personal_keys = {
        "approval_policy",
        "model",
        "model_provider",
        "notify",
        "openai_base_url",
        "otel",
        "profile",
        "sandbox_mode",
        "service_tier",
    }
    for key in sorted(personal_keys & data.keys()):
        errors.append(
            f"{path}: personal setting {key!r} belongs in user or profile config"
        )
    agents = data.get("agents", {})
    max_threads = agents.get("max_threads")
    max_depth = agents.get("max_depth")
    if not isinstance(max_threads, int) or not 1 <= max_threads <= 8:
        errors.append(f"{path}: agents.max_threads must be an integer from 1 to 8")
    if max_depth != 1:
        errors.append(f"{path}: agents.max_depth must remain 1 for bounded delegation")


def validate_opencode(path: Path, errors: list[str]) -> None:
    data = load_json(path, errors)
    if data.get("$schema") != "https://opencode.ai/config.json":
        errors.append(f"{path}: missing current OpenCode schema URL")
    for key in ("model", "small_model", "provider"):
        if key in data:
            errors.append(
                f"{path}: provider-specific setting {key!r} must remain user-level"
            )
    permission = data.get("permission", {})
    if permission.get("edit") != "ask":
        errors.append(f"{path}: edit permission must be 'ask'")
    if permission.get("external_directory") != "deny":
        errors.append(f"{path}: external_directory permission must be 'deny'")
    skill_permissions = permission.get("skill", {})
    for name in MANUAL_SKILLS:
        if skill_permissions.get(name) != "ask":
            errors.append(f"{path}: {name} skill permission must be 'ask'")
    compaction = data.get("compaction", {})
    if compaction.get("auto") is not True or compaction.get("prune") is not True:
        errors.append(f"{path}: compaction auto and prune must both be true")
    reserved = compaction.get("reserved")
    if not isinstance(reserved, int) or reserved < 8000:
        errors.append(f"{path}: compaction.reserved must be at least 8000")
    ignored = set(data.get("watcher", {}).get("ignore", []))
    for pattern in {".git/**", "node_modules/**", "output/**"}:
        if pattern not in ignored:
            errors.append(f"{path}: watcher.ignore is missing {pattern!r}")


def validate_paths_and_docs(errors: list[str]) -> None:
    if any((ROOT / ".opencode" / "agent").glob("*.md")):
        errors.append(".opencode/agent is legacy; use .opencode/agents")
    expected_agents = {
        "accessibility-review.md",
        "design-review.md",
        "researcher.md",
        "reviewer.md",
        "security-review.md",
        "verifier.md",
    }
    actual_agents = {
        path.name for path in (ROOT / ".opencode" / "agents").glob("*.md")
    }
    missing_agents = sorted(expected_agents - actual_agents)
    if missing_agents:
        errors.append(f".opencode/agents: missing {', '.join(missing_agents)}")

    for harness in ("claude", "opencode"):
        template = (
            ROOT
            / "templates"
            / "commands"
            / harness
            / "ai-onboard-update.md"
        )
        realized = (
            ROOT / f".{harness}" / "commands" / "ai-onboard-update.md"
        )
        if not template.is_file() or not realized.is_file():
            errors.append(
                f"{harness}: update-check command template and realization are required"
            )
        elif template.read_bytes() != realized.read_bytes():
            errors.append(
                f"{harness}: update-check command must match its canonical template"
            )
    for required_path in (
        ROOT
        / "templates"
        / "commands"
        / "codex"
        / "ai-onboard-update.md",
        ROOT
        / "templates"
        / "notifications"
        / "github"
        / "ai-onboard-update-check.yml",
        ROOT / "scripts" / "install_macos_update_notifier.py",
    ):
        if not required_path.is_file():
            errors.append(f"{required_path}: required notification asset is missing")
    hooks = {
        "pre-commit": "--identity-only",
        "pre-merge-commit": "--identity-only",
        "pre-applypatch": "--identity-only",
        "pre-push": "--pre-push",
    }
    for hook_name, required_scope in hooks.items():
        hook_path = ROOT / ".githooks" / hook_name
        if not hook_path.is_file():
            errors.append(f"{hook_path}: required Git identity hook is missing")
            continue
        if not os.access(hook_path, os.X_OK):
            errors.append(f"{hook_path}: Git hook must be executable")
        hook = hook_path.read_text(encoding="utf-8")
        for required in ("check-git", required_scope):
            if required not in hook:
                errors.append(
                    f"{hook_path}: Git hook is missing {required!r}"
                )

    workflow_path = (
        ROOT
        / "templates"
        / "notifications"
        / "github"
        / "ai-onboard-update-check.yml"
    )
    if workflow_path.is_file():
        workflow = workflow_path.read_text(encoding="utf-8")
        for forbidden in ("uses:", "actions/checkout", "subprocess"):
            if forbidden in workflow:
                errors.append(
                    f"{workflow_path}: scheduled checker must not contain "
                    f"{forbidden!r}"
                )
        for required in (
            "api.github.com",
            'source.get("repository"',
            'source.get("channel"',
            "VERSION_PATTERN",
            "RELEASE_CLASSIFICATIONS",
        ):
            if required not in workflow:
                errors.append(
                    f"{workflow_path}: scheduled checker is missing "
                    f"{required!r}"
                )

    lint_workflow_path = ROOT / ".github" / "workflows" / "lint.yml"
    if not lint_workflow_path.is_file():
        errors.append(f"{lint_workflow_path}: required CI workflow is missing")
    else:
        lint_workflow = lint_workflow_path.read_text(encoding="utf-8")
        active_workflow = "\n".join(
            line
            for line in lint_workflow.splitlines()
            if not line.lstrip().startswith("#")
        )
        active_lines = active_workflow.splitlines()
        try:
            on_start = active_lines.index("on:")
        except ValueError:
            on_block: list[str] = []
        else:
            on_end = next(
                (
                    index
                    for index in range(on_start + 1, len(active_lines))
                    if active_lines[index].strip()
                    and not active_lines[index].startswith(" ")
                ),
                len(active_lines),
            )
            on_block = active_lines[on_start + 1 : on_end]
        for trigger in ("push", "pull_request"):
            header = f"  {trigger}:"
            try:
                trigger_start = on_block.index(header)
            except ValueError:
                errors.append(
                    f"{lint_workflow_path}: deployment checks must run on "
                    f"every {trigger.replace('_', ' ')}"
                )
                continue
            trigger_end = next(
                (
                    index
                    for index in range(trigger_start + 1, len(on_block))
                    if on_block[index].strip()
                    and len(on_block[index]) - len(on_block[index].lstrip()) <= 2
                ),
                len(on_block),
            )
            if any(
                line.strip()
                for line in on_block[trigger_start + 1 : trigger_end]
            ):
                errors.append(
                    f"{lint_workflow_path}: {trigger} must not have branch, "
                    "path, or event filters"
                )
        if not on_block:
            errors.append(
                f"{lint_workflow_path}: deployment checks must run on every "
                "push and pull request"
            )
        deploy_job = re.search(
            r"(?ms)^  deploy-smoke:\s*\n"
            r"(?P<body>.*?)(?=^  [a-zA-Z0-9_-]+:\s*\n|\Z)",
            active_workflow,
        )
        if not deploy_job:
            errors.append(
                f"{lint_workflow_path}: deploy-smoke job is missing"
            )
            deploy_job_body = ""
        else:
            deploy_job_body = deploy_job.group("body")
        for required in (
            "harness: [claude, codex, opencode]",
            'scripts/test_deployments.py --harness "${{ matrix.harness }}"',
        ):
            if required not in deploy_job_body:
                errors.append(
                    f"{lint_workflow_path}: deployment matrix is missing "
                    f"{required!r}"
                )
        for forbidden in ("if:", "continue-on-error:", "exclude:", "needs:"):
            if any(
                line.strip().startswith(forbidden)
                for line in deploy_job_body.splitlines()
            ):
                errors.append(
                    f"{lint_workflow_path}: deploy-smoke must not contain "
                    f"{forbidden!r}"
                )
        git_identity_job = re.search(
            r"(?ms)^  git-identity:\s*\n"
            r"(?P<body>.*?)(?=^  [a-zA-Z0-9_-]+:\s*\n|\Z)",
            active_workflow,
        )
        if not git_identity_job:
            errors.append(
                f"{lint_workflow_path}: git-identity job is missing"
            )
        else:
            git_identity_body = git_identity_job.group("body")
            for required in (
                "fetch-depth: 0",
                "check-git --history-only",
            ):
                if required not in git_identity_body:
                    errors.append(
                        f"{lint_workflow_path}: git-identity job is missing "
                        f"{required!r}"
                    )

    docs = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (
            ROOT / "docs" / "setup" / "claude-code.md",
            ROOT / "docs" / "setup" / "codex.md",
            ROOT / "docs" / "setup" / "opencode.md",
            ROOT / "agents" / "README.md",
            ROOT / "agents" / "opencode" / "README.md",
        )
    )
    stale_phrases = {
        ".opencode/agent/": "use .opencode/agents/",
        "repo's [34 skills]": "use the generated current inventory",
        "CLAUDE.local.md` is deprecated": "Claude Code still supports local memory",
        'model = "gpt-5-codex"': "use current model guidance or omit personal models",
    }
    for phrase, remedy in stale_phrases.items():
        if phrase in docs:
            errors.append(f"setup docs: stale phrase {phrase!r}; {remedy}")


def validate_package_manifest(errors: list[str]) -> None:
    path = ROOT / "package-manifest.json"
    data = load_json(path, errors)
    if data.get("schema") != 1:
        errors.append(f"{path}: schema must be 1")
    if data.get("package") != "ai-onboard":
        errors.append(f"{path}: package must be 'ai-onboard'")
    if not re.fullmatch(r"\d+\.\d+\.\d+", str(data.get("version", ""))):
        errors.append(f"{path}: version must be semantic major.minor.patch")
    if data.get("default_channel") not in {"stable", "edge"}:
        errors.append(f"{path}: default_channel must be stable or edge")
    release = data.get("release", {})
    if release.get("classification") not in {
        "fix",
        "security",
        "feature",
        "maintenance",
    }:
        errors.append(f"{path}: release classification is invalid")
    if not str(release.get("summary", "")).strip():
        errors.append(f"{path}: release summary is required")
    if not str(release.get("notes_url", "")).startswith("https://"):
        errors.append(f"{path}: release notes URL must use HTTPS")

    catalog = load_json(ROOT / "site" / "data" / "catalog.json", errors)
    categories = {
        category.get("name") for category in catalog.get("categories", [])
    }
    profiles = data.get("profiles", {})
    if "core" not in profiles:
        errors.append(f"{path}: a core profile is required")
    claimed: set[str] = set()
    for name, profile in profiles.items():
        if not re.fullmatch(r"[a-z][a-z0-9-]*", name):
            errors.append(f"{path}: invalid profile name {name!r}")
        unknown = set(profile.get("categories", [])) - categories
        if unknown:
            errors.append(
                f"{path}: profile {name!r} has unknown categories {sorted(unknown)}"
            )
        claimed.update(profile.get("categories", []))
    required = categories - {"Manual workflow foundations"}
    missing = required - claimed
    if missing:
        errors.append(f"{path}: profiles do not cover categories {sorted(missing)}")

    for required_path in (
        ROOT / "scripts" / "ai_onboard.py",
        ROOT / "scripts" / "test_deployments.py",
        ROOT / "tests" / "test_ai_onboard.py",
        ROOT / "tests" / "test_deployments.py",
    ):
        if not required_path.is_file():
            errors.append(f"{required_path}: required lifecycle file is missing")


def user_config_warnings() -> list[str]:
    warnings: list[str] = []
    home = Path.home()

    claude_path = home / ".claude" / "settings.json"
    if claude_path.is_file():
        data = load_json(claude_path, warnings)
        model = data.get("model")
        if isinstance(model, str) and (
            "\x1b" in model or re.search(r"\[\d+(?:;\d+)*m\]?$", model)
        ):
            warnings.append(f"{claude_path}: model value contains terminal formatting")

    codex_path = home / ".codex" / "config.toml"
    if codex_path.is_file():
        data = load_toml(codex_path, warnings)
        features = data.get("features", {})
        for key in ("codex_hooks", "js_repl"):
            if key in features:
                warnings.append(f"{codex_path}: remove obsolete feature key {key!r}")

    return warnings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--include-user",
        action="store_true",
        help="Also report safe diagnostics for user-level harness configuration.",
    )
    args = parser.parse_args()

    errors: list[str] = []
    validate_agents_md(errors)
    validate_claude(ROOT / ".claude" / "settings.json", errors)
    validate_claude(ROOT / "templates" / "configs" / "claude.settings.json", errors)
    validate_codex(ROOT / ".codex" / "config.toml", errors)
    validate_codex(ROOT / "templates" / "configs" / "codex.config.toml", errors)
    validate_opencode(ROOT / "opencode.json", errors)
    validate_opencode(ROOT / "templates" / "configs" / "opencode.json", errors)
    validate_paths_and_docs(errors)
    validate_package_manifest(errors)

    if errors:
        print("harness configuration validation failed:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    print("harness configuration validation passed: Claude, Codex, and OpenCode")

    if args.include_user:
        warnings = user_config_warnings()
        if warnings:
            print("user configuration warnings:")
            for warning in warnings:
                print(f"  - {warning}")
        else:
            print("user configuration diagnostics passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
