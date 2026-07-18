# Tool matrix — which file does each AI tool read?

The whole point of this repo is to maintain **one** instructions file. To do that you need to know what
each tool looks for and how to redirect it to `AGENTS.md`. This table is the reference.

## Project-level instruction files

| Tool | Native file(s) | Reads `AGENTS.md`? | How to wire it to `AGENTS.md` |
|------|----------------|:---:|-------------------------------|
| **OpenAI Codex CLI** | `AGENTS.md` | ✅ native | Nothing to do. Also reads `~/.codex/AGENTS.md` (global) and nested files. |
| **OpenCode** | `AGENTS.md` | ✅ native | Nothing to do. Legacy `.opencode` still honored; global at `~/.config/opencode/AGENTS.md`. |
| **Cursor** | `.cursor/rules/*.mdc`, `.cursorrules` (legacy) | ✅ native | Reads `AGENTS.md`. Use `.cursor/rules/` only for Cursor-specific scoped/auto-attached rules. |
| **Zed** | `AGENTS.md` | ✅ native | Nothing to do. |
| **Jules** (Google) | `AGENTS.md` | ✅ native | Nothing to do. |
| **Aider** | `CONVENTIONS.md` (via config) | ➖ indirect | Point Aider at it: `read: AGENTS.md` in `.aider.conf.yml`, or `/read AGENTS.md`. |
| **Claude Code** | `CLAUDE.md` + `.claude/` | ➖ via import | `echo "@AGENTS.md" > CLAUDE.md` — imports the shared file, leaves room for Claude-only extras. |
| **Gemini CLI** | `GEMINI.md` | ⚙️ configurable | Symlink `ln -s AGENTS.md GEMINI.md`, or set `contextFileName` to `AGENTS.md` in settings. |
| **GitHub Copilot** | `.github/copilot-instructions.md` | ❌ no | Symlink: `mkdir -p .github && ln -s ../AGENTS.md .github/copilot-instructions.md`. |
| **Windsurf** | `.windsurf/rules/*.md`, `.windsurfrules` (legacy) | ❌ no | Symlink a rule file to `AGENTS.md`, or keep a thin rule that says "follow AGENTS.md". |
| **Cline** | `.clinerules/` | ❌ no | Symlink a file in `.clinerules/` to `AGENTS.md`. |

> Legend: ✅ native = reads `AGENTS.md` out of the box · ⚙️ configurable = one setting away · ➖ indirect =
> needs a one-line import/redirect · ❌ = needs a symlink. **Verify against each tool's current docs** —
> this ecosystem moves fast and native `AGENTS.md` support keeps expanding.

## The two wiring techniques

**1. Symlink** — both filenames resolve to the exact same bytes. Best when the tool reads a whole file verbatim.

```bash
ln -s AGENTS.md GEMINI.md
```

Caveat: symlinks need care on Windows (enable Developer Mode / `git config core.symlinks true`) and some
sandboxed runners don't follow them. When in doubt, use an import.

**2. Import / include** — a tiny native file that pulls in `AGENTS.md`, leaving room for tool-specific additions.

```bash
# Claude Code supports @path imports inside CLAUDE.md
printf '@AGENTS.md\n\n## Claude-only notes\n- <hooks, slash-command hints, etc.>\n' > CLAUDE.md
```

## Precedence (all tools follow the same intuition)

1. **Closer to the file wins.** A `packages/api/AGENTS.md` overrides the root `AGENTS.md` for anything under `packages/api/`.
2. **Explicit user prompt beats the file.** If you tell the agent to do X, that wins over the doc.
3. **Global < project < subdirectory.** `~/.codex/AGENTS.md` is the weakest; a nested project file is strongest.

Keep the root file general and push specifics down into nested files rather than growing one giant document.

## Where tool-specific power features live (keep these OUT of AGENTS.md)

| Tool | Config / feature files | Purpose |
|------|------------------------|---------|
| Claude Code | `.claude/settings.json`, `.claude/commands/`, `.claude/agents/`, `.claude/skills/`, hooks | Permissions, slash commands, subagents, skills, lifecycle hooks |
| Codex | `.codex/config.toml`, `~/.codex/config.toml`, `~/.codex/*.config.toml` | Project agent bounds; personal model, approval, sandbox, and named profiles |
| OpenCode | `opencode.json`, `.opencode/agents/` | Permissions, compaction, providers, agents, MCP servers, themes |
| Cursor | `.cursor/rules/*.mdc` | Scoped/auto-attached rules with glob triggers |
| Gemini CLI | `.gemini/settings.json` | Context filename, tools, MCP |

These are documented per-tool in [`setup/`](setup/). They stay out of `AGENTS.md` so the
shared file remains portable across every harness.

The starter configs in [`../templates/configs/`](../templates/configs/) cover Claude Code, Codex, and
OpenCode. Install them with the [lifecycle manager](install-management.md), which merges only managed keys,
records checksums, and supports safe upgrade and uninstall. `templates/link.sh --configs` remains a
legacy copy path without lifecycle tracking.
