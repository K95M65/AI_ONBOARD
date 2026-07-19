#!/usr/bin/env python3
"""Manage reversible project or user-global AI_ONBOARD installations.

The manager is dependency-free. It records desired state separately from the
resolved lock, never overwrites divergent user files, and removes only content
whose current checksum still matches content it installed.
"""

from __future__ import annotations

import argparse
import contextlib
import copy
import hashlib
import json
import os
import plistlib
import queue
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import threading
import time
import tomllib
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator


SCHEMA = 1
DESIRED_NAME = "ai-onboard.json"
LOCK_NAME = ".ai-onboard.lock.json"
STATE_DIR = ".ai-onboard"
GLOBAL_DESIRED_NAME = f"{STATE_DIR}/ai-onboard.json"
GLOBAL_LOCK_NAME = f"{STATE_DIR}/ai-onboard.lock.json"
GLOBAL_LAUNCHER = ".local/bin/ai-onboard"
UPDATE_STATUS_NAME = f"{STATE_DIR}/update-status.json"
SUPPORTED_HARNESSES = ("claude", "codex", "opencode")
DEFAULT_REPOSITORY = "K95M65/AI_ONBOARD"
UPDATE_AVAILABLE_EXIT = 10
RELEASE_CLASSIFICATIONS = {"fix", "security", "feature", "maintenance"}
VERSION_PATTERN = re.compile(
    r"\d+\.\d+\.\d+(?:-[0-9A-Za-z]+(?:[.-][0-9A-Za-z]+)*)?"
    r"(?:\+[0-9A-Za-z]+(?:[.-][0-9A-Za-z]+)*)?"
)
GITHUB_NOREPLY_PATTERN = re.compile(
    r"^[^@\s<>]+@users\.noreply\.github\.com$",
    re.IGNORECASE,
)
GITHUB_SERVICE_NOREPLY = "noreply@github.com"
GIT_IDENT_EMAIL_PATTERN = re.compile(r"<([^<>\s]+)>\s+\d+\s+[+-]\d{4}$")
NOTIFIER_LABEL_PREFIX = "com.rsthrives.ai-onboard-update"
REVIEW_REQUIRED_ARTIFACTS = {
    ".github/workflows/ai-onboard-update-check.yml",
}
MAX_ARCHIVE_BYTES = 100 * 1024 * 1024
MAX_EXTRACTED_BYTES = 256 * 1024 * 1024
MAX_ARCHIVE_MEMBERS = 20_000
PROJECT_MANAGED_ARTIFACT_PATTERNS = (
    re.compile(r"\.agents/skills/[a-z0-9]+(?:-[a-z0-9]+)*"),
    re.compile(r"\.claude/skills/[a-z0-9]+(?:-[a-z0-9]+)*"),
    re.compile(r"\.claude/agents/[a-z0-9]+(?:-[a-z0-9]+)*\.md"),
    re.compile(r"\.codex/agents/[a-z0-9]+(?:-[a-z0-9]+)*\.toml"),
    re.compile(r"\.opencode/agents/[a-z0-9]+(?:-[a-z0-9]+)*\.md"),
    re.compile(r"\.ai-onboard/bin/ai_onboard\.py"),
    re.compile(r"\.ai-onboard/bin/install_macos_update_notifier\.py"),
    re.compile(r"\.ai-onboard/share/codex-prompts/ai-onboard-update\.md"),
    re.compile(r"\.claude/commands/ai-onboard-update\.md"),
    re.compile(r"\.opencode/commands/ai-onboard-update\.md"),
    re.compile(r"\.github/workflows/ai-onboard-update-check\.yml"),
)
GLOBAL_MANAGED_ARTIFACT_PATTERNS = (
    re.compile(r"\.agents/skills/[a-z0-9]+(?:-[a-z0-9]+)*"),
    re.compile(r"\.claude/skills/[a-z0-9]+(?:-[a-z0-9]+)*"),
    re.compile(r"\.claude/agents/[a-z0-9]+(?:-[a-z0-9]+)*\.md"),
    re.compile(r"\.codex/agents/[a-z0-9]+(?:-[a-z0-9]+)*\.toml"),
    re.compile(r"\.config/opencode/agents/[a-z0-9]+(?:-[a-z0-9]+)*\.md"),
    re.compile(r"\.local/bin/ai-onboard"),
)
ALLOWED_CONFIG_VALUES: dict[str, dict[str, Any]] = {
    ".claude/settings.json": {
        "/permissions/deny": [
            "Read(./.env)",
            "Read(./.env.*)",
            "Read(./secrets/**)",
        ],
        "/skillOverrides/goal-contract": "user-invocable-only",
        "/skillOverrides/grill-requirements": "user-invocable-only",
    },
    ".codex/config.toml": {
        "/agents/max_threads": 4,
        "/agents/max_depth": 1,
    },
    "opencode.json": {
        "/$schema": "https://opencode.ai/config.json",
        "/permission/edit": "ask",
        "/permission/bash": "ask",
        "/permission/external_directory": "deny",
        "/permission/skill/*": "allow",
        "/permission/skill/goal-contract": "ask",
        "/permission/skill/grill-requirements": "ask",
        "/compaction/auto": True,
        "/compaction/prune": True,
        "/compaction/reserved": 12000,
        "/watcher/ignore": [
            ".git/**",
            ".agents/skills/**",
            ".claude/skills/**",
            "node_modules/**",
            "dist/**",
            "output/**",
        ],
    },
}


class LifecycleError(RuntimeError):
    """User-actionable lifecycle failure."""


@dataclass(frozen=True)
class Source:
    root: Path
    manifest: dict[str, Any]
    catalog: dict[str, Any]
    revision: str
    content_digest: str


@dataclass(frozen=True)
class Artifact:
    source: Path
    destination: str
    source_label: str


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise LifecycleError(f"cannot read JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise LifecycleError(f"{path} must contain a JSON object")
    return value


def validate_version(value: object) -> str:
    if not isinstance(value, str) or len(value) > 64:
        raise LifecycleError("package version must be a bounded semantic version")
    if not VERSION_PATTERN.fullmatch(value):
        raise LifecycleError(f"invalid package semantic version: {value!r}")
    return value


def atomic_write(path: Path, text: str, dry_run: bool = False) -> None:
    if dry_run:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = (path.stat().st_mode & 0o7777) if path.is_file() else 0o600
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.tmp-",
        dir=path.parent,
        text=True,
    )
    temporary = Path(temporary_name)
    try:
        os.fchmod(descriptor, mode)
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(text)
        os.replace(temporary, path)
    finally:
        with contextlib.suppress(OSError):
            os.close(descriptor)
        temporary.unlink(missing_ok=True)


def write_json(path: Path, value: dict[str, Any], dry_run: bool = False) -> None:
    atomic_write(path, json.dumps(value, indent=2, sort_keys=True) + "\n", dry_run)


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    if path.is_symlink():
        digest.update(b"symlink\0")
        digest.update(os.readlink(path).encode())
        return digest.hexdigest()
    if path.is_file():
        digest.update(b"file\0")
        digest.update(path.read_bytes())
        return digest.hexdigest()
    if path.is_dir():
        digest.update(b"directory\0")
        for child in sorted(path.rglob("*")):
            relative = child.relative_to(path).as_posix()
            digest.update(relative.encode())
            digest.update(b"\0")
            if child.is_symlink():
                digest.update(b"symlink\0")
                digest.update(os.readlink(child).encode())
            elif child.is_dir():
                digest.update(b"directory\0")
            else:
                digest.update(child.read_bytes())
            digest.update(b"\0")
        return digest.hexdigest()
    return "missing"


def copy_path(source: Path, destination: Path, dry_run: bool = False) -> None:
    if dry_run:
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    staged = destination.with_name(f".{destination.name}.stage-{os.getpid()}")
    if staged.exists() or staged.is_symlink():
        remove_path(staged)
    if source.is_dir():
        shutil.copytree(source, staged, symlinks=True)
    else:
        shutil.copy2(source, staged)
    if destination.exists() or destination.is_symlink():
        remove_path(destination)
    os.replace(staged, destination)


