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

## How to work

> Unlike the rest of this file, this section is **not** project-specific — it's the default working
> style we ask every agent to follow, distilled from OpenAI's and Anthropic's published guidance. Keep it
> as-is unless you have a reason to change it. Rationale and sources: [`docs/agent-behavior.md`](docs/agent-behavior.md).

- **Understand before you change.** Read the relevant code and confirm how it works before editing. If you're unsure what a file contains or how something is structured, open it — don't guess.
- **Plan when it's non-trivial.** If you can describe the change in one sentence, just make it. Otherwise outline the steps first, especially for multi-file or unfamiliar work.
- **Be persistent within scope.** See the task through to a working, verified result before handing back — don't stop at "should work." But check in *first* before expanding scope beyond what was asked, and before anything irreversible (data loss, deploys, force-push, deleting files you didn't create).
- **Verify, then claim.** Run the checks relevant to what you changed (above) and show the evidence — the command and its output — instead of asserting success. If you can't verify it, say so; don't ship it.
- **Fix causes, not symptoms.** Don't suppress an error or weaken a check just to make it pass.
- **Match the surroundings.** Follow the conventions below and the style of nearby code; prefer editing existing files over adding new ones.
- **Delegate deliberately.** Split work off to a subagent only for context isolation, parallelism, or an independent lens (e.g. adversarial review) — not to mirror a team org chart. Layer-specific rules live in the nearest `AGENTS.md`. See [`docs/delegation.md`](docs/delegation.md).
- **Report honestly.** If tests fail, a step was skipped, or you got blocked, say so plainly with the details.

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
