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

## Power features (`~/.gemini/settings.json`)

Credential-bearing MCP definitions belong in the user settings file, not committed project settings.
Gemini CLI expands `$NAME` from the launch environment:

```json
{
  "mcpServers": {
    "github": {
      "command": "/absolute/path/to/reviewed/github-mcp-server",
      "env": { "GITHUB_TOKEN": "$GITHUB_TOKEN" }
    }
  }
}
```

Use a reviewed, version-pinned executable; avoid unpinned `npx -y` launchers for credential-bearing
servers. Never put a literal token in `settings.json`, `GEMINI.md`, or a command argument.

## Recommended baseline

```bash
mkdir -p .gemini
cat > .gemini/settings.json <<'JSON'
{ "contextFileName": "AGENTS.md" }
JSON
```

> `contextFileName` and settings keys can change between Gemini CLI releases — confirm with `gemini --help`
> or the official docs.
