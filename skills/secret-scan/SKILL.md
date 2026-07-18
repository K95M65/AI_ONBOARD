---
name: secret-scan
description: Scan a repository for committed secrets (API keys, tokens, private keys) including git history. Use when auditing a codebase for leaked credentials, before open-sourcing, or when reviewing an unfamiliar repo. Complements the security-audit surface scan, which only covers the current tree.
---

# Secret scan

## When to use

Hunting for committed secrets across the **current tree and git history**. Complements
`security-audit`'s `surface-scan.sh`, which greps only the working tree.

## Steps

1. Run `bash scripts/scan.sh [path]`. It prefers a real scanner and falls back to grep:
   - **`gitleaks detect`** (tree + history) if installed — best.
   - else **`trufflehog filesystem`** if installed.
   - else a best-effort **grep over tracked files** — tree only, history **not** covered (it says so).
2. For each hit: confirm it's a real secret (not a placeholder or test fixture), and determine whether it's
   live.
3. If a live secret is found: **rotate it first.** A committed secret must be assumed compromised — removing
   it from the code is not enough.
4. If it's in **history**, note that scrubbing requires a history rewrite (`git filter-repo`) *and* rotation;
   a new commit that deletes the file does not remove it from history.

## Notes

- **Rotate first, scrub second.** Order matters.
- The grep fallback is shallow (tree only, limited patterns) — install `gitleaks` for real history coverage:
  <https://github.com/gitleaks/gitleaks>.
