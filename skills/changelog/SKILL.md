---
name: changelog
description: Assemble release notes / a CHANGELOG entry from Conventional Commits since the last tag. Use when cutting a release or updating CHANGELOG.md. Pairs with the conventional-commit skill.
---

# Changelog

Pairs with `conventional-commit` — it writes the commits, this rolls them into release notes.

## When to use

Cutting a release, or updating `CHANGELOG.md`.

## Steps

1. Collect and group commits: `bash scripts/collect.sh [from-ref]`. With no argument it uses the last tag →
   `HEAD`; the commits are grouped by Conventional Commit type (`feat`, `fix`, …).
2. Format into a [Keep a Changelog](https://keepachangelog.com) entry under a version header, mapping types
   to sections:
   - `feat` → **Added / Changed**, `fix` → **Fixed**, `perf` → **Performance**, `deprecate` → **Deprecated**,
     `remove` → **Removed**, security fixes → **Security**.
3. **Surface breaking changes** at the top: any commit with `!` (e.g. `feat!:`) or a `BREAKING CHANGE:`
   footer. These drive the major-version bump.
4. Rewrite terse commit subjects into user-facing lines — the audience is a user reading release notes, not a
   developer reading git.

## Template

```markdown
## [x.y.z] — YYYY-MM-DD
### ⚠ Breaking changes
- …
### Added
- …
### Fixed
- …
```

## Notes

- `chore`/`ci`/`build`/`test`/`docs` usually don't belong in user-facing notes — omit or fold into one line.
- Date is intentionally not auto-filled by the script (avoid surprises); set it when you cut the release.
