# Security audit — notes-app

> **Illustrative worked example** of the [`security-audit`](../../skills/security-audit/) skill's output,
> following the report format in [`docs/security-audit.md`](../../docs/security-audit.md). `notes-app` is a
> config-only example with no real source, so the findings below are representative of the *described*
> architecture — they show the deliverable's shape and rigor, not real traced bugs.

**Scope:** `api/` routes and data access, `web/` API client, auth flow, secret handling.
**Method:** surface-scan → threat model of each route → category review (see skill `reference.md`).

---

### [Critical] Notes readable across users (IDOR on `GET /notes/:id`)
- **Location:** `api/routes/notes.ts:42` (handler), `api/repos/notes.ts:18` (query)
- **Category:** authz
- **Exploit scenario:** the handler authenticates the request but fetches by `:id` alone
  (`findById(params.id)`) without checking the note's `ownerId` against the session user. Any logged-in user
  can read any note by incrementing the id.
- **Confidence:** confirmed (traced handler → repo, no ownership check on either)
- **Fix:** scope the query to the owner — `findByIdForUser(params.id, session.userId)` — and return 404 (not
  403) on a miss so ids aren't enumerable.

### [High] Secret logged on startup
- **Location:** `api/index.ts:15`
- **Category:** secrets
- **Exploit scenario:** `console.log('config', config)` prints the full config object, including
  `DATABASE_URL` (with password) and the JWT signing secret, to stdout — captured by the log aggregator and
  readable by anyone with log access. Violates the root `AGENTS.md` "never log secrets" rule.
- **Confidence:** confirmed
- **Fix:** remove the log, or serialize an allow-list of non-sensitive fields.

### [Medium] Permissive CORS with credentials
- **Location:** `api/index.ts:22`
- **Category:** config
- **Exploit scenario:** `cors({ origin: '*', credentials: true })` lets any origin make credentialed
  requests; combined with cookie auth this enables cross-site read of API responses. (Browsers block the
  literal `*`+credentials combo, but the pattern often gets "fixed" by reflecting the Origin header, which is
  worse.)
- **Confidence:** plausible (needs confirmation of the auth transport)
- **Fix:** allow-list known front-end origins explicitly; never reflect arbitrary `Origin`.

### [Low] No rate limit on `POST /auth/login`
- **Location:** `api/routes/auth.ts:8`
- **Category:** availability / abuse
- **Exploit scenario:** unlimited login attempts enable credential stuffing / brute force.
- **Confidence:** confirmed (no middleware present)
- **Fix:** add per-IP + per-account rate limiting and backoff on the login route.

---

## Summary

- **Findings:** 1 Critical, 1 High, 1 Medium, 1 Low.
- **Fix first:** the IDOR (Critical) — it exposes every user's notes and is trivially exploitable.
- **Out of scope / not reviewed:** the `web/` frontend beyond its API client, dependency CVEs (no lockfile
  reviewed), infrastructure/deploy config, and the Prisma migration history. Absence from this report does
  **not** mean those areas are clean.
