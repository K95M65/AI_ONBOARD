from __future__ import annotations

import json
import hashlib
import importlib.util
import io
import os
import plistlib
import subprocess
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
MANAGER = ROOT / "scripts" / "ai_onboard.py"
MANAGER_SPEC = importlib.util.spec_from_file_location(
    "ai_onboard_manager", MANAGER
)
assert MANAGER_SPEC and MANAGER_SPEC.loader
MANAGER_MODULE = importlib.util.module_from_spec(MANAGER_SPEC)
sys.modules[MANAGER_SPEC.name] = MANAGER_MODULE
MANAGER_SPEC.loader.exec_module(MANAGER_MODULE)
NOTIFIER = ROOT / "scripts" / "install_macos_update_notifier.py"
NOTIFIER_SPEC = importlib.util.spec_from_file_location(
    "ai_onboard_macos_notifier", NOTIFIER
)
assert NOTIFIER_SPEC and NOTIFIER_SPEC.loader
MACOS_NOTIFIER = importlib.util.module_from_spec(NOTIFIER_SPEC)
NOTIFIER_SPEC.loader.exec_module(MACOS_NOTIFIER)


class LifecycleManagerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        base = Path(self.temp.name)
        self.source = base / "source"
        self.target = base / "target"
        self.source.mkdir()
        self.target.mkdir()
        (self.target / "AGENTS.md").write_text("# User project\n", encoding="utf-8")
        self.make_source("1.0.0", "core v1")

    def make_source(self, version: str, core_body: str) -> None:
        manifest = {
            "schema": 1,
            "package": "ai-onboard",
            "version": version,
            "repository": "example/ai-onboard",
            "default_channel": "edge",
            "release": {
                "classification": "fix",
                "summary": f"Reliability fixes in {version}.",
                "notes_url": f"https://example.com/releases/{version}",
            },
            "profiles": {
                "core": {"categories": ["Engineering & delivery"]},
                "security": {"categories": ["Security & trust"]},
            },
        }
        catalog = {
            "skills": [
                {
                    "name": "core-tool",
                    "category": "Engineering & delivery",
                    "path": "skills/core-tool/SKILL.md",
                },
                {
                    "name": "security-tool",
                    "category": "Security & trust",
                    "path": "skills/security-tool/SKILL.md",
                },
            ]
        }
        self.write_json(self.source / "package-manifest.json", manifest)
        self.write_json(self.source / "site/data/catalog.json", catalog)
        self.write(self.source / "skills/core-tool/SKILL.md", core_body + "\n")
        self.write(self.source / "skills/security-tool/SKILL.md", "security v1\n")
        self.write(
            self.source / "agents/researcher.md",
            "---\nname: researcher\n---\nresearch v1\n",
        )
        self.write(
            self.source / "agents/codex/researcher.toml",
            'name = "researcher"\ndescription = "Research"\ndeveloper_instructions = "v1"\n',
        )
        self.write(
            self.source / "agents/opencode/researcher.md",
            "---\ndescription: Research\nmode: subagent\n---\nresearch v1\n",
        )
        self.write_json(
            self.source / "templates/configs/claude.settings.json",
            {
                "permissions": {
                    "deny": ["Read(./.env)", "Read(./secrets/**)"]
                },
                "skillOverrides": {
                    "goal-contract": "user-invocable-only"
                },
            },
        )
        self.write(
            self.source / "templates/configs/codex.config.toml",
            "[agents]\nmax_threads = 4\nmax_depth = 1\n",
        )
        self.write_json(
            self.source / "templates/configs/opencode.json",
            {
                "$schema": "https://opencode.ai/config.json",
                "compaction": {"auto": True, "prune": True, "reserved": 12000},
            },
        )
        self.write(
            self.source
            / "templates/commands/claude/ai-onboard-update.md",
            "Check AI_ONBOARD updates with the installed manager.\n",
        )
        self.write(
            self.source
            / "templates/commands/opencode/ai-onboard-update.md",
            "Check AI_ONBOARD updates with the installed manager.\n",
        )
        self.write(
            self.source
            / "templates/commands/codex/ai-onboard-update.md",
            "---\ndescription: Check AI_ONBOARD updates\n---\nCheck updates.\n",
        )
        self.write(
            self.source
            / "templates/notifications/github/ai-onboard-update-check.yml",
            "name: AI_ONBOARD update check\n",
        )
        self.write(
            self.source / "scripts/install_macos_update_notifier.py",
            "#!/usr/bin/env python3\nprint('fixture notifier')\n",
        )

    @staticmethod
    def write(path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    @classmethod
    def write_json(cls, path: Path, value: object) -> None:
        cls.write(path, json.dumps(value, indent=2) + "\n")

    def run_manager(
        self, *args: str, expected: int = 0
    ) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            [
                sys.executable,
                str(MANAGER),
                "--source",
                str(self.source),
                "--target",
                str(self.target),
                *args,
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(
            result.returncode,
            expected,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        return result

    def install_full_fixture(self) -> None:
        self.write_json(
            self.target / ".claude/settings.json",
            {"permissions": {"deny": ["UserRule"]}, "userSetting": True},
        )
        self.write(
            self.target / ".codex/config.toml",
            "[custom]\nenabled = true\n",
        )
        self.run_manager(
            "install",
            "--harness",
            "claude,codex,opencode",
            "--profile",
            "core",
            "--agents",
            "--configs",
        )

    def test_install_records_desired_state_and_preserves_user_config(self) -> None:
        self.install_full_fixture()

        self.assertTrue((self.target / ".claude/skills/core-tool").is_dir())
        self.assertTrue((self.target / ".agents/skills/core-tool").is_dir())
        self.assertFalse((self.target / ".agents/skills/security-tool").exists())
        self.assertTrue((self.target / ".claude/agents/researcher.md").is_file())
        self.assertTrue((self.target / ".codex/agents/researcher.toml").is_file())
        self.assertTrue((self.target / ".opencode/agents/researcher.md").is_file())

        desired = json.loads(
            (self.target / "ai-onboard.json").read_text(encoding="utf-8")
        )
        lock = json.loads(
            (self.target / ".ai-onboard.lock.json").read_text(encoding="utf-8")
        )
        self.assertEqual(desired["profiles"], ["core"])
        self.assertEqual(
            desired["harnesses"], ["claude", "codex", "opencode"]
        )
        self.assertEqual(lock["package_version"], "1.0.0")
        self.assertTrue(lock["artifacts"])

        claude = json.loads(
            (self.target / ".claude/settings.json").read_text(encoding="utf-8")
        )
        self.assertTrue(claude["userSetting"])
        self.assertEqual(
            claude["permissions"]["deny"],
            ["UserRule", "Read(./.env)", "Read(./secrets/**)"],
        )
        codex = (self.target / ".codex/config.toml").read_text(encoding="utf-8")
        self.assertIn("[custom]", codex)
        self.assertIn("[agents]", codex)

    def test_upgrade_stages_conflict_instead_of_overwriting_modified_skill(
        self,
    ) -> None:
        self.install_full_fixture()
        installed = self.target / ".agents/skills/core-tool/SKILL.md"
        installed.write_text("user customization\n", encoding="utf-8")
        self.make_source("1.1.0", "core v2")

        result = self.run_manager("upgrade")

        self.assertIn("conflict", result.stdout.lower())
        self.assertEqual(
            installed.read_text(encoding="utf-8"), "user customization\n"
        )
        conflict = (
            self.target
            / ".ai-onboard/conflicts/.agents/skills/core-tool/SKILL.md"
        )
        self.assertEqual(conflict.read_text(encoding="utf-8"), "core v2\n")

    def test_uninstall_removes_only_unchanged_owned_artifacts(self) -> None:
        self.install_full_fixture()
        modified_agent = self.target / ".claude/agents/researcher.md"
        modified_agent.write_text("user agent\n", encoding="utf-8")

        result = self.run_manager("uninstall")

        self.assertIn("preserved modified", result.stdout.lower())
        self.assertFalse((self.target / ".agents/skills/core-tool").exists())
        self.assertTrue(modified_agent.exists())
        self.assertTrue((self.target / "AGENTS.md").exists())
        claude = json.loads(
            (self.target / ".claude/settings.json").read_text(encoding="utf-8")
        )
        self.assertEqual(claude["permissions"]["deny"], ["UserRule"])
        self.assertTrue(claude["userSetting"])

    def test_adopt_marks_identical_existing_copy_without_claiming_removal(
        self,
    ) -> None:
        destination = self.target / ".agents/skills/core-tool/SKILL.md"
        self.write(destination, "core v1\n")

        self.run_manager(
            "adopt",
            "--harness",
            "codex",
            "--profile",
            "core",
        )
        lock = json.loads(
            (self.target / ".ai-onboard.lock.json").read_text(encoding="utf-8")
        )
        matching = [
            artifact
            for artifact in lock["artifacts"]
            if artifact["path"] == ".agents/skills/core-tool"
        ]
        self.assertEqual(matching[0]["ownership"], "adopted")

        self.run_manager("uninstall")
        self.assertTrue(destination.exists())

    def test_profile_add_syncs_only_new_capability(self) -> None:
        self.run_manager(
            "install",
            "--harness",
            "codex",
            "--profile",
            "core",
        )

        self.run_manager("profile", "add", "security")

        self.assertTrue((self.target / ".agents/skills/security-tool").is_dir())
        desired = json.loads(
            (self.target / "ai-onboard.json").read_text(encoding="utf-8")
        )
        self.assertEqual(desired["profiles"], ["core", "security"])

    def test_status_detects_drift_and_cleanup_keeps_newest_backup(self) -> None:
        self.run_manager(
            "install",
            "--harness",
            "codex",
            "--profile",
            "core",
        )
        installed = self.target / ".agents/skills/core-tool/SKILL.md"
        installed.write_text("drift\n", encoding="utf-8")

        result = self.run_manager("status", expected=1)
        self.assertIn("modified", result.stdout.lower())

        self.write(self.target / ".ai-onboard/backups/001/old.txt", "old")
        self.write(self.target / ".ai-onboard/backups/002/new.txt", "new")
        self.run_manager("cleanup", "--keep-releases", "1")
        self.assertFalse((self.target / ".ai-onboard/backups/001").exists())
        self.assertTrue((self.target / ".ai-onboard/backups/002").exists())

    def test_uninstall_removes_configs_created_entirely_by_manager(self) -> None:
        self.run_manager(
            "install",
            "--harness",
            "claude,codex,opencode",
            "--profile",
            "core",
            "--configs",
        )

        self.run_manager("sync")
        self.run_manager("uninstall")

        self.assertFalse((self.target / ".claude/settings.json").exists())
        self.assertFalse((self.target / ".codex/config.toml").exists())
        self.assertFalse((self.target / "opencode.json").exists())

    def test_adopted_config_entries_survive_default_uninstall(self) -> None:
        self.write_json(
            self.target / ".claude/settings.json",
            {
                "permissions": {
                    "deny": ["Read(./.env)", "Read(./secrets/**)"]
                },
                "skillOverrides": {
                    "goal-contract": "user-invocable-only"
                },
            },
        )
        self.run_manager(
            "adopt",
            "--harness",
            "claude",
            "--profile",
            "core",
            "--configs",
        )

        self.run_manager("uninstall")

        adopted = json.loads(
            (self.target / ".claude/settings.json").read_text(encoding="utf-8")
        )
        self.assertIn("permissions", adopted)
        self.assertIn("skillOverrides", adopted)

    def test_adopted_toml_entries_survive_sync_and_default_uninstall(
        self,
    ) -> None:
        codex_config = self.target / ".codex/config.toml"
        self.write(
            codex_config,
            "[agents]\nmax_threads = 4\nmax_depth = 1\n",
        )
        self.run_manager(
            "adopt",
            "--harness",
            "codex",
            "--profile",
            "core",
            "--configs",
        )

        self.run_manager("sync")
        self.run_manager("uninstall")

        self.assertIn(
            "max_threads = 4", codex_config.read_text(encoding="utf-8")
        )

    def test_config_merge_preserves_existing_file_permissions(self) -> None:
        config = self.target / ".claude/settings.json"
        self.write_json(config, {"userSetting": True})
        config.chmod(0o600)

        self.run_manager(
            "install",
            "--harness",
            "claude",
            "--profile",
            "core",
            "--configs",
        )

        self.assertEqual(os.stat(config).st_mode & 0o777, 0o600)

    def test_dry_run_and_upgrade_check_do_not_change_project(self) -> None:
        self.run_manager(
            "install",
            "--harness",
            "codex",
            "--profile",
            "core",
            "--dry-run",
        )
        self.assertFalse((self.target / "ai-onboard.json").exists())

        self.run_manager(
            "install",
            "--harness",
            "codex",
            "--profile",
            "core",
        )
        before = (self.target / ".ai-onboard.lock.json").read_bytes()
        result = self.run_manager("upgrade", "--check")
        self.assertIn("Update not needed", result.stdout)
        self.assertEqual(
            (self.target / ".ai-onboard.lock.json").read_bytes(), before
        )

    def test_install_rejects_catalog_destination_outside_target(self) -> None:
        catalog_path = self.source / "site/data/catalog.json"
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        catalog["skills"][0]["name"] = "../../../outside-skill"
        self.write_json(catalog_path, catalog)
        escaped = self.target.parent / "outside-skill"

        result = self.run_manager(
            "install",
            "--harness",
            "codex",
            "--profile",
            "core",
            expected=2,
        )

        self.assertIn("invalid package path", result.stderr)
        self.assertFalse(escaped.exists())

    def test_uninstall_rejects_tampered_lock_path_outside_target(self) -> None:
        self.run_manager(
            "install",
            "--harness",
            "codex",
            "--profile",
            "core",
        )
        outside = self.target.parent / "outside.txt"
        outside.write_text("do not remove\n", encoding="utf-8")
        lock_path = self.target / ".ai-onboard.lock.json"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        lock["artifacts"].append(
            {
                "path": "../outside.txt",
                "source": "tampered",
                "sha256": "not-relevant",
                "ownership": "owned",
            }
        )
        self.write_json(lock_path, lock)

        result = self.run_manager("uninstall", expected=2)

        self.assertIn("outside managed namespaces", result.stderr)
        self.assertTrue(outside.exists())

    def test_uninstall_rejects_tampered_lock_path_inside_target(self) -> None:
        self.run_manager(
            "install",
            "--harness",
            "codex",
            "--profile",
            "core",
        )
        sensitive = self.target / ".git/HEAD"
        self.write(sensitive, "ref: refs/heads/main\n")
        digest = hashlib.sha256()
        digest.update(b"file\0")
        digest.update(sensitive.read_bytes())
        lock_path = self.target / ".ai-onboard.lock.json"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        lock["artifacts"].append(
            {
                "path": ".git/HEAD",
                "source": "tampered",
                "sha256": digest.hexdigest(),
                "ownership": "owned",
            }
        )
        self.write_json(lock_path, lock)

        result = self.run_manager("uninstall", expected=2)

        self.assertIn("outside managed namespaces", result.stderr)
        self.assertTrue(sensitive.exists())

    def test_uninstall_rejects_tampered_config_pointer(self) -> None:
        config_path = self.target / ".claude/settings.json"
        self.write_json(config_path, {"userSetting": True})
        self.run_manager(
            "install",
            "--harness",
            "claude",
            "--profile",
            "core",
            "--configs",
        )
        lock_path = self.target / ".ai-onboard.lock.json"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        lock["configs"][0]["managed"].append(
            {
                "pointer": "/userSetting",
                "kind": "value",
                "value": True,
                "ownership": "owned",
            }
        )
        self.write_json(lock_path, lock)

        result = self.run_manager("uninstall", expected=2)

        self.assertIn("pointer is not managed", result.stderr)
        current = json.loads(config_path.read_text(encoding="utf-8"))
        self.assertTrue(current["userSetting"])

    def test_uninstall_rejects_unapproved_item_at_managed_pointer(self) -> None:
        self.install_full_fixture()
        lock_path = self.target / ".ai-onboard.lock.json"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        deny_record = next(
            entry
            for entry in lock["configs"][0]["managed"]
            if entry["pointer"] == "/permissions/deny"
        )
        deny_record["items"].append("UserRule")
        self.write_json(lock_path, lock)

        result = self.run_manager("uninstall", expected=2)

        self.assertIn("lock config entry is invalid", result.stderr)
        current = json.loads(
            (self.target / ".claude/settings.json").read_text(encoding="utf-8")
        )
        self.assertIn("UserRule", current["permissions"]["deny"])

    def test_upgrade_preserves_adopted_artifact(self) -> None:
        installed = self.target / ".agents/skills/core-tool/SKILL.md"
        self.write(installed, "core v1\n")
        self.run_manager(
            "adopt",
            "--harness",
            "codex",
            "--profile",
            "core",
        )
        self.make_source("1.1.0", "core v2")

        result = self.run_manager("upgrade")

        self.assertIn("preserved adopted", result.stdout)
        self.assertEqual(installed.read_text(encoding="utf-8"), "core v1\n")
        conflict = (
            self.target
            / ".ai-onboard/conflicts/.agents/skills/core-tool/SKILL.md"
        )
        self.assertEqual(conflict.read_text(encoding="utf-8"), "core v2\n")

    def test_sync_does_not_restore_missing_adopted_artifact(self) -> None:
        installed = self.target / ".agents/skills/core-tool/SKILL.md"
        self.write(installed, "core v1\n")
        self.run_manager(
            "adopt",
            "--harness",
            "codex",
            "--profile",
            "core",
        )
        installed.unlink()
        installed.parent.rmdir()

        self.run_manager("sync")

        self.assertFalse(installed.exists())

    def test_toml_merge_accepts_commented_table_header(self) -> None:
        config = self.target / ".codex/config.toml"
        self.write(config, "[agents] # user comment\nmax_threads = 4\n")

        self.run_manager(
            "install",
            "--harness",
            "codex",
            "--profile",
            "core",
            "--configs",
        )

        text = config.read_text(encoding="utf-8")
        self.assertEqual(text.count("[agents]"), 1)
        self.assertIn("max_depth = 1", text)

    def test_toml_merge_accepts_quoted_table_header(self) -> None:
        config = self.target / ".codex/config.toml"
        self.write(config, '["agents"]\nmax_threads = 4\n')

        self.run_manager(
            "install",
            "--harness",
            "codex",
            "--profile",
            "core",
            "--configs",
        )

        text = config.read_text(encoding="utf-8")
        self.assertNotIn("\n[agents]\n", text)
        self.assertIn("max_depth = 1", text)

    def test_uninstall_validates_configs_before_removing_artifacts(self) -> None:
        self.run_manager(
            "install",
            "--harness",
            "codex",
            "--profile",
            "core",
            "--agents",
            "--configs",
        )
        managed_skill = self.target / ".agents/skills/core-tool"
        config = self.target / ".codex/config.toml"
        config.write_text("[agents\ninvalid = true\n", encoding="utf-8")

        result = self.run_manager("uninstall", expected=2)

        self.assertIn("invalid TOML", result.stderr)
        self.assertTrue(managed_skill.exists())
        self.assertTrue((self.target / ".ai-onboard.lock.json").exists())

    def test_install_preflights_invalid_config_before_copying_artifacts(
        self,
    ) -> None:
        config = self.target / ".codex/config.toml"
        self.write(config, "[agents\ninvalid = true\n")

        result = self.run_manager(
            "install",
            "--harness",
            "codex",
            "--profile",
            "core",
            "--configs",
            expected=2,
        )

        self.assertIn("invalid TOML", result.stderr)
        self.assertFalse((self.target / ".agents/skills/core-tool").exists())
        self.assertFalse((self.target / ".ai-onboard/bin/ai_onboard.py").exists())
        self.assertFalse((self.target / ".ai-onboard.lock.json").exists())

    def test_install_preflights_non_file_config_destination(self) -> None:
        (self.target / ".codex/config.toml").mkdir(parents=True)

        result = self.run_manager(
            "install",
            "--harness",
            "codex",
            "--profile",
            "core",
            "--configs",
            expected=2,
        )

        self.assertIn("not a regular file", result.stderr)
        self.assertFalse((self.target / ".agents/skills/core-tool").exists())
        self.assertFalse((self.target / ".ai-onboard/bin/ai_onboard.py").exists())
        self.assertFalse((self.target / ".ai-onboard.lock.json").exists())

    def test_uninstall_removes_owned_list_items_and_preserves_user_item(
        self,
    ) -> None:
        self.run_manager(
            "install",
            "--harness",
            "claude",
            "--profile",
            "core",
            "--configs",
        )
        config = self.target / ".claude/settings.json"
        current = json.loads(config.read_text(encoding="utf-8"))
        current["permissions"]["deny"].append("UserRule")
        self.write_json(config, current)

        self.run_manager("uninstall")

        remaining = json.loads(config.read_text(encoding="utf-8"))
        self.assertEqual(remaining["permissions"]["deny"], ["UserRule"])

    def test_status_detects_missing_managed_config(self) -> None:
        self.run_manager(
            "install",
            "--harness",
            "claude",
            "--profile",
            "core",
            "--configs",
        )
        (self.target / ".claude/settings.json").unlink()

        result = self.run_manager("status", expected=1)

        self.assertIn("modified config", result.stdout)

    def test_status_detects_directory_symlink_added_to_managed_skill(
        self,
    ) -> None:
        self.run_manager(
            "install",
            "--harness",
            "codex",
            "--profile",
            "core",
        )
        external = self.target.parent / "external-directory"
        self.write(external / "secret.txt", "external\n")
        added = self.target / ".agents/skills/core-tool/external"
        added.symlink_to(external, target_is_directory=True)

        result = self.run_manager("status", expected=1)

        self.assertIn("modified", result.stdout)

    def test_upgrade_removes_obsolete_owned_list_items(self) -> None:
        self.install_full_fixture()
        template_path = self.source / "templates/configs/claude.settings.json"
        template = json.loads(template_path.read_text(encoding="utf-8"))
        template["permissions"]["deny"] = ["Read(./.env)"]
        self.write_json(template_path, template)

        self.run_manager("upgrade")

        current = json.loads(
            (self.target / ".claude/settings.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            current["permissions"]["deny"], ["UserRule", "Read(./.env)"]
        )

    def test_upgrade_check_detects_changed_local_source_content(self) -> None:
        self.run_manager(
            "install",
            "--harness",
            "codex",
            "--profile",
            "core",
        )
        self.make_source("1.0.0", "changed without version bump")

        result = self.run_manager("upgrade", "--check")

        self.assertIn("Update available", result.stdout)

    def test_upgrade_check_json_reports_release_and_optional_exit_code(
        self,
    ) -> None:
        self.run_manager(
            "install",
            "--harness",
            "codex",
            "--profile",
            "core",
        )
        self.make_source("1.0.1", "core fix")

        result = self.run_manager(
            "upgrade",
            "--check",
            "--json",
            "--exit-code",
            expected=10,
        )

        status = json.loads(result.stdout)
        self.assertTrue(status["update_available"])
        self.assertEqual(status["current"]["version"], "1.0.0")
        self.assertEqual(status["latest"]["version"], "1.0.1")
        self.assertEqual(status["release"]["classification"], "fix")
        self.assertEqual(
            status["release"]["notes_url"],
            "https://example.com/releases/1.0.1",
        )
        self.assertIn("checked_at", status)

    def test_install_rejects_invalid_semantic_version_metadata(self) -> None:
        manifest_path = self.source / "package-manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["version"] = "1.0.1\n::warning::forged"
        self.write_json(manifest_path, manifest)

        result = self.run_manager(
            "install",
            "--harness",
            "codex",
            "--profile",
            "core",
            expected=2,
        )

        self.assertIn("invalid package semantic version", result.stderr)

    def test_upgrade_check_cache_is_opt_in_and_doctor_surfaces_notice(
        self,
    ) -> None:
        self.run_manager(
            "install",
            "--harness",
            "codex",
            "--profile",
            "core",
        )
        self.make_source("1.0.1", "core fix")
        cache = self.target / ".ai-onboard/update-status.json"

        self.run_manager("upgrade", "--check", "--json")
        self.assertFalse(cache.exists())

        self.run_manager("upgrade", "--check", "--cache")
        cached = json.loads(cache.read_text(encoding="utf-8"))
        self.assertTrue(cached["update_available"])

        result = self.run_manager("doctor")
        self.assertIn("Update available", result.stdout)
        self.assertIn("Reliability fixes in 1.0.1.", result.stdout)

        self.run_manager("upgrade")
        self.assertFalse(cache.exists())
        result = self.run_manager("doctor")
        self.assertNotIn("Update available", result.stdout)

    def test_notifications_feature_installs_portable_command_assets(
        self,
    ) -> None:
        self.run_manager(
            "install",
            "--harness",
            "claude,codex,opencode",
            "--profile",
            "core",
            "--notifications",
        )

        desired = json.loads(
            (self.target / "ai-onboard.json").read_text(encoding="utf-8")
        )
        self.assertTrue(desired["features"]["notifications"])
        self.assertTrue(
            (
                self.target
                / ".claude/commands/ai-onboard-update.md"
            ).is_file()
        )
        self.assertTrue(
            (
                self.target
                / ".opencode/commands/ai-onboard-update.md"
            ).is_file()
        )
        self.assertTrue(
            (
                self.target
                / ".ai-onboard/share/codex-prompts/ai-onboard-update.md"
            ).is_file()
        )
        self.assertTrue(
            (
                self.target
                / ".github/workflows/ai-onboard-update-check.yml"
            ).is_file()
        )
        self.assertTrue(
            (
                self.target
                / ".ai-onboard/bin/install_macos_update_notifier.py"
            ).is_file()
        )

        self.run_manager("uninstall")
        self.assertFalse(
            (
                self.target
                / ".claude/commands/ai-onboard-update.md"
            ).exists()
        )
        self.assertFalse(
            (
                self.target
                / ".github/workflows/ai-onboard-update-check.yml"
            ).exists()
        )

    def test_macos_notifier_builds_project_scoped_launch_agent(self) -> None:
        manager = self.target / ".ai-onboard/bin/ai_onboard.py"
        self.write(manager, "# manager\n")

        label, payload = MACOS_NOTIFIER.launch_agent(self.target, "weekly")
        destination = MACOS_NOTIFIER.plist_path(
            self.target / "home", label
        )

        self.assertRegex(
            label, r"^com\.rsthrives\.ai-onboard-update\.[0-9a-f]{12}$"
        )
        self.assertEqual(payload["StartInterval"], 7 * 24 * 60 * 60)
        self.assertEqual(
            payload["ProgramArguments"],
            [
                sys.executable,
                str(manager),
                "--target",
                str(self.target),
                "upgrade",
                "--check",
                "--cache",
                "--notify",
            ],
        )
        self.assertEqual(
            destination,
            self.target
            / "home/Library/LaunchAgents"
            / f"{label}.plist",
        )

    def test_uninstall_removes_matching_macos_notifier_and_update_cache(
        self,
    ) -> None:
        self.run_manager(
            "install",
            "--harness",
            "codex",
            "--profile",
            "core",
            "--notifications",
        )
        self.make_source("1.0.1", "core fix")
        self.run_manager("upgrade", "--check", "--cache")
        cache = self.target / ".ai-onboard/update-status.json"
        self.assertTrue(cache.is_file())

        home = self.target / "home"
        label, payload = MACOS_NOTIFIER.launch_agent(
            self.target.resolve(), "weekly"
        )
        launch_agent = MACOS_NOTIFIER.plist_path(home, label)
        launch_agent.parent.mkdir(parents=True)
        with launch_agent.open("wb") as handle:
            plistlib.dump(payload, handle)

        with (
            mock.patch.object(Path, "home", return_value=home),
            mock.patch.object(MANAGER_MODULE.sys, "platform", "darwin"),
            mock.patch.object(
                MANAGER_MODULE.subprocess,
                "run",
                side_effect=[
                    subprocess.CompletedProcess([], 0),
                    subprocess.CompletedProcess([], 1),
                ],
            ) as launchctl,
        ):
            result = MANAGER_MODULE.command_uninstall(
                MANAGER_MODULE.argparse.Namespace(
                    dry_run=False,
                    purge=False,
                ),
                self.target.resolve(),
            )

        self.assertEqual(result, 0)
        self.assertFalse(cache.exists())
        self.assertFalse(launch_agent.exists())
        self.assertEqual(
            [call.args[0][1] for call in launchctl.call_args_list],
            ["bootout", "print"],
        )

    def test_uninstall_stops_when_macos_notifier_remains_loaded(
        self,
    ) -> None:
        self.run_manager(
            "install",
            "--harness",
            "codex",
            "--profile",
            "core",
            "--notifications",
        )
        manager = self.target / ".ai-onboard/bin/ai_onboard.py"
        home = self.target / "home"
        label, payload = MACOS_NOTIFIER.launch_agent(
            self.target.resolve(), "weekly"
        )
        launch_agent = MACOS_NOTIFIER.plist_path(home, label)
        launch_agent.parent.mkdir(parents=True)
        with launch_agent.open("wb") as handle:
            plistlib.dump(payload, handle)

        with (
            mock.patch.object(Path, "home", return_value=home),
            mock.patch.object(MANAGER_MODULE.sys, "platform", "darwin"),
            mock.patch.object(
                MANAGER_MODULE.subprocess,
                "run",
                side_effect=[
                    subprocess.CompletedProcess([], 1),
                    subprocess.CompletedProcess([], 0),
                ],
            ),
            self.assertRaisesRegex(
                MANAGER_MODULE.LifecycleError,
                "remains loaded",
            ),
        ):
            MANAGER_MODULE.command_uninstall(
                MANAGER_MODULE.argparse.Namespace(
                    dry_run=False,
                    purge=False,
                ),
                self.target.resolve(),
            )

        self.assertTrue(launch_agent.is_file())
        self.assertTrue(manager.is_file())

    def test_upgrade_requires_review_before_replacing_active_workflow(
        self,
    ) -> None:
        self.run_manager(
            "install",
            "--harness",
            "codex",
            "--profile",
            "core",
            "--notifications",
        )
        workflow = (
            self.target
            / ".github/workflows/ai-onboard-update-check.yml"
        )
        original = workflow.read_text(encoding="utf-8")
        self.make_source("1.1.0", "core v2")
        self.write(
            self.source
            / "templates/notifications/github/ai-onboard-update-check.yml",
            "name: changed workflow\n",
        )

        result = self.run_manager("upgrade")

        self.assertIn("review required", result.stdout)
        self.assertEqual(workflow.read_text(encoding="utf-8"), original)
        conflict = (
            self.target
            / ".ai-onboard/conflicts"
            / ".github/workflows/ai-onboard-update-check.yml"
        )
        self.assertEqual(
            conflict.read_text(encoding="utf-8"),
            "name: changed workflow\n",
        )

    def test_install_rejects_symlinked_local_source_content(self) -> None:
        external = self.source.parent / "external-skill"
        self.write(external / "SKILL.md", "external\n")
        linked = self.source / "skills/linked-skill"
        linked.symlink_to(external, target_is_directory=True)

        result = self.run_manager(
            "install",
            "--harness",
            "codex",
            "--profile",
            "core",
            expected=2,
        )

        self.assertIn("symlink", result.stderr)

    def test_safe_extract_skips_archive_symlinks(self) -> None:
        archive = self.target / "source.tar.gz"
        destination = self.target / "extracted"
        destination.mkdir()
        body = b"# Project instructions\n"

        with tarfile.open(archive, "w:gz") as bundle:
            regular = tarfile.TarInfo("repo/AGENTS.md")
            regular.size = len(body)
            bundle.addfile(regular, io.BytesIO(body))
            linked = tarfile.TarInfo("repo/GEMINI.md")
            linked.type = tarfile.SYMTYPE
            linked.linkname = "AGENTS.md"
            bundle.addfile(linked)
            hard_linked = tarfile.TarInfo("repo/COPILOT.md")
            hard_linked.type = tarfile.LNKTYPE
            hard_linked.linkname = "repo/AGENTS.md"
            bundle.addfile(hard_linked)

        MANAGER_MODULE.safe_extract(archive, destination)

        self.assertEqual(
            (destination / "repo/AGENTS.md").read_bytes(),
            body,
        )
        self.assertFalse((destination / "repo/GEMINI.md").exists())
        self.assertFalse((destination / "repo/COPILOT.md").exists())

    def test_safe_extract_rejects_negative_archive_member_size(self) -> None:
        archive = self.target / "source.tar.gz"
        destination = self.target / "extracted"
        destination.mkdir()

        with tarfile.open(archive, "w:gz") as bundle:
            linked = tarfile.TarInfo("repo/GEMINI.md")
            linked.type = tarfile.SYMTYPE
            linked.linkname = "AGENTS.md"
            linked.size = -1
            bundle.addfile(linked)

        with self.assertRaisesRegex(
            MANAGER_MODULE.LifecycleError,
            "invalid size metadata",
        ):
            MANAGER_MODULE.safe_extract(archive, destination)

    def test_safe_extract_bounds_member_enumeration_without_getmembers(self) -> None:
        destination = self.target / "extracted"
        destination.mkdir()

        class OversizedBundle:
            def __init__(self) -> None:
                self.iterated = 0
                self.extracted = False

            def __enter__(self) -> "OversizedBundle":
                return self

            def __exit__(self, *_args: object) -> None:
                return None

            def __iter__(self):
                for index in range(MANAGER_MODULE.MAX_ARCHIVE_MEMBERS + 1):
                    self.iterated += 1
                    yield tarfile.TarInfo(f"repo/{index}")

            def getmembers(self) -> list[tarfile.TarInfo]:
                raise AssertionError("safe_extract must not materialize every member")

            def extractall(self, *_args: object, **_kwargs: object) -> None:
                self.extracted = True

        bundle = OversizedBundle()
        with mock.patch.object(
            MANAGER_MODULE.tarfile,
            "open",
            return_value=bundle,
        ):
            with self.assertRaisesRegex(
                MANAGER_MODULE.LifecycleError,
                "too many entries",
            ):
                MANAGER_MODULE.safe_extract(
                    self.target / "oversized.tar.gz",
                    destination,
                )

        self.assertEqual(
            bundle.iterated,
            MANAGER_MODULE.MAX_ARCHIVE_MEMBERS + 1,
        )
        self.assertFalse(bundle.extracted)

    def test_read_only_command_does_not_create_missing_target(self) -> None:
        missing = self.target.parent / "missing-project"
        result = subprocess.run(
            [
                sys.executable,
                str(MANAGER),
                "--source",
                str(self.source),
                "--target",
                str(missing),
                "status",
            ],
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 2)
        self.assertFalse(missing.exists())


class GitIdentityCheckTests(unittest.TestCase):
    NOREPLY = "5134637+K95M65@users.noreply.github.com"
    PRIVATE = "maintainer@example.com"

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repository = Path(self.temp.name) / "repository"
        self.repository.mkdir()
        self.git("init", "-q", "-b", "main")
        self.git("config", "commit.gpgsign", "false")
        self.git("config", "user.name", "Test Maintainer")
        self.git("config", "user.email", self.NOREPLY)

    def git(
        self,
        *args: str,
        email: str | None = None,
    ) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        if email:
            environment.update(
                {
                    "GIT_AUTHOR_NAME": "Test Maintainer",
                    "GIT_AUTHOR_EMAIL": email,
                    "GIT_COMMITTER_NAME": "Test Maintainer",
                    "GIT_COMMITTER_EMAIL": email,
                }
            )
        return subprocess.run(
            ["git", "-C", str(self.repository), *args],
            env=environment,
            text=True,
            capture_output=True,
            check=True,
        )

    def commit(self, email: str) -> str:
        marker = self.repository / "marker.txt"
        marker.write_text(f"{email}\n", encoding="utf-8")
        self.git("add", "marker.txt")
        self.git("commit", "-q", "-m", "test identity", email=email)
        return self.git("rev-parse", "HEAD").stdout.strip()

    def check(
        self,
        *args: str,
        email: str,
        expected: int,
        input_text: str | None = None,
    ) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        environment.update(
            {
                "GIT_AUTHOR_NAME": "Test Maintainer",
                "GIT_AUTHOR_EMAIL": email,
                "GIT_COMMITTER_NAME": "Test Maintainer",
                "GIT_COMMITTER_EMAIL": email,
            }
        )
        result = subprocess.run(
            [
                sys.executable,
                str(MANAGER),
                "--target",
                str(self.repository),
                "check-git",
                *args,
            ],
            env=environment,
            input=input_text,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(
            result.returncode,
            expected,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        return result

    def test_check_git_accepts_noreply_process_and_history(self) -> None:
        self.commit(self.NOREPLY)

        result = self.check(email=self.NOREPLY, expected=0)

        self.assertIn("Git process identity passed", result.stdout)
        self.assertIn("Git history passed: 1 reachable commit(s)", result.stdout)

    def test_check_git_rejects_private_process_email_without_echoing_it(
        self,
    ) -> None:
        self.commit(self.NOREPLY)

        result = self.check(
            "--identity-only",
            email=self.PRIVATE,
            expected=1,
        )

        self.assertIn(
            "author email is not a GitHub no-reply address",
            result.stdout,
        )
        self.assertIn(
            "committer email is not a GitHub no-reply address",
            result.stdout,
        )
        self.assertNotIn(self.PRIVATE, result.stdout)

    def test_check_git_rejects_private_history_email_without_echoing_it(
        self,
    ) -> None:
        commit = self.commit(self.PRIVATE)

        result = self.check(
            "--history-only",
            email=self.NOREPLY,
            expected=1,
        )

        self.assertIn(commit[:12], result.stdout)
        self.assertIn("author and committer email", result.stdout)
        self.assertNotIn(self.PRIVATE, result.stdout)

    def test_history_check_catches_author_override_before_push(self) -> None:
        marker = self.repository / "marker.txt"
        marker.write_text("override\n", encoding="utf-8")
        self.git("add", "marker.txt")
        self.git(
            "commit",
            "-q",
            "-m",
            "test author override",
            "--author",
            f"Override Author <{self.PRIVATE}>",
            email=self.NOREPLY,
        )

        result = self.check(
            "--history-only",
            email=self.NOREPLY,
            expected=1,
        )

        self.assertIn(
            "author email is not a GitHub no-reply address",
            result.stdout,
        )
        self.assertNotIn("author and committer", result.stdout)
        self.assertNotIn(self.PRIVATE, result.stdout)

    def test_pre_push_checks_dangling_object_from_hook_input(self) -> None:
        safe_commit = self.commit(self.NOREPLY)
        private_commit = self.commit(self.PRIVATE)
        self.git("reset", "--hard", safe_commit)

        history = self.check(
            "--history-only",
            email=self.NOREPLY,
            expected=0,
        )
        self.assertNotIn(private_commit[:12], history.stdout)

        result = self.check(
            "--pre-push",
            email=self.NOREPLY,
            expected=1,
            input_text=(
                f"refs/heads/private {private_commit} "
                f"refs/heads/private {'0' * 40}\n"
            ),
        )

        self.assertIn(private_commit[:12], result.stdout)
        self.assertNotIn(self.PRIVATE, result.stdout)


if __name__ == "__main__":
    unittest.main()
