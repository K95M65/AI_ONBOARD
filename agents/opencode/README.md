# opencode reference subagents

The opencode realization of the [reference subagents](../README.md). opencode uses the same `.md`
frontmatter-plus-body format as Claude Code, but a **different frontmatter schema** — so these are *ported*,
not identical to `../*.md`.

[Explore how the roles enter a request workflow](https://k95m65.github.io/AI_ONBOARD/#router).

## Install

Copy into `.opencode/agents/` (project) or `~/.config/opencode/agents/` (global):

```bash
mkdir -p .opencode/agents && cp agents/opencode/*.md .opencode/agents/
```

For ownership tracking, upgrades, and uninstall, use the
[managed installer](../../docs/install-management.md) with `--harness opencode --agents`. The legacy
`link.sh --agents` copy path remains available. The filename becomes the agent name.

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

When a ported role changes, keep its canonical `../<name>.md`, this realization, and the nearest README in
sync; then run `python3 scripts/sync_project_docs.py` from the repository root.
