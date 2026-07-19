# Threat model — STRIDE prompts & template

## STRIDE, with prompts

Apply each to your processes, data stores, data flows, and especially **trust-boundary crossings**.

| Category | Threat | Ask | Typical control |
|----------|--------|-----|-----------------|
| **S**poofing | Attacker pretends to be someone/something | Can identity be forged? Is every actor authenticated? | authn, mutual TLS, signed tokens |
| **T**ampering | Unauthorized modification of data/code | Can data be altered in transit or at rest? | integrity checks, signing, authz, input validation |
| **R**epudiation | Denying an action, no proof | Can you prove who did what? | audit logs, signed receipts |
| **I**nformation disclosure | Exposure of data | Can someone read what they shouldn't? | authz-on-data, encryption, least-exposure responses |
| **D**enial of service | Making it unavailable | Can one actor exhaust resources? | rate limits, quotas, bounded work |
| **E**levation of privilege | Gaining unauthorized capability | Can a user become admin / escape a boundary? | authz on every action, sandboxing, least privilege |

## Data-flow diagram (text is fine)

```
[User] --HTTPS--> ( API handler ) --query--> [DB]
   |                    |
   |                    +--calls--> ( 3rd-party API )
trust boundary: ^ internet↔service    ^ service↔external
```

Number each boundary crossing; those are where most real threats live.

## Threat table template

```markdown
| # | Element / flow | STRIDE | Threat | Likelihood×Impact | Mitigation | Owner |
|---|----------------|--------|--------|-------------------|-----------|-------|
| 1 | POST /login    | S, D   | credential stuffing | High×High | rate limit + lockout | api |
| 2 | GET /notes/:id | I, E   | IDOR — read others' notes | High×High | authz on ownerId | api |
```

## Output doc skeleton

```markdown
# Threat model — <feature/system>
## Scope & assumptions
## Data flow (DFD)
## Assets
## Threats (table above)
## Top risks to address first
## Out of scope
```

Keep it proportionate: a login feature warrants a page, not a treatise. The value is naming the boundary
crossings and the assets — the table falls out of that.

## Priority rubric

Rate each threat using likelihood × impact:

- **Critical:** likely exploitation with severe impact; fix before release.
- **High:** a credible path to significant impact.
- **Medium:** limited impact or a hard precondition.
- **Low:** minor impact, unlikely conditions, or defense-in-depth.

Label uncertainty explicitly and keep unconfirmed threats below Critical.
