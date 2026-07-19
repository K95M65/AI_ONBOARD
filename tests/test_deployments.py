from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEPLOYMENT_TEST = ROOT / "scripts" / "test_deployments.py"


class DeploymentSmokeScriptTests(unittest.TestCase):
    def test_full_deployment_for_each_supported_harness(self) -> None:
        for harness in ("claude", "codex", "opencode"):
            with self.subTest(harness=harness):
                result = subprocess.run(
                    [
                        sys.executable,
                        str(DEPLOYMENT_TEST),
                        "--harness",
                        harness,
                    ],
                    cwd=ROOT,
                    text=True,
                    capture_output=True,
                    check=False,
                )

                self.assertEqual(
                    result.returncode,
                    0,
                    msg=(
                        f"{harness} deployment failed\n"
                        f"stdout:\n{result.stdout}\n"
                        f"stderr:\n{result.stderr}"
                    ),
                )
                self.assertIn(f"PASS {harness}", result.stdout)


if __name__ == "__main__":
    unittest.main()
