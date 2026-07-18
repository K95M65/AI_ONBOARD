# Choosing a mechanism — AGENTS.md vs Skills vs Subagents

This repo gives you a few different places to put agent knowledge. Putting a thing in the wrong one is the
most common way to waste context or scatter logic: a procedure pasted into every project's `AGENTS.md`
bloats every session; a fact buried in a skill never loads when you need it. This doc is the decision rule.

## The three mechanisms at a glance

| | **AGENTS.md** (+ layer profiles) | **Skill** | **Subagent** |
|---|---|---|---|
| **Loaded** | Every session, always | On demand, when triggered | On delegation, in its own context |
| **Answers** | "How does *this project* work?" | "How do I *perform this task*?" | "*Who* handles this — isolated / independent?" |
| **Reusable across repos?** | No — this repo | Yes | Yes (it's a role) |
| **Who runs it** | Context for the current agent | The current agent runs the procedure *inline* | A *separate* agent, returns a summary |
| **Cost** | Paid every session | Paid only when used | A whole extra context window |

## The decision, in order

Ask these top to bottom; take the first "yes":

1. **Is it a durable fact about *this project* that applies broadly, every session?**
   → **`AGENTS.md`.** Root file for repo-wide facts; a **nested `AGENTS.md`** (layer profile) for facts that
   apply only under `web/`, `api/`, etc. (Keep it lean — every line is paid on every session.)

2. **Is it a repeatable *procedure or capability* — especially one with scripts — needed only *sometimes*?**
   → **Skill.** It stays out of context until its `description` matches the task, then loads on demand.
   Reusable across every repo and (being an open standard) across Claude Code + Codex.

3. **Do you need context *isolation*, *parallelism*, or an *independent lens* (the grader ≠ the author)?**
   → **Subagent.** Delegate the work to a separate context that hands back a summary. If none of these three
   applies, don't delegate — just do the work inline.

If nothing above fits, it's probably a one-off: put it in your prompt, not a persistent mechanism.

## The subtle one: skill vs subagent

Same expertise can live in either — they differ in **delivery**, not knowledge:

- A **skill** is a procedure the **current agent runs inline**. No isolation: it reads into the working
  context and the same agent executes it.
- A **subagent** is **delegated, isolated** context. A different agent runs it and returns only a summary.

`security-review` is the clean example. It exists here as a **subagent** — because a security review wants an
*independent lens* (the reviewer shouldn't be the author) and *fresh context*. But the same checklist could
also be a **skill** the driver runs inline when it just wants to self-check a small change. Not redundant —
different delivery for different needs:

- Reach for the **skill** when you only need the *procedure* applied.
- Reach for the **subagent** when you need the reviewer *separate* from the author, or need to protect the
  main context from a large investigation.

## AGENTS.md vs skill

Both can hold "how to do X," so the tie-breaker is **cost and reuse**:

- `AGENTS.md` is paid **every session** and describes **this project**. A sometimes-relevant procedure sitting
  in it is dead weight on every unrelated task — and bloat makes the agent follow the *rest* of the file less
  well. Anthropic's own guidance: don't put sometimes-relevant procedures in the always-loaded file.
- A **skill** is paid **only when triggered** and is **portable** across repos. That's where a repeatable
  procedure belongs.

Rule of thumb: if you'd copy the same procedure into three different projects' `AGENTS.md`, it's a skill.

## They compose

These aren't exclusive — the stack works *because* they layer:

- A **layer profile** (`AGENTS.md`) *names* which **skills** apply in its area ("frontend → `dataviz`,
  `component-scaffold`").
- A **subagent** *invokes* **skills** inside its own context, and reads the nearest **`AGENTS.md`** for
  project conventions.
- So a task can flow: driver reads `AGENTS.md` → delegates review to a **subagent** → which pulls in a
  **skill** to do the check.

## Smell tests (anti-patterns)

- **A procedure copy-pasted into every project's `AGENTS.md`** → make it a skill.
- **A subagent that just runs a procedure** with no isolation/parallelism/independent-lens benefit → make it
  a skill; delegation buys you nothing here.
- **A skill that encodes project-specific facts** (paths, service names) → those belong in `AGENTS.md`; keep
  the skill portable.
- **A subagent created to "be the frontend developer"** → org-chart anti-pattern; execution stays merged. See
  [`../agents/README.md`](../agents/README.md#why-theres-no-developer-agent).

## Adjacent: guidance vs enforcement

All three mechanisms are **advisory** — the model may not comply. For steps that **must** happen every time,
reach past them to deterministic enforcement: **hooks** and `permissions.deny` in Claude Code, **sandbox
modes + approval policies** in Codex. See [`agent-behavior.md`](agent-behavior.md#guidance-vs-enforcement-important-caveat).
