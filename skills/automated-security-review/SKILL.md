---
name: automated-security-review
description: Wire automated security scanning into CI so every pull request is scanned for vulnerable dependencies, committed secrets, and code weaknesses. Use when setting up or improving a project's security gates in GitHub Actions.
---

# Automated security review

Turns the manual security skills into a **standing gate**: what `dependency-vuln-scan`, `secret-scan`, and a
SAST run do by hand, run automatically on every PR.

## When to use

Setting up (or hardening) a repo's CI security checks.

## Steps

1. Generate a starter GitHub Actions workflow:
   ```bash
   bash scripts/gen-workflow.sh [.github/workflows]
   ```
   It writes `security.yml` with three jobs: **dependency scan** (npm audit / govulncheck), **secret scan**
   (gitleaks, full history), and **SAST** (Semgrep). Refuses to overwrite an existing file.
2. Adapt it to your stack: enable the ecosystem jobs you use, set severity thresholds, and decide which jobs
   **block** the merge vs report only.
3. Require the check in branch protection so failures actually gate the merge.
4. Keep the human lens too: automated scans catch known patterns; the `security-review` subagent and
   `security-audit` skill catch logic/authz bugs that scanners miss. Automation is the floor, not the ceiling.

## What to gate on

- **Block:** committed secrets (any), new Critical/High dependency CVEs, SAST High findings.
- **Report:** Medium/Low — surface without blocking, triage in review.

## Notes

- The workflow pins actions and runs on `pull_request` + `push` to the default branch.
- False positives are expected — tune ignore files (`.gitleaksignore`, Semgrep rule selection) rather than
  disabling a whole job.
