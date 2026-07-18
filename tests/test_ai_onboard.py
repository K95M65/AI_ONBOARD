from __future__ import annotations

import json
import hashlib
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANAGER = ROOT / "scripts" / "ai_onboard.py"


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


if __name__ == "__main__":
    unittest.main()
