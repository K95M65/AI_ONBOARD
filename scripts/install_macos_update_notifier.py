#!/usr/bin/env python3
"""Install or remove an opt-in macOS AI_ONBOARD update notifier."""

from __future__ import annotations

import argparse
import hashlib
import os
import plistlib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


INTERVALS = {
    "daily": 24 * 60 * 60,
    "weekly": 7 * 24 * 60 * 60,
}


def project_identity(target: Path) -> str:
    return hashlib.sha256(str(target).encode()).hexdigest()[:12]


def launch_agent_label(target: Path) -> str:
    return f"com.rsthrives.ai-onboard-update.{project_identity(target)}"


def launch_agent(target: Path, interval: str) -> tuple[str, dict[str, object]]:
    manager = target / ".ai-onboard/bin/ai_onboard.py"
    if not manager.is_file():
        raise ValueError(
            "installed manager is missing; install AI_ONBOARD notifications first"
        )
    label = launch_agent_label(target)
    logs = target / ".ai-onboard/logs"
    payload: dict[str, object] = {
        "Label": label,
        "ProgramArguments": [
            sys.executable,
            str(manager),
            "--target",
            str(target),
            "upgrade",
            "--check",
            "--cache",
            "--notify",
        ],
        "RunAtLoad": True,
        "StartInterval": INTERVALS[interval],
        "StandardOutPath": str(logs / "update-check.log"),
        "StandardErrorPath": str(logs / "update-check-error.log"),
        "ProcessType": "Background",
    }
    return label, payload


def plist_path(home: Path, label: str) -> Path:
    return home / "Library/LaunchAgents" / f"{label}.plist"


def launchctl(*arguments: str, check: bool = True) -> int:
    process = subprocess.run(
        ["launchctl", *arguments],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if check and process.returncode:
        raise RuntimeError(f"launchctl {' '.join(arguments)} failed")
    return process.returncode


def atomic_write_plist(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.tmp-", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        os.fchmod(descriptor, 0o600)
        with os.fdopen(descriptor, "wb") as handle:
            plistlib.dump(payload, handle, sort_keys=True)
        os.replace(temporary, path)
    finally:
        try:
            os.close(descriptor)
        except OSError:
            pass
        temporary.unlink(missing_ok=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Manage the opt-in macOS AI_ONBOARD update notifier."
    )
    parser.add_argument("action", choices=("install", "uninstall", "status"))
    parser.add_argument("--target", default=".", help="Managed project root")
    parser.add_argument(
        "--interval", choices=tuple(INTERVALS), default="weekly"
    )
    parser.add_argument("--dry-run", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if sys.platform != "darwin":
        print("error: the LaunchAgent notifier is available only on macOS", file=sys.stderr)
        return 2
    if not shutil.which("launchctl"):
        print("error: launchctl is unavailable", file=sys.stderr)
        return 2

    target = Path(args.target).resolve()
    home = Path.home()
    label = launch_agent_label(target)
    destination = plist_path(home, label)
    domain = f"gui/{os.getuid()}"

    if args.action == "status":
        loaded = launchctl("print", f"{domain}/{label}", check=False) == 0
        print(
            f"{'loaded' if loaded else 'not loaded'}: {label}"
            f" ({destination})"
        )
        return 0 if loaded else 1

    if args.action == "uninstall":
        print(f"Uninstall {label} from {destination}")
        if args.dry_run:
            return 0
        service = f"{domain}/{label}"
        launchctl("bootout", service, check=False)
        if launchctl("print", service, check=False) == 0:
            print(
                f"error: {label} remains loaded; plist preserved",
                file=sys.stderr,
            )
            return 2
        destination.unlink(missing_ok=True)
        return 0

    try:
        _, payload = launch_agent(target, args.interval)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(
        f"Install {label} with a {args.interval} update check at {destination}"
    )
    if args.dry_run:
        print(plistlib.dumps(payload, sort_keys=True).decode())
        return 0
    (target / ".ai-onboard/logs").mkdir(parents=True, exist_ok=True)
    atomic_write_plist(destination, payload)
    launchctl("bootout", f"{domain}/{label}", check=False)
    launchctl("bootstrap", domain, str(destination))
    print(
        "Notifier installed; AI_ONBOARD uninstall removes it automatically "
        "while the project stays at this path."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
