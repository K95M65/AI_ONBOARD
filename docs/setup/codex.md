# Codex CLI setup

OpenAI's Codex CLI reads `AGENTS.md` **natively** — root, nested, and a global `~/.codex/AGENTS.md`. If
you've placed [`AGENTS.md`](../../AGENTS.md) at your repo root, Codex already uses it. Nothing to wire.

## Instruction file hierarchy

Codex layers these, weakest → strongest:

```
~/.codex/AGENTS.md      # your personal global defaults (all projects)
  <  ./AGENTS.md        # project root
    <  ./sub/AGENTS.md  # nested, closest-to-file wins
```

Put personal preferences ("explain your plan before editing") in the global file; put project facts in the
committed project file.

## Power features (`~/.codex/config.toml`)

Codex's behavior — model, how much it can do without asking, sandboxing — lives in `~/.codex/config.toml`,
not in `AGENTS.md`.

```toml
# Default model & provider
model = "gpt-5-codex"

# How much autonomy Codex has before asking you
approval_policy = "on-request"   # untrusted | on-failure | on-request | never

# Filesystem/network sandbox for commands Codex runs
sandbox_mode = "workspace-write" # read-only | workspace-write | danger-full-access
```

### Approval + sandbox, in plain terms

| You want… | approval_policy | sandbox_mode |
|-----------|-----------------|--------------|
| Watch every step, approve edits | `on-request` | `read-only` |
| Let it edit files, ask before shell/net | `on-request` | `workspace-write` |
| Full autopilot (CI, throwaway env) | `never` | `danger-full-access` ⚠️ |

Only use `danger-full-access` in an already-isolated environment.

### Profiles — named config bundles

Switch whole configs with `codex --profile <name>`:

```toml
[profiles.review]
model = "gpt-5-codex"
approval_policy = "on-request"
sandbox_mode = "read-only"

[profiles.ci]
approval_policy = "never"
sandbox_mode = "workspace-write"
```

### MCP servers

Declare tools/data sources under `[mcp_servers]`:

```toml
[mcp_servers.github]
command = "npx"
args = ["-y", "@modelcontextprotocol/server-github"]
env = { GITHUB_TOKEN = "..." }
```

## Recommended baseline

```bash
# Project: AGENTS.md at root is auto-detected — done.
# Personal: set sane defaults once
mkdir -p ~/.codex
cat > ~/.codex/config.toml <<'TOML'
model = "gpt-5-codex"
approval_policy = "on-request"
sandbox_mode = "workspace-write"
TOML
```

> Flag names and defaults have shifted across Codex releases — check `codex --help` and the current docs if
> a key here is rejected.
