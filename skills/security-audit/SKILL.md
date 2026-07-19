---
name: security-audit
description: Systematically audit a codebase or system for security vulnerabilities against a threat model. Use when reviewing a whole codebase or feature (your own pre-release code or an unfamiliar external/client project) for security issues — not a single diff.
---

# Security audit

Codebase-agnostic — **assume you may be seeing this code for the first time.** Works for a pre-release pass on
your own code and for an unfamiliar external/client codebase.

> For a single **diff**, the `security-review` subagent is the lighter tool. Use this skill for a whole
> codebase, service, or feature.

## Method

1. **Orient — map the attack surface fast.** Entry points (HTTP routes, CLI args, queue/message consumers,
   webhooks), trust boundaries, data stores, secrets, outbound calls, and the auth flow. Run
   `bash scripts/surface-scan.sh [path]` to grep for common risk indicators and get a starting map. Read the
   nearest `AGENTS.md` for context if one exists.
2. **Threat-model.** For each entry point: *who* can reach it, *what* can they influence, *what's the worst
   outcome?* List the assets worth protecting (PII, credentials, money, infra access).
3. **Review by category.** Walk [`reference.md`](reference.md) — authn/authz, input validation, injection,
   secrets, crypto/TLS, data exposure, deserialization, dependencies, config — plus whatever the stack makes
   most likely.
4. **Confirm.** Trace each candidate finding to a concrete exploit path in the code. Mark suspicions you
   can't trace as "plausible, needs confirmation" — don't assert what you haven't traced.
5. **Report.** One finding per issue, highest severity first, using the severity rubric and report format in
   [`reference.md`](reference.md): severity, `file:line`, exploit scenario, fix.

## Rules

- **Confirmed over comprehensive** — one traced Critical beats ten vague "considers".
- **Severity = impact × exploitability**, per the rubric — not gut feel.
- **Read and report only.** Never run a found exploit against a live system or exfiltrate data.
- The root `AGENTS.md` holds the always-on rules (e.g. never log secrets) — flag violations against them.
