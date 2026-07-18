# Identity management — patterns & pitfalls

## Session vs JWT — pick deliberately

| | Server session | JWT (stateless) |
|---|----------------|-----------------|
| Revocation | Easy (delete server-side) | Hard (needs denylist / short TTL + refresh) |
| Scale | Needs shared session store | No lookup on validate |
| Best for | Most web apps | Service-to-service, short-lived access tokens |

If you use JWTs: short `exp`, refresh-token rotation, validate `alg`/`iss`/`aud`/`exp` every request, reject
`alg:none`, and don't put sensitive data in the (readable) payload.

## Common pitfalls

- **IDOR** — authorize the *resource* by owner, not just "is logged in".
- **Missing function-level authz** — the endpoint isn't in the UI, but it's still callable.
- **Trusting the client** — role/flags from a cookie or request body instead of the server.
- **`alg:none` / weak JWT secret** — accepting unsigned or HMAC-with-public-key tokens.
- **No CSRF protection** on cookie-authenticated state-changing routes (use SameSite + tokens).
- **Session fixation** — rotate the session id on login.
- **Verbose auth errors** — "user not found" vs "wrong password" enables enumeration.
- **Long-lived tokens** with broad scope — blast radius on leak.

## Cookie flags for session cookies

`Secure; HttpOnly; SameSite=Lax` (or `Strict` for pure first-party); scope `Path`/`Domain` narrowly; set a
sensible `Max-Age`.
