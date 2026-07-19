#!/usr/bin/env python3
"""Smoke-test full managed deployments for each supported AI harness."""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path
from typing import Any, Iterator


ROOT = Path(__file__).resolve().parents[1]
MANAGER = ROOT / "scripts" / "ai_onboard.py"
MANIFEST = ROOT / "package-manifest.json"
CATALOG = ROOT / "site" / "data" / "catalog.json"
SUPPORTED_HARNESSES = ("claude", "codex", "opencode")
AGENTS_SENTINEL = "# Deployment smoke-test project\n"
NOREPLY_EMAIL = "41898282+github-actions[bot]@users.noreply.github.com"
PACKAGE_SOURCE_PATHS = (
    "package-manifest.json",
    "site/data/catalog.json",
    "scripts/ai_onboard.py",
    "scripts/install_macos_update_notifier.py",
    "templates/configs",
    "templates/commands",
    "templates/notifications",
    "agents",
    "skills",
)


class DeploymentFailure(RuntimeError):
    """A deployment did not satisfy the smoke-test contract."""


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise DeploymentFailure(f"cannot read JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise DeploymentFailure(f"{path} must contain a JSON object")
    return value


def run_command(
    arguments: list[str],
    *,
    environment: dict[str, str],
    verbose: bool,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        arguments,
        cwd=ROOT,
        env=environment,
        text=True,
        capture_output=True,
        check=False,
    )
    if verbose:
        print(f"$ {' '.join(arguments)}")
        if result.stdout:
            print(result.stdout, end="")
        if result.stderr:
            print(result.stderr, end="", file=sys.stderr)
    if result.returncode:
        raise DeploymentFailure(
            f"command failed with exit {result.returncode}: "
            f"{' '.join(arguments)}\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )
    return result


def deployment_environment(home: Path) -> dict[str, str]:
    home.mkdir()
    environment = os.environ.copy()
    environment.update(
        {
            "HOME": str(home),
            "XDG_CACHE_HOME": str(home / ".cache"),
            "XDG_CONFIG_HOME": str(home / ".config"),
            "XDG_DATA_HOME": str(home / ".local" / "share"),
            "XDG_STATE_HOME": str(home / ".local" / "state"),
            "GIT_AUTHOR_NAME": "AI_ONBOARD deployment test",
            "GIT_AUTHOR_EMAIL": NOREPLY_EMAIL,
            "GIT_COMMITTER_NAME": "AI_ONBOARD deployment test",
            "GIT_COMMITTER_EMAIL": NOREPLY_EMAIL,
        }
    )
    return environment


@contextlib.contextmanager
def deployment_source() -> Iterator[Path]:
    """Snapshot current package content so dirty changes remain testable."""
    with tempfile.TemporaryDirectory(
        prefix="ai-onboard-package-source-"
    ) as temporary:
        snapshot = Path(temporary) / "source"
        snapshot.mkdir()
        for relative in PACKAGE_SOURCE_PATHS:
            source = ROOT / relative
            destination = snapshot / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            if source.is_dir():
                shutil.copytree(source, destination, symlinks=True)
            else:
                shutil.copy2(source, destination)
        environment = os.environ.copy()
        environment.update(
            {
                "GIT_AUTHOR_NAME": "AI_ONBOARD package snapshot",
                "GIT_AUTHOR_EMAIL": NOREPLY_EMAIL,
                "GIT_COMMITTER_NAME": "AI_ONBOARD package snapshot",
                "GIT_COMMITTER_EMAIL": NOREPLY_EMAIL,
            }
        )
        try:
            for arguments in (
                ("init", "-q", "-b", "main"),
                ("config", "commit.gpgsign", "false"),
                ("add", "."),
                ("commit", "-q", "-m", "snapshot package under test"),
            ):
                subprocess.run(
                    ["git", "-C", str(snapshot), *arguments],
                    env=environment,
                    check=True,
                    capture_output=True,
                    text=True,
                )
        except (OSError, subprocess.CalledProcessError) as exc:
            raise DeploymentFailure(
                "cannot create clean Git snapshot for deployment tests"
            ) from exc
        yield snapshot


def require_file(path: Path) -> None:
    if not path.is_file():
        raise DeploymentFailure(f"expected file is missing: {path}")


def require_absent(path: Path) -> None:
    if path.exists() or path.is_symlink():
        raise DeploymentFailure(f"expected path to be absent: {path}")


def require_empty_or_absent(path: Path) -> None:
    if not path.exists():
        return
    if not path.is_dir() or any(path.iterdir()):
        raise DeploymentFailure(f"expected directory to be empty or absent: {path}")


def snapshot_tree(root: Path) -> dict[str, tuple[str, int, str]]:
    snapshot: dict[str, tuple[str, int, str]] = {}
    for current, directories, files in os.walk(root, followlinks=False):
        directories.sort()
        files.sort()
        for name in [*directories, *files]:
            path = Path(current) / name
            relative = path.relative_to(root).as_posix()
            metadata = os.lstat(path)
            mode = stat.S_IMODE(metadata.st_mode)
            if stat.S_ISLNK(metadata.st_mode):
                snapshot[relative] = ("symlink", mode, os.readlink(path))
            elif stat.S_ISDIR(metadata.st_mode):
                snapshot[relative] = ("directory", mode, "")
            elif stat.S_ISREG(metadata.st_mode):
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
                snapshot[relative] = ("file", mode, digest)
            else:
                snapshot[relative] = ("other", mode, "")
    return snapshot


def assert_equal(actual: object, expected: object, label: str) -> None:
    if actual != expected:
        raise DeploymentFailure(
            f"{label} mismatch: expected {expected!r}, got {actual!r}"
        )


def expected_skill_names() -> set[str]:
    catalog = read_json(CATALOG)
    names = {
        str(skill.get("name", ""))
        for skill in catalog.get("skills", [])
        if isinstance(skill, dict)
    }
    if not names or "" in names:
        raise DeploymentFailure("catalog contains an invalid skill name")
    return names


def expected_agent_names(harness: str) -> set[str]:
    if harness == "claude":
        paths = (ROOT / "agents").glob("*.md")
        return {path.name for path in paths if path.name != "README.md"}
    if harness == "codex":
        return {
            path.name for path in (ROOT / "agents" / "codex").glob("*.toml")
        }
    return {
        path.name
        for path in (ROOT / "agents" / "opencode").glob("*.md")
        if path.name != "README.md"
    }


def seed_user_config(target: Path, harness: str) -> Path:
    if harness == "claude":
        path = target / ".claude" / "settings.json"
        path.parent.mkdir(parents=True)
        path.write_text(
            json.dumps({"user": {"preserved": True}}, indent=2) + "\n",
            encoding="utf-8",
        )
        return path
    if harness == "codex":
        path = target / ".codex" / "config.toml"
        path.parent.mkdir(parents=True)
        path.write_text("[user]\npreserved = true\n", encoding="utf-8")
        return path
    path = target / "opencode.json"
    path.write_text(
        json.dumps({"user": {"preserved": True}}, indent=2) + "\n",
        encoding="utf-8",
    )
    return path


def load_harness_config(path: Path, harness: str) -> dict[str, Any]:
    if harness == "codex":
        return tomllib.loads(path.read_text(encoding="utf-8"))
    return read_json(path)


def expected_installed_config(harness: str) -> dict[str, Any]:
    if harness == "claude":
        template = read_json(
            ROOT / "templates" / "configs" / "claude.settings.json"
        )
    elif harness == "codex":
        template = tomllib.loads(
            (ROOT / "templates" / "configs" / "codex.config.toml").read_text(
                encoding="utf-8"
            )
        )
    else:
        template = read_json(ROOT / "templates" / "configs" / "opencode.json")
    return {"user": {"preserved": True}, **template}


def prune_empty_mappings(value: Any) -> Any:
    if not isinstance(value, dict):
        return value
    result = {
        key: prune_empty_mappings(child)
        for key, child in value.items()
    }
    return {
        key: child
        for key, child in result.items()
        if child != {}
    }


def verify_user_config(path: Path, harness: str, *, installed: bool) -> None:
    require_file(path)
    data = load_harness_config(path, harness)
    if installed:
        expected = expected_installed_config(harness)
    else:
        data = prune_empty_mappings(data)
        expected = {"user": {"preserved": True}}
    assert_equal(
        data,
        expected,
        (
            f"{harness} merged config"
            if installed
            else f"{harness} config cleanup"
        ),
    )


def installed_paths(
    target: Path,
    harness: str,
) -> tuple[Path, Path, Path]:
    if harness == "claude":
        return (
            target / ".claude" / "skills",
            target / ".claude" / "agents",
            target / ".claude" / "commands" / "ai-onboard-update.md",
        )
    if harness == "codex":
        return (
            target / ".agents" / "skills",
            target / ".codex" / "agents",
            target
            / ".ai-onboard"
            / "share"
            / "codex-prompts"
            / "ai-onboard-update.md",
        )
    return (
        target / ".agents" / "skills",
        target / ".opencode" / "agents",
        target / ".opencode" / "commands" / "ai-onboard-update.md",
    )


def global_installed_paths(
    home: Path,
    harness: str,
) -> tuple[Path, Path]:
    if harness == "claude":
        return (
            home / ".claude" / "skills",
            home / ".claude" / "agents",
        )
    if harness == "codex":
        return (
            home / ".agents" / "skills",
            home / ".codex" / "agents",
        )
    return (
        home / ".agents" / "skills",
        home / ".config" / "opencode" / "agents",
    )


def verify_installed_layout(
    target: Path,
    harness: str,
    profiles: list[str],
    package_version: str,
) -> tuple[int, int]:
    require_file(target / "ai-onboard.json")
    require_file(target / ".ai-onboard.lock.json")
    require_file(target / ".ai-onboard/bin/ai_onboard.py")
    require_file(target / ".ai-onboard/bin/install_macos_update_notifier.py")
    require_file(target / ".github/workflows/ai-onboard-update-check.yml")

    desired = read_json(target / "ai-onboard.json")
    lock = read_json(target / ".ai-onboard.lock.json")
    assert_equal(desired.get("harnesses"), [harness], "desired harnesses")
    assert_equal(desired.get("profiles"), profiles, "desired profiles")
    assert_equal(
        desired.get("features"),
        {
            "agents": True,
            "configs": True,
            "notifications": True,
            "workflow_foundations": True,
        },
        "desired features",
    )
    assert_equal(lock.get("package_version"), package_version, "locked version")
    if not re.fullmatch(r"[0-9a-f]{40}", str(lock.get("source_revision", ""))):
        raise DeploymentFailure("lockfile has no immutable Git source revision")

    skills_root, agents_root, command_path = installed_paths(target, harness)
    actual_skills = {
        path.name
        for path in skills_root.iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    }
    expected_skills = expected_skill_names()
    assert_equal(actual_skills, expected_skills, f"{harness} installed skills")

    actual_agents = {
        path.name for path in agents_root.iterdir() if path.is_file()
    }
    expected_agents = expected_agent_names(harness)
    assert_equal(actual_agents, expected_agents, f"{harness} installed agents")
    require_file(command_path)

    if harness != "claude":
        require_absent(target / ".claude" / "skills")
    if harness != "codex":
        require_absent(target / ".codex" / "agents")
    if harness != "opencode":
        require_absent(target / ".opencode" / "agents")

    return len(actual_skills), len(actual_agents)


def verify_global_installed_layout(
    home: Path,
    harness: str,
    profiles: list[str],
    package_version: str,
) -> tuple[int, int]:
    desired_path = home / ".ai-onboard/ai-onboard.json"
    lock_path = home / ".ai-onboard/ai-onboard.lock.json"
    launcher = home / ".local/bin/ai-onboard"
    require_file(desired_path)
    require_file(lock_path)
    require_file(launcher)
    if not os.access(launcher, os.X_OK):
        raise DeploymentFailure("global launcher is not executable")
    require_absent(home / "ai-onboard.json")
    require_absent(home / ".ai-onboard.lock.json")

    desired = read_json(desired_path)
    lock = read_json(lock_path)
    assert_equal(desired.get("scope"), "global", "global desired scope")
    assert_equal(desired.get("harnesses"), [harness], "global harnesses")
    assert_equal(desired.get("profiles"), profiles, "global profiles")
    assert_equal(
        desired.get("features"),
        {
            "agents": True,
            "configs": False,
            "notifications": False,
            "workflow_foundations": True,
        },
        "global desired features",
    )
    assert_equal(
        lock.get("package_version"),
        package_version,
        "global locked version",
    )

    skills_root, agents_root = global_installed_paths(home, harness)
    actual_skills = {
        path.name
        for path in skills_root.iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    }
    actual_agents = {
        path.name for path in agents_root.iterdir() if path.is_file()
    }
    assert_equal(
        actual_skills,
        expected_skill_names(),
        f"{harness} global skills",
    )
    assert_equal(
        actual_agents,
        expected_agent_names(harness),
        f"{harness} global agents",
    )
    return len(actual_skills), len(actual_agents)


def verify_lifecycle(
    target: Path,
    *,
    source: Path,
    environment: dict[str, str],
    verbose: bool,
) -> None:
    manager = target / ".ai-onboard/bin/ai_onboard.py"
    prefix = [
        sys.executable,
        str(manager),
        "--source",
        str(source),
        "--target",
        str(target),
    ]
    git_check = run_command(
        [*prefix, "check-git"],
        environment=environment,
        verbose=verbose,
    )
    if "Git process identity passed" not in git_check.stdout:
        raise DeploymentFailure(
            f"unexpected Git identity output:\n{git_check.stdout}"
        )
    if "Git history passed" not in git_check.stdout:
        raise DeploymentFailure(
            f"unexpected Git history output:\n{git_check.stdout}"
        )

    status = run_command(
        [*prefix, "status"],
        environment=environment,
        verbose=verbose,
    )
    if "0 drifted managed item(s)" not in status.stdout:
        raise DeploymentFailure(f"unexpected status output:\n{status.stdout}")

    doctor = run_command(
        [*prefix, "doctor"],
        environment=environment,
        verbose=verbose,
    )
    if "Doctor passed" not in doctor.stdout:
        raise DeploymentFailure(f"unexpected doctor output:\n{doctor.stdout}")

    update = run_command(
        [*prefix, "upgrade", "--check", "--json"],
        environment=environment,
        verbose=verbose,
    )
    try:
        update_status = json.loads(update.stdout)
    except json.JSONDecodeError as exc:
        raise DeploymentFailure(
            f"update check did not emit JSON: {update.stdout}"
        ) from exc
    assert_equal(
        update_status.get("update_available"),
        False,
        "local-source update availability",
    )
    assert_equal(
        update_status.get("current"),
        update_status.get("latest"),
        "current/latest deployment state",
    )

    before_sync_preview = snapshot_tree(target)
    run_command(
        [*prefix, "sync", "--dry-run"],
        environment=environment,
        verbose=verbose,
    )
    assert_equal(
        snapshot_tree(target),
        before_sync_preview,
        "sync dry-run project snapshot",
    )

    before_uninstall_preview = snapshot_tree(target)
    run_command(
        [*prefix, "uninstall", "--dry-run"],
        environment=environment,
        verbose=verbose,
    )
    assert_equal(
        snapshot_tree(target),
        before_uninstall_preview,
        "uninstall dry-run project snapshot",
    )
    require_file(manager)


def verify_global_lifecycle(
    home: Path,
    *,
    source: Path,
    environment: dict[str, str],
    verbose: bool,
) -> None:
    launcher = home / ".local/bin/ai-onboard"
    prefix = [str(launcher), "--source", str(source)]

    status = run_command(
        [*prefix, "status"],
        environment=environment,
        verbose=verbose,
    )
    if "0 drifted managed item(s)" not in status.stdout:
        raise DeploymentFailure(
            f"unexpected global status output:\n{status.stdout}"
        )

    doctor = run_command(
        [*prefix, "doctor"],
        environment=environment,
        verbose=verbose,
    )
    if "Doctor passed" not in doctor.stdout:
        raise DeploymentFailure(
            f"unexpected global doctor output:\n{doctor.stdout}"
        )

    update = run_command(
        [*prefix, "upgrade", "--check", "--json"],
        environment=environment,
        verbose=verbose,
    )
    update_status = json.loads(update.stdout)
    assert_equal(
        update_status.get("update_available"),
        False,
        "global local-source update availability",
    )

    before_sync_preview = snapshot_tree(home)
    run_command(
        [*prefix, "sync", "--dry-run"],
        environment=environment,
        verbose=verbose,
    )
    assert_equal(
        snapshot_tree(home),
        before_sync_preview,
        "global sync dry-run snapshot",
    )

    before_uninstall_preview = snapshot_tree(home)
    run_command(
        [str(launcher), "uninstall", "--dry-run"],
        environment=environment,
        verbose=verbose,
    )
    assert_equal(
        snapshot_tree(home),
        before_uninstall_preview,
        "global uninstall dry-run snapshot",
    )


def verify_global_uninstalled_layout(home: Path, harness: str) -> None:
    skills_root, agents_root = global_installed_paths(home, harness)
    require_empty_or_absent(skills_root)
    require_empty_or_absent(agents_root)
    require_absent(home / ".local/bin/ai-onboard")
    require_absent(home / ".ai-onboard/ai-onboard.lock.json")
    require_file(home / ".ai-onboard/ai-onboard.json")


def verify_uninstalled_layout(
    target: Path,
    harness: str,
    config_path: Path,
) -> None:
    skills_root, agents_root, command_path = installed_paths(target, harness)
    require_empty_or_absent(skills_root)
    require_empty_or_absent(agents_root)
    require_absent(command_path)
    require_absent(target / ".ai-onboard/bin/ai_onboard.py")
    require_absent(target / ".ai-onboard/bin/install_macos_update_notifier.py")
    require_absent(target / ".github/workflows/ai-onboard-update-check.yml")
    require_absent(target / ".ai-onboard.lock.json")
    require_file(target / "ai-onboard.json")
    assert_equal(
        (target / "AGENTS.md").read_text(encoding="utf-8"),
        AGENTS_SENTINEL,
        "user AGENTS.md preservation",
    )
    verify_user_config(config_path, harness, installed=False)


def test_deployment(
    harness: str,
    *,
    source: Path,
    verbose: bool,
) -> None:
    manifest = read_json(MANIFEST)
    profiles = sorted(str(name) for name in manifest.get("profiles", {}))
    package_version = str(manifest.get("version", ""))
    if not profiles or not package_version:
        raise DeploymentFailure("package manifest has no profiles or version")

    with tempfile.TemporaryDirectory(
        prefix=f"ai-onboard-{harness}-deploy-"
    ) as temporary:
        target = Path(temporary) / "project"
        target.mkdir()
        environment = deployment_environment(Path(temporary) / "home")
        (target / "AGENTS.md").write_text(
            AGENTS_SENTINEL,
            encoding="utf-8",
        )
        config_path = seed_user_config(target, harness)
        run_command(
            ["git", "-C", str(target), "init", "-q", "-b", "main"],
            environment=environment,
            verbose=verbose,
        )
        run_command(
            ["git", "-C", str(target), "config", "commit.gpgsign", "false"],
            environment=environment,
            verbose=verbose,
        )
        run_command(
            [
                "git",
                "-C",
                str(target),
                "add",
                "AGENTS.md",
                config_path.relative_to(target).as_posix(),
            ],
            environment=environment,
            verbose=verbose,
        )
        run_command(
            [
                "git",
                "-C",
                str(target),
                "commit",
                "-q",
                "-m",
                "seed deployment fixture",
            ],
            environment=environment,
            verbose=verbose,
        )

        run_command(
            [
                sys.executable,
                str(MANAGER),
                "--source",
                str(source),
                "--target",
                str(target),
                "install",
                "--harness",
                harness,
                "--profile",
                ",".join(profiles),
                "--agents",
                "--configs",
                "--notifications",
                "--workflow-foundations",
            ],
            environment=environment,
            verbose=verbose,
        )

        skill_count, agent_count = verify_installed_layout(
            target,
            harness,
            profiles,
            package_version,
        )
        verify_user_config(config_path, harness, installed=True)
        verify_lifecycle(
            target,
            source=source,
            environment=environment,
            verbose=verbose,
        )

        installed_manager = target / ".ai-onboard/bin/ai_onboard.py"
        run_command(
            [
                sys.executable,
                str(installed_manager),
                "--target",
                str(target),
                "uninstall",
            ],
            environment=environment,
            verbose=verbose,
        )
        verify_uninstalled_layout(target, harness, config_path)

    print(
        f"PASS {harness} project: AI_ONBOARD {package_version}, "
        f"{skill_count} skills, {agent_count} agents"
    )


def test_global_deployment(
    harness: str,
    *,
    source: Path,
    verbose: bool,
) -> None:
    manifest = read_json(MANIFEST)
    profiles = sorted(str(name) for name in manifest.get("profiles", {}))
    package_version = str(manifest.get("version", ""))

    with tempfile.TemporaryDirectory(
        prefix=f"ai-onboard-{harness}-global-"
    ) as temporary:
        home = Path(temporary) / "home"
        environment = deployment_environment(home)
        run_command(
            [
                sys.executable,
                str(MANAGER),
                "--source",
                str(source),
                "--target",
                str(home),
                "--global",
                "install",
                "--harness",
                harness,
                "--profile",
                ",".join(profiles),
                "--agents",
                "--workflow-foundations",
            ],
            environment=environment,
            verbose=verbose,
        )
        skill_count, agent_count = verify_global_installed_layout(
            home,
            harness,
            profiles,
            package_version,
        )
        verify_global_lifecycle(
            home,
            source=source,
            environment=environment,
            verbose=verbose,
        )
        run_command(
            [str(home / ".local/bin/ai-onboard"), "uninstall"],
            environment=environment,
            verbose=verbose,
        )
        verify_global_uninstalled_layout(home, harness)

    print(
        f"PASS {harness} global: AI_ONBOARD {package_version}, "
        f"{skill_count} skills, {agent_count} agents"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Smoke-test complete AI_ONBOARD installs for Codex, Claude, "
            "and OpenCode."
        )
    )
    parser.add_argument(
        "--harness",
        action="append",
        choices=SUPPORTED_HARNESSES,
        help="Harness to test; repeat to select multiple (default: all).",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print lifecycle command output.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    harnesses = args.harness or list(SUPPORTED_HARNESSES)
    with deployment_source() as source:
        for harness in harnesses:
            try:
                test_deployment(
                    harness,
                    source=source,
                    verbose=args.verbose,
                )
                test_global_deployment(
                    harness,
                    source=source,
                    verbose=args.verbose,
                )
            except DeploymentFailure as exc:
                print(f"FAIL {harness}: {exc}", file=sys.stderr)
                return 1
    print(f"Deployment smoke tests passed: {', '.join(harnesses)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
