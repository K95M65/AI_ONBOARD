# Codex reference subagents

The Codex realization of the [reference subagents](../README.md) — ready-to-use `.codex/agents/*.toml` files.
Copy them in and Codex can delegate to them by name:

```bash
mkdir -p .codex/agents
cp agents/codex/*.toml .codex/agents/      # project-scoped
# or ~/.codex/agents/ for all your projects
```

## Why these are hand-written, not generated

Each `.toml` here mirrors the matching `../<name>.md` (the Claude Code / canonical form), but the two
formats don't map 1:1, so there's no auto-converter:

- **Instructions** — the Markdown body becomes `developer_instructions` (verbatim).
- **Model tier** — Claude's `model: haiku|opus|inherit` has no equivalent Codex name (`gpt-5-codex` etc. are
  version-specific). We express the *tier* with `model_reasoning_effort` (`low` for the mechanical
  `verifier`, `high` for the `security-review` lens) instead, which is portable across versions. Add an
  explicit `model = "..."` if you want to pin one.
- **Tools** — Claude's `tools:` list becomes a `sandbox_mode` (all these roles are read-only, except
  `verifier`, which needs `workspace-write` to run tests).

**If you edit a role, change both files.** The `../<name>.md` body is the source of truth; keep the
`developer_instructions` here in sync with it.

## Version caveats

Codex is on a fast release train. The subagent file schema, `model_reasoning_effort` levels, and profile
mechanics have shifted across versions — see [`../../docs/setup/codex.md`](../../docs/setup/codex.md#realizing-subagents--layer-profiles).
Check `codex --version` and the live docs if a key is rejected.