def remove_path(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink(missing_ok=True)
    elif path.is_dir():
        shutil.rmtree(path)


def managed_path(target: Path, relative: str) -> Path:
    """Resolve one managed path without allowing it to escape the target."""
    relative_path = Path(relative)
    if (
        not relative
        or relative_path.is_absolute()
        or ".." in relative_path.parts
    ):
        raise LifecycleError(
            f"managed path is outside the target project: {relative!r}"
        )
    target_resolved = target.resolve()
    candidate = target / relative_path
    resolved = candidate.resolve(strict=False)
    if resolved != target_resolved and target_resolved not in resolved.parents:
        raise LifecycleError(
            f"managed path is outside the target project: {relative!r}"
        )
    return candidate


def desired_state_name(global_scope: bool) -> str:
    return GLOBAL_DESIRED_NAME if global_scope else DESIRED_NAME


def lock_state_name(global_scope: bool) -> str:
    return GLOBAL_LOCK_NAME if global_scope else LOCK_NAME


def desired_is_global(desired: dict[str, Any]) -> bool:
    scope = desired.get("scope", "project")
    if scope not in {"project", "global"}:
        raise LifecycleError(f"unsupported installation scope {scope!r}")
    return scope == "global"


def invoked_from_global_launcher() -> bool:
    return Path(__file__).name == Path(GLOBAL_LAUNCHER).name


def backup_path(target: Path, relative: str, dry_run: bool = False) -> None:
    source = managed_path(target, relative)
    if dry_run or not source.exists():
        return
    stamp = time.strftime("%Y%m%d-%H%M%S")
    backup = managed_path(
        target, f"{STATE_DIR}/backups/{stamp}/{relative}"
    )
    backup.parent.mkdir(parents=True, exist_ok=True)
    if source.is_dir():
        shutil.copytree(source, backup, symlinks=True, dirs_exist_ok=True)
    else:
        shutil.copy2(source, backup)


def stage_conflict(
    source: Path, target: Path, relative: str, dry_run: bool = False
) -> None:
    managed_path(target, relative)
    conflict = managed_path(target, f"{STATE_DIR}/conflicts/{relative}")
    copy_path(source, conflict, dry_run)


def package_content_digest(root: Path) -> str:
    digest = hashlib.sha256()
    selected_paths = [
        root / "package-manifest.json",
        root / "site/data/catalog.json",
        root / "scripts/ai_onboard.py",
        root / "scripts/install_macos_update_notifier.py",
        root / "templates/configs",
        root / "templates/commands",
        root / "templates/notifications",
        root / "agents",
        root / "skills",
    ]
    for selected in selected_paths:
        if not selected.exists() and not selected.is_symlink():
            continue
        if selected.is_symlink():
            raise LifecycleError(f"package source contains a symlink: {selected}")
        files = [selected] if selected.is_file() else sorted(selected.rglob("*"))
        for path in files:
            if path.is_symlink():
                raise LifecycleError(f"package source contains a symlink: {path}")
            if path.is_dir():
                continue
            relative = path.relative_to(root).as_posix()
            digest.update(relative.encode())
            digest.update(b"\0")
            digest.update(path.read_bytes())
            digest.update(b"\0")
    return digest.hexdigest()


def git_revision(root: Path, content_digest: str) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return f"content:{content_digest[:16]}"
    top_level = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "--show-toplevel"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    if Path(top_level).resolve() != root:
        raise LifecycleError("package source must be the root of its Git checkout")
    package_paths = (
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
    dirty = subprocess.run(
        [
            "git",
            "-C",
            str(root),
            "status",
            "--porcelain",
            "--untracked-files=all",
            "--",
            *package_paths,
        ],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    if dirty:
        raise LifecycleError(
            "package source has uncommitted managed content; commit it before install"
        )
    return result.stdout.strip()


def git_output(target: Path, *arguments: str) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(target), *arguments],
            check=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except OSError as exc:
        raise LifecycleError("git is required for check-git") from exc
    except subprocess.TimeoutExpired as exc:
        raise LifecycleError(
            f"git timed out during check-git: {' '.join(arguments)}"
        ) from exc
    except subprocess.CalledProcessError as exc:
        raise LifecycleError(
            f"cannot inspect Git repository for check-git: {' '.join(arguments)}"
        ) from exc
    return result.stdout.strip()


def git_ident_email(target: Path, variable: str) -> str:
    identity = git_output(target, "var", variable)
    match = GIT_IDENT_EMAIL_PATTERN.search(identity)
    if not match:
        raise LifecycleError(f"git returned an invalid {variable} value")
    return match.group(1)


def is_github_noreply(
    email: str,
    *,
    allow_github_service: bool = False,
) -> bool:
    return bool(GITHUB_NOREPLY_PATTERN.fullmatch(email)) or (
        allow_github_service
        and email.casefold() == GITHUB_SERVICE_NOREPLY
    )


def git_stream_lines(
    target: Path,
    *arguments: str,
    max_line_bytes: int = 4096,
    timeout_seconds: int = 30,
) -> Iterator[str]:
    try:
        process = subprocess.Popen(
            ["git", "-C", str(target), *arguments],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
    except OSError as exc:
        raise LifecycleError("git is required for check-git") from exc

    assert process.stdout is not None
    chunks: queue.Queue[bytes | None] = queue.Queue(maxsize=8)

    def read_stdout() -> None:
        try:
            while chunk := process.stdout.read(4096):
                chunks.put(chunk)
        finally:
            chunks.put(None)

    reader = threading.Thread(target=read_stdout, daemon=True)
    reader.start()
    deadline = time.monotonic() + timeout_seconds
    buffered = bytearray()

    try:
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise LifecycleError("git timed out during check-git")
            try:
                chunk = chunks.get(timeout=remaining)
            except queue.Empty as exc:
                raise LifecycleError("git timed out during check-git") from exc
            if chunk is None:
                break
            buffered.extend(chunk)
            while b"\n" in buffered:
                raw_line, _, remainder = buffered.partition(b"\n")
                buffered = bytearray(remainder)
                if len(raw_line) > max_line_bytes:
                    raise LifecycleError(
                        "git returned oversized identity metadata"
                    )
                try:
                    yield raw_line.decode("utf-8")
                except UnicodeDecodeError as exc:
                    raise LifecycleError(
                        "git returned invalid identity metadata"
                    ) from exc
            if len(buffered) > max_line_bytes:
                raise LifecycleError(
                    "git returned oversized identity metadata"
                )
        if buffered:
            try:
                yield buffered.decode("utf-8")
            except UnicodeDecodeError as exc:
                raise LifecycleError(
                    "git returned invalid identity metadata"
                ) from exc
        remaining = max(0.0, deadline - time.monotonic())
        try:
            return_code = process.wait(timeout=remaining)
        except subprocess.TimeoutExpired as exc:
            raise LifecycleError("git timed out during check-git") from exc
        if return_code:
            raise LifecycleError("cannot inspect Git metadata for check-git")
    except BaseException:
        if process.poll() is None:
            process.kill()
            process.wait()
        raise
    finally:
        process.stdout.close()


def git_history_identities(
    target: Path,
    revisions: tuple[str, ...] = ("--all",),
) -> Iterator[tuple[str, str, str]]:
    for line in git_stream_lines(
        target,
        "log",
        "--format=%H%x09%ae%x09%ce",
        *revisions,
    ):
        parts = line.split("\t")
        if len(parts) != 3:
            raise LifecycleError("git returned invalid commit identity metadata")
        yield parts[0], parts[1], parts[2]


def pre_push_revisions() -> Iterator[tuple[str, ...]]:
    oid_pattern = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})")
    while True:
        line = sys.stdin.readline(4097)
        if not line:
            return
        if len(line) > 4096:
            raise LifecycleError("git pre-push metadata is oversized")
        parts = line.split()
        if len(parts) != 4:
            raise LifecycleError("git pre-push metadata is invalid")
        _, local_oid, _, remote_oid = parts
        if not oid_pattern.fullmatch(local_oid):
            raise LifecycleError("git pre-push local object ID is invalid")
        if not oid_pattern.fullmatch(remote_oid):
            raise LifecycleError("git pre-push remote object ID is invalid")
        if set(local_oid) == {"0"}:
            continue
        if set(remote_oid) == {"0"}:
            yield (local_oid,)
        else:
            yield (local_oid, "--not", remote_oid)


def command_check_git(
    target: Path,
    *,
    identity_only: bool,
    history_only: bool,
    pre_push: bool,
) -> int:
    git_output(target, "rev-parse", "--is-inside-work-tree")
    issues = 0

    if not history_only and not pre_push:
        for role, variable in (
            ("author", "GIT_AUTHOR_IDENT"),
            ("committer", "GIT_COMMITTER_IDENT"),
        ):
            if not is_github_noreply(git_ident_email(target, variable)):
                print(
                    f"  error: Git {role} email is not a GitHub no-reply address"
                )
                issues += 1
        if not issues:
            print("Git process identity passed")

    if not identity_only:
        history_count = 0
        history_issues = 0
        revisions = (
            pre_push_revisions()
            if pre_push
            else iter([("--all",)])
        )
        for revision in revisions:
            for commit, author_email, committer_email in git_history_identities(
                target,
                revision,
            ):
                history_count += 1
                unsafe_roles = []
                if not is_github_noreply(
                    author_email,
                    allow_github_service=True,
                ):
                    unsafe_roles.append("author")
                if not is_github_noreply(
                    committer_email,
                    allow_github_service=True,
                ):
                    unsafe_roles.append("committer")
                if unsafe_roles:
                    roles = " and ".join(unsafe_roles)
                    print(
                        f"  error: commit {commit[:12]} {roles} email "
                        "is not a GitHub no-reply address"
                    )
                    history_issues += 1
        issues += history_issues
        if not history_issues:
            label = "outgoing" if pre_push else "reachable"
            print(f"Git history passed: {history_count} {label} commit(s)")

    if issues:
        print(f"Git identity check found {issues} issue(s)")
        return 1
    return 0


def load_source(root: Path, revision: str | None = None) -> Source:
    root = root.resolve()
    manifest = read_json(root / "package-manifest.json")
    catalog = read_json(root / "site" / "data" / "catalog.json")
    if manifest.get("schema") != SCHEMA:
        raise LifecycleError(
            f"unsupported package manifest schema {manifest.get('schema')!r}"
        )
    validate_version(manifest.get("version"))
    content_digest = package_content_digest(root)
    return Source(
        root,
        manifest,
        catalog,
        revision or git_revision(root, content_digest),
        content_digest,
    )


def source_artifact(root: Path, path: Path) -> Path:
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise LifecycleError(f"package artifact is outside the source: {path}") from exc
    if path.is_symlink():
        raise LifecycleError(f"package artifact is a symlink: {path}")
    resolved = path.resolve(strict=False)
    if resolved != root and root not in resolved.parents:
        raise LifecycleError(f"package artifact is outside the source: {path}")
    if path.is_dir():
        for child in path.rglob("*"):
            if child.is_symlink():
                raise LifecycleError(f"package artifact contains a symlink: {child}")
    if not path.exists():
        raise LifecycleError(f"package artifact is missing: {path}")
    return path


def github_token() -> str | None:
    return os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")


def validate_repository(repository: str) -> str:
    if not re.fullmatch(
        r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository
    ):
        raise LifecycleError(
            f"invalid GitHub repository in desired state: {repository!r}"
        )
    return repository


def validate_revision(revision: str) -> str:
    if (
        not re.fullmatch(r"[A-Za-z0-9._/-]{1,200}", revision)
        or ".." in revision.split("/")
    ):
        raise LifecycleError(f"invalid source revision: {revision!r}")
    return revision


def github_json(api_path: str) -> dict[str, Any]:
    url = f"https://api.github.com/{api_path.lstrip('/')}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "AI_ONBOARD lifecycle manager",
    }
    token = github_token()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(
        url,
        headers=headers,
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            value = json.load(response)
    except (OSError, urllib.error.HTTPError, json.JSONDecodeError) as exc:
        try:
            result = subprocess.run(
                ["gh", "api", api_path.lstrip("/")],
                check=True,
                capture_output=True,
                text=True,
            )
            value = json.loads(result.stdout)
        except (
            OSError,
            subprocess.CalledProcessError,
            json.JSONDecodeError,
        ) as fallback_exc:
            raise LifecycleError(
                f"GitHub request failed for {url}: {exc}. "
                "For a private repository, authenticate gh or set GH_TOKEN."
            ) from fallback_exc
    if not isinstance(value, dict):
        raise LifecycleError(f"unexpected GitHub response for {url}")
    return value


def safe_extract(archive: Path, destination: Path) -> None:
    destination_resolved = destination.resolve()
    with tarfile.open(archive, "r:gz") as bundle:
        safe_members: list[tarfile.TarInfo] = []
        total_size = 0
        for member_index, member in enumerate(bundle, start=1):
            if member_index > MAX_ARCHIVE_MEMBERS:
                raise LifecycleError("source archive contains too many entries")
            if member.size < 0:
                raise LifecycleError("source archive contains invalid size metadata")
            total_size += member.size
            if total_size > MAX_EXTRACTED_BYTES:
                raise LifecycleError("source archive expands beyond the safety limit")
            candidate = (destination / member.name).resolve()
            if (
                candidate != destination_resolved
                and destination_resolved not in candidate.parents
            ):
                raise LifecycleError("archive contains an unsafe path")
            if member.issym() or member.islnk():
                continue
            if not (member.isdir() or member.isreg()):
                raise LifecycleError("archive contains an unsupported file type")
            safe_members.append(member)
        try:
            bundle.extractall(
                destination,
                members=safe_members,
                filter="data",
            )
        except TypeError:  # Python 3.11 without the extraction-filter backport.
            bundle.extractall(destination, members=safe_members)


def download_archive(repository: str, revision: str, archive: Path) -> None:
    url = f"https://codeload.github.com/{repository}/tar.gz/{revision}"
    headers = {"User-Agent": "AI_ONBOARD lifecycle manager"}
    token = github_token()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    try:
        size = 0
        with urllib.request.urlopen(request, timeout=60) as response:
            length = response.headers.get("Content-Length")
            if length and int(length) > MAX_ARCHIVE_BYTES:
                raise LifecycleError("source archive exceeds the download limit")
            with archive.open("wb") as handle:
                while chunk := response.read(1024 * 1024):
                    size += len(chunk)
                    if size > MAX_ARCHIVE_BYTES:
                        raise LifecycleError(
                            "source archive exceeds the download limit"
                        )
                    handle.write(chunk)
        return
    except (OSError, urllib.error.HTTPError) as exc:
        api_path = f"repos/{repository}/tarball/{revision}"
        try:
            process = subprocess.Popen(
                ["gh", "api", api_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
            )
            if process.stdout is None:
                raise LifecycleError("could not read authenticated GitHub archive")
            size = 0
            with archive.open("wb") as handle:
                while chunk := process.stdout.read(1024 * 1024):
                    size += len(chunk)
                    if size > MAX_ARCHIVE_BYTES:
                        process.kill()
                        process.wait()
                        archive.unlink(missing_ok=True)
                        raise LifecycleError(
                            "source archive exceeds the download limit"
                        )
                    handle.write(chunk)
            return_code = process.wait()
            if return_code:
                raise subprocess.CalledProcessError(
                    return_code, ["gh", "api", api_path]
                )
            return
        except (OSError, subprocess.CalledProcessError) as fallback_exc:
            archive.unlink(missing_ok=True)
            raise LifecycleError(
                f"could not download {url}: {exc}. "
                "For a private repository, authenticate gh or set GH_TOKEN."
            ) from fallback_exc


@contextlib.contextmanager
def remote_source(
    repository: str, channel: str, locked_revision: str | None = None
) -> Iterator[Source]:
    repository = validate_repository(repository)
    if locked_revision:
        revision = validate_revision(locked_revision)
        if not re.fullmatch(r"[0-9a-fA-F]{40}", revision):
            raise LifecycleError(
                "locked remote revision must be an immutable commit SHA"
            )
    elif channel == "stable":
        release = github_json(
            f"repos/{repository}/releases/latest"
        )
        ref = str(release.get("tag_name", ""))
        if not ref:
            raise LifecycleError(
                f"{repository} has no stable release; use channel 'edge'"
            )
        ref = validate_revision(ref)
        commit = github_json(
            f"repos/{repository}/commits/"
            f"{urllib.parse.quote(ref, safe='')}"
        )
        revision = validate_revision(str(commit.get("sha", "")))
    elif channel == "edge":
        commit = github_json(
            f"repos/{repository}/commits/main"
        )
        revision = validate_revision(str(commit.get("sha", "")))
    else:
        ref = validate_revision(channel)
        commit = github_json(
            f"repos/{repository}/commits/"
            f"{urllib.parse.quote(ref, safe='')}"
        )
        revision = validate_revision(str(commit.get("sha", "")))
    if not revision:
        raise LifecycleError("could not resolve a source revision")

    with tempfile.TemporaryDirectory(prefix="ai-onboard-source-") as temporary:
        temporary_path = Path(temporary)
        archive = temporary_path / "source.tar.gz"
        download_archive(repository, revision, archive)
        extracted = temporary_path / "extracted"
        extracted.mkdir()
        safe_extract(archive, extracted)
        roots = [path for path in extracted.iterdir() if path.is_dir()]
        if len(roots) != 1:
            raise LifecycleError("downloaded source archive has an invalid layout")
        yield load_source(roots[0], revision)


@contextlib.contextmanager
def resolve_source(
    source_arg: str | None,
    target: Path,
    *,
    global_scope: bool = False,
    use_locked_revision: bool = False,
) -> Iterator[Source]:
    if source_arg:
        yield load_source(Path(source_arg))
        return
    repository_root = Path(__file__).resolve().parents[1]
    if (repository_root / "package-manifest.json").is_file():
        yield load_source(repository_root)
        return

    desired_path = managed_path(target, desired_state_name(global_scope))
    desired = read_json(desired_path) if desired_path.is_file() else {}
    source_config = desired.get("source", {})
    repository = str(source_config.get("repository", DEFAULT_REPOSITORY))
    channel = str(source_config.get("channel", "stable"))
    locked_revision = None
    lock_path = managed_path(target, lock_state_name(global_scope))
    if use_locked_revision and lock_path.is_file():
        locked_revision = str(
            read_json(lock_path).get("source_revision", "")
        ) or None
    with remote_source(repository, channel, locked_revision) as source:
        yield source


def split_csv(values: list[str] | None) -> list[str]:
    result: list[str] = []
    for value in values or []:
        for item in value.split(","):
            item = item.strip().lower()
            if item and item not in result:
                result.append(item)
    return result


def validate_harnesses(harnesses: list[str]) -> list[str]:
    invalid = sorted(set(harnesses) - set(SUPPORTED_HARNESSES))
    if invalid:
        raise LifecycleError(f"unknown harnesses: {', '.join(invalid)}")
    return sorted(harnesses)


def validate_profiles(source: Source, profiles: list[str]) -> list[str]:
    available = source.manifest.get("profiles", {})
    invalid = sorted(set(profiles) - set(available))
    if invalid:
        raise LifecycleError(f"unknown profiles: {', '.join(invalid)}")
    return sorted(profiles)


def selected_skills(
    source: Source, profiles: list[str], workflow_foundations: bool
) -> list[dict[str, Any]]:
    categories: set[str] = set()
    explicit: set[str] = set()
    profile_config = source.manifest.get("profiles", {})
    for profile in profiles:
        definition = profile_config[profile]
        categories.update(definition.get("categories", []))
        explicit.update(definition.get("skills", []))
    if workflow_foundations:
        categories.add("Manual workflow foundations")

    skills = []
    for skill in source.catalog.get("skills", []):
        if skill.get("category") in categories or skill.get("name") in explicit:
            skills.append(skill)
    return sorted(skills, key=lambda skill: str(skill.get("name", "")))


def desired_artifacts(
    source: Source, desired: dict[str, Any], include_manager: bool = True
) -> list[Artifact]:
    harnesses = desired["harnesses"]
    features = desired["features"]
    global_scope = desired_is_global(desired)
    skills = selected_skills(
        source,
        desired["profiles"],
        bool(features.get("workflow_foundations")),
    )
    artifacts: dict[str, Artifact] = {}

    for skill in skills:
        name = str(skill["name"])
        catalog_path = Path(str(skill["path"]))
        if (
            not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name)
            or catalog_path.is_absolute()
            or ".." in catalog_path.parts
            or not catalog_path.parts
            or catalog_path.parts[0] != "skills"
            or catalog_path.name != "SKILL.md"
            or catalog_path.parent.name != name
        ):
            raise LifecycleError(
                f"catalog skill has an invalid package path: {name!r}"
            )
        skill_file = source.root / catalog_path
        skill_root = source_artifact(source.root, skill_file.parent)
        if "claude" in harnesses:
            relative = f".claude/skills/{name}"
            artifacts[relative] = Artifact(
                skill_root, relative, str(skill_file.parent.relative_to(source.root))
            )
        if "codex" in harnesses or "opencode" in harnesses:
            relative = f".agents/skills/{name}"
            artifacts[relative] = Artifact(
                skill_root, relative, str(skill_file.parent.relative_to(source.root))
            )

    if features.get("agents"):
        if "claude" in harnesses:
            for path in sorted((source.root / "agents").glob("*.md")):
                if path.name == "README.md":
                    continue
                path = source_artifact(source.root, path)
                relative = f".claude/agents/{path.name}"
                artifacts[relative] = Artifact(
                    path, relative, str(path.relative_to(source.root))
                )
        if "codex" in harnesses:
            for path in sorted((source.root / "agents/codex").glob("*.toml")):
                path = source_artifact(source.root, path)
                relative = f".codex/agents/{path.name}"
                artifacts[relative] = Artifact(
                    path, relative, str(path.relative_to(source.root))
                )
        if "opencode" in harnesses:
            agent_root = (
                ".config/opencode/agents"
                if global_scope
                else ".opencode/agents"
            )
            for path in sorted((source.root / "agents/opencode").glob("*.md")):
                if path.name == "README.md":
                    continue
                path = source_artifact(source.root, path)
                relative = f"{agent_root}/{path.name}"
                artifacts[relative] = Artifact(
                    path, relative, str(path.relative_to(source.root))
                )

    if features.get("notifications"):
        if global_scope:
            raise LifecycleError(
                "--notifications is available only for project installs"
            )
        notification_artifacts = []
        if "claude" in harnesses:
            notification_artifacts.append(
                (
                    "templates/commands/claude/ai-onboard-update.md",
                    ".claude/commands/ai-onboard-update.md",
                )
            )
        if "opencode" in harnesses:
            notification_artifacts.append(
                (
                    "templates/commands/opencode/ai-onboard-update.md",
                    ".opencode/commands/ai-onboard-update.md",
                )
            )
        if "codex" in harnesses:
            notification_artifacts.append(
                (
                    "templates/commands/codex/ai-onboard-update.md",
                    f"{STATE_DIR}/share/codex-prompts/ai-onboard-update.md",
                )
            )
        notification_artifacts.append(
            (
                "templates/notifications/github/ai-onboard-update-check.yml",
                ".github/workflows/ai-onboard-update-check.yml",
            )
        )
        macos_installer = source.root / "scripts/install_macos_update_notifier.py"
        if macos_installer.is_file():
            notification_artifacts.append(
                (
                    "scripts/install_macos_update_notifier.py",
                    f"{STATE_DIR}/bin/install_macos_update_notifier.py",
                )
            )
        for source_relative, destination in notification_artifacts:
            path = source_artifact(source.root, source.root / source_relative)
            artifacts[destination] = Artifact(
                path, destination, source_relative
            )

    if include_manager:
        packaged_manager = source.root / "scripts" / "ai_onboard.py"
        manager = (
            packaged_manager
            if packaged_manager.is_file()
            else Path(__file__).resolve()
        )
        if packaged_manager.is_file():
            manager = source_artifact(source.root, manager)
        relative = (
            GLOBAL_LAUNCHER
            if global_scope
            else f"{STATE_DIR}/bin/ai_onboard.py"
        )
        artifacts[relative] = Artifact(manager, relative, "scripts/ai_onboard.py")

    return [artifacts[key] for key in sorted(artifacts)]


def desired_configs(source: Source, desired: dict[str, Any]) -> list[tuple[str, str, Path]]:
    if not desired["features"].get("configs"):
        return []
    if desired_is_global(desired):
        raise LifecycleError("--configs is available only for project installs")
    result: list[tuple[str, str, Path]] = []
    harnesses = desired["harnesses"]
    if "claude" in harnesses:
        result.append(
            (
                ".claude/settings.json",
                "json",
                source.root / "templates/configs/claude.settings.json",
            )
        )
    if "codex" in harnesses:
        result.append(
            (
                ".codex/config.toml",
                "toml",
                source.root / "templates/configs/codex.config.toml",
            )
        )
    if "opencode" in harnesses:
        result.append(
            (
                "opencode.json",
                "json",
                source.root / "templates/configs/opencode.json",
            )
        )
    return [
        (relative, config_format, source_artifact(source.root, template))
        for relative, config_format, template in result
    ]


def pointer(parts: tuple[str, ...]) -> str:
    return "/" + "/".join(part.replace("~", "~0").replace("/", "~1") for part in parts)


def pointer_parts(value: str) -> tuple[str, ...]:
    if not value.startswith("/"):
        raise LifecycleError(f"invalid managed JSON pointer {value!r}")
    if value == "/":
        return ()
    return tuple(
        part.replace("~1", "/").replace("~0", "~")
        for part in value.removeprefix("/").split("/")
    )


def get_nested(value: dict[str, Any], parts: tuple[str, ...]) -> tuple[bool, Any]:
    current: Any = value
    for part in parts:
        if not isinstance(current, dict) or part not in current:
            return False, None
        current = current[part]
    return True, current


def set_nested(value: dict[str, Any], parts: tuple[str, ...], new_value: Any) -> None:
    current = value
    for part in parts[:-1]:
        child = current.get(part)
        if not isinstance(child, dict):
            child = {}
            current[part] = child
        current = child
    current[parts[-1]] = copy.deepcopy(new_value)


def delete_nested(value: dict[str, Any], parts: tuple[str, ...]) -> None:
    parents: list[tuple[dict[str, Any], str]] = []
    current = value
    for part in parts[:-1]:
        child = current.get(part)
        if not isinstance(child, dict):
            return
        parents.append((current, part))
        current = child
    current.pop(parts[-1], None)
    for parent, key in reversed(parents):
        child = parent.get(key)
        if isinstance(child, dict) and not child:
            parent.pop(key, None)


def flatten_config(
    value: dict[str, Any], prefix: tuple[str, ...] = ()
) -> list[tuple[tuple[str, ...], Any]]:
    result: list[tuple[tuple[str, ...], Any]] = []
    for key, child in value.items():
        parts = prefix + (str(key),)
        if isinstance(child, dict):
            result.extend(flatten_config(child, parts))
        else:
            result.append((parts, child))
    return result


def merge_json_config(
    path: Path,
    desired_value: dict[str, Any],
    previous_records: list[dict[str, Any]],
    dry_run: bool,
) -> list[dict[str, Any]]:
    current = read_json(path) if path.is_file() else {}
    previous = {record["pointer"]: record for record in previous_records}
    next_records: list[dict[str, Any]] = []
    wanted_keys = {
        pointer(parts) for parts, _ in flatten_config(desired_value)
    }

    for parts, wanted in flatten_config(desired_value):
        key = pointer(parts)
        exists, present = get_nested(current, parts)
        prior = previous.get(key)
        if prior and prior.get("ownership") == "adopted":
            next_records.append(prior)
            continue
        if isinstance(wanted, list):
            if not exists:
                set_nested(current, parts, wanted)
                next_records.append(
                    {
                        "pointer": key,
                        "kind": "list_items",
                        "items": copy.deepcopy(wanted),
                        "ownership": "owned",
                    }
                )
            elif (
                prior
                and prior.get("kind") == "value"
                and present == prior.get("value")
            ):
                set_nested(current, parts, wanted)
                next_records.append(
                    {
                        "pointer": key,
                        "kind": "list_items",
                        "items": copy.deepcopy(wanted),
                        "ownership": prior.get("ownership", "owned"),
                    }
                )
            elif isinstance(present, list):
                old_items = (
                    prior.get("items", [])
                    if prior and prior.get("kind") == "list_items"
                    else prior.get("value", [])
                    if prior and isinstance(prior.get("value"), list)
                    else []
                )
                if not prior or prior.get("ownership", "owned") == "owned":
                    for item in old_items:
                        if item not in wanted and item in present:
                            present.remove(item)
                retained = [item for item in old_items if item in present and item in wanted]
                added = [item for item in wanted if item not in present]
                if added:
                    present.extend(copy.deepcopy(added))
                managed_items = retained + [item for item in added if item not in retained]
                if managed_items:
                    next_records.append(
                        {
                            "pointer": key,
                            "kind": "list_items",
                            "items": managed_items,
                            "ownership": prior.get("ownership", "owned")
                            if prior
                            else "owned",
                        }
                    )
            continue

        if prior and prior.get("kind") == "value":
            if exists and present == prior.get("value"):
                set_nested(current, parts, wanted)
                next_records.append(
                    {
                        "pointer": key,
                        "kind": "value",
                        "value": copy.deepcopy(wanted),
                        "ownership": prior.get("ownership", "owned"),
                    }
                )
            else:
                next_records.append(prior)
        elif not exists:
            set_nested(current, parts, wanted)
            next_records.append(
                {
                    "pointer": key,
                    "kind": "value",
                    "value": copy.deepcopy(wanted),
                    "ownership": "owned",
                }
            )

    for key, prior in previous.items():
        if key in wanted_keys or prior.get("ownership") == "adopted":
            continue
        parts = pointer_parts(key)
        exists, present = get_nested(current, parts)
        if prior.get("kind") == "value":
            if exists and present == prior.get("value"):
                delete_nested(current, parts)
            elif exists:
                next_records.append(prior)
        elif prior.get("kind") == "list_items" and isinstance(present, list):
            for item in prior.get("items", []):
                if item in present:
                    present.remove(item)

    write_json(path, current, dry_run)
    return next_records


def toml_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, str):
        return json.dumps(value)
    if isinstance(value, list):
        return "[" + ", ".join(toml_value(item) for item in value) + "]"
    raise LifecycleError(f"unsupported TOML value {value!r}")


