# Gemini CLI setup

Google's Gemini CLI defaults to a context file named `GEMINI.md`. You have two ways to keep
[`AGENTS.md`](../../AGENTS.md) as the source of truth — a symlink, or a config setting.

## Wiring

**Option A — symlink (simplest):**

```bash
ln -s AGENTS.md GEMINI.md
```

**Option B — tell Gemini to use `AGENTS.md` directly** via `.gemini/settings.json`:

```json
{ "contextFileName": "AGENTS.md" }
```

Option B avoids symlink pitfalls on Windows and in some sandboxes; Option A means any tool expecting
`GEMINI.md` also just works.

## Hierarchical context

Like the others, Gemini layers context files from global → project → subdirectory:

```
~/.gemini/GEMINI.md        # personal global
  <  ./GEMINI.md (→ AGENTS.md)   # project
    <  ./sub/GEMINI.md      # nested
```

Check what's actually loaded in a session with the `/memory show` command; refresh with `/memory refresh`.

## Power features (`.gemini/settings.json`)

Tool-specific config — context filename, MCP servers, tool allow/deny, telemetry — lives here, not in the
context file.

```json
{
  "contextFileName": "AGENTS.md",
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_TOKEN": "..." }
    }
  }
}
```

## Recommended baseline

```bash
mkdir -p .gemini
cat > .gemini/settings.json <<'JSON'
{ "contextFileName": "AGENTS.md" }
JSON
```

> `contextFileName` and settings keys can change between Gemini CLI releases — confirm with `gemini --help`
> or the official docs.
