# AI_ONBOARD

Universal onboarding configuration for AI coding tools — **write your agent instructions once, use them across every harness.**

Codex, Claude Code, opencode, Cursor, Gemini CLI, Aider, Windsurf and friends each look for their *own* config file. Maintaining a separate `CLAUDE.md`, `GEMINI.md`, `.cursorrules`, and `AGENTS.md` by hand means they drift apart within a week. This repo treats **`AGENTS.md` as the single source of truth** and wires every other tool to it.

---

## The idea

```
                 ┌─────────────────┐
                 │    AGENTS.md    │   ← you edit this, and only this
                 │ (source of truth)│
                 └────────┬────────┘
          ┌───────────────┼────────────────┐
          │               │                │
     CLAUDE.md        GEMINI.md      read natively
    (@import)        (symlink)       (no wiring)
          │               │                │
     Claude Code      Gemini CLI   Codex · Cursor · opencode
```

- **[AGENTS.md](https://agents.md)** is an open, tool-agnostic standard already read natively by Codex, opencode, Cursor, Jules, Zed, Aider, and 20k+ repos.
- Tools that use a *different* filename are pointed back at `AGENTS.md` via a **symlink** or a **one-line import**, so there is exactly one file to maintain.

## Repository layout

| Path | What it is |
|------|------------|
| [`AGENTS.md`](AGENTS.md) | The universal agent-instructions template — your source of truth |
| [`docs/tool-matrix.md`](docs/tool-matrix.md) | Which config file *each* AI tool actually reads (start here) |
| [`docs/agents-md.md`](docs/agents-md.md) | The `AGENTS.md` format, sections, and precedence rules |
| [`docs/agent-behavior.md`](docs/agent-behavior.md) | The behavioral contract — how agents should work, with OpenAI/Anthropic citations |
| [`docs/delegation.md`](docs/delegation.md) | How agents delegate to subagents (by function) and specialize by layer (profiles) |
| [`docs/skills.md`](docs/skills.md) | The Agent Skills format (`SKILL.md`) and how to author portable skills |
| `docs/setup/` | Per-tool setup guides (Claude Code, Codex, opencode, Cursor, Gemini CLI) |
| [`agents/`](agents/) | Reference subagents (researcher, reviewer, verifier, security/design lenses) |
| [`examples/`](examples/) | Worked end-to-end setups — a full-stack monorepo wired for Claude Code + Codex |
| `skills/` | A library of reusable, portable skills |
| `templates/` | Drop-in starter files |

## Quickstart

1. Copy [`AGENTS.md`](AGENTS.md) into your project root and fill it in.
2. Wire up whichever tools you use (see [`docs/tool-matrix.md`](docs/tool-matrix.md) for the full list):

   ```bash
   # Claude Code — import AGENTS.md from CLAUDE.md (one line, keeps CLAUDE.md for extras)
   echo "@AGENTS.md" > CLAUDE.md

   # Gemini CLI — symlink so both filenames resolve to one file
   ln -s AGENTS.md GEMINI.md

   # Codex / opencode / Cursor / Zed / Aider — read AGENTS.md natively, nothing to do
   ```

   Or run [`templates/link.sh`](templates/link.sh) from your project root to wire all of these at once
   (`--agents` also installs the reference subagents).

3. Commit. Every agent now onboards from the same instructions.

## Scope

This repo covers **project-level onboarding files** (what an agent should know when it opens your repo) and **portable skills** (reusable capabilities). It is intentionally tool-agnostic: tool-specific power features (Claude Code hooks, Codex `config.toml`, etc.) are documented in `docs/setup/` but kept *out* of the shared `AGENTS.md` so it stays portable.

---

*Status: active. Core docs, per-tool setup (Claude Code + Codex are the primary focus), the behavioral +
delegation model, reference subagents, and a worked example are all in place.*