def toml_table_name(line: str) -> str | None:
    match = re.match(r"^\s*\[\s*(.+?)\s*\]\s*(?:#.*)?$", line)
    if not match:
        return None
    name = match.group(1).strip()
    if (
        len(name) >= 2
        and name[0] == name[-1]
        and name[0] in {"'", '"'}
    ):
        return name[1:-1]
    return name


def set_toml_key(text: str, parts: tuple[str, ...], value: Any) -> str:
    if len(parts) == 1:
        section = ""
        key = parts[0]
    elif len(parts) == 2:
        section, key = parts
    else:
        raise LifecycleError(f"unsupported nested TOML key {'.'.join(parts)}")
    lines = text.splitlines()
    start = 0
    end = len(lines)
    if section:
        heading_text = f"[{section}]"
        try:
            start = next(
                i
                for i, line in enumerate(lines)
                if toml_table_name(line) == section
            ) + 1
        except StopIteration:
            if lines and lines[-1].strip():
                lines.append("")
            lines.extend([heading_text, f"{key} = {toml_value(value)}"])
            return "\n".join(lines) + "\n"
        end = next(
            (
                i
                for i in range(start, len(lines))
                if toml_table_name(lines[i]) is not None
            ),
            len(lines),
        )
    pattern = re.compile(rf"^\s*{re.escape(key)}\s*=")
    for index in range(start, end):
        if pattern.match(lines[index]):
            lines[index] = f"{key} = {toml_value(value)}"
            return "\n".join(lines) + "\n"
    lines.insert(end, f"{key} = {toml_value(value)}")
    return "\n".join(lines) + "\n"


