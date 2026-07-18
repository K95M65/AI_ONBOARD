---
name: prisma-migrate
description: Safely create and apply a Prisma schema migration, guarding against running against a non-local database. Use when changing prisma/schema.prisma or adding/altering database tables, columns, indexes, or relations.
---

# Prisma migrate

## When to use

Any change to `schema.prisma` — a new model, field, index, or relation. Never edit the database by hand and
never hand-write migration SQL.

## Steps

1. Edit `schema.prisma`.
2. Create the migration:
   ```bash
   bash scripts/new-migration.sh <migration-name>
   ```
   - Generates the SQL and applies it to your **local dev** database via `prisma migrate dev`.
   - **Refuses to run** if `DATABASE_URL` looks non-local (staging/prod) unless you pass `--force`.
3. Review the generated SQL under `prisma/migrations/<timestamp>_<name>/` before committing.
4. Commit `schema.prisma` and the new migration folder **together**.

## Safety

- The local-only guard is a safety net, not a substitute for judgment: migrating a shared or production
  database still requires explicit human confirmation.
- Never delete or edit an already-applied migration — create a new one that carries the correction.
- If `migrate dev` reports drift or wants to reset, **stop** and ask — a reset drops data.
