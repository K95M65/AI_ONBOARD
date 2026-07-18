# Security audit — category checklist

Loaded on demand. The methodology, severity rubric, and report format live in
[`../../docs/security-audit.md`](../../docs/security-audit.md); this is the operational **what to look for**.

Walk each category against the attack surface you mapped. Not every category applies to every stack — spend
time where the entry points and assets are.

## Authentication & authorization

- [ ] Every entry point (route, command, consumer) enforces authn where it should.
- [ ] Authorization is checked on the **resource/data**, not just the route — no IDOR (can user A read user
      B's record by changing an id?).
- [ ] No auth logic bypassable by ordering, default-allow, or a missing `return` after a failed check.
- [ ] Session/token handling: expiry, rotation, revocation; tokens not in URLs or logs.

## Input validation & injection

- [ ] All external input validated/normalized at the boundary (body, query, headers, CLI args, env, files).
- [ ] **SQL/NoSQL:** parameterized queries only — no string-built queries.
- [ ] **Command:** no shell-out with interpolated input; if unavoidable, use arg arrays, never a shell string.
- [ ] **Path traversal:** user-controlled paths are constrained to an allowed root; `..` can't escape.
- [ ] **XSS/template:** output encoded for its sink; no untrusted HTML; templates auto-escape.
- [ ] **SSRF:** outbound URLs from user input are allow-listed; no fetching arbitrary internal hosts.

## Secrets & sensitive data

- [ ] No secrets hard-coded or committed (keys, tokens, passwords, connection strings).
- [ ] Secrets not logged, not in error messages, not in analytics/telemetry.
- [ ] PII minimized in logs/responses; sensitive fields not over-returned by APIs.

## Crypto & transport

- [ ] TLS verification not disabled (`InsecureSkipVerify`, `verify=False`).
- [ ] No weak/broken primitives (MD5, SHA1 for security, DES, ECB); no home-rolled crypto.
- [ ] Randomness for security uses a CSPRNG, not `Math.random`/`rand`.
- [ ] Passwords hashed with a slow KDF (bcrypt/scrypt/argon2), salted.

## Deserialization, dependencies, config

- [ ] No unsafe deserialization of untrusted data (`pickle`, `yaml.load`, native `readObject`, etc.).
- [ ] Dependencies: known-vulnerable versions? unexpected/typosquat packages? lockfile present?
- [ ] Config: debug/verbose off in prod; permissive CORS (`*` with credentials); default creds; open
      admin/management endpoints; overly broad cloud IAM.

## Availability & abuse

- [ ] Rate limiting / quotas on public or expensive endpoints.
- [ ] No unbounded resource use from a single request (zip bombs, huge payloads, N+1 amplification).

## Stack-specific quick hits

- **Web/API:** authz-on-data (IDOR), mass-assignment, CSRF on state-changing routes.
- **CLI:** command injection via `exec`, path traversal on file args, TOCTOU on file writes, trusting `$PATH`.
- **Data/pipeline:** injection into query engines, unsafe eval of expressions, secrets in job configs.
