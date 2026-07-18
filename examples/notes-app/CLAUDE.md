@AGENTS.md

## Claude Code notes

- Reference subagents live in `.claude/agents/` — delegate reviews to `reviewer`, security-sensitive
  changes to `security-review`, and verification to `verifier`.
- Use plan mode for anything touching `api/prisma/` or `packages/shared/` — those ripple across layers.
- The `/test` command runs the suite for a given package.
