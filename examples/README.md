# Examples

Worked, read-top-to-bottom references showing how the pieces in this repo fit together in a real project.
These are **config, not runnable app source** — the point is the wiring.

## `notes-app`

A minimal full-stack TypeScript monorepo (Next.js `web/` + Fastify `api/`) wired for **Claude Code and
Codex**. It demonstrates the whole stack in one place:

| Piece | File | Shows |
|-------|------|-------|
| Source of truth | [`notes-app/AGENTS.md`](notes-app/AGENTS.md) | Project facts + the universal *How to work* contract + delegation pointer |
| Layer profile (frontend) | [`notes-app/web/AGENTS.md`](notes-app/web/AGENTS.md) | Nested profile: fast model, design tokens, `test:web` + screenshot |
| Layer profile (backend) | [`notes-app/api/AGENTS.md`](notes-app/api/AGENTS.md) | Nested profile: strong model, authz on every route, `test:api` |
| Claude Code wiring | [`notes-app/CLAUDE.md`](notes-app/CLAUDE.md) | One-line `@AGENTS.md` import + Claude-only notes |
| Claude Code perms | [`notes-app/.claude/settings.json`](notes-app/.claude/settings.json) | Allow the check commands; deny destructive ones |
| Claude Code path rule | [`notes-app/.claude/rules/frontend.md`](notes-app/.claude/rules/frontend.md) | Path-scoped rule that loads only under `web/**` |
| Codex wiring | [`notes-app/.codex/config.toml`](notes-app/.codex/config.toml) | Per-layer profiles (`--profile frontend` / `backend`) |

**Subagents** aren't duplicated here — install the repo's reference set:

```bash
# from the repo root
mkdir -p examples/notes-app/.claude/agents examples/notes-app/.codex/agents
cp agents/*.md examples/notes-app/.claude/agents/ && rm examples/notes-app/.claude/agents/README.md
cp agents/codex/*.toml examples/notes-app/.codex/agents/
```

Read `notes-app/AGENTS.md` first, then the nested `web/` and `api/` profiles, then the per-tool wiring.
