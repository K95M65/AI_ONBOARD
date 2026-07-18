---
name: preserve-web-evidence
description: Preserves lawful public-web evidence with reproducible provenance using screenshots, PDFs, saved responses, WARC, or WACZ according to the required fidelity. Use when an authorized investigation, audit, research project, or change record needs durable source capture, replay, hashing, or a snapshot manifest; do not use for covert collection, private or authenticated content without explicit authority, or browser regression testing.
---

# Preserve web evidence

Capture the smallest lawful artifact that can support the claim and be independently checked later.
Preservation records what was observed; it does not prove that the source was true.

## Establish the capture boundary

State the public URL or authorized target, purpose, time window, required fidelity, allowed crawl scope,
personal-data handling, and retention destination. Do not bypass authentication, paywalls, robots controls,
rate limits, CAPTCHAs, or access restrictions.

Use no paid service by default. Prefer already-available browser capabilities and free or local tools. Do
not install a crawler, extension, or container unless the user authorizes setup.

## Choose the artifact

Read [references/capture-formats.md](references/capture-formats.md), then select deliberately:

- screenshot for visible appearance;
- PDF for a paginated human-readable rendering;
- saved response or HTML for static source inspection;
- WARC for protocol-level web records;
- WACZ for a packaged, indexed, replay-oriented collection.

Use more than one format only when each answers a different evidence question.

## Capture with provenance

For every artifact, record:

- original URL, final URL, redirects, and UTC retrieval time;
- collector and tool/version;
- viewport, browser, locale, and authentication state when material;
- crawl scope, depth, inclusions, exclusions, and rate limits;
- source title, observed date, and the claim the artifact supports;
- capture errors, missing resources, dynamic states, and known replay limits.

For an interactive page, deliberately visit the material states within scope. Do not expand into adjacent
profiles, personal data, or unrelated domains merely because the crawler can.

## Preserve integrity

1. Save artifacts in the authorized workspace using stable, non-sensitive names.
2. Generate a SHA-256 digest for each final artifact when a hashing tool is available.
3. Write a manifest that maps digest, filename, URL, retrieval time, method, and handling notes.
4. Replay or reopen the artifact without relying on the live source when the format supports it.
5. Spot-check text, images, navigation, timestamps, and the specific evidence-bearing state.
6. Keep originals immutable; create redacted derivatives separately and record their relationship.

Do not describe a screenshot, PDF, Playwright trace, or HAR as a WARC. Do not claim completeness when
service workers, streaming media, cross-origin resources, authentication, or client state were not captured.

## Protect people and sources

Minimize personal data, redact unnecessary identifiers from reports, and state retention and sharing
limits. Capturing public information does not erase privacy, copyright, contractual, or safety obligations.
Stop when another capture would be disproportionate to the stated purpose.

## Compose without overlap

- Let `conduct-open-source-investigation` own collection questions, entity resolution, corroboration, and
  reporting; use this skill only for evidence preservation.
- Use `test-browser-workflows` for application QA, visual regression, and traces.
- Use `data-storytelling` for a substantial evidence narrative.

Finish with the manifest, integrity results, replay status, gaps, and the exact evidence claim each artifact
can and cannot support.
