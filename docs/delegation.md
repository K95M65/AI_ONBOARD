# Delegation & layers — how one agent becomes several

The [behavioral contract](agent-behavior.md) covers how a *single* agent works. This doc covers the level
above it: **when an agent should split work across subagents, and how to specialize that work by area.**

The whole model rests on keeping two axes separate:

- **Function = the role (the verb).** *What* the agent is doing: research, plan, execute, review, verify.
  This is the axis you split delegation on.
- **Layer = a profile (the adjective).** *Where* it's working: frontend, backend, data… A layer is **not a
  role** — it's an overlay that pins `{model, skills, conventions, checks}` to a slice of the codebase and
  attaches to whatever function-agent is operating there.

> **The one-line principle:** *Function defines the role; layer parameterizes it. Delegate for context
> isolation, parallelism, or an independent lens — never to mirror a human org chart.*

You never build a `frontend-developer`. You build an **executor**, and when it enters `web/**` it adopts the
**frontend profile**. The same executor in `api/**` adopts the **backend profile**. One role, specialized by
where it's working — so you keep full-stack, whole-feature coherence *and* per-area specialization.

---

## Axis 1 — Functions (the delegation taxonomy)

Split subagents by function. Each task type maps to a delegation shape:

| Task type | What the agent does |
|-----------|---------------------|
| **Trivial** (one-sentence diff) | Do it inline. No subagent, no plan. |
| **Feature / vertical slice** | Plan → execute as one full-stack slice → verify. Fan out only if parts are independently parallelizable. |
| **Bug / debug** | Spawn an isolated investigation subagent (protects main context) → apply fix → verify. |
| **Research / unknown** | Delegate to a research subagent; it returns a *summary*, not the raw dump. |
| **Review / audit** | Delegate to specialist reviewer(s) — **adversarial, never the author**. Often several lenses in parallel. |
| **Large migration / sweep** | Fan out parallel workers, one per unit of work. |

**Why delegate at all?** Only three reasons, and none of them is "that's a different person's job":

1. **Context isolation** — the subtask would bloat the main thread (deep investigation, large research).
2. **Parallelism** — independent units that can run at once (a sweep, multi-lens review).
3. **Independent lens** — the grader shouldn't be the author (adversarial review, second opinion).

If none of the three applies, don't delegate — just do it.

---

## Axis 2 — Layers (profiles that specialize the work)

Layers come in **two kinds**, and they bind differently. Getting this right is what keeps the model clean.

### Path-scoped layers — activate by location

**Frontend · Backend · Infrastructure · Data.** These own directories, so their profile is a **nested
`AGENTS.md`** in the layer's subtree. Closest-file-wins precedence *is* the activation mechanism — the
profile switches on when the agent touches files it governs. A profile pins:

- **Model** — the tier this work wants (fast model for high-volume UI; strong model for auth/data).
- **Skills** — which portable skills apply here.
- **Conventions** — the house rules for this layer.
- **Checks** — the verification commands that prove *this* layer's work is done.

```markdown
# web/AGENTS.md   ← the frontend profile, scoped by its location

## Layer profile: frontend
- Model:  prefer a fast model — high-volume, low-ambiguity UI work.
- Skills: dataviz, component-scaffold.
- Rules:  use design tokens (never hard-coded hex); match existing component patterns.
- Checks: `npm run test:web`, and compare a screenshot before claiming done.
```

Copy [`templates/AGENTS.layer.md`](../templates/AGENTS.layer.md) into a subdirectory to start one.

### Cross-cutting layers — apply everywhere, as a lens

**Security · Design.** These don't own a subtree — they're concerns that cut across *all* the path layers.
Don't force them into a directory profile. Realize them as:

- **Review-function agents** — a `security` reviewer and a `design`/UI reviewer that run over whatever was
  changed, regardless of which path layer it lives in. (This is exactly how the GSD suite ships
  `gsd-security-auditor` and `gsd-ui-auditor` — as reviewers, not directories.)
- **Skills** — e.g. a `security-review` or design-token skill any agent can invoke.
- **A few global rules** — the handful of always-on constraints (e.g. "never log secrets") live in the
  *root* `AGENTS.md`, not a nested one.

---

## The two axes composed — a role × layer matrix

Put them together and you get a matrix, not a headcount. The cell is *computed* (a function-agent picks up a
profile), never *staffed*:

|            | frontend | backend | infrastructure | data |
|------------|----------|---------|----------------|------|
| **execute** | fast model · design skills · token rules | strong model · authz rules | IaC skills · dry-run first | strong model · migration skills |
| **verify**  | `test:web` + screenshot | `test:api` | plan/dry-run diff | data-integrity checks |

…with **Security** and **Design** overlaid as review lenses across every column.

---

## The seam: declaration is portable, realization is tool-specific

A profile has two halves, and they live in different places:

- **Declarative half — portable.** "Frontend work should use a fast model and the dataviz skill." That's
  just prose in a nested `AGENTS.md`; every tool can read it. **Put it in `AGENTS.md`.**
- **Realization half — tool-specific.** *Actually* pinning the model and surfacing the skill only for
  `web/**` is done differently per harness. **Put it in [`setup/`](setup/).**

This is the same guidance-vs-enforcement split as the behavioral contract, one level down: `AGENTS.md`
*declares* the profile; the tool config *binds* it. See
[`setup/claude-code.md`](setup/claude-code.md#realizing-layer-profiles) for the first concrete wiring
(subagent `model:` frontmatter, `.claude/rules/` with `paths:`, and skill surfacing).
