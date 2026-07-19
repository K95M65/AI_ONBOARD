# Skills library

Portable, reusable [Agent Skills](../docs/skills.md) — an open standard, so each folder works **as-is in
Claude Code, Codex, and opencode** (and 30+ other tools). Copy or symlink a folder into a harness's skills
directory (opencode also reads the `.claude/skills` and `.agents/skills` trees, so it needs no separate copy):

[Explore and filter the live skills map](https://k95m65.github.io/AI_ONBOARD/#catalog).

<!-- generated:skills-inventory:start -->
**68 portable skills · 7 capability groups · one shared format.**
<!-- generated:skills-inventory:end -->

| Harness | Personal | Project (team-shared) |
|---------|----------|-----------------------|
| Claude Code | `~/.claude/skills/<name>/` | `.claude/skills/<name>/` |
| Codex | `~/.agents/skills/<name>/` | `.agents/skills/<name>/` (vendor-neutral — **not** `.codex/skills`) |

## Installing skills

For a maintained project install, select the smallest useful
[capability profiles](../docs/install-management.md#capability-profiles):

```bash
python3 /path/to/AI_ONBOARD/scripts/ai_onboard.py \
  --target /path/to/project \
  install \
  --harness claude,codex,opencode \
  --profile core \
  --profile product
```

The manager records ownership and checksums, supports upgrades, and never replaces a target `AGENTS.md`.
For one-off use, individual skills remain ordinary portable folders:

```bash
# Claude Code (project, team-shared)
mkdir -p .claude/skills && cp -R skills/dataviz .claude/skills/

# Codex (project) — same folder, different directory
mkdir -p .agents/skills && cp -R skills/dataviz .agents/skills/

# Use it in both without duplicating: one canonical copy, symlinked into each tree
ln -s "$PWD/skills/dataviz" .claude/skills/dataviz
ln -s "$PWD/skills/dataviz" .agents/skills/dataviz
```

## Skills in this library

### Manual workflow foundations

These two original AI_ONBOARD skills are manually invoked through explicit user intent. They normalize
workflows that some harnesses already provide natively, remain visible in the catalog, and are excluded
from all capability profiles:

| Skill | What it does |
|-------|--------------|
| [`goal-contract`](workflow-foundations/goal-contract/) | Define a measurable execution contract, prefer native goal state, and use an honest conversation fallback when no native capability exists |
| [`grill-requirements`](workflow-foundations/grill-requirements/) | Pressure-test a request one consequential decision at a time and return a decision brief before planning or implementation |

```bash
python3 /path/to/AI_ONBOARD/scripts/ai_onboard.py \
  --target /path/to/project \
  install \
  --profile core \
  --workflow-foundations
```

Both skills may match explicit natural-language intent or a direct skill invocation; neither may be inferred
from an ordinary task. `goal-contract` does not create a parallel ledger when native goal state exists;
`grill-requirements` runs only when the user explicitly asks to be grilled or interviewed. See
[`../docs/workflow-foundations.md`](../docs/workflow-foundations.md).

### Web design

| Skill | What it does |
|-------|--------------|
| [`design-and-build-website`](design-and-build-website/) | Strategy-to-launch workflow for conversion-oriented websites — brief, wireframes, copy, visual system, componentwise build, browser QA, independent review, and publishing |

### Product and app design

| Skill | What it does |
|-------|--------------|
| [`design-product-interface`](design-product-interface/) | Research-to-release workflow for interactive products across web apps, macOS, mobile, Windows/Linux desktop, and cross-platform shells |
| [`coordinate-data-views`](coordinate-data-views/) | Synchronize complementary table, list, chart, map, diagram, timeline, or canvas views around one shared interaction model |
| [`conduct-user-research`](conduct-user-research/) | Plan, conduct, and synthesize ethical product research and usability studies |
| [`shape-product-opportunity`](shape-product-opportunity/) | Turn an outcome into evidence-backed opportunities, assumptions, solution options, and experiments |
| [`design-product-content`](design-product-content/) | Design product terminology, interface copy, onboarding, help, recovery content, and localization behavior |
| [`audit-accessibility`](audit-accessibility/) | Audit and plan remediation across web, native, content, cognitive, and localization concerns |
| [`evolve-design-system`](evolve-design-system/) | Audit and evolve a design system through governance, contribution, migration, versioning, and adoption |
| [`define-brand-foundation`](define-brand-foundation/) | Establish durable positioning, voice, visual principles, evidence, and brand governance |
| [`measure-product-experiments`](measure-product-experiments/) | Define decision-driven metrics, event contracts, experiments, guardrails, and learning loops |

These additions selectively synthesize tool-free design patterns reviewed in the MIT-licensed
[`dembrandt-skills`](https://github.com/dembrandt/dembrandt-skills) project. They are original portable
instructions and do not install or require the Dembrandt package.

The research, product, content, brand, accessibility, design-system, and measurement skills are original
portable workflows informed by a review of the [AI UX Playground skills catalog](https://aiuxplayground.com/skills/)
and its canonical upstream sources. They require no design application, analytics SDK, or external service;
tool-specific work composes only when the project already uses it.

### Apple platform engineering

| Skill | What it does |
|-------|--------------|
| [`develop-apple-platform-app`](develop-apple-platform-app/) | Target-aware Swift and macOS engineering orchestrator from project inspection through verification and distribution |
| [`swift-concurrency`](swift-concurrency/) | Diagnose and implement Swift concurrency with project-aware isolation and language settings |
| [`swift-testing-expert`](swift-testing-expert/) | Write and migrate Swift Testing suites while preserving valid XCTest use |
| [`swiftui-ui-patterns`](swiftui-ui-patterns/) | Apply focused SwiftUI composition, state, navigation, settings, and menu-bar patterns |
| [`swift-api-design-guidelines`](swift-api-design-guidelines/) | Design clear Swift APIs from declarations and call sites |
| [`swift-architecture`](swift-architecture/) | Evaluate architecture patterns against the actual scope, team, dependencies, and targets |
| [`swiftui-accessibility-auditor`](swiftui-accessibility-auditor/) | Audit SwiftUI semantics, VoiceOver, Dynamic Type, focus, and keyboard behavior |
| [`appkit-accessibility-auditor`](appkit-accessibility-auditor/) | Audit AppKit semantics, VoiceOver, key-view order, tables, outlines, and keyboard behavior |
| [`swiftui-performance-audit`](swiftui-performance-audit/) | Diagnose SwiftUI rendering and update costs, escalating to profiling evidence when needed |
| [`swiftdata-expert`](swiftdata-expert/) | Implement or debug SwiftData when the project's targets and persistence architecture support it |
| [`core-data-expert`](core-data-expert/) | Maintain Core Data stacks, migrations, concurrency, history, performance, and CloudKit integration |

The Apple specialists are adapted from independently MIT-licensed repositories surfaced through
[`twostraws/Swift-Agent-Skills`](https://github.com/twostraws/Swift-Agent-Skills). Every vendored folder
contains its exact upstream license and a notice pinned to the reviewed commit. The Twostraws “Pro” skills
are not installed; `develop-apple-platform-app` routes to the more target-aware specialists above.

### Security & audit

| Skill | What it does |
|-------|--------------|
| [`map-attack-surface`](map-attack-surface/) | Map internal and external assets, ownership, reachability, privilege boundaries, attack paths, coverage gaps, and monitoring — passive-first with explicit authorization gates |
| [`threat-model`](threat-model/) | STRIDE + data-flow threat model — design-time framing |
| [`secure-coding`](secure-coding/) | Write-time defensive practices, per category |
| [`input-sanitization`](input-sanitization/) | Validate-in / encode-out per sink (SQLi, XSS, command, path, SSRF) |
| [`identity-management`](identity-management/) | Authn/authz patterns — sessions, JWT/OAuth, RBAC, MFA, IDOR |
| [`secret-management`](secret-management/) | Store/inject/scope/rotate secrets safely |
| [`vulnerability-hardening`](vulnerability-hardening/) | Config/deploy hardening — headers, TLS, least privilege |
| [`security-audit`](security-audit/) | Systematic whole-codebase audit — threat model, checklist, surface-scan |
| [`manage-vulnerability-risk`](manage-vulnerability-risk/) | Normalize and validate findings, prioritize using threat and business context, assign treatment, govern exceptions, retest, and report coverage |
| [`assess-security-controls`](assess-security-controls/) | Evaluate selected current framework requirements using traceable evidence, design and operating tests, consistent judgments, and an improvement plan |
| [`dependency-vuln-scan`](dependency-vuln-scan/) | Scan dependencies for known CVEs (npm/Go/osv-scanner) |
| [`secret-scan`](secret-scan/) | Scan for committed secrets incl. git history |
| [`automated-security-review`](automated-security-review/) | Wire the scanners into CI as a PR gate (GitHub Actions) |

These consulting workflows are tool-free and scanner-agnostic. They keep asset discovery, vulnerability
enumeration, risk treatment, and control assurance separate; active external validation requires explicit
targets and rules of engagement. See [`docs/security-consulting.md`](../docs/security-consulting.md) for the
composition and authorization model.

### Code scaffolding

| Skill | What it does |
|-------|--------------|
| [`component-scaffold`](component-scaffold/) | Scaffold a React/TS component (component + test + index) |
| [`cobra-command`](cobra-command/) | Scaffold a Go Cobra subcommand + table-driven test |
| [`prisma-migrate`](prisma-migrate/) | Safely create + apply a Prisma migration; guards non-local DBs |

### Engineering quality

| Skill | What it does |
|-------|--------------|
| [`develop-test-first`](develop-test-first/) | Drive one behavior from a focused failing test through the smallest passing change and verified refactor |
| [`debug-systematically`](debug-systematically/) | Reproduce a failure, test causal hypotheses, fix the root cause when authorized, and retain regression evidence |
| [`simplify-code-safely`](simplify-code-safely/) | Remove accidental complexity while preserving observable behavior and public contracts |
| [`test-browser-workflows`](test-browser-workflows/) | Exercise rendered browser behavior, Playwright workflows, responsive states, accessibility structure, visual baselines, and traces |

Independent review remains with the read-only `reviewer` subagent; these skills guide implementation and
testing in the main working context. They are original workflows that cover gaps identified while reviewing
the MIT-licensed [Superpowers](https://github.com/obra/superpowers) methodology and the installed
Playwright guidance without copying either package.

### Dev workflow

| Skill | What it does |
|-------|--------------|
| [`conventional-commit`](conventional-commit/) | Write a Conventional Commits message from staged changes |
| [`pr-description`](pr-description/) | Write a PR description from the branch's commits + diff |
| [`changelog`](changelog/) | Roll Conventional Commits since the last tag into release notes |

### GitHub (`gh` CLI)

| Skill | What it does |
|-------|--------------|
| [`gh-pr`](gh-pr/) | Create/update a pull request (pairs with `pr-description`) |
| [`gh-issue`](gh-issue/) | Create, triage, and link issues |
| [`gh-release`](gh-release/) | Cut a GitHub release with changelog/auto notes (pairs with `changelog`) |

### Competitive intelligence & communication

| Skill | What it does |
|-------|--------------|
| [`conduct-open-source-investigation`](conduct-open-source-investigation/) | Conduct lawful, evidence-led OSINT with public sources and free or local tools only — scope, collection, entity resolution, verification, contradiction and gap analysis, and reporting |
| [`competitive-intel`](competitive-intel/) | Ethical CI cycle — scope → gather → analyze → communicate |
| [`market-research`](market-research/) | Market sizing (TAM/SAM/SOM), sources, source credibility |
| [`analytical-frameworks`](analytical-frameworks/) | SWOT, Porter, value chain, BCG, JTBD, PESTEL — data → insight |
| [`data-storytelling`](data-storytelling/) | Turn analysis into an executive narrative (pairs with `dataviz`) |
| [`preserve-web-evidence`](preserve-web-evidence/) | Preserve public sources as screenshots, PDFs, responses, WARC, or WACZ with provenance, integrity, and replay checks |
| [`retrieve-technical-docs`](retrieve-technical-docs/) | Retrieve version-matched official technical documentation using local and free-first sources, with optional Obsidian persistence |

The OSINT orchestrator is an original, tool-free workflow informed by a review of the MIT-licensed
[`smixs/osint-skill`](https://github.com/smixs/osint-skill) and
[`dkyazzentwatwa/osint-ai`](https://github.com/dkyazzentwatwa/osint-ai) projects. It vendors no upstream
code, requires no API keys or paid services, and explicitly excludes data brokers, access bypass, deceptive
interaction, invasive personal profiling, and regulated decisions about a person.

### Data, notes & onboarding

| Skill | What it does |
|-------|--------------|
| [`dataviz`](dataviz/) | Correct, readable, accessible charts — choice, color, a11y. *(Claude Code has a richer built-in `dataviz`; prefer that there — [see note](dataviz/SKILL.md#note--name-collision-on-claude-code).)* |
| [`obsidian`](obsidian/) | Read/write an Obsidian vault through local Markdown by default, with optional URI or existing local REST/MCP integration |
| [`agents-md-init`](agents-md-init/) | Bootstrap an `AGENTS.md` by detecting the stack + commands |

### Cloudflare (vendored — [`cloudflare/`](cloudflare/))

A curated set of Cloudflare's own Agent Skills (Apache-2.0), for teams on the Cloudflare Developer Platform:
`wrangler`, `workers-best-practices`, `durable-objects`, `cloudflare-one`, `turnstile-spin`, `agents-sdk`,
`cloudflare-email-service`, `sandbox-sdk`. See [`cloudflare/README.md`](cloudflare/README.md) and
[`cloudflare/NOTICE.md`](cloudflare/NOTICE.md) for provenance. `link.sh --skills` installs these too.
The managed installer selects them with `--profile cloudflare`; the legacy full-copy path also includes
them with `link.sh --skills`.

## Authoring a new skill

Follow [docs/skills.md](../docs/skills.md). The short version:

1. `mkdir skills/<name>` with a `SKILL.md`.
2. Frontmatter needs `name` and a trigger-rich `description` (what it does + when to use it).
3. Put deterministic work in `scripts/`; keep `SKILL.md` lean and push depth into referenced files.
4. Make it self-contained so it runs when dropped into any repo.

After adding or changing canonical skill metadata, run `python3 scripts/sync_project_docs.py` from the
repository root. This regenerates the website catalog and synchronized inventory blocks; CI verifies that
the generated files are current. Run `python3 scripts/check_skills.py` to validate skill names,
descriptions, local references, Codex UI prompts, and high lexical trigger overlap. Semantic job boundaries
still require review.
