---
name: secret-management
description: Store, inject, scope, and rotate secrets safely — API keys, tokens, DB credentials, signing keys. Use when adding a secret to a project, wiring secrets into an app or CI, or setting up rotation. Complements secret-scan (which detects leaked secrets).
---

# Secret management

The lifecycle side of secrets: `secret-scan` *finds* leaked ones; this is how to *handle* them so they don't
leak in the first place.

## When to use

Adding or wiring a secret (env, app, CI/CD), choosing where secrets live, or setting up rotation.

## Rules

1. **Never in source or logs.** Not in code, config committed to git, error messages, or telemetry. If it's
   ever been committed, treat it as compromised — rotate.
2. **Store in a secret manager, inject at runtime.** Local dev: `.env` (gitignored). Prod: a real store
   (cloud KMS/Secrets Manager, Vault, GitHub Actions secrets, **Cloudflare `wrangler secret put` / Secrets
   Store**). App reads from the environment/binding, never from a file in the repo.
3. **Least privilege + short lifetime.** Scope each secret to exactly what needs it; prefer short-lived,
   auto-rotated credentials (OIDC federation, workload identity) over long-lived static keys.
4. **One secret, one purpose, one consumer** where practical — so rotation and revocation are surgical.
5. **Rotate on a schedule and on exposure.** Have a rotation runbook *before* you need it; test it.

## On Cloudflare

- Workers secrets: `wrangler secret put <NAME>` (encrypted, not in `wrangler.toml`); read via the env binding.
- Prefer **Secrets Store** for shared/rotatable secrets across Workers.
- Never put secrets in `vars` (those are plaintext config), only in secrets.

## Verify

Run `secret-scan` on the repo and history; confirm no secret is committed and each has a rotation owner.
