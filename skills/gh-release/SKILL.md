---
name: gh-release
description: Cut a GitHub release with the gh CLI, using changelog or auto-generated notes. Use when tagging and publishing a release. Pairs with the changelog skill.
---

# GitHub release

## Steps

1. Assemble notes with the `changelog` skill (save to `RELEASE-NOTES.md`), or let GitHub
   generate them.
2. Create the tag + release:
   ```bash
   gh release create v<x.y.z> --title "v<x.y.z>" --notes-file RELEASE-NOTES.md
   ```
   - Auto notes instead: `--generate-notes`.
   - Pre-release: `--prerelease`. Draft: `--draft`.
   - Attach build artifacts: `gh release create v<x.y.z> ./dist/* --notes-file RELEASE-NOTES.md`.
3. Verify: `gh release view v<x.y.z> --web`.

## Versioning (SemVer)

- **major** — breaking changes (the `changelog` breaking section drives this).
- **minor** — new features, backward-compatible.
- **patch** — fixes only.

## Notes

- Tag the intended commit — releases are awkward to unpublish cleanly.
- **Never move or reuse a published tag**; cut a new patch instead.
- Releasing from CI: `gh` uses `GITHUB_TOKEN`; ensure it has `contents: write`.
