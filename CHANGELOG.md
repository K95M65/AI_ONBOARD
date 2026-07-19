# Changelog

All notable user-visible changes to AI_ONBOARD are documented here.

## [0.2.0] - 2026-07-18

### Added

- Managed, profile-based installs with desired state, a lockfile, safe upgrades, drift detection, conflict
  staging, uninstall previews, and opt-in update notifications.
- Complete isolated deployment smoke tests for Claude Code, Codex, and OpenCode.
- GitHub no-reply identity checks for the active process, reachable history, hooks, and exact outgoing
  pre-push ranges.
- Public project map, release documentation, contribution guidance, and private vulnerability reporting.

### Changed

- New installs now track the versioned `stable` channel; `edge` remains an explicit opt-in.
- Packaged skills are validated as standalone installed artifacts and cannot link to repository-only files.
- GitHub Actions are pinned to immutable full commit SHAs with least-privilege Pages permissions.
- Credential-bearing MCP examples use user-level configuration, inherited environment variables, and
  reviewed version-pinned executables.

### Security

- Archive extraction bounds member enumeration before retaining metadata, preventing unbounded
  `getmembers()` allocation.
- Turnstile helpers no longer expose widget secrets in stdout, stderr, chat, or command arguments; secrets
  move through new mode-`0600` transfer files.
- Legacy wiring preserves `CLAUDE.md` symlinks instead of following or replacing them.
- OpenCode project shell commands now require approval.

[0.2.0]: https://github.com/K95M65/AI_ONBOARD/releases/tag/v0.2.0
