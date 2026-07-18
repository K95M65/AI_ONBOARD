---
name: test-browser-workflows
description: Designs and runs browser-based validation for websites and web applications, including critical user flows, responsive behavior, keyboard interaction, accessibility structure, visual regression, screenshots, and traces. Use when testing rendered browser behavior, adding or improving Playwright end-to-end tests, reproducing a UI failure, or collecting browser QA evidence; do not use for unit tests alone or for archival capture of public sources.
---

# Test browser workflows

Prove rendered behavior in a real browser. Use the repository's existing test stack when one exists and
keep one-off exploration distinct from durable regression coverage.

## Choose the testing mode

1. **Exploratory QA** — exercise a changed surface interactively and retain concise evidence.
2. **Repeatable workflow test** — add a repository-owned test for behavior that must remain stable.
3. **Visual regression** — compare controlled screenshots when appearance itself is the contract.
4. **Failure diagnosis** — capture a trace, screenshot, console output, and failing request around a
   reproducible browser defect.

Read [references/playwright-strategy.md](references/playwright-strategy.md) when Playwright is available or
being considered.

## Inspect before testing

- Read project instructions, preview commands, existing browser tests, fixtures, selectors, and CI setup.
- Identify the supported browsers, viewport contract, test data, authentication path, and external-service
  boundaries.
- Use an already-available browser capability or test runner. Do not install Playwright, browsers, or other
  tooling unless the user requests setup or the repository already declares that dependency.
- Prefer the active harness's browser-control rules for interactive inspection.

## Define a risk-led matrix

Cover the smallest matrix that proves the requested outcome:

- primary task and highest-cost failure path;
- loading, empty, error, disabled, success, and recovery states that can occur;
- narrow, medium, and wide layouts where responsive behavior changes;
- keyboard order, visible focus, accessible names, landmarks, headings, and status announcements;
- navigation, history, deep links, forms, validation, downloads, and external links;
- console errors, failed requests, redirects, and persistence boundaries;
- long content, zoom, reduced motion, and touch targets when relevant.

Do not multiply browsers, devices, and states without a risk reason.

## Automate durable behavior

- Use resilient role, label, text, or test-id locators; do not couple tests to decorative DOM structure.
- Assert user-visible outcomes and meaningful state, not implementation details.
- Control test data, time, randomness, animation, and network dependencies where deterministic comparison
  requires it.
- Wait for observable conditions rather than sleeping for arbitrary durations.
- Keep each test independent and make setup failures distinguishable from product failures.
- Capture traces, screenshots, video, or network evidence on failure when the repository supports it.
- For visual baselines, pin the browser, operating system, fonts, viewport, data, and volatile regions.

## Verify and report

Run the narrow test first, then the relevant broader suite. For each scenario, record the expected result,
observed result, environment, and artifact path. Report flaky or untested surfaces explicitly.

A browser screenshot or Playwright trace is testing evidence, not a preservation-grade web archive. Use
`preserve-web-evidence` when a public source must be captured with provenance and replay fidelity.

## Compose without overlap

- Let `design-and-build-website` own an end-to-end marketing-site build.
- Use `audit-accessibility` for a dedicated accessibility audit and remediation workflow.
- Use `debug-systematically` when the browser failure needs root-cause isolation.
- Use a verifier agent for independent acceptance after the author fixes the implementation.

Finish when the critical behavior is exercised, failures are reproducible, durable tests match repository
conventions, and the evidence distinguishes what passed from what remains untested.
