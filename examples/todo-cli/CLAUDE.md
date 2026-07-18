@AGENTS.md

## Claude Code notes

- Reference subagents live in `.claude/agents/`. Delegate reviews to `reviewer`, security-sensitive changes
  (path/arg handling) to `security-review`, and verification to `verifier`. **`design-review` does not apply**
  — this CLI has no UI.
- Use plan mode for changes under `internal/store/` — the persistence format can corrupt saved tasks.
