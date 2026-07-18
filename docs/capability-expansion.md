# Capability expansion decisions

This review adds original, portable workflows where AI_ONBOARD had a real job gap. It does not copy or
install Context7, Superpowers, Webrecorder, Playwright, or a frontend-design package.

## Decisions

| Capability | Decision | Why |
|------------|----------|-----|
| Browser and Playwright testing | Add `test-browser-workflows` | Website QA existed inside an orchestrator, but reusable web-app workflow testing did not |
| WARC, WACZ, and source snapshots | Add `preserve-web-evidence` | OSINT needed a separate preservation job with provenance, integrity, replay, and privacy boundaries |
| Current technical documentation | Add `retrieve-technical-docs` | Version-aware retrieval should work from local and official sources without requiring a hosted service |
| Obsidian integration | Extend `obsidian` | Direct Markdown is the free portable base; URI and existing local REST/MCP are optional enhancements |
| Code simplification | Add `simplify-code-safely` | The read-only reviewer may identify complexity, but implementation needs a behavior-preserving workflow |
| Systematic debugging | Add `debug-systematically` | Root-cause isolation and regression evidence were not a named reusable procedure |
| Test-first development | Add `develop-test-first` | Generic red-green-refactor guidance was missing outside platform-specific testing skills |
| Code review | Keep the existing `reviewer` agent | Independent review already exists and should remain isolated from the author |
| Frontend visual implementation | Keep the existing website/product orchestrators | The reviewed frontend-design guidance is a useful bounded visual lens, not a replacement for strategy, content, accessibility, or verification |

## Playwright and browser evidence

Playwright already supports full-page and element screenshots, traces with DOM snapshots, screenshot
comparisons, and ARIA snapshot assertions. The new browser-testing skill selects among interactive QA,
durable end-to-end tests, visual regression, and diagnostic traces instead of assuming every browser task
needs a new test suite. It does not install Playwright or duplicate the active browser harness.

Testing artifacts are not preservation archives. A screenshot records visible appearance in its captured
state; a trace or HAR helps diagnose execution; WARC/WACZ records network-delivered resources for later
replay. The preservation skill keeps those claims separate. References:
[Playwright screenshots](https://playwright.dev/docs/screenshots),
[tracing](https://playwright.dev/docs/trace-viewer),
[visual comparisons](https://playwright.dev/docs/test-snapshots), and
[ARIA snapshots](https://playwright.dev/docs/aria-snapshots).

## WARC and snapshot tooling

WARC is the standardized web-archive record format maintained through the IIPC/ISO ecosystem. For free,
high-fidelity local capture, [Browsertrix Crawler](https://github.com/webrecorder/browsertrix-crawler) can
run in a container and generate WACZ, while
[ArchiveWeb.page](https://github.com/webrecorder/archiveweb.page) supports interactive browser capture.
[ReplayWeb.page](https://github.com/webrecorder/replayweb.page) can verify replay. These are optional tools,
not bundle dependencies. See the [WARC 1.1 overview](https://iipc.github.io/warc-specifications/specifications/warc-format/warc-1.1/)
and [Browsertrix user guide](https://crawler.docs.browsertrix.com/user-guide/).

## Context7, free-first alternatives, and Obsidian

[Context7](https://github.com/upstash/context7) is useful for locating current library passages. Its MCP
and CLI client are MIT-licensed and it has a free hosted tier, but the indexing/crawling backend is not in
the public repository; self-hosted deployment is presented as an enterprise option. AI_ONBOARD therefore
treats Context7 as optional discovery, never as the only authority or a required install.

The free-first retrieval ladder is:

1. project lockfiles, installed types/source, tests, and vendored documentation;
2. versioned official documentation, tagged source, changelogs, and migration guides;
3. official [`llms.txt`](https://llmstxt.org/) indexes where published;
4. free/offline indexes such as [DevDocs](https://devdocs.io/about);
5. Context7 when already connected, followed by primary-source verification.

Durable findings can be written directly into an Obsidian vault as Markdown with version, source, retrieval
date, and invalidation condition. This needs no paid service. Official
[Obsidian URI](https://help.obsidian.md/Extending%2BObsidian/Obsidian%2BURI) actions can open or create notes;
an already-installed local REST/MCP community plugin may provide richer interaction. Obsidian Sync remains
optional and paid, not a dependency.

## Superpowers review

The [reviewed Superpowers skills](https://github.com/obra/superpowers/tree/d884ae04edebef577e82ff7c4e143debd0bbec99/skills) cover brainstorming,
plans, parallel agents, worktrees, test-driven development, systematic debugging, code-review handoffs,
verification, and branch completion. AI_ONBOARD keeps its own mechanism boundaries:

| Superpowers-style job | AI_ONBOARD route |
|-----------------------|------------------|
| Brainstorming and requirements | `grill-requirements`, `shape-product-opportunity`, or direct collaboration |
| Goal and plan state | `goal-contract` plus the harness's native plan/goal tools |
| Parallel or subagent execution | `docs/delegation.md` and bounded reference agents |
| Test-driven development | `develop-test-first` |
| Systematic debugging | `debug-systematically` |
| Requesting code review | independent `reviewer` agent |
| Receiving review feedback | harness/GitHub review workflows |
| Verification before completion | project contract plus independent `verifier` |
| Worktrees and branch completion | native git behavior plus `gh-pr`, `changelog`, and `gh-release` |

This avoids an always-on meta-skill and keeps each procedure discoverable by its own narrow trigger.

## Frontend-design review

The installed frontend-design guidance contributes one strong idea: commit to a specific visual concept and
execute it coherently instead of producing interchangeable UI. AI_ONBOARD already places that idea inside
`design-and-build-website` and `design-product-interface`, where strategy, structure, real content,
responsive states, accessibility, testing, and independent review remain first-class. No upstream
frontend-design files are copied into this repository.

The originality review was performed on 2026-07-18 against Superpowers commit
`d884ae04edebef577e82ff7c4e143debd0bbec99` and the installed frontend-design `SKILL.md` with SHA-256
`b81e2ff87ed8fa4d6c377ccb127a7254c9e6a77e3ae94f21e6b514f7bb2945a0`, so the comparison can be
reproduced even if either upstream source later changes.
