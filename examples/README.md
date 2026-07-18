# Examples

Worked, read-top-to-bottom references showing how the pieces in this repo fit together in a real project.
These are **config, not runnable app source** — the point is the wiring.

[Use the interactive request router](https://k95m65.github.io/AI_ONBOARD/#router) for a visual version of
the same context → skills → independent review → evidence sequence.

Two **shapes**, to show the model isn't web-specific — the same framework flexes to fit the project:

| Example | Shape | Layers | Design lens? |
|---------|-------|--------|:---:|
| [`notes-app`](notes-app/) | full-stack web monorepo (TS) | frontend · backend · data | ✅ |
| [`todo-cli`](todo-cli/) | single-binary CLI (Go) | by *concern*: commands · core | ⛔ (no UI) |

`security-review` applies to **both**; `design-review` only to the one with a UI. That's the point — which
layer profiles you write, and which subagents you wire, follow the project's shape.

## `notes-app`

A minimal full-stack TypeScript monorepo (Next.js `web/` + Fastify `api/`) wired for **Claude Code and
Codex**. It demonstrates the whole stack in one place:

| Piece | File | Shows |
|-------|------|-------|
| Source of truth | [`notes-app/AGENTS.md`](notes-app/AGENTS.md) | Project facts + the universal *How to work* contract + delegation pointer |
| Layer profile (frontend) | [`notes-app/web/AGENTS.md`](notes-app/web/AGENTS.md) | Nested profile: fast model, design tokens, `pnpm test -- web` + screenshot |
| Layer profile (backend) | [`notes-app/api/AGENTS.md`](notes-app/api/AGENTS.md) | Nested profile: strong model, authz on every route, `test:api` |
| Claude Code wiring | [`notes-app/CLAUDE.md`](notes-app/CLAUDE.md) | One-line `@AGENTS.md` import + Claude-only notes |
| Claude Code perms | [`notes-app/.claude/settings.json`](notes-app/.claude/settings.json) | Allow the check commands; deny destructive ones |
| Claude Code path rule | [`notes-app/.claude/rules/frontend.md`](notes-app/.claude/rules/frontend.md) | Path-scoped rule that loads only under `web/**` |
| Codex wiring | [`notes-app/.codex/config.toml`](notes-app/.codex/config.toml) | Per-layer profiles (`--profile frontend` / `backend`) |
| Security audit (worked) | [`notes-app/SECURITY-AUDIT.md`](notes-app/SECURITY-AUDIT.md) | Illustrative output of the `security-audit` skill |

**Subagents** aren't duplicated here — install the repo's reference set:

```bash
# from the repo root
mkdir -p examples/notes-app/.claude/agents examples/notes-app/.codex/agents
cp agents/*.md examples/notes-app/.claude/agents/ && rm examples/notes-app/.claude/agents/README.md
cp agents/codex/*.toml examples/notes-app/.codex/agents/
```

Read `notes-app/AGENTS.md` first, then the nested `web/` and `api/` profiles, then the per-tool wiring.

## `todo-cli`

A single-binary **Go** CLI (Cobra; tasks stored as JSON under `~/.todo/`) wired for **Claude Code and
Codex**. It's the *contrast* to `notes-app` — a different shape, so different choices:

| Piece | File | Shows |
|-------|------|-------|
| Source of truth | [`todo-cli/AGENTS.md`](todo-cli/AGENTS.md) | Go stack, single binary; *no* FE/BE/data layers |
| Layer profile (commands) | [`todo-cli/cmd/AGENTS.md`](todo-cli/cmd/AGENTS.md) | Nested profile: fast model, thin commands, `go test ./cmd/...` |
| Layer profile (core) | [`todo-cli/internal/AGENTS.md`](todo-cli/internal/AGENTS.md) | Nested profile: strong model, testable logic, path-traversal guard, `-race` |
| Claude Code wiring | [`todo-cli/CLAUDE.md`](todo-cli/CLAUDE.md) | `@AGENTS.md` + note that `design-review` doesn't apply |
| Claude Code perms | [`todo-cli/.claude/settings.json`](todo-cli/.claude/settings.json) | Allow `go test`/`build`/`vet`; deny destructive |
| Codex wiring | [`todo-cli/.codex/config.toml`](todo-cli/.codex/config.toml) | Per-layer profiles (`--profile commands` / `core`) |

What changed vs `notes-app`: layers are split by **concern** (interface vs logic), not by web tier; the
**`design-review`** subagent and the frontend skills drop out; **`security-review`** stays (path traversal,
untrusted args). Same framework, different shape.

When examples change the demonstrated operating model, update this index and the matching website workflow
in the same change.
