# Reference subagents

A small, portable starter set of subagents that realize the **function axis** of
[`../docs/delegation.md`](../docs/delegation.md): research, review, and verify — plus the two cross-cutting
review lenses (**security**, **design**). These are the roles where delegation actually pays off — context
isolation, parallelism, or an independent lens — not an org chart.

There is deliberately **no `frontend-executor` / `backend-executor`** here. Execution stays merged and
full-stack (a feature is a vertical slice); layers specialize *execution* via nested `AGENTS.md` profiles, not
via separate executor agents. See [`../docs/delegation.md`](../docs/delegation.md).

## The set

| Agent | Function | Delegate reason | Read-only? |
|-------|----------|-----------------|:---------:|
| [`researcher`](researcher.md) | research | context isolation | ✅ |
| [`reviewer`](reviewer.md) | review | independent lens | ✅ |
| [`verifier`](verifier.md) | verify | independent lens / isolation | ✅ |
| [`security-review`](security-review.md) | review · cross-cutting | independent lens | ✅ |
| [`design-review`](design-review.md) | review · cross-cutting | independent lens | ✅ |

## Format & portability

Each file is written as a **Claude Code subagent** (YAML frontmatter + a system-prompt body) so it drops
straight into `.claude/agents/`. The frontmatter is Claude-specific; the **body is the portable role
contract** — the part that transfers to any tool. Each body opens with a `Function: … · Delegate reason: …`
line so the role reads as a spec regardless of harness.

The `model:` values are **recommendations that demonstrate the principle**, not mandates — a fast model for
the mechanical `verifier`, a strong model for the `security-review` lens, `inherit` (use the session model)
elsewhere. Tune them per your layer profiles.

## Install

```bash
# Claude Code — the role .md files ARE the drop-in format (this README is docs, so drop it)
mkdir -p .claude/agents && cp agents/*.md .claude/agents/ && rm .claude/agents/README.md

# Codex — ready-made .toml versions live in codex/
mkdir -p .codex/agents && cp agents/codex/*.toml .codex/agents/
```

Or let [`../templates/link.sh`](../templates/link.sh) `--agents` do both (it already skips this README).

## Realizing them per tool

- **Claude Code** — the `*.md` files here *are* the format; copy into `.claude/agents/`, frontmatter works
  as-is. See [`../docs/setup/claude-code.md`](../docs/setup/claude-code.md#realizing-layer-profiles).
- **Codex** — ready-to-use `.toml` versions ship in [`codex/`](codex/) (the body maps to
  `developer_instructions`). See
  [`../docs/setup/codex.md`](../docs/setup/codex.md#realizing-subagents--layer-profiles) and
  [`codex/README.md`](codex/README.md).

Cross-cutting agents (`security-review`, `design-review`) run over the **diff**, across every path layer —
they are reviewers, not directories. Keep their always-on rules (e.g. "never log secrets") in the **root**
`AGENTS.md`.
