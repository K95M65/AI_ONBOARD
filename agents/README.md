# Reference subagents

A small, portable starter set of subagents that realize the **function axis** of
[`../docs/delegation.md`](../docs/delegation.md): research, review, and verify — plus the cross-cutting
review lenses (**security**, **design**, **accessibility**). These are the roles where delegation actually pays off — context
isolation, parallelism, or an independent lens — not an org chart.

[See these roles in the interactive request flow](https://k95m65.github.io/AI_ONBOARD/#router).

<!-- generated:agents-inventory:start -->
**6 reference subagents · research, review, verification, security, design, and accessibility.**
<!-- generated:agents-inventory:end -->

## Why there's no `developer` agent

The developer isn't missing — **it's the driver.** This set is the specialist *eyes* you delegate *to*; the
generalist *hands* that write code is the main agent you're already running. Implementation is the default
behavior, and it's already fully specified without a dedicated persona by two things:

- the **behavioral contract** (`AGENTS.md` → *How to work*: understand → plan → change → verify), and
- the **layer profile** it picks up by location (the nested `AGENTS.md` that pins model, skills, conventions,
  and checks for `web/`, `api/`, …).

So "execute × frontend" isn't an agent — it's the driver working in `web/` with the frontend profile applied.
A canned `frontend-developer` would just be the main agent carrying a frozen, worse copy of that profile.
Splitting execution by layer also backfires: a feature is a vertical slice through both layers, and a
frontend/backend handoff mid-feature is how contract mismatches happen. Merged execution keeps the slice
coherent. (Codex makes the same point natively — its built-in `worker` is the execution agent and `explorer`
≈ our `researcher`; redefining them would only shadow better defaults.)

**The one exception — parallelism.** An executor-as-subagent earns its place only when you fan out genuinely
independent units (a migration sweep, or independent FE/BE tickets run concurrently in separate contexts or
worktrees). Even then it's thin: its instructions are just *the behavioral contract + "do this one unit"*,
because it inherits the layer profile by path. That's why it's not in the default set — a single canned
executor would carry the wrong model/tools for half the layers, and per-layer developer agents would
reintroduce the org-chart split this model rejects. If you need it, add one minimal `worker` (full tools,
`model: inherit`) with a *"parallel fan-out only"* guardrail — don't build a roster. See
[`../docs/delegation.md`](../docs/delegation.md).

## The set

| Agent | Function | Delegate reason | Read-only? |
|-------|----------|-----------------|:---------:|
| [`researcher`](researcher.md) | research | context isolation | ✅ |
| [`reviewer`](reviewer.md) | review | independent lens | ✅ |
| [`verifier`](verifier.md) | verify | independent lens / isolation | ✅ |
| [`security-review`](security-review.md) | review · cross-cutting | independent lens | ✅ |
| [`design-review`](design-review.md) | review · cross-cutting | independent lens | ✅ |
| [`accessibility-review`](accessibility-review.md) | review · cross-cutting | independent lens | ✅ |

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

# opencode — ported .md versions live in opencode/
mkdir -p .opencode/agents && cp agents/opencode/*.md .opencode/agents/
```

For a managed installation across selected harnesses, use
[`scripts/ai_onboard.py`](../scripts/ai_onboard.py) with `--agents`; it records ownership and supports safe
upgrade and uninstall:

```bash
python3 /path/to/AI_ONBOARD/scripts/ai_onboard.py \
  --target /path/to/project \
  install \
  --harness claude,codex,opencode \
  --profile core \
  --agents
```

[`../templates/link.sh`](../templates/link.sh) `--agents` remains a legacy copy path.

## Realizing them per tool

- **Claude Code** — the `*.md` files here *are* the format; copy into `.claude/agents/`, frontmatter works
  as-is. See [`../docs/setup/claude-code.md`](../docs/setup/claude-code.md#realizing-layer-profiles).
- **Codex** — ready-to-use `.toml` versions ship in [`codex/`](codex/) (the body maps to
  `developer_instructions`). See
  [`../docs/setup/codex.md`](../docs/setup/codex.md#realizing-subagents--layer-profiles) and
  [`codex/README.md`](codex/README.md).
- **opencode** — ported `.md` versions ship in [`opencode/`](opencode/) (`mode: subagent` + a `permission:`
  block instead of a `tools:` list). See
  [`../docs/setup/opencode.md`](../docs/setup/opencode.md#realizing-subagents--skills) and
  [`opencode/README.md`](opencode/README.md).

Cross-cutting agents (`security-review`, `design-review`, `accessibility-review`) run over the **diff**,
across every path layer — they are reviewers, not directories. Keep their always-on rules (e.g. "never log
secrets") in the **root** `AGENTS.md`. For a whole-codebase security pass (not a diff), `security-review` invokes the
[`security-audit`](../skills/security-audit/) skill — see [`../docs/security-audit.md`](../docs/security-audit.md).
For a whole product or application accessibility pass, use the `audit-accessibility` skill; delegate the
independent lens when author/reviewer separation matters.

After adding or changing canonical agent frontmatter, run `python3 scripts/sync_project_docs.py` from the
repository root so the website catalog and synchronized inventory remain current.
