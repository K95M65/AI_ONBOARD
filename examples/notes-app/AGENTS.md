# AGENTS.md

## Project overview

`notes-app` — a TypeScript monorepo for a personal notes tool. Next.js frontend (`web/`), Fastify API
(`api/`), Postgres via Prisma. Package manager is **pnpm**; workspaces defined in `pnpm-workspace.yaml`.

## Setup

```bash
pnpm install
cp .env.example .env      # fill in DATABASE_URL
pnpm db:migrate           # apply Prisma migrations
pnpm dev                  # web on :3000, api on :4000
```

## Build, test, and lint

Run the checks relevant to files you changed before considering a task done.

```bash
pnpm build                # typecheck + compile all packages
pnpm test                 # full suite
pnpm test -- web/notes    # single test path — prefer this while iterating
pnpm lint                 # eslint + prettier check
```

## How to work

> Not project-specific — the default working style, kept as-is from the AI_ONBOARD template.

- **Understand before you change.** Read the relevant code first; if unsure, open the file — don't guess.
- **Plan when it's non-trivial.** One-sentence diff → just do it; otherwise outline steps first.
- **Be persistent within scope.** Finish and verify before handing back, but check in first before expanding
  scope or doing anything irreversible (migrations against real data, deploys, force-push).
- **Verify, then claim.** Run the checks above and show the command + output; don't assert success.
- **Fix causes, not symptoms.** Don't suppress an error or weaken a check to make it pass.
- **Match the surroundings.** Follow the conventions below and nearby code.
- **Delegate deliberately.** Subagent only for isolation, parallelism, or an independent lens. Layer rules
  live in the nearest `AGENTS.md`.
- **Report honestly.** Say plainly if tests fail, a step was skipped, or you got blocked.

## Project structure

- `web/` — Next.js app (React, TypeScript). Has its own `AGENTS.md` (frontend profile).
- `api/` — Fastify service + Prisma schema. Has its own `AGENTS.md` (backend profile).
- `packages/shared/` — types and Zod schemas shared by both. Changes here ripple to both — run the full suite.

## Conventions

- **Language:** TypeScript strict mode. Formatting is Prettier — do not hand-format.
- **Naming:** camelCase functions, PascalCase components, kebab-case files.
- **Imports:** use the `@/` path alias, not `../../` chains.
- **Commits:** Conventional Commits; keep changes atomic.

## Security & safety

- **Never log secrets** or PII, in any layer. Secrets live in `.env` (gitignored) — never inline them.
- Destructive commands (`db:reset`, prod deploys) require explicit human confirmation.
