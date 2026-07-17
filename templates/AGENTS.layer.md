# AGENTS.md — layer profile

> Copy this into a **subdirectory** that owns a layer (e.g. `web/`, `api/`, `infra/`, `data/`) and rename it
> to `AGENTS.md`. Agents read the closest `AGENTS.md` to the file they're editing, so this profile activates
> automatically when work happens in this subtree — no wiring needed. Keep it to what *differs* from the root
> file; don't repeat the root. See [`docs/delegation.md`](../docs/delegation.md).

## Layer profile: [frontend | backend | infrastructure | data]

- **Model:** [the tier this work wants — e.g. a fast model for high-volume UI, a strong model for auth/data.
  Portable *declaration* only; the actual pinning is per-tool — see docs/setup/.]
- **Skills:** [which skills apply here — e.g. `dataviz`, `component-scaffold`.]
- **Rules:** [the house rules that differ from the root — e.g. use design tokens, never hard-coded hex.]
- **Checks:** [the verification commands that prove *this* layer's work is done — e.g. `npm run test:web`,
  plus a screenshot compare for UI.]

## Structure (this layer only)

- `[components/]` — [what lives here]
- `[lib/]` — [what lives here]

## Don't

- ⛔ [layer-specific guardrails — e.g. don't call the backend directly from components; go through the API client.]

<!--
Cross-cutting layers (Security, Design) are NOT path profiles — they apply everywhere. Realize them as
review-function agents + skills, with a few always-on rules in the ROOT AGENTS.md. See docs/delegation.md.
-->
