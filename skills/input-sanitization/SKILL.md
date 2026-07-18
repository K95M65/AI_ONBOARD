---
name: input-sanitization
description: Correctly validate untrusted input and encode output per sink to prevent injection (SQL, command, XSS, path, SSRF). Use when handling any external input — request bodies, query params, headers, CLI args, file contents, env vars — or when fixing an injection finding.
---

# Input sanitization

The single highest-value secure-coding discipline: most vulnerabilities are mishandled untrusted input.

## The principle: validate in, encode out

These are **two different jobs** — you usually need both:

- **Validate at the boundary.** Allow-list the shape/type/range you expect and reject early. **Normalize
  first** (Unicode, path, case), *then* validate — otherwise an encoded payload slips past.
- **Encode at the sink.** The same value is safe or dangerous depending on where it goes. Encode for the
  destination at the moment you use it, not once up front.

## Per-sink rules

See [`reference.md`](reference.md) for the table. The essentials:

- **SQL / NoSQL:** parameterized queries / prepared statements. Never string-build.
- **Shell / OS command:** pass an argument array to `exec`; never build a shell string. Better: don't shell
  out.
- **HTML / template:** context-aware output encoding (body vs attribute vs JS vs URL); let the template
  engine auto-escape; never inject untrusted HTML.
- **Filesystem path:** resolve and confirm the result stays within an allowed root; reject `..`.
- **Outbound URL (SSRF):** allow-list destination hosts; block internal/link-local ranges.

## Rules

- **Allow-list, never block-list.** Enumerating "bad" characters always misses one.
- **Validation ≠ encoding.** Passing validation doesn't make a value safe to concatenate into a query.
- **Server-side only.** Client-side validation is UX; the server must re-check everything.
