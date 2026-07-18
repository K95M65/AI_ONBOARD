# opencode reference subagents

The opencode realization of the [reference subagents](../README.md). opencode uses the same `.md`
frontmatter-plus-body format as Claude Code, but a **different frontmatter schema** — so these are *ported*,
not identical to `../*.md`.

## Install

Copy into `.opencode/agent/` (project) or `~/.config/opencode/agents/` (global):

```bash
mkdir -p .opencode/agent && cp agents/opencode/*.md .opencode/agent/
```

`link.sh --agents` does this too. The filename becomes the agent name.

## What changed from the Claude Code version

- **`description`** — kept (required in opencode too).
- **`mode: subagent`** — added (opencode needs it; without it, agents default to `all`).
- **Claude's `tools:` comma-list → a `permission:` block.** `researcher`, `reviewer`, `security-review`,
  `design-review` are read-only (`edit: deny`, `write: deny`); `verifier` denies `edit` only (it must run
  checks).
- **`model` omitted** — opencode is multi-provider (`provider/model`), so these inherit the session model
  rather than pin a provider. Set one per agent for a tier (e.g. a fast model for `verifier`, a strong one
  for `security-review`).
- **Body (the role contract) is unchanged** from the canonical `../<name>.md`.

## Invocation

opencode reaches subagents by **@mention** (`@reviewer look at this`) and via the **Task tool** — same
orchestration as Claude Code's subagent dispatch. See
[`../../docs/setup/opencode.md`](../../docs/setup/opencode.md#realizing-subagents--skills).