def remove_toml_key(text: str, parts: tuple[str, ...]) -> str:
    section = parts[0] if len(parts) == 2 else ""
    key = parts[-1]
    lines = text.splitlines()
    in_section = not section
    pattern = re.compile(rf"^\s*{re.escape(key)}\s*=")
    result = []
    for line in lines:
        table = toml_table_name(line)
        if table is not None:
            in_section = table == section
        if in_section and pattern.match(line):
            continue
        result.append(line)
    return "\n".join(result).rstrip() + "\n"


def merge_toml_config(
    path: Path,
    desired_value: dict[str, Any],
    previous_records: list[dict[str, Any]],
    dry_run: bool,
) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    try:
        current = tomllib.loads(text)
    except tomllib.TOMLDecodeError as exc:
        raise LifecycleError(f"cannot merge invalid TOML {path}: {exc}") from exc
    previous = {record["pointer"]: record for record in previous_records}
    next_records: list[dict[str, Any]] = []
    wanted_keys = {
        pointer(parts) for parts, _ in flatten_config(desired_value)
    }
    for parts, wanted in flatten_config(desired_value):
        key = pointer(parts)
        exists, present = get_nested(current, parts)
        prior = previous.get(key)
        if prior and prior.get("ownership") == "adopted":
            next_records.append(prior)
        elif prior and exists and present == prior.get("value"):
            text = set_toml_key(text, parts, wanted)
            set_nested(current, parts, wanted)
            next_records.append(
                {
                    "pointer": key,
                    "kind": "value",
                    "value": wanted,
                    "ownership": prior.get("ownership", "owned"),
                }
            )
        elif prior:
            next_records.append(prior)
        elif not exists:
            text = set_toml_key(text, parts, wanted)
            set_nested(current, parts, wanted)
            next_records.append(
                {
                    "pointer": key,
                    "kind": "value",
                    "value": wanted,
                    "ownership": "owned",
                }
            )
    for key, prior in previous.items():
        if key in wanted_keys or prior.get("ownership") == "adopted":
            continue
        parts = pointer_parts(key)
        exists, present = get_nested(current, parts)
        if exists and present == prior.get("value"):
            text = remove_toml_key(text, parts)
            delete_nested(current, parts)
        elif exists:
            next_records.append(prior)
    atomic_write(path, text, dry_run)
    return next_records


