# Cloudflare skills (vendored)

A curated set of [Cloudflare's Agent Skills](https://github.com/cloudflare/skills) for teams building on the
Cloudflare Developer Platform. Vendored here (Apache-2.0) so they install and version alongside the rest of
this library — see [`NOTICE.md`](NOTICE.md) for provenance and attribution.

Because Agent Skills is an open standard, these are the **same `SKILL.md` format** as the rest of `skills/`
and install into the same places (`.claude/skills/` for Claude Code, `.agents/skills/` for Codex).

## What's here

| Skill | What it does |
|-------|--------------|
| [`wrangler`](wrangler/) | Workers CLI — deploy/dev/manage Workers, KV, R2, D1, Queues, Workflows, Secrets Store |
| [`workers-best-practices`](workers-best-practices/) | Review/author Workers code vs production best practices (doubles as a linter) |
| [`durable-objects`](durable-objects/) | Build/review Durable Objects — RPC, SQLite, alarms, WebSockets, Vitest |
| [`cloudflare-one`](cloudflare-one/) | Zero Trust / SASE — Access, Gateway, WARP, Tunnel, DLP (pairs with `identity-management`) |
| [`turnstile-spin`](turnstile-spin/) | End-to-end Turnstile/CAPTCHA bot protection setup (has scripts — see NOTICE) |
| [`agents-sdk`](agents-sdk/) | Stateful AI agents on Workers — Agent class, state, Workflows, MCP, streaming |
| [`cloudflare-email-service`](cloudflare-email-service/) | Transactional email — Workers binding/REST, routing, SPF/DKIM/DMARC |
| [`sandbox-sdk`](sandbox-sdk/) | Sandboxed code execution on Workers — interpreters, CI, untrusted code |

## Install

Same as any skill in this repo — `link.sh --skills` picks these up automatically (it discovers skills at any
depth), or copy a folder directly:

```bash
cp -R skills/cloudflare/wrangler .claude/skills/     # Claude Code
cp -R skills/cloudflare/wrangler .agents/skills/     # Codex
```

## Note on retrieval bias

These skills deliberately tell the agent to **prefer retrieving current Cloudflare docs over memorized
knowledge** — Cloudflare's platform moves fast. That's intended; don't "fix" it.

## Staying current

These are pinned to an upstream commit (`.upstream-commit`). To refresh, re-vendor from
<https://github.com/cloudflare/skills>, or install upstream live via `npx skills` / the Claude Code plugin
(`/plugin install cloudflare@cloudflare`) and skip the vendored copy.
