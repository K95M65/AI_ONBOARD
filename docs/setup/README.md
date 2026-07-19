# Per-tool setup guides

Each guide covers **two things** for one tool:

1. **Wiring** — how to point that tool at the shared [`AGENTS.md`](../../AGENTS.md) so you maintain one file.
2. **Power features** — the tool-specific config (hooks, `config.toml`, rules, MCP) that is *deliberately
   kept out* of `AGENTS.md` to keep it portable.

[The interactive project map](https://k95m65.github.io/AI_ONBOARD/) shows where harness wiring ends and
on-demand skills and independent agents begin.

For new projects, use the [managed installer](../install-management.md) to select harnesses and capability
profiles, preserve a lockfile, and gain safe upgrade, cleanup, and uninstall commands. The guides below
explain each harness's native behavior; the manager applies those decisions without replacing `AGENTS.md`.
The core profile includes the portable update-check skill. Add `--notifications` for native
Claude/OpenCode slash commands, the optional Codex compatibility-prompt source, and scheduled notices.

| Guide | Native file | Config surface |
|-------|-------------|----------------|
| [Claude Code](claude-code.md) | `CLAUDE.md` + `.claude/` | settings, commands, subagents, skills, hooks |
| [Codex CLI](codex.md) | `AGENTS.md` | `~/.codex/config.toml`, profiles, skills, optional compatibility prompts, MCP |
| [OpenCode](opencode.md) | `AGENTS.md` | `opencode.json`, agents, slash commands, permissions, compaction, MCP |
| [Cursor](cursor.md) | `.cursor/rules/*.mdc` | scoped/auto-attached rules |
| [Gemini CLI](gemini-cli.md) | `GEMINI.md` | `.gemini/settings.json`, MCP |

The at-a-glance wiring commands for every tool (including Copilot, Windsurf, Cline, Zed, Aider) live in the
[tool matrix](../tool-matrix.md). These guides go deeper on the five tools with the richest config surface.

> ⚠️ This ecosystem changes fast. Treat filenames and flags here as *current-as-of-writing* and confirm
> against each tool's official docs when something doesn't match.

When a harness setup changes, update its guide, this index when the matrix changes, and any affected website
copy in the same change. Run `python3 scripts/check_harness_configs.py` and
`python3 scripts/sync_project_docs.py --check`, plus
`python3 -m unittest -v tests/test_ai_onboard.py`, before handing off.
