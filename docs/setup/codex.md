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

## Configuration layers

Personal defaults live in `~/.codex/config.toml`. Trusted repositories can add shared runtime behavior in
`.codex/config.toml`; closer project files override broader ones. Keep provider, credentials, personal
model choice, approval mode, and UI preferences out of committed project configuration.

```toml
# Personal default example; use a model available to your account.
model = "gpt-5.6"
model_reasoning_effort = "high"

# How much autonomy Codex has before asking you
approval_policy = "on-request"   # untrusted | on-request | never | granular policy

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

### Profiles — separate named config files

Codex 0.134.0 and later loads profiles from separate files under `$CODEX_HOME`. Do not use legacy inline
`[profiles.<name>]` tables.

```toml
# ~/.codex/deep-review.config.toml
model = "gpt-5.6"
model_reasoning_effort = "xhigh"
approval_policy = "on-request"
sandbox_mode = "read-only"
```

```bash
codex --profile deep-review
codex --profile deep-review exec "Review the staged diff."
```

Keep profile files small: they layer above user config and below trusted project config and CLI flags.

### Minimal project configuration

AI_ONBOARD's project template tunes delegation without pinning a provider or model:

```toml
[agents]
max_threads = 4
max_depth = 1
```

Stable feature flags should normally be omitted so Codex can use current defaults. Remove obsolete keys
rather than carrying them forward; inspect the installed release with `codex features list`.

### Update-check workflow

The portable `check-ai-onboard-updates` skill is the supported Codex workflow. Ask Codex to check
AI_ONBOARD updates or invoke `$check-ai-onboard-updates`; it runs the installed manager, distinguishes
upstream releases from local drift, and previews rather than applies an upgrade.

Codex's older custom prompts are user-scoped and deprecated in favor of skills. If a user still wants an
explicit slash prompt, copy the optional compatibility template after installing `--notifications`:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/prompts"
cp .ai-onboard/share/codex-prompts/ai-onboard-update.md \
  "${CODEX_HOME:-$HOME/.codex}/prompts/ai-onboard-update.md"
```

Restart Codex or open a new task, then invoke `/prompts:ai-onboard-update`. The lifecycle manager does not
write to a user's Codex home automatically.

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

The repo ships **ready-made `.toml` files** in [`agents/codex/`](../../agents/codex/) — copy them straight in,
no translation needed:

```bash
mkdir -p .codex/agents && cp agents/codex/*.toml .codex/agents/
```

Each agent's portable body (the role contract) becomes `developer_instructions`. Required keys: `name`,
`description`, `developer_instructions`. Optional: `model`, `model_reasoning_effort`, `sandbox_mode`,
`mcp_servers`, `skills.config`. Model *tier* is expressed with `model_reasoning_effort` (portable across
versions) rather than a version-specific model name — see
[`agents/codex/README.md`](../../agents/codex/README.md).

Delegate by asking Codex to spawn it in-session; inspect running threads with `/agent` and `/subagents`.
Headless equivalent:

```bash
codex --profile review exec --sandbox read-only "Review the staged diff for correctness bugs."
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

GOAL and GRILL remain explicit-intent skills. Codex has native persisted goals, so `goal-contract` hands
activation to that native mechanism instead of creating a parallel ledger. Codex does not currently expose
Claude's per-skill `user-invocable-only` visibility setting; the skill trigger and native goal activation
gate enforce the boundary.

## Recommended baseline

```bash
python3 /path/to/AI_ONBOARD/scripts/ai_onboard.py \
  --target /path/to/project \
  install \
  --harness codex \
  --profile core \
  --agents \
  --configs

# Personal defaults and named profile files stay under ~/.codex/.
codex features list
```

The manager leaves `AGENTS.md` in user control, installs the selected portable skills and Codex agent
realizations, and merges only the bounded project config keys it owns. Use the installed manager for
[`status`, upgrades, and cleanup](../install-management.md).

Use `codex --version`, `codex features list`, and the current manual before changing unstable keys.
