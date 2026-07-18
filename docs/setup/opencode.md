# opencode setup

opencode reads `AGENTS.md` **natively** (project root, nested, and a global
`~/.config/opencode/AGENTS.md`). With [`AGENTS.md`](../../AGENTS.md) at your repo root, you're wired. The
legacy `.opencode` instruction file is still honored but `AGENTS.md` is the recommended name.

Generate a starter from your codebase any time with the `/init` command inside opencode — then trim it and
fold anything reusable back into your shared `AGENTS.md`.

## Power features (`opencode.json`)

Everything configurable — providers, models, agents, MCP, themes, keybinds — lives in `opencode.json`
(project) or `~/.config/opencode/opencode.json` (global). Keep it out of `AGENTS.md`.

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "anthropic/claude-sonnet-4-5",
  "theme": "system",
  "autoshare": false
}
```

### Providers & models

opencode is provider-agnostic (Anthropic, OpenAI, Google, local via Ollama, OpenRouter, …). Set a default
`model` as `provider/model`, and configure credentials with the `opencode auth login` command.

### Custom agents

Define specialized agents — either in `opencode.json` under `agent`, or as Markdown files in
`.opencode/agent/<name>.md` with frontmatter:

```markdown
---
description: Reviews diffs for security issues. Read-only.
mode: subagent
tools:
  write: false
  edit: false
---
You are a security reviewer. Flag injection, authz, and secret-handling issues...
```

`mode: primary` agents are ones you switch to interactively; `mode: subagent` ones are delegated to.

### Custom commands

Reusable prompts as `.opencode/command/<name>.md`, invoked as `/name`. Supports `$ARGUMENTS` and shell
injection via `!`command``.

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

### Reference subagents → `.opencode/agent/`

opencode's agent format is `.md` with frontmatter + a system-prompt body (like Claude Code) but a different
schema. The repo ships **ported** versions in [`agents/opencode/`](../../agents/opencode/):

```bash
mkdir -p .opencode/agent && cp agents/opencode/*.md .opencode/agent/    # or: link.sh --agents
```

The port adds `mode: subagent`, swaps Claude's `tools:` comma-list for a `permission:` block (read-only for
the review/research roles; `verifier` denies `edit` only), and omits `model` — opencode is multi-provider, so
set `provider/model` per agent if you want a tier. Reach subagents by **@mention** (`@reviewer …`) or the
**Task tool**. Layer profiles work via nested `AGENTS.md` (native); like Codex, opencode can't auto-switch
model by path — set a per-agent `model`/`permission` instead.

### Skills — nothing to do

opencode reads the **open Agent Skills** standard natively and scans `.opencode/skills/`, **`.claude/skills/`**,
and **`.agents/skills/`** (project + global). So the repo's [34 skills](../../skills/) work in opencode
**as-is** — if you've run `link.sh --skills` (which populates `.claude/skills/` and `.agents/skills/`),
opencode picks them up with zero extra steps. Skills load on demand via opencode's `skill` tool, so make sure
that tool isn't denied in your permission config. (A skill's folder name must equal its `name:` field and
match `^[a-z0-9]+(-[a-z0-9]+)*$`.)

## Recommended baseline

```bash
# Project AGENTS.md is auto-detected. Add a minimal project config:
cat > opencode.json <<'JSON'
{
  "$schema": "https://opencode.ai/config.json",
  "model": "anthropic/claude-sonnet-4-5"
}
JSON
```

> opencode ships frequently; confirm the config schema at <https://opencode.ai/docs> if a field here is
> rejected.
