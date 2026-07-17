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

> `CLAUDE.local.md` is deprecated — use imports (`@path`) instead.

## Power features (the `.claude/` directory)

These are Claude-specific and stay **out** of `AGENTS.md`.

```
.claude/
├── settings.json         # permissions, env vars, hooks (team-shared, committed)
├── settings.local.json   # personal overrides (gitignored)
├── commands/             # custom slash commands — one .md per command
│   └── test.md
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

Use the `/permissions` command or the `update-config` skill to edit these safely.

### Custom slash commands

`.claude/commands/test.md` becomes `/test`. The file body is the prompt; `$ARGUMENTS` and `$1`, `$2` inject args.

```markdown
---
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

### Hooks (automation the model can't skip)

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

> The harness (not the model) executes hooks, which is why they're the right tool for *guaranteed* behavior.
> Use the `update-config` skill to add them.

### Skills

Drop portable skills from this repo's [`skills/`](../../skills/) into `.claude/skills/`. See
[docs/skills.md](../skills.md).

### MCP servers

Add via `claude mcp add <name> …` or a project `.mcp.json`. Keep MCP config here, not in `AGENTS.md`.

## Recommended baseline

```bash
printf '@AGENTS.md\n' > CLAUDE.md
mkdir -p .claude/skills .claude/commands
# commit .claude/settings.json; gitignore .claude/settings.local.json
```