def apply_configs(
    source: Source,
    target: Path,
    desired: dict[str, Any],
    old_lock: dict[str, Any],
    dry_run: bool,
) -> list[dict[str, Any]]:
    previous = {
        record["path"]: record for record in old_lock.get("configs", [])
    }
    records: list[dict[str, Any]] = []
    configured = desired_configs(source, desired)
    configured_paths = {relative for relative, _, _ in configured}
    for relative, config_format, template in configured:
        prior = previous.get(relative, {})
        prior_records = prior.get("managed", [])
        path = managed_path(target, relative)
        existed = path.is_file()
        if config_format == "json":
            wanted = read_json(template)
            managed = merge_json_config(
                path, wanted, prior_records, dry_run
            )
        else:
            wanted = tomllib.loads(template.read_text(encoding="utf-8"))
            managed = merge_toml_config(
                path, wanted, prior_records, dry_run
            )
        records.append(
            {
                "path": relative,
                "format": config_format,
                "managed": managed,
                "created": prior.get("created", not existed),
            }
        )
        print(f"  config {relative}: merged {len(managed)} managed entries")
    for relative, prior in previous.items():
        if relative in configured_paths:
            continue
        remove_managed_config(target, prior, dry_run=dry_run, purge=False)
        print(f"  config {relative}: removed obsolete managed entries")
    return records


