# Claude Code setup

Claude Code (Anthropic's CLI) reads `CLAUDE.md`, not `AGENTS.md` — but it supports `@import` syntax, so you
wire it up in one line and keep `AGENTS.md` as the source of truth.

## Wiring

```bash
printf '@AGENTS.md\n' > CLAUDE.md
```

That's it — `CLAUDE.md` now pulls in the shared file. Add Claude-only notes below the import if you want:

```markdown
@AGENTS.md

## Claude Code notes
- Use the `/test` slash command to run the suite in watch mode.
- The `db-migrate` subagent handles schema changes — delegate those to it.
```

Memory file scopes (all optional, all layer together):

| File | Scope | Committed? |
|------|-------|-----------|
| `./CLAUDE.md` | This project | ✅ yes — team-shared |
| `~/.claude/CLAUDE.md` | All your projects | ❌ personal |
| `./subdir/CLAUDE.md` | Just that subtree | ✅ yes |

`CLAUDE.local.md` remains available for uncommitted project-local memory. Prefer
`.claude/settings.local.json` for personal settings and keep shared project facts in the imported
`AGENTS.md`.

## Power features (the `.claude/` directory)

These are Claude-specific and stay **out** of `AGENTS.md`.

```
.claude/
├── settings.json         # permissions, env vars, hooks (team-shared, committed)
├── settings.local.json   # personal overrides (gitignored)
├── rules/                # Claude-only path-scoped rules
├── agents/               # subagents — one .md per agent, with frontmatter
│   └── db-migrate.md
└── skills/               # skills — one folder per skill
    └── my-skill/SKILL.md
```

### settings.json — permissions & env

```json
{
  "permissions": {
    "allow": ["Bash(npm run test:*)", "Bash(npm run lint)"],
    "deny": ["Bash(rm -rf *)", "Read(./.env)"]
  },
  "env": { "NODE_ENV": "test" }
}
```

Use `/permissions` to inspect and edit resolved rules, `/config` for settings, and `/doctor` to diagnose
invalid or conflicting configuration.

AI_ONBOARD's conservative project template also keeps manual workflow foundations manual:

```json
{
  "skillOverrides": {
    "goal-contract": "user-invocable-only",
    "grill-requirements": "user-invocable-only"
  }
}
```

`user-invocable-only` requires Claude Code 2.1.129 or later. It removes both descriptions from automatic
model selection and loads the skill only when the user invokes it.

### Custom commands and skills

Claude Code still accepts command definitions, but new reusable workflows should normally be skills.
`.claude/skills/test/SKILL.md` becomes `/test`, can carry references or scripts, and can be either manually
or model invoked.

```markdown
---
name: test
description: Run the test suite for a given package
---
Run `npm test -- packages/$1` and summarize failures.
```

### Subagents

`.claude/agents/db-migrate.md` defines a specialized agent with its own tools and system prompt:

```markdown
---
name: db-migrate
description: Handles Prisma schema changes and migrations. Use for any DB schema work.
tools: Read, Edit, Bash
---
You are a database migration specialist. Always create a migration file, never edit the DB directly...
```

### Hooks (deterministic enforcement)

Hooks run **shell commands** on lifecycle events (`PreToolUse`, `PostToolUse`, `Stop`, …). Use them for
"always run X after an edit" — e.g. auto-format on every file write:

```json
{
  "hooks": {
    "PostToolUse": [
      { "matcher": "Edit|Write",
        "hooks": [{ "type": "command", "command": "npx prettier --write \"$CLAUDE_FILE_PATHS\"" }] }
    ]
  }
}
```

Use hooks for deterministic guardrails and mechanical automation. Keep reasoning-heavy procedures in
skills, and do not run the full test suite after every edit.

### Skills

Drop portable skills from this repo's [`skills/`](../../skills/) into `.claude/skills/`. See
[docs/skills.md](../skills.md).

### MCP servers

Add via `claude mcp add <name> …` or a project `.mcp.json`. Keep MCP config here, not in `AGENTS.md`.

## Realizing layer profiles

[`docs/delegation.md`](../delegation.md) describes **layer profiles** — pinning `{model, skills, conventions,
checks}` to a slice of the codebase. The *declaration* is portable (a nested `AGENTS.md`); here's how Claude
Code *realizes* the tool-specific half.

**Conventions, path-scoped** — `.claude/rules/` with `paths:` frontmatter loads a rule only when Claude
touches matching files, so a layer's house rules don't cost context elsewhere:

```markdown
---
paths: ["web/**"]
---
Frontend: use design tokens, never hard-coded hex. Match existing component patterns.
```

(The portable equivalent is a nested `web/AGENTS.md` — use that for cross-tool repos, `.claude/rules/` when
you want Claude-only, path-triggered loading.)

**Model + tools, per function** — a subagent's frontmatter pins the model for that role. Pair a fast model
with a high-volume layer, a strong model with a risky one:

```markdown
---
name: ui-executor
description: Implements frontend changes under web/. Use for component and styling work.
model: haiku
tools: Read, Edit, Bash
---
Implement the change using design tokens. Run `npm run test:web` and compare a screenshot before finishing.
```

**Cross-cutting layers (Security, Design)** are reviewers, not directories — define them as `review`-function
subagents (e.g. a `security-review` and a `design-review` agent) that run over the diff regardless of which
path layer changed. Keep their always-on rules in the root `AGENTS.md`.

**Skills** — surface a layer's skills by dropping them in `.claude/skills/`; scope which ones are active with
the `gsd-surface` skill or per-subagent `tools`/prompt.

## Recommended baseline

```bash
python3 /path/to/AI_ONBOARD/scripts/ai_onboard.py \
  --target /path/to/project \
  install \
  --harness claude \
  --profile core \
  --agents \
  --configs
```

This writes the thin `CLAUDE.md` import, installs the selected skills and reference agents, and safely
merges AI_ONBOARD's managed settings keys. It never replaces the target `AGENTS.md`; personal settings stay
in `.claude/settings.local.json`. Use the installed manager for
[`status`, upgrades, and cleanup](../install-management.md).

If project agents already provide review and security lenses, disable overlapping review plugins for that
project instead of paying for two competing authorities. Browser or Playwright plugins remain complementary:
they provide tools, while `test-browser-workflows` provides the validation procedure.
