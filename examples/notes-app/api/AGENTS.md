# AGENTS.md — api/ (backend layer profile)

> Nearest-file-wins: this applies to work under `api/`. Only what *differs* from the root file lives here.

## Layer profile: backend

- **Model:** prefer a strong model — auth, data integrity, and migrations are high-stakes.
- **Skills:** `prisma-migrate`.
- **Rules:** every route handler checks authz before touching data. Validate all input with the Zod schemas
  in `packages/shared`. All DB access goes through the repository layer in `api/repos/` — no inline queries.
- **Checks:** `pnpm test -- api`. For schema changes, generate a migration (`pnpm db:migrate:dev`) — never
  edit the database by hand.

## Structure (this layer)

- `api/routes/` — Fastify route handlers.
- `api/repos/` — data access; the only place that talks to Prisma.
- `api/prisma/schema.prisma` — the schema. Changes here require a migration.

## Don't

- ⛔ Don't run `db:migrate` against a non-local database without human confirmation.
- ⛔ Don't return raw Prisma models to the client — map through the DTOs in `packages/shared`.
