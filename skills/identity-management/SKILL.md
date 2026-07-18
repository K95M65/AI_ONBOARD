---
name: identity-management
description: Design and review authentication and authorization — sessions, tokens (JWT), OAuth2/OIDC, RBAC/ABAC, MFA, and password handling. Use when building or auditing login, access control, or any "who can do what" logic.
---

# Identity management

The two questions: **authentication** (who are you?) and **authorization** (what may you do?). Most access
bugs are authorization bugs — see the checklist and [`reference.md`](reference.md).

## When to use

Building or reviewing login, sessions, access control, or any permission decision.

## Authentication

- **Passwords:** hash with a slow, salted KDF (Argon2id / bcrypt / scrypt) — never fast hashes, never
  plaintext. Enforce length over complexity; check against breached-password lists.
- **MFA:** offer TOTP/WebAuthn for sensitive accounts; WebAuthn/passkeys where you can.
- **Sessions vs tokens:** server sessions (opaque id + secure cookie) are simplest and revocable. JWTs are
  stateless but hard to revoke — keep them short-lived with a refresh flow, and validate `alg`, `iss`, `aud`,
  `exp` every time. Never accept `alg: none`.
- **OAuth2 / OIDC:** use a library; use Authorization Code + PKCE; validate `state` (CSRF) and the id-token
  signature. Don't invent your own flow.

## Authorization

- **Enforce on every action, server-side, deny-by-default.** Never rely on a hidden UI element as a control.
- **Check the resource, not just the route** — the #1 bug is IDOR (user A reads user B's record by id).
- **RBAC or ABAC**, centrally enforced (middleware/policy layer), not scattered per-handler `if`s.
- **Least privilege** for the identity's scope and token lifetime.

## On Cloudflare

For app-level access without building auth, **Cloudflare Access** (Zero Trust) gates apps by identity/policy;
pair with Workers for fine-grained checks. See the `cloudflare-one` skill if vendored.

## Verify

Pair with `security-review`/`security-audit`; specifically probe for IDOR, missing server-side checks,
`alg:none`/unvalidated JWTs, and long-lived tokens.
