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
