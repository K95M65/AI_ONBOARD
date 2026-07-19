---
name: secure-coding
description: Practices for writing secure code — the defensive habits and per-category rules that prevent vulnerabilities before they ship. Use when implementing security-sensitive features (auth, input handling, data access, crypto) or as a checklist while reviewing them.
---

# Secure coding

The **write-time** member of the security set: `threat-model` frames what to protect (before),
`secure-coding` prevents defects (during), `security-audit` / `security-review` catch what slipped (after).

## When to use

Implementing or reviewing code that handles untrusted input, authentication/authorization, sensitive data,
secrets, or cryptography.

## Core habits

- **Validate in, encode out.** Validate untrusted input at the boundary; encode output for its sink. (Deep
  dive: the `input-sanitization` skill.)
- **Least privilege.** Narrowest scope, capability, and lifetime for every token, query, and process.
- **Fail closed.** On error or ambiguity, deny — never default-allow.
- **Never trust the client.** Re-verify every check server-side; client-side validation is UX, not security.
- **Keep secrets out of code and logs.** (Deep dive: `secret-management`; detection: `secret-scan`.)
- **Prefer safe defaults and reviewed libraries** over hand-rolled security (crypto, auth, parsers).

## By category

Walk [`reference.md`](reference.md): injection, authz/IDOR, crypto, error handling & logging,
deserialization, and dependencies. For the two biggest areas use the focused skills —
`input-sanitization` and `identity-management`.

## Verify

Pair with `security-review` (on a diff) or `security-audit` (on a codebase), and run `dependency-vuln-scan`
and `secret-scan`. Wire them into CI with `automated-security-review`.