def adopt_configs(
    source: Source,
    target: Path,
    desired: dict[str, Any],
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for relative, config_format, template in desired_configs(source, desired):
        path = managed_path(target, relative)
        if not path.is_file():
            continue
        if config_format == "json":
            current = read_json(path)
            wanted = read_json(template)
        else:
            try:
                current = tomllib.loads(path.read_text(encoding="utf-8"))
                wanted = tomllib.loads(template.read_text(encoding="utf-8"))
            except tomllib.TOMLDecodeError as exc:
                raise LifecycleError(f"cannot adopt invalid TOML {path}: {exc}") from exc
        managed: list[dict[str, Any]] = []
        for parts, value in flatten_config(wanted):
            exists, present = get_nested(current, parts)
            if isinstance(value, list) and exists and isinstance(present, list):
                matching = [item for item in value if item in present]
                if matching:
                    managed.append(
                        {
                            "pointer": pointer(parts),
                            "kind": "list_items",
                            "items": matching,
                            "ownership": "adopted",
                        }
                    )
            elif exists and present == value:
                managed.append(
                    {
                        "pointer": pointer(parts),
                        "kind": "value",
                        "value": copy.deepcopy(value),
                        "ownership": "adopted",
                    }
                )
        if managed:
            records.append(
                {
                    "path": relative,
                    "format": config_format,
                    "managed": managed,
                    "created": False,
                }
            )
            print(f"  adopted {len(managed)} matching entries from {relative}")
    return records


def apply_artifact(
    artifact: Artifact,
    target: Path,
    previous: dict[str, Any] | None,
    *,
    adopt_only: bool,
    dry_run: bool,
) -> dict[str, Any] | None:
    destination = managed_path(target, artifact.destination)
    incoming_hash = sha256_path(artifact.source)

    if previous:
        if not destination.exists() and not destination.is_symlink():
            if previous.get("ownership") == "adopted":
                print(f"  preserved missing adopted {artifact.destination}")
                return previous
            if adopt_only:
                print(f"  missing {artifact.destination}: not adopted")
                return None
            copy_path(artifact.source, destination, dry_run)
            print(f"  restored {artifact.destination}")
            return {
                "path": artifact.destination,
                "source": artifact.source_label,
                "sha256": incoming_hash,
                "ownership": "owned",
            }
        current_hash = sha256_path(destination)
        if previous.get("ownership") == "adopted":
            if current_hash != incoming_hash and not adopt_only:
                stage_conflict(artifact.source, target, artifact.destination, dry_run)
                print(f"  conflict {artifact.destination}: preserved adopted file")
            return previous
        if current_hash == previous.get("sha256"):
            if current_hash != incoming_hash and not adopt_only:
                if artifact.destination in REVIEW_REQUIRED_ARTIFACTS:
                    stage_conflict(
                        artifact.source,
                        target,
                        artifact.destination,
                        dry_run,
                    )
                    print(
                        f"  review required {artifact.destination}: "
                        "preserved active workflow"
                    )
                    return previous
                backup_path(target, artifact.destination, dry_run)
                copy_path(artifact.source, destination, dry_run)
                print(f"  upgraded {artifact.destination}")
            return {
                "path": artifact.destination,
                "source": artifact.source_label,
                "sha256": incoming_hash if not adopt_only else current_hash,
                "ownership": previous.get("ownership", "owned"),
            }
        if incoming_hash == current_hash:
            return {
                "path": artifact.destination,
                "source": artifact.source_label,
                "sha256": current_hash,
                "ownership": previous.get("ownership", "owned"),
            }
        if not adopt_only:
            stage_conflict(artifact.source, target, artifact.destination, dry_run)
            print(f"  conflict {artifact.destination}: preserved modified file")
        else:
            print(f"  different {artifact.destination}: not adopted")
        return previous

    if destination.exists() or destination.is_symlink():
        current_hash = sha256_path(destination)
        if current_hash == incoming_hash:
            print(f"  adopted {artifact.destination}")
            return {
                "path": artifact.destination,
                "source": artifact.source_label,
                "sha256": current_hash,
                "ownership": "adopted",
            }
        if not adopt_only:
            stage_conflict(artifact.source, target, artifact.destination, dry_run)
            print(f"  conflict {artifact.destination}: preserved existing file")
        else:
            print(f"  different {artifact.destination}: not adopted")
        return None

    if adopt_only:
        return None
    copy_path(artifact.source, destination, dry_run)
    print(f"  installed {artifact.destination}")
    return {
        "path": artifact.destination,
        "source": artifact.source_label,
        "sha256": incoming_hash,
        "ownership": "owned",
    }


def remove_obsolete_artifact(
    target: Path, record: dict[str, Any], dry_run: bool
) -> None:
    destination = managed_path(target, str(record["path"]))
    if not destination.exists() and not destination.is_symlink():
        return
    if record.get("ownership") != "owned":
        print(f"  preserved adopted {record['path']}")
        return
    if sha256_path(destination) != record.get("sha256"):
        print(f"  preserved modified {record['path']}")
        return
    if not dry_run:
        remove_path(destination)
    print(f"  removed obsolete {record['path']}")


def build_desired(
    source: Source,
    harnesses: list[str],
    profiles: list[str],
    *,
    global_scope: bool,
    agents: bool,
    configs: bool,
    workflow_foundations: bool,
    notifications: bool,
) -> dict[str, Any]:
    repository = str(
        source.manifest.get("repository", DEFAULT_REPOSITORY)
    )
    channel = str(source.manifest.get("default_channel", "stable"))
    return {
        "schema": SCHEMA,
        "scope": "global" if global_scope else "project",
        "source": {"repository": repository, "channel": channel},
        "harnesses": validate_harnesses(harnesses),
        "profiles": validate_profiles(source, profiles),
        "features": {
            "agents": agents,
            "configs": configs,
            "notifications": notifications,
            "workflow_foundations": workflow_foundations,
        },
    }


def load_desired(
    target: Path,
    global_scope: bool = False,
) -> dict[str, Any]:
    name = desired_state_name(global_scope)
    path = managed_path(target, name)
    if not path.is_file():
        raise LifecycleError(f"{name} is missing; run install or adopt")
    desired = read_json(path)
    if desired.get("schema") != SCHEMA:
        raise LifecycleError(
            f"unsupported desired-state schema {desired.get('schema')!r}"
        )
    if desired_is_global(desired) != global_scope:
        expected = "global" if global_scope else "project"
        raise LifecycleError(
            f"desired state does not describe a {expected} installation"
        )
    return desired


def load_lock(
    target: Path,
    global_scope: bool = False,
) -> dict[str, Any]:
    path = managed_path(target, lock_state_name(global_scope))
    if not path.is_file():
        return {"schema": SCHEMA, "artifacts": [], "configs": []}
    lock = read_json(path)
    if lock.get("schema") != SCHEMA:
        raise LifecycleError(f"unsupported lock schema {lock.get('schema')!r}")
    if "package_version" in lock:
        validate_version(lock["package_version"])
    artifacts = lock.get("artifacts", [])
    configs = lock.get("configs", [])
    if not isinstance(artifacts, list) or not isinstance(configs, list):
        raise LifecycleError("lock artifacts and configs must be lists")
    patterns = (
        GLOBAL_MANAGED_ARTIFACT_PATTERNS
        if global_scope
        else PROJECT_MANAGED_ARTIFACT_PATTERNS
    )
    for record in artifacts:
        if not isinstance(record, dict):
            raise LifecycleError("lock artifact entries must be objects")
        relative = record.get("path")
        if not isinstance(relative, str) or not any(
            pattern.fullmatch(relative)
            for pattern in patterns
        ):
            raise LifecycleError(
                f"lock artifact path is outside managed namespaces: {relative!r}"
            )
        if not re.fullmatch(r"[0-9a-f]{64}", str(record.get("sha256", ""))):
            raise LifecycleError(f"lock artifact has invalid checksum: {relative}")
        if record.get("ownership") not in {"owned", "adopted"}:
            raise LifecycleError(f"lock artifact has invalid ownership: {relative}")
    if global_scope and configs:
        raise LifecycleError("global lock cannot manage harness configuration")
    for config in configs:
        if not isinstance(config, dict):
            raise LifecycleError("lock config entries must be objects")
        relative = config.get("path")
        allowed = ALLOWED_CONFIG_VALUES.get(str(relative))
        expected_format = "toml" if relative == ".codex/config.toml" else "json"
        if allowed is None or config.get("format") != expected_format:
            raise LifecycleError(
                f"lock config path is outside managed destinations: {relative!r}"
            )
        managed = config.get("managed", [])
        if not isinstance(managed, list):
            raise LifecycleError(f"lock config has invalid managed entries: {relative}")
        for entry in managed:
            if not isinstance(entry, dict):
                raise LifecycleError(f"lock config entry is invalid: {relative}")
            key = entry.get("pointer")
            if key not in allowed:
                raise LifecycleError(
                    f"lock config pointer is not managed: {relative}{key}"
                )
            approved = allowed[str(key)]
            if entry.get("kind") == "value":
                recorded = entry.get("value")
                valid_value = (
                    isinstance(approved, list)
                    and isinstance(recorded, list)
                    and all(item in approved for item in recorded)
                ) or (
                    not isinstance(approved, list)
                    and recorded == approved
                )
            elif entry.get("kind") == "list_items":
                items = entry.get("items")
                valid_value = (
                    isinstance(approved, list)
                    and isinstance(items, list)
                    and all(item in approved for item in items)
                )
            else:
                valid_value = False
            if not valid_value or entry.get("ownership", "owned") not in {
                "owned",
                "adopted",
            }:
                raise LifecycleError(
                    f"lock config entry is invalid: {relative}{key}"
                )
    return lock


def ensure_state_gitignore(target: Path, dry_run: bool) -> None:
    atomic_write(
        managed_path(target, f"{STATE_DIR}/.gitignore"),
        "*\n!.gitignore\n",
        dry_run,
    )


def preflight_configs(
    source: Source,
    target: Path,
    desired: dict[str, Any],
    old_lock: dict[str, Any],
) -> None:
    configured = desired_configs(source, desired)
    formats = {
        relative: config_format
        for relative, config_format, _ in configured
    }
    for relative, config_format, template in configured:
        if config_format == "json":
            read_json(template)
        else:
            try:
                tomllib.loads(template.read_text(encoding="utf-8"))
            except tomllib.TOMLDecodeError as exc:
                raise LifecycleError(
                    f"cannot read package TOML {template}: {exc}"
                ) from exc
    for previous in old_lock.get("configs", []):
        formats.setdefault(str(previous["path"]), str(previous["format"]))
    for relative, config_format in formats.items():
        path = managed_path(target, relative)
        if path.is_symlink() or (path.exists() and not path.is_file()):
            raise LifecycleError(
                f"config destination is not a regular file: {path}"
            )
        if not path.is_file():
            continue
        if config_format == "json":
            read_json(path)
        else:
            try:
                tomllib.loads(path.read_text(encoding="utf-8"))
            except tomllib.TOMLDecodeError as exc:
                raise LifecycleError(f"cannot merge invalid TOML {path}: {exc}") from exc


def reconcile(
    source: Source,
    target: Path,
    desired: dict[str, Any],
    *,
    adopt_only: bool = False,
    dry_run: bool = False,
) -> dict[str, Any]:
    global_scope = desired_is_global(desired)
    old_lock = load_lock(target, global_scope)
    preflight_configs(source, target, desired, old_lock)
    previous = {
        record["path"]: record for record in old_lock.get("artifacts", [])
    }
    wanted_artifacts = desired_artifacts(
        source, desired, include_manager=not adopt_only
    )
    wanted_paths = {artifact.destination for artifact in wanted_artifacts}
    records: list[dict[str, Any]] = []
    for artifact in wanted_artifacts:
        record = apply_artifact(
            artifact,
            target,
            previous.get(artifact.destination),
            adopt_only=adopt_only,
            dry_run=dry_run,
        )
        if record:
            records.append(record)

    if not adopt_only:
        for relative, record in previous.items():
            if relative not in wanted_paths:
                remove_obsolete_artifact(target, record, dry_run)
        configs = apply_configs(source, target, desired, old_lock, dry_run)
    else:
        configs = adopt_configs(source, target, desired)

    lock = {
        "schema": SCHEMA,
        "package_version": source.manifest["version"],
        "source_revision": source.revision,
        "source_digest": source.content_digest,
        "resolved_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "artifacts": records,
        "configs": configs,
    }
    ensure_state_gitignore(target, dry_run)
    write_json(
        managed_path(target, desired_state_name(global_scope)),
        desired,
        dry_run,
    )
    write_json(
        managed_path(target, lock_state_name(global_scope)),
        lock,
        dry_run,
    )
    return lock


def uninstall_json_config(
    path: Path,
    records: list[dict[str, Any]],
    dry_run: bool,
    purge: bool,
) -> None:
    if not path.is_file():
        return
    current = read_json(path)
    for record in reversed(records):
        if record.get("ownership") == "adopted" and not purge:
            continue
        parts = pointer_parts(record["pointer"])
        exists, present = get_nested(current, parts)
        if not exists:
            continue
        if record.get("kind") == "value" and present == record.get("value"):
            delete_nested(current, parts)
        elif record.get("kind") == "list_items" and isinstance(present, list):
            for item in record.get("items", []):
                if item in present:
                    present.remove(item)
            if not present:
                delete_nested(current, parts)
    write_json(path, current, dry_run)


def uninstall_toml_config(
    path: Path,
    records: list[dict[str, Any]],
    dry_run: bool,
    purge: bool,
) -> None:
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    try:
        current = tomllib.loads(text)
    except tomllib.TOMLDecodeError as exc:
        raise LifecycleError(f"cannot uninstall from invalid TOML {path}: {exc}") from exc
    for record in reversed(records):
        if record.get("ownership") == "adopted" and not purge:
            continue
        parts = pointer_parts(record["pointer"])
        exists, present = get_nested(current, parts)
        if exists and present == record.get("value"):
            text = remove_toml_key(text, parts)
            delete_nested(current, parts)
    atomic_write(path, text, dry_run)


def config_has_values(value: Any) -> bool:
    if isinstance(value, dict):
        return any(config_has_values(child) for child in value.values())
    return True


def remove_managed_config(
    target: Path,
    config: dict[str, Any],
    *,
    dry_run: bool,
    purge: bool,
) -> None:
    path = managed_path(target, str(config["path"]))
    if config.get("format") == "json":
        uninstall_json_config(
            path, config.get("managed", []), dry_run, purge
        )
        if (
            config.get("created")
            and path.is_file()
            and not read_json(path)
            and not dry_run
        ):
            path.unlink()
    else:
        uninstall_toml_config(
            path, config.get("managed", []), dry_run, purge
        )
        if config.get("created") and path.is_file() and not dry_run:
            parsed = tomllib.loads(path.read_text(encoding="utf-8"))
            if not config_has_values(parsed):
                path.unlink()


def command_install(args: argparse.Namespace, source: Source, target: Path) -> int:
    if not args.global_scope and not managed_path(target, "AGENTS.md").is_file():
        raise LifecycleError(
            "AGENTS.md is missing; start from AI_ONBOARD/templates/AGENTS.md"
        )
    if args.global_scope and args.configs:
        raise LifecycleError("--configs is available only for project installs")
    if args.global_scope and args.notifications:
        raise LifecycleError(
            "--notifications is available only for project installs"
        )
    harnesses = split_csv(args.harness) or list(SUPPORTED_HARNESSES)
    profiles = split_csv(args.profile) or ["core"]
    desired = build_desired(
        source,
        harnesses,
        profiles,
        global_scope=args.global_scope,
        agents=args.agents,
        configs=args.configs,
        workflow_foundations=args.workflow_foundations,
        notifications=args.notifications,
    )
    print(
        f"Installing AI_ONBOARD {source.manifest['version']} "
        f"{'globally ' if args.global_scope else ''}"
        f"for {', '.join(desired['harnesses'])}"
    )
    reconcile(source, target, desired, dry_run=args.dry_run)
    if args.global_scope:
        launcher = managed_path(target, GLOBAL_LAUNCHER)
        print(f"Global launcher: {launcher}")
        if str(launcher.parent) not in os.environ.get("PATH", "").split(os.pathsep):
            print(
                f"  add {launcher.parent} to PATH to run 'ai-onboard'",
                file=sys.stderr,
            )
    return 0


def command_adopt(args: argparse.Namespace, source: Source, target: Path) -> int:
    if not args.global_scope and not managed_path(target, "AGENTS.md").is_file():
        raise LifecycleError(
            "AGENTS.md is missing; adoption requires the project's shared contract"
        )
    if args.global_scope and args.configs:
        raise LifecycleError("--configs is available only for project installs")
    if args.global_scope and args.notifications:
        raise LifecycleError(
            "--notifications is available only for project installs"
        )
    harnesses = split_csv(args.harness) or list(SUPPORTED_HARNESSES)
    profiles = split_csv(args.profile) or ["core"]
    desired = build_desired(
        source,
        harnesses,
        profiles,
        global_scope=args.global_scope,
        agents=args.agents,
        configs=args.configs,
        workflow_foundations=args.workflow_foundations,
        notifications=args.notifications,
    )
    print("Adopting exact existing AI_ONBOARD artifacts; no product files are changed")
    reconcile(source, target, desired, adopt_only=True, dry_run=args.dry_run)
    return 0


def command_sync(
    args: argparse.Namespace, source: Source, target: Path, label: str = "Syncing"
) -> int:
    desired = load_desired(target, args.global_scope)
    validate_harnesses(list(desired.get("harnesses", [])))
    validate_profiles(source, list(desired.get("profiles", [])))
    print(f"{label} AI_ONBOARD {source.manifest['version']}")
    reconcile(source, target, desired, dry_run=args.dry_run)
    if not args.dry_run:
        managed_path(target, UPDATE_STATUS_NAME).unlink(missing_ok=True)
    return 0


def display_text(value: object, limit: int = 280) -> str:
    text = "".join(
        character
        for character in str(value)
        if ord(character) >= 32 and not 127 <= ord(character) <= 159
    )
    return " ".join(text.split())[:limit]


def release_metadata(source: Source) -> dict[str, str]:
    raw = source.manifest.get("release", {})
    if not isinstance(raw, dict):
        raise LifecycleError("package release metadata must be an object")
    classification = str(raw.get("classification", "maintenance")).lower()
    if classification not in RELEASE_CLASSIFICATIONS:
        raise LifecycleError(
            "package release classification must be fix, security, feature, "
            "or maintenance"
        )
    summary = display_text(raw.get("summary", ""))
    notes_url = display_text(raw.get("notes_url", ""), 2048)
    if notes_url:
        parsed = urllib.parse.urlparse(notes_url)
        if parsed.scheme != "https" or not parsed.netloc:
            raise LifecycleError("package release notes URL must use HTTPS")
    return {
        "classification": classification,
        "summary": summary,
        "notes_url": notes_url,
    }


def build_update_status(
    old: dict[str, Any], source: Source
) -> dict[str, Any]:
    changed = (
        old.get("package_version") != source.manifest.get("version")
        or old.get("source_revision") != source.revision
        or old.get("source_digest") != source.content_digest
    )
    checked_at = (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )
    return {
        "schema": SCHEMA,
        "checked_at": checked_at,
        "update_available": changed,
        "current": {
            "version": str(old.get("package_version", "none")),
            "revision": str(old.get("source_revision", "")),
            "digest": str(old.get("source_digest", "")),
        },
        "latest": {
            "version": str(source.manifest.get("version", "unknown")),
            "revision": source.revision,
            "digest": source.content_digest,
        },
        "release": release_metadata(source),
    }


def print_update_status(status: dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(status, sort_keys=True))
        return
    current = status["current"]
    latest = status["latest"]
    current_version = display_text(current["version"], 64)
    latest_version = display_text(latest["version"], 64)
    print(
        f"Update {'available' if status['update_available'] else 'not needed'}: "
        f"{current_version} -> {latest_version}"
    )
    if status["update_available"]:
        release = status["release"]
        label = str(release["classification"]).capitalize()
        if release["summary"]:
            print(f"{label}: {release['summary']}")
        if release["notes_url"]:
            print(f"Release notes: {release['notes_url']}")


def send_update_notification(status: dict[str, Any]) -> None:
    if not status.get("update_available"):
        return
    release = status["release"]
    latest = status["latest"]
    title = "AI_ONBOARD update available"
    classification = display_text(release["classification"], 32).capitalize()
    latest_version = display_text(latest["version"], 64)
    summary = display_text(release["summary"])
    message = (
        f"{classification} {latest_version}: "
        f"{summary or 'Review the available update.'}"
    )
    if sys.platform == "darwin" and shutil.which("osascript"):
        script = (
            "on run argv\n"
            "display notification (item 1 of argv) with title (item 2 of argv)\n"
            "end run"
        )
        subprocess.run(
            ["osascript", "-e", script, message, title],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return
    if sys.platform.startswith("linux") and shutil.which("notify-send"):
        subprocess.run(
            ["notify-send", title, message],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return
    print(
        "Desktop notification unavailable; the update result was still recorded.",
        file=sys.stderr,
    )


def show_cached_update_status(target: Path) -> None:
    path = managed_path(target, UPDATE_STATUS_NAME)
    if not path.exists():
        return
    if not path.is_file():
        print(f"  warning: update status is not a regular file: {path}")
        return
    try:
        status = read_json(path)
    except LifecycleError as exc:
        print(f"  warning: {exc}")
        return
    if status.get("schema") != SCHEMA:
        print("  warning: cached update status has an unsupported schema")
        return
    if status.get("update_available") is not True:
        return
    latest = status.get("latest")
    release = status.get("release")
    if not isinstance(latest, dict) or not isinstance(release, dict):
        print("  warning: cached update status has invalid fields")
        return
    try:
        version = validate_version(latest.get("version"))
    except LifecycleError as exc:
        print(f"  warning: cached update status has {exc}")
        return
    classification = display_text(
        release.get("classification", "maintenance"), 32
    ).lower()
    if classification not in RELEASE_CLASSIFICATIONS:
        print("  warning: cached update status has invalid classification")
        return
    print(f"Update available: {version} ({classification})")
    summary = display_text(release.get("summary", ""))
    if summary:
        print(f"  {summary}")
    notes_url = display_text(release.get("notes_url", ""), 2048)
    if notes_url:
        parsed = urllib.parse.urlparse(notes_url)
        if parsed.scheme == "https" and parsed.netloc:
            print(f"  {notes_url}")
        else:
            print("  warning: cached release notes URL is invalid")


def macos_notifier_label(target: Path) -> str:
    identity = hashlib.sha256(str(target.resolve()).encode()).hexdigest()[:12]
    return f"{NOTIFIER_LABEL_PREFIX}.{identity}"


def remove_macos_update_notifier(
    target: Path,
    dry_run: bool,
) -> None:
    if sys.platform != "darwin":
        return
    label = macos_notifier_label(target)
    destination = (
        Path.home() / "Library" / "LaunchAgents" / f"{label}.plist"
    )
    if not destination.exists() and not destination.is_symlink():
        return
    if destination.is_symlink() or not destination.is_file():
        print(f"  preserved unexpected notifier path {destination}")
        return
    try:
        with destination.open("rb") as handle:
            payload = plistlib.load(handle)
    except (OSError, plistlib.InvalidFileException) as exc:
        print(f"  preserved unreadable notifier {destination}: {exc}")
        return
    expected_arguments = [
        str(target / f"{STATE_DIR}/bin/ai_onboard.py"),
        "--target",
        str(target),
        "upgrade",
        "--check",
        "--cache",
        "--notify",
    ]
    arguments = payload.get("ProgramArguments")
    if (
        payload.get("Label") != label
        or not isinstance(arguments, list)
        or len(arguments) != len(expected_arguments) + 1
        or arguments[1:] != expected_arguments
    ):
        print(f"  preserved unrecognized notifier {destination}")
        return
    if dry_run:
        print(f"  would remove macOS update notifier {label}")
        return
    service = f"gui/{os.getuid()}/{label}"
    try:
        subprocess.run(
            ["launchctl", "bootout", service],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        loaded = (
            subprocess.run(
                ["launchctl", "print", service],
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            ).returncode
            == 0
        )
    except OSError as exc:
        raise LifecycleError(
            f"cannot unload macOS update notifier {label}: {exc}"
        ) from exc
    if loaded:
        raise LifecycleError(
            f"macOS update notifier {label} remains loaded; "
            f"run 'launchctl bootout {service}' and retry"
        )
    destination.unlink(missing_ok=True)
    print(f"  removed macOS update notifier {label}")


def command_status(
    target: Path,
    verbose: bool = False,
    global_scope: bool = False,
) -> int:
    desired_exists = managed_path(
        target, desired_state_name(global_scope)
    ).is_file()
    lock_exists = managed_path(target, lock_state_name(global_scope)).is_file()
    if not desired_exists or not lock_exists:
        location = "for this user" if global_scope else "in this project"
        print(f"AI_ONBOARD is not fully managed {location}")
        return 1
    lock = load_lock(target, global_scope)
    drift = 0
    clean = 0
    print(
        f"AI_ONBOARD {lock.get('package_version', 'unknown')} "
        f"({lock.get('source_revision', 'unknown')})"
    )
    for record in lock.get("artifacts", []):
        path = managed_path(target, str(record["path"]))
        if not path.exists() and not path.is_symlink():
            print(f"  missing  {record['path']}")
            drift += 1
        elif sha256_path(path) != record.get("sha256"):
            print(f"  modified {record['path']}")
            drift += 1
        else:
            clean += 1
            if verbose:
                print(f"  clean    {record['path']}")
    for config in lock.get("configs", []):
        path = managed_path(target, str(config["path"]))
        config_drift = False
        if not path.is_file():
            config_drift = True
        else:
            try:
                current = (
                    read_json(path)
                    if config.get("format") == "json"
                    else tomllib.loads(path.read_text(encoding="utf-8"))
                )
            except (LifecycleError, OSError, tomllib.TOMLDecodeError):
                config_drift = True
            else:
                for entry in config.get("managed", []):
                    exists, present = get_nested(
                        current, pointer_parts(entry["pointer"])
                    )
                    if entry.get("kind") == "value":
                        matches = exists and present == entry.get("value")
                    else:
                        matches = (
                            exists
                            and isinstance(present, list)
                            and all(
                                item in present
                                for item in entry.get("items", [])
                            )
                        )
                    if not matches:
                        config_drift = True
                        break
        if config_drift:
            print(f"  modified config {config['path']}")
            drift += 1
        else:
            clean += 1
            if verbose:
                print(f"  clean    config {config['path']}")
    print(f"Status: {clean} clean, {drift} drifted managed item(s)")
    return 1 if drift else 0


def command_doctor(target: Path, global_scope: bool = False) -> int:
    issues = 0
    try:
        desired = load_desired(target, global_scope)
        validate_harnesses(list(desired.get("harnesses", [])))
    except LifecycleError as exc:
        print(f"  error: {exc}")
        issues += 1
    try:
        load_lock(target, global_scope)
    except LifecycleError as exc:
        print(f"  error: {exc}")
        issues += 1
    status = command_status(target, global_scope=global_scope)
    issues += status
    show_cached_update_status(target)
    conflicts = managed_path(target, f"{STATE_DIR}/conflicts")
    if conflicts.is_dir() and any(path.is_file() for path in conflicts.rglob("*")):
        print(f"  warning: unresolved conflicts in {conflicts}")
    if issues:
        print(f"Doctor found {issues} issue(s)")
        return 1
    print("Doctor passed")
    return 0


def command_uninstall(args: argparse.Namespace, target: Path) -> int:
    global_scope = getattr(args, "global_scope", False)
    lock = load_lock(target, global_scope)
    for config in lock.get("configs", []):
        path = managed_path(target, str(config["path"]))
        if not path.is_file():
            continue
        if config.get("format") == "json":
            read_json(path)
        else:
            try:
                tomllib.loads(path.read_text(encoding="utf-8"))
            except tomllib.TOMLDecodeError as exc:
                raise LifecycleError(
                    f"cannot uninstall from invalid TOML {path}: {exc}"
                ) from exc
    print("Uninstalling managed AI_ONBOARD artifacts")
    if not global_scope:
        remove_macos_update_notifier(target, dry_run=args.dry_run)
    update_status = managed_path(target, UPDATE_STATUS_NAME)
    if update_status.is_symlink() or update_status.is_file():
        if not args.dry_run:
            update_status.unlink(missing_ok=True)
        print(f"  removed {UPDATE_STATUS_NAME}")
    elif update_status.exists():
        print(f"  preserved unexpected update status path {update_status}")
    for record in sorted(
        lock.get("artifacts", []),
        key=lambda item: len(str(item.get("path", ""))),
        reverse=True,
    ):
        destination = managed_path(target, str(record["path"]))
        if not destination.exists() and not destination.is_symlink():
            continue
        ownership = record.get("ownership")
        unchanged = sha256_path(destination) == record.get("sha256")
        if ownership == "owned" and unchanged:
            if not args.dry_run:
                remove_path(destination)
            print(f"  removed {record['path']}")
        elif ownership == "adopted" and unchanged and args.purge:
            if not args.dry_run:
                remove_path(destination)
            print(f"  purged adopted {record['path']}")
        elif not unchanged:
            print(f"  preserved modified {record['path']}")
        else:
            print(f"  preserved adopted {record['path']}")

    for config in lock.get("configs", []):
        remove_managed_config(
            target,
            config,
            dry_run=args.dry_run,
            purge=args.purge,
        )
        print(f"  removed unchanged managed keys from {config['path']}")

    if not args.dry_run:
        managed_path(
            target, lock_state_name(global_scope)
        ).unlink(missing_ok=True)
        if args.purge:
            managed_path(
                target, desired_state_name(global_scope)
            ).unlink(missing_ok=True)
    print(
        "Desired state preserved; use --purge to remove it"
        if not args.purge
        else "Managed desired state purged"
    )
    return 0


def command_cleanup(args: argparse.Namespace, target: Path) -> int:
    backups = managed_path(target, f"{STATE_DIR}/backups")
    releases = sorted(
        [path for path in backups.iterdir() if path.is_dir()]
        if backups.is_dir()
        else []
    )
    remove = releases[: max(0, len(releases) - args.keep_releases)]
    for path in remove:
        if not args.dry_run:
            shutil.rmtree(path)
        print(f"  removed backup {path.name}")
    print(f"Cleanup kept {min(len(releases), args.keep_releases)} backup set(s)")
    return 0


def command_profile(
    args: argparse.Namespace, source: Source, target: Path
) -> int:
    desired = load_desired(target, args.global_scope)
    profiles = list(desired.get("profiles", []))
    available = source.manifest.get("profiles", {})
    if args.name not in available:
        raise LifecycleError(f"unknown profile {args.name!r}")
    if args.action == "add" and args.name not in profiles:
        profiles.append(args.name)
    elif args.action == "remove" and args.name in profiles:
        profiles.remove(args.name)
    if not profiles:
        raise LifecycleError("at least one profile must remain installed")
    desired["profiles"] = sorted(profiles)
    write_json(
        managed_path(target, desired_state_name(args.global_scope)),
        desired,
        args.dry_run,
    )
    print(f"Profile {args.action}: {args.name}")
    reconcile(source, target, desired, dry_run=args.dry_run)
    return 0


def add_install_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--harness",
        action="append",
        help="Comma-separated harnesses: claude,codex,opencode",
    )
    parser.add_argument(
        "--profile",
        action="append",
        help="Comma-separated capability profiles (default: core)",
    )
    parser.add_argument("--agents", action="store_true")
    parser.add_argument("--configs", action="store_true")
    parser.add_argument(
        "--notifications",
        action="store_true",
        help="Install slash-command, scheduled-check, and notifier assets",
    )
    parser.add_argument("--workflow-foundations", action="store_true")
    parser.add_argument("--dry-run", action="store_true")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Install, upgrade, inspect, and remove AI_ONBOARD safely."
    )
    parser.add_argument(
        "--target",
        help=(
            "Project root, or alternate home root with --global "
            "(default: current directory or $HOME)"
        ),
    )
    scope = parser.add_mutually_exclusive_group()
    scope.add_argument(
        "--global",
        dest="global_scope",
        action="store_true",
        help="Manage a user-global installation across repositories",
    )
    scope.add_argument(
        "--project",
        dest="global_scope",
        action="store_false",
        help="Manage a project installation",
    )
    parser.set_defaults(global_scope=None)
    parser.add_argument(
        "--source",
        help="AI_ONBOARD source checkout; otherwise use the local package or configured remote",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    install = subparsers.add_parser("install")
    add_install_options(install)
    adopt = subparsers.add_parser("adopt")
    add_install_options(adopt)

    for name in ("sync", "upgrade"):
        command = subparsers.add_parser(name)
        command.add_argument("--check", action="store_true")
        command.add_argument(
            "--json",
            action="store_true",
            help="Emit a machine-readable update result (with --check)",
        )
        command.add_argument(
            "--cache",
            action="store_true",
            help="Save the update result for doctor (with --check)",
        )
        command.add_argument(
            "--notify",
            action="store_true",
            help="Send a desktop notice when an update exists (with --check)",
        )
        command.add_argument(
            "--exit-code",
            action="store_true",
            help=f"Return {UPDATE_AVAILABLE_EXIT} when an update exists",
        )
        command.add_argument("--dry-run", action="store_true")

    status = subparsers.add_parser("status")
    status.add_argument("--verbose", action="store_true")
    subparsers.add_parser("doctor")

    check_git = subparsers.add_parser(
        "check-git",
        help="Require GitHub no-reply author and committer identities",
    )
    check_git_scope = check_git.add_mutually_exclusive_group()
    check_git_scope.add_argument(
        "--identity-only",
        action="store_true",
        help="Check only the effective Git author and committer process",
    )
    check_git_scope.add_argument(
        "--history-only",
        action="store_true",
        help="Check only commits reachable from local Git refs",
    )
    check_git_scope.add_argument(
        "--pre-push",
        action="store_true",
        help="Check exact outgoing ranges supplied by a Git pre-push hook",
    )

    uninstall = subparsers.add_parser("uninstall")
    uninstall.add_argument("--purge", action="store_true")
    uninstall.add_argument("--dry-run", action="store_true")

    cleanup = subparsers.add_parser("cleanup")
    cleanup.add_argument("--keep-releases", type=int, default=2)
    cleanup.add_argument("--dry-run", action="store_true")

    profile = subparsers.add_parser("profile")
    profile.add_argument("action", choices=("add", "remove"))
    profile.add_argument("name")
    profile.add_argument("--dry-run", action="store_true")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.global_scope is None:
        args.global_scope = invoked_from_global_launcher()
    if args.target:
        target = Path(args.target).resolve()
    elif args.command == "check-git":
        target = Path.cwd().resolve()
    else:
        target = (
            Path.home().resolve()
            if args.global_scope
            else Path.cwd().resolve()
        )

    try:
        if not target.is_dir():
            raise LifecycleError(
                f"target project directory does not exist: {target}"
            )
        if args.command == "status":
            return command_status(
                target,
                args.verbose,
                global_scope=args.global_scope,
            )
        if args.command == "doctor":
            return command_doctor(target, args.global_scope)
        if args.command == "check-git":
            return command_check_git(
                target,
                identity_only=args.identity_only,
                history_only=args.history_only,
                pre_push=args.pre_push,
            )
        if args.command == "uninstall":
            return command_uninstall(args, target)
        if args.command == "cleanup":
            if args.keep_releases < 0:
                raise LifecycleError("--keep-releases must be non-negative")
            return command_cleanup(args, target)

        use_locked = args.command in {"sync", "profile"} and not args.source
        with resolve_source(
            args.source,
            target,
            global_scope=args.global_scope,
            use_locked_revision=use_locked,
        ) as source:
            if args.command == "install":
                return command_install(args, source, target)
            if args.command == "adopt":
                return command_adopt(args, source, target)
            if args.command == "profile":
                return command_profile(args, source, target)
            if args.command in {"sync", "upgrade"}:
                check_options = (
                    args.json or args.cache or args.notify or args.exit_code
                )
                if check_options and not args.check:
                    raise LifecycleError(
                        "--json, --cache, --notify, and --exit-code require --check"
                    )
                old = load_lock(target, args.global_scope)
                if (
                    args.command == "sync"
                    and old.get("source_digest")
                    and old.get("source_digest") != source.content_digest
                ):
                    raise LifecycleError(
                        "locked source content does not match its recorded digest"
                    )
                if args.check:
                    status = build_update_status(old, source)
                    if args.cache:
                        write_json(
                            managed_path(target, UPDATE_STATUS_NAME), status
                        )
                    if args.notify:
                        send_update_notification(status)
                    print_update_status(status, args.json)
                    if args.exit_code and status["update_available"]:
                        return UPDATE_AVAILABLE_EXIT
                    return 0
                return command_sync(
                    args,
                    source,
                    target,
                    label="Upgrading" if args.command == "upgrade" else "Syncing",
                )
    except LifecycleError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
