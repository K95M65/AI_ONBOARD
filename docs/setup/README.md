# Per-tool setup guides

Each guide covers **two things** for one tool:

1. **Wiring** — how to point that tool at the shared [`AGENTS.md`](../../AGENTS.md) so you maintain one file.
2. **Power features** — the tool-specific config (hooks, `config.toml`, rules, MCP) that is *deliberately
   kept out* of `AGENTS.md` to keep it portable.

| Guide | Native file | Config surface |
|-------|-------------|----------------|
| [Claude Code](claude-code.md) | `CLAUDE.md` + `.claude/` | settings, commands, subagents, skills, hooks |
| [Codex CLI](codex.md) | `AGENTS.md` | `~/.codex/config.toml`, profiles, MCP |
| [opencode](opencode.md) | `AGENTS.md` | `opencode.json`, agents, MCP |
| [Cursor](cursor.md) | `.cursor/rules/*.mdc` | scoped/auto-attached rules |
| [Gemini CLI](gemini-cli.md) | `GEMINI.md` | `.gemini/settings.json`, MCP |

The at-a-glance wiring commands for every tool (including Copilot, Windsurf, Cline, Zed, Aider) live in the
[tool matrix](../tool-matrix.md). These guides go deeper on the five tools with the richest config surface.

> ⚠️ This ecosystem changes fast. Treat filenames and flags here as *current-as-of-writing* and confirm
> against each tool's official docs when something doesn't match.
