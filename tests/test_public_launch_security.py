from __future__ import annotations

import json
import os
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LINK_SCRIPT = ROOT / "templates" / "link.sh"
TURNSTILE_SCRIPTS = (
    ROOT / "skills" / "cloudflare" / "turnstile-spin" / "scripts"
)


class PublicLaunchSecurityTests(unittest.TestCase):
    def test_auth_probe_uses_cloudflare_api_without_unpinned_npx(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            npx_marker = directory / "npx-ran"
            fake_npx = directory / "npx"
            fake_npx.write_text(
                "#!/usr/bin/env bash\n"
                f"touch '{npx_marker}'\n"
                "exit 99\n",
                encoding="utf-8",
            )
            fake_npx.chmod(0o755)
            fake_curl = directory / "curl"
            fake_curl.write_text(
                "#!/usr/bin/env bash\n"
                "case \"$*\" in *test-token*) exit 97 ;; esac\n"
                "[ -z \"${CLOUDFLARE_API_TOKEN+x}\" ] || exit 98\n"
                "output=''\n"
                "url=''\n"
                "while [ \"$#\" -gt 0 ]; do\n"
                "  case \"$1\" in\n"
                "    -o) output=\"$2\"; shift 2 ;;\n"
                "    http*) url=\"$1\"; shift ;;\n"
                "    *) shift ;;\n"
                "  esac\n"
                "done\n"
                "case \"$url\" in\n"
                "  */accounts/account/challenges/widgets)\n"
                "    printf '%s' '{\"success\":true}' > \"$output\"\n"
                "    printf '200'\n"
                "    ;;\n"
                "  */accounts)\n"
                "    printf '%s' '{\"success\":true,\"result\":[{\"id\":\"account\",\"name\":\"Test\"}]}'\n"
                "    ;;\n"
                "  *) exit 1 ;;\n"
                "esac\n",
                encoding="utf-8",
            )
            fake_curl.chmod(0o755)
            environment = {
                **os.environ,
                "PATH": f"{directory}:{os.environ['PATH']}",
                "CLOUDFLARE_API_TOKEN": "test-token",
            }

            result = subprocess.run(
                ["bash", str(TURNSTILE_SCRIPTS / "auth-probe.sh")],
                env=environment,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["status"], "ok")
            self.assertFalse(npx_marker.exists())

    def test_link_script_preserves_existing_claude_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary) / "project"
            project.mkdir()
            (project / "AGENTS.md").write_text("# Project\n", encoding="utf-8")
            external = Path(temporary) / "private-claude.md"
            external.write_text("PRIVATE SENTINEL\n", encoding="utf-8")
            (project / "CLAUDE.md").symlink_to(external)

            result = subprocess.run(
                ["bash", str(LINK_SCRIPT)],
                cwd=project,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((project / "CLAUDE.md").is_symlink())
            self.assertEqual(
                (project / "CLAUDE.md").readlink(),
                external,
            )
            self.assertEqual(
                external.read_text(encoding="utf-8"),
                "PRIVATE SENTINEL\n",
            )
            self.assertIn("symlink", result.stdout)

    def test_widget_create_writes_secret_only_to_restricted_file(self) -> None:
        body = {
            "success": True,
            "result": {
                "sitekey": "public-site-key",
                "secret": "TURNSTILE_PRIVATE_SENTINEL",
            },
        }
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            fake_curl = directory / "curl"
            fake_curl.write_text(
                "#!/usr/bin/env bash\n"
                "case \"$*\" in *test-token*) exit 97 ;; esac\n"
                "[ -z \"${CLOUDFLARE_API_TOKEN+x}\" ] || exit 98\n"
                "output=''\n"
                "while [ \"$#\" -gt 0 ]; do\n"
                "  if [ \"$1\" = '-o' ]; then output=\"$2\"; shift 2; else shift; fi\n"
                "done\n"
                f"printf '%s' '{json.dumps(body)}' > \"$output\"\n"
                "printf '200'\n",
                encoding="utf-8",
            )
            fake_curl.chmod(0o755)
            secret_file = directory / "widget-secret"
            environment = {
                **os.environ,
                "PATH": f"{directory}:{os.environ['PATH']}",
                "CLOUDFLARE_API_TOKEN": "test-token",
            }

            result = subprocess.run(
                [
                    "bash",
                    str(TURNSTILE_SCRIPTS / "widget-create.sh"),
                    "--account-id",
                    "account",
                    "--name",
                    "widget",
                    "--domains",
                    "localhost,127.0.0.1",
                    "--secret-file",
                    str(secret_file),
                ],
                env=environment,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertNotIn("TURNSTILE_PRIVATE_SENTINEL", result.stdout)
            self.assertNotIn("TURNSTILE_PRIVATE_SENTINEL", result.stderr)
            self.assertEqual(
                json.loads(result.stdout),
                {"status": "ok", "sitekey": "public-site-key"},
            )
            self.assertEqual(
                secret_file.read_text(encoding="utf-8"),
                "TURNSTILE_PRIVATE_SENTINEL",
            )
            self.assertEqual(
                stat.S_IMODE(secret_file.stat().st_mode),
                0o600,
            )

    def test_fetch_secret_writes_secret_only_to_restricted_file(self) -> None:
        body = {
            "result": {
                "secret": "TURNSTILE_PRIVATE_SENTINEL",
                "clearance_level": "no_clearance",
                "domains": ["example.com"],
            },
        }
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            fake_curl = directory / "curl"
            fake_curl.write_text(
                "#!/usr/bin/env bash\n"
                "case \"$*\" in *test-token*) exit 97 ;; esac\n"
                "[ -z \"${CLOUDFLARE_API_TOKEN+x}\" ] || exit 98\n"
                "output=''\n"
                "while [ \"$#\" -gt 0 ]; do\n"
                "  if [ \"$1\" = '-o' ]; then output=\"$2\"; shift 2; else shift; fi\n"
                "done\n"
                f"printf '%s' '{json.dumps(body)}' > \"$output\"\n"
                "printf '200'\n",
                encoding="utf-8",
            )
            fake_curl.chmod(0o755)
            secret_file = directory / "widget-secret"
            environment = {
                **os.environ,
                "PATH": f"{directory}:{os.environ['PATH']}",
                "CLOUDFLARE_API_TOKEN": "test-token",
            }

            result = subprocess.run(
                [
                    "bash",
                    str(TURNSTILE_SCRIPTS / "fetch-secret.sh"),
                    "--account-id",
                    "account",
                    "--sitekey",
                    "public-site-key",
                    "--secret-file",
                    str(secret_file),
                ],
                env=environment,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertNotIn("TURNSTILE_PRIVATE_SENTINEL", result.stdout)
            self.assertNotIn("TURNSTILE_PRIVATE_SENTINEL", result.stderr)
            self.assertEqual(
                json.loads(result.stdout),
                {
                    "status": "ok",
                    "clearance_level": "no_clearance",
                    "domains": ["example.com"],
                },
            )
            self.assertEqual(
                secret_file.read_text(encoding="utf-8"),
                "TURNSTILE_PRIVATE_SENTINEL",
            )
            self.assertEqual(
                stat.S_IMODE(secret_file.stat().st_mode),
                0o600,
            )


if __name__ == "__main__":
    unittest.main()
