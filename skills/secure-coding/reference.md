# Secure coding — category checklist

The habits in [`SKILL.md`](SKILL.md), made concrete. Cross-references the focused skills where one exists.

## Injection (→ `input-sanitization`)
- Parameterize queries; never build SQL/NoSQL/LDAP from strings.
- Shell out with arg arrays, never an interpolated shell string; avoid shelling out at all if you can.
- Context-aware output encoding for HTML/JS/attributes; constrain file paths to an allowed root.

## Authorization & identity (→ `identity-management`)
- Check authz on the **resource**, not just the route (no IDOR).
- Enforce on the server for every action; deny by default.
- Sessions/tokens: short-lived, rotated, revocable; never in URLs or logs.

## Cryptography
- Use vetted libraries; no home-rolled crypto.
- Strong primitives only (AES-GCM, SHA-256+, Argon2/bcrypt/scrypt for passwords); no MD5/SHA1/DES/ECB.
- CSPRNG for anything security-relevant (tokens, salts) — not `Math.random`/`rand`.
- Secrets and keys from a secret store, not source (→ `secret-management`).

## Error handling & logging
- Fail closed; don't leak stack traces, queries, or internal detail to users.
- Never log secrets, tokens, or PII. Log security events (authn/authz failures) for detection.
- Don't swallow errors that hide a security-relevant failure.

## Deserialization & parsing
- No unsafe deserialization of untrusted data (`pickle`, `yaml.load`, native `readObject`).
- Set limits: max body size, max depth, timeouts — guard against resource exhaustion.

## Dependencies (→ `dependency-vuln-scan`)
- Pin versions and commit a lockfile; review new/updated deps.
- Prefer fewer, well-maintained dependencies; scan them in CI.

## Concurrency & state
- Watch for TOCTOU (check-then-use) on files and auth; make critical sections atomic.
- Don't rely on client-supplied state for security decisions.
