# QA and publishing

Verify the implemented experience, obtain independent review, and release through the repository's
established path.

## Run project checks

Run the relevant install, typecheck, build, lint, unit, integration, and end-to-end commands from the
repository instructions. Fix causes and rerun affected checks. Do not treat unrelated pre-existing failures
as passing; report them with evidence.

## Inspect rendered behavior

Use supported preview or browser tooling at representative narrow, medium, and wide viewports. Follow any
active builder's browser restrictions and state when rendered inspection is unavailable. Check:

- navigation, links, buttons, forms, validation, success, and failure paths;
- keyboard order, visible focus, skip behavior, accessible names, headings, landmarks, and contrast;
- zoom, reduced motion, long content, missing optional content, overflow, and touch targets;
- loading, empty, error, disabled, and completion states that can occur;
- images, aspect ratios, responsive media, icons, and alternative text;
- metadata, page titles, descriptions, canonical URLs, social previews, robots, sitemap, and structured data
  when relevant;
- console errors, failed requests, broken routes, and obvious performance regressions.

Capture screenshots or other rendered evidence for important pages and states.

## Review independently

Use a separate design-review agent when available. Require findings across tokens, consistency,
accessibility, responsiveness, and state coverage. Use a verifier agent to check acceptance criteria and
commands independently. Add a security review when the site handles untrusted input, authentication,
payments, uploads, or sensitive data.

Resolve material findings and repeat the relevant verification.

## Prepare release

1. Identify the existing hosting configuration, environment requirements, build output, and rollback path.
2. Verify that secrets are injected through the approved environment and never committed.
3. Produce a clean production build or export.
4. Summarize the exact target, expected external changes, and known limitations.
5. Treat an explicit request to publish or deploy as authorization for the named target. Otherwise obtain
   authorization before creating or changing a live deployment; follow the active hosting skill's
   access-level approval rules.
6. Deploy only through the repository's established workflow or an appropriate installed deployment skill.
7. Smoke-test the live URL, including its primary conversion path.

Report the deployed version and URL, verification evidence, operational dependencies, and rollback method.
