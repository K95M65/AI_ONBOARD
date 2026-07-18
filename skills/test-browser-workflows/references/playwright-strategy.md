# Playwright strategy

Use the lightest Playwright surface that matches the job.

| Need | Preferred surface | Durable repository change |
|------|-------------------|---------------------------|
| Inspect a local page once | Existing browser control or Playwright CLI | No |
| Reproduce a browser defect | CLI or a focused script with trace capture | Only when the repro should remain |
| Protect a user workflow in CI | Existing `@playwright/test` suite | Yes |
| Compare appearance | `toHaveScreenshot()` in a pinned environment | Yes |
| Compare accessible structure | ARIA snapshot assertions where stable and meaningful | Yes |

For CLI work, snapshot the page before using element references and refresh the snapshot after navigation or
large DOM changes. For repository tests, follow the existing config, fixtures, projects, reporters, and
artifact paths rather than creating a second Playwright setup.

Visual comparisons are sensitive to browser versions, operating systems, fonts, antialiasing, animation,
dynamic data, and viewport size. Stabilize those inputs and review baseline updates as product changes, not
as automatic test repairs.

Traces are diagnostic bundles, not archival records. They may contain page content, requests, and other
sensitive test data; retain and share them according to the project's data policy.
