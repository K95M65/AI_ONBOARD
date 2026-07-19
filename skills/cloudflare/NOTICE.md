# NOTICE — vendored Cloudflare skills

The skills in this directory are **vendored from the upstream Cloudflare project** and are **not original to
AI_ONBOARD**.

- **Source:** <https://github.com/cloudflare/skills>
- **Upstream commit:** `70215303d44a81a0db3219428f4825b604fc6061` (see [`.upstream-commit`](.upstream-commit))
- **License:** Apache License 2.0 — see [`LICENSE`](LICENSE). Copyright © Cloudflare, Inc.

## Modifications

Per Apache-2.0 §4(b), changes are stated here:

- The eight skill folders below were relocated from upstream `skills/<name>/` into
  `skills/cloudflare/<name>/` for organization within this library.
- `turnstile-spin` was security-adapted so API tokens are never requested in chat and widget secrets are
  written only to caller-selected, new mode-`0600` transfer files rather than stdout. Its bundled creation
  and recovery instructions were updated to match.
- The other seven skill folders were copied verbatim. This NOTICE, the `README.md`, and
  `.upstream-commit` were added.

## Vendored skills (curated subset)

`wrangler`, `workers-best-practices`, `durable-objects`, `cloudflare-one`, `turnstile-spin`, `agents-sdk`,
`cloudflare-email-service`, `sandbox-sdk`.

## Deliberately not vendored

- **`cloudflare`** (the umbrella skill, ~320 reference files / 1.9 MB) — too large to vendor wholesale;
  install upstream if you need it.
- **`cloudflare-one-migrations`** — only useful mid-migration off another vendor.
- **`web-perf`** — hard-requires the external `chrome-devtools-mcp` server, so it won't work standalone here.

Get any of these from upstream: `npx skills`, or the Claude Code plugin (`/plugin install cloudflare@cloudflare`).

## Caveat — `turnstile-spin` scripts

`turnstile-spin/scripts/` (`auth-probe.sh`, `widget-create.sh`, `fetch-secret.sh`, `validate.sh`,
`persist-skill.sh`) call the Cloudflare API and require `CLOUDFLARE_API_TOKEN` (and optionally
`CLOUDFLARE_ACCOUNT_ID`) in the environment. Review `persist-skill.sh` before use — it writes state back.
