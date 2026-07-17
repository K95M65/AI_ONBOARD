# AGENTS.md

> **This is a template.** Replace the bracketed placeholders with facts about *your* project, delete
> sections you don't need, and keep it short — agents read this on every session, so every line costs
> context. Aim for signal over completeness. See [`docs/agents-md.md`](docs/agents-md.md) for the format.

## Project overview

[One or two sentences: what this project is, who it's for, and the tech stack. Example:
"A TypeScript monorepo for the Acme billing platform. Next.js frontend, Fastify API, Postgres via Prisma."]

## Setup

```bash
[# the exact commands to get from a fresh clone to a running dev environment]
[npm install]
[cp .env.example .env]
[npm run dev]
```

## Build, test, and lint

Run these before considering a task done. Agents: **always run the checks relevant to files you changed.**

```bash
[npm run build]      # [compile / typecheck]
[npm test]           # [full test suite]
[npm test -- path]   # [single test file — prefer this while iterating]
[npm run lint]       # [lint + format check]
```

## Project structure

- `[src/]` — [what lives here]
- `[tests/]` — [test layout and naming convention]
- `[packages/]` — [for monorepos: what each package does]

## Conventions

- **Language / style:** [e.g. TypeScript strict mode; formatting is handled by Prettier — do not hand-format.]
- **Naming:** [e.g. camelCase for functions, PascalCase for components, kebab-case for files.]
- **Imports:** [e.g. use the `@/` path alias, not relative `../../` chains.]
- **Tests:** [e.g. every new module gets a colocated `*.test.ts`; use the existing test helpers in `tests/util`.]
- **Commits:** [e.g. Conventional Commits; keep changes atomic.]

## What to do / not do

- ✅ [Prefer editing existing files over adding new ones.]
- ✅ [Match the style of surrounding code.]
- ⛔ [Never commit secrets, `.env` files, or generated artifacts.]
- ⛔ [Do not modify `[generated/]` or `[migrations/]` by hand.]
- ⛔ [Do not upgrade dependencies unless the task is specifically about that.]

## Security & safety

- [Secrets live in `.env` (gitignored) and in the CI secret store — never inline them.]
- [Destructive commands (`db reset`, prod deploys) require explicit human confirmation.]

## Good to know

- [Any non-obvious gotchas: flaky tests, slow builds, required services, auth quirks.]
- [Links to deeper docs: architecture, ADRs, runbooks.]

---
<!--
Notes for maintaining this file (delete before shipping, or keep — agents ignore HTML comments):

- Nested AGENTS.md files override this one for their subtree. Put package-specific rules in
  packages/<name>/AGENTS.md rather than bloating this root file.
- Keep tool-specific config OUT of this file so it stays portable. Claude Code hooks, Codex
  config.toml, etc. belong in their own files — see docs/setup/.
-->
