# AGENTS.md

## Project

AI_ONBOARD is the source repository for the **@RSTHRIVES Portable Agent Workflow Framework**. It is a
dependency-free collection of Markdown guidance, portable Agent Skills, reference subagents, installer
templates, Python validators, shell wiring, and a static HTML/CSS/JavaScript product site.

## Setup and preview

No package installation or build step is required.

```bash
python3 -m http.server 4173 --directory site
```

Open `http://127.0.0.1:4173/` to inspect the site.

## Required checks

Run checks relevant to the files you change. Before finishing a multi-file or public-facing change, run:

```bash
python3 scripts/sync_project_docs.py --check
python3 scripts/check_skills.py
python3 scripts/check_harness_configs.py
python3 -m unittest -v tests/test_ai_onboard.py
python3 scripts/check_site.py
node --check site/app.js
bash -n templates/link.sh
shellcheck templates/link.sh
git diff --check
```

When changing any shell script, match CI:

```bash
find . -path ./skills/cloudflare -prune -o -name '*.sh' -type f -print0 \
  | xargs -0r shellcheck --severity=warning
```

## Structure

- `skills/` — canonical portable skills. Treat `.agents/skills/` and `.claude/skills/` as installed mirrors.
- `agents/` — canonical reference-agent definitions plus Codex and OpenCode ports.
- `templates/` — non-destructive project wiring and harness-config templates.
- `docs/` — framework, setup, security, workflow, and maintenance documentation.
- `scripts/` — dependency-free generators and validators.
- `site/` — static GitHub Pages source; `site/data/catalog.json` is generated.
- `examples/` — worked onboarding examples.

## Working conventions

- Preserve portability: shared project facts and commands belong here; provider, model, credentials, and
  personal UI preferences belong in user-level harness configuration.
- Keep root instructions concise. Put reusable procedures in skills and path-specific facts in nested
  `AGENTS.md` files.
- Edit canonical files, not installed mirrors or generated artifacts. Run
  `python3 scripts/sync_project_docs.py` after skill, agent, category, or inventory changes.
- Update the nearest README and the product site when capabilities, setup, supported harnesses, public
  workflows, or repository structure change.
- GOAL (`goal-contract`) and GRILL (`grill-requirements`) are manual workflow foundations. They require
  explicit user intent and are skipped during ordinary work.
- Keep review agents independent and read-only. Use them for material UI, security-sensitive, public-facing,
  multi-file, or release-bound changes; use direct checks for small, low-risk edits.
- Preserve existing user changes in a dirty worktree. Never commit secrets, `.env` files, credentials, or
  generated private data.
- Do not deploy, publish, release, force-push, or perform destructive operations unless the user explicitly
  authorizes that external action.

## Harness configuration

- Claude Code imports this file from `CLAUDE.md`; project settings live in `.claude/settings.json`.
- Codex and OpenCode read this file natively; project settings live in `.codex/config.toml` and
  `opencode.json`.
- Do not duplicate this policy in harness-specific files. Those files should contain only permissions,
  runtime tuning, tool wiring, and compatibility settings.
