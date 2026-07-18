# OpenCode setup

OpenCode reads `AGENTS.md` **natively** (project root, nested, and a global
`~/.config/opencode/AGENTS.md`). With [`AGENTS.md`](../../AGENTS.md) at your repo root, you're wired. The
legacy `.opencode` instruction file is still honored but `AGENTS.md` is the recommended name.

Generate a starter from your codebase any time with the `/init` command inside OpenCode — then trim it and
fold anything reusable back into your shared `AGENTS.md`.

## Power features (`opencode.json`)

Everything configurable — providers, models, agents, MCP, themes, keybinds — lives in `opencode.json`
(project) or `~/.config/opencode/opencode.json` (global). Keep provider/model choices personal unless the
repository genuinely requires one provider.

```json
{
  "$schema": "https://opencode.ai/config.json",
  "permission": {
    "edit": "ask",
    "bash": "ask",
    "external_directory": "deny"
  }
}
```

### Providers & models

OpenCode is provider-agnostic (Anthropic, OpenAI, Google, local via Ollama, OpenRouter, …). Set a default
`model` as `provider/model`, and configure credentials with the `opencode auth login` command.

### Custom agents

Define specialized agents — either in `opencode.json` under `agent`, or as Markdown files in
`.opencode/agents/<name>.md` with frontmatter:

```markdown
---
description: Reviews diffs for security issues. Read-only.
mode: subagent
permission:
  edit: deny
---
You are a security reviewer. Flag injection, authz, and secret-handling issues...
```

`mode: primary` agents are ones you switch to interactively; `mode: subagent` ones are delegated to.

### Custom commands

Reusable prompts live at `.opencode/commands/<name>.md` and are invoked as `/name`. They support
`$ARGUMENTS` and shell injection with the `` !`command` `` syntax.

### MCP servers

```json
{
  "mcp": {
    "github": {
      "type": "local",
      "command": ["npx", "-y", "@modelcontextprotocol/server-github"],
      "environment": { "GITHUB_TOKEN": "..." }
    }
  }
}
```

Remote MCP servers use `"type": "remote"` with a `url`.

## Realizing subagents & skills

### Reference subagents → `.opencode/agents/`

OpenCode's agent format is `.md` with frontmatter + a system-prompt body (like Claude Code) but a different
schema. The repo ships **ported** versions in [`agents/opencode/`](../../agents/opencode/):

```bash
mkdir -p .opencode/agents && cp agents/opencode/*.md .opencode/agents/    # or: link.sh --agents
```

The port adds `mode: subagent`, swaps Claude's `tools:` comma-list for a `permission:` block (read-only for
the review/research roles; `verifier` denies `edit` only), and omits `model` — OpenCode is multi-provider, so
set `provider/model` per agent if you want a tier. Reach subagents by **@mention** (`@reviewer …`) or the
**Task tool**. Layer profiles work via nested `AGENTS.md` (native); like Codex, OpenCode can't auto-switch
model by path — set a per-agent `model`/`permission` instead.

### Skills — nothing to do

OpenCode reads the **open Agent Skills** standard natively and scans `.opencode/skills/`, **`.claude/skills/`**,
and **`.agents/skills/`** (project + global). The repository's generated skill catalog works in OpenCode
**as-is** — if you've run `link.sh --skills` (which populates `.claude/skills/` and `.agents/skills/`),
OpenCode picks them up with zero extra steps. Skills load on demand via OpenCode's `skill` tool, so make sure
that tool isn't denied in your permission config. (A skill's folder name must equal its `name:` field and
match `^[a-z0-9]+(-[a-z0-9]+)*$`.)

## Recommended baseline

```bash
python3 /path/to/AI_ONBOARD/scripts/ai_onboard.py \
  --target /path/to/project \
  install \
  --harness opencode \
  --profile core \
  --agents \
  --configs
opencode debug config
```

The manager leaves native `AGENTS.md` ownership with the project, installs the selected skills and OpenCode
agent ports, and merges only its managed configuration keys. Use the installed manager for
[`status`, upgrades, and cleanup](../install-management.md).

The template enables automatic compaction, prunes old tool output, reserves a context buffer, and ignores
noisy generated directories. GOAL and GRILL use `permission.skill = "ask"` so an attempted load crosses an
explicit approval boundary. OpenCode has no documented user-only visibility mode equivalent to Claude's
`user-invocable-only`.

OpenCode ships frequently; confirm the resolved schema with `opencode debug config` after upgrades.
