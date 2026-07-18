---
paths: ["web/**"]
---
Frontend work (Claude Code, path-scoped — loads only when touching `web/**`):

- Use design tokens from `@/styles/tokens`; never hard-coded hex, spacing, or font sizes.
- Route all API calls through the typed client in `web/lib/api.ts` — no raw `fetch` in components.
- Before claiming a UI change done, run `pnpm test -- web` and compare a screenshot of the affected view.

> This mirrors the frontend layer profile in `web/AGENTS.md`. The nested `AGENTS.md` is the portable,
> cross-tool form; this rule is the Claude-only, path-triggered realization. Use one or the other — this
> file shows the Claude-native option.
