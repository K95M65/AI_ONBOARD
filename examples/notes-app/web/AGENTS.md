# AGENTS.md — web/ (frontend layer profile)

> Nearest-file-wins: this applies to work under `web/`. Only what *differs* from the root file lives here.

## Layer profile: frontend

- **Model:** prefer a fast model — high-volume, low-ambiguity component/styling work.
- **Skills:** `dataviz` (charts), `component-scaffold`.
- **Rules:** use design tokens from `@/styles/tokens` — never hard-coded hex, spacing, or font sizes. Match
  existing component patterns in `web/components/`.
- **Checks:** `pnpm test -- web` and compare a screenshot of the affected view before claiming done.

## Structure (this layer)

- `web/app/` — Next.js routes (App Router).
- `web/components/` — shared React components.
- `web/styles/tokens.ts` — the design tokens. Source of truth for color/spacing/type.

## Don't

- ⛔ Don't call the API with raw `fetch` from components — use the typed client in `web/lib/api.ts`.
- ⛔ Don't add a UI library without discussion; we hand-roll on the token system.
