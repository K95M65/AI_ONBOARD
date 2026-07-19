---
name: dependency-vuln-scan
description: Scan a project's dependencies for known vulnerabilities (CVEs). Use when auditing a codebase's supply chain, gating a release, or triaging an unfamiliar project's dependencies. Supports npm/pnpm/yarn and Go, plus osv-scanner.
---

# Dependency vulnerability scan

## When to use

Checking installed dependencies for known CVEs — part of a security audit, a pre-release gate, or sizing up
an unfamiliar repo's supply chain.

## Steps

1. Run `bash scripts/scan.sh [path]` (defaults to `.`). It detects the ecosystem and runs the matching
   scanner:
   - **Node** (`package.json`): `npm audit` (or `pnpm`/`yarn` if that's the lockfile).
   - **Go** (`go.mod`): `govulncheck ./...`.
   - **Any lockfile**: `osv-scanner` if installed (broadest, cross-ecosystem).
2. Triage by **reachability**, not just severity: a Critical on a hot path outranks a Critical in an unused
   transitive dep. `govulncheck` reports call-path reachability; for npm, check whether the vulnerable API is
   actually used.
3. For each actionable item note: advisory id, affected package@version, fixed version, and whether the
   upgrade is breaking.
4. Fold results into an audit report or remediation list. Prioritize using impact × exploitability:
   reachable severe impact first, then limited-impact or hard-precondition findings.

## Notes

- The script **degrades gracefully** — if a scanner isn't installed it prints the install command and moves on.
- A clean scan means "no *known* vulns in the advisory DBs *at scan time*" — not "safe". Re-run over time.
