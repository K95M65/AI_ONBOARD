---
name: threat-model
description: Produce a threat model for a feature or system using STRIDE and a data-flow view. Use at design time before building something security-sensitive, or as the framing step of a security audit — to decide what's worth protecting before hunting for bugs.
---

# Threat model

The **design-time** companion to `security-audit`: the audit *finds* bugs; this decides *what you're
protecting and from whom*, so the audit knows where to look.

## When to use

Before building a security-sensitive feature (auth, payments, file handling, multi-tenant data), or as the
first step of an audit on an unfamiliar system.

## Steps

1. **Draw the data flow.** List external entities (users, third parties), processes (services, handlers),
   data stores, and the **trust boundaries** the data crosses. A rough text DFD is enough.
2. **Identify assets.** What's worth stealing or breaking? PII, credentials, money, integrity of records,
   availability.
3. **Apply STRIDE** to each element and each boundary crossing — see [`reference.md`](reference.md) for the
   per-category prompts.
4. **Rate & prioritize.** For each threat: likelihood × impact (reuse the severity rubric in
   [`../../docs/security-audit.md`](../../docs/security-audit.md)). Focus on boundary crossings.
5. **Assign mitigations.** For each meaningful threat, name the control (authz check, validation, rate limit,
   encryption) and where it lives. Gaps become audit targets or backlog items.

## Output

A short doc: the DFD, the asset list, a threat table (element → STRIDE category → threat → likelihood/impact →
mitigation/owner), and the top risks to address first. See the template in [`reference.md`](reference.md).
