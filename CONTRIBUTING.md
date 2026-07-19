# Contributing to AI_ONBOARD

AI_ONBOARD accepts focused fixes, documentation improvements, new portable skills, harness compatibility
work, and lifecycle-manager changes.

## Before you change anything

1. Open an issue for a material new capability or behavior change so its portability and profile fit can be
   discussed.
2. Branch from `main`.
3. Keep Git identities on GitHub's `users.noreply.github.com` domain:

   ```bash
   git config user.name "YOUR_GITHUB_NAME"
   git config user.email "YOUR_GITHUB_ID+YOUR_GITHUB_NAME@users.noreply.github.com"
   python3 scripts/ai_onboard.py --target . check-git
   ```

Never commit credentials, `.env` files, personal configuration, or private data.

## Canonical-source workflow

- Edit canonical skills in `skills/`; do not edit ignored installed mirrors in `.agents/skills/` or
  `.claude/skills/`.
- Put shared repository facts in `AGENTS.md`; keep provider, model, credential, and UI preferences in
  user-level harness configuration.
- Update the nearest README and the public site when setup, supported harnesses, capabilities, or public
  workflows change.
- Run `python3 scripts/sync_project_docs.py` after changing skill, agent, category, or inventory metadata.
- Preserve vendored licenses and update the relevant NOTICE when adapting vendored content.

## Validate

Run the checks in `AGENTS.md`. Public-facing or multi-file changes must also pass:

```bash
python3 scripts/test_deployments.py
python3 scripts/ai_onboard.py --target . check-git --history-only
git diff --check
```

The deployment suite snapshots the current source into isolated temporary projects and validates full
Claude Code, Codex, and OpenCode installs without provider credentials.

## Pull requests

Use a focused Conventional Commit title. Explain the user-visible outcome, tests, security or compatibility
impact, documentation changes, and any follow-up. Keep unrelated changes out of the pull request and respond
to review without rewriting other contributors' work.
