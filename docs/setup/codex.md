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

> Newer Codex may define profiles as separate `~/.codex/<name>.config.toml` files instead of inline
> `[profiles.x]` tables — check your version (see the version caveats below).

### MCP servers

Declare tools/data sources under `[mcp_servers]`:

```toml
[mcp_servers.github]
command = "npx"
args = ["-y", "@modelcontextprotocol/server-github"]
env = { GITHUB_TOKEN = "..." }
```

## Realizing subagents & layer profiles

Codex has a **named-subagent system** — `.codex/agents/*.toml` (project) or `~/.codex/agents/` (global),
alongside built-in `default`, `worker`, and `explorer` agents. The repo's
[reference subagents](../../agents/) map onto it directly.

### Reference subagents → `.codex/agents/*.toml`

Each agent's portable body (the role contract) becomes `developer_instructions`. Required keys: `name`,
`description`, `developer_instructions`. Optional: `model`, `model_reasoning_effort`, `sandbox_mode`,
`mcp_servers`, `skills.config`.

```toml
# .codex/agents/reviewer.toml
name = "reviewer"
description = "Adversarial review of a diff. Use after implementation; never the author."
model = "gpt-5-codex"
sandbox_mode = "read-only"          # reviewers don't write
developer_instructions = """
You are an adversarial reviewer. You did not write this code...
# (paste the body of agents/reviewer.md here)
"""
```

Delegate by asking Codex to spawn it in-session; inspect running threads with `/agent` and `/subagents`.
Headless equivalent:

```bash
codex exec --profile review --sandbox read-only "Review the staged diff for correctness bugs."
```

### Layer profiles — the one real gap vs Claude Code

Codex **cannot auto-switch model by path** the way Claude Code's `.claude/rules/` `paths:` can. Realize the
two halves separately:

- **Per-layer conventions → nested `AGENTS.md`.** Automatic and portable — Codex reads the closest file
  natively, so a layer's rules and checks work with zero Codex-specific setup. This half is free.
- **Per-layer model / sandbox → a profile or subagent you select.** Either run `codex --profile backend` for
  a session of backend work, or define per-layer subagents (`.codex/agents/backend.toml`,
  `.codex/agents/frontend.toml`) that each pin their own `model` / `model_reasoning_effort` / `sandbox_mode`
  and route work to them. Selection is manual/prompt-driven, **not** path-triggered.

### Cross-cutting lenses

`security-review` and `design-review` become subagents (or `codex exec` calls) run over the **diff** — not
tied to a directory, same as everywhere else.

> **Version caveats.** Profile *definition* has shifted across releases (older: inline `[profiles.<name>]`
> tables; current docs: separate `~/.codex/<name>.config.toml` files). Per-subagent `model`/effort selection
> had a reported regression around v5.6. Model names (`gpt-5-codex`, …) are illustrative. Check
> `codex --version` and the live docs before relying on an example.

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
