---
name: design-and-build-website
description: Guides a strategy-to-launch workflow for conversion-oriented marketing websites. Use when creating or substantially redesigning a landing page, company website, portfolio, campaign site, or product-marketing experience and the task spans strategy, wireframes, conversion copy, visual direction, componentwise implementation, QA, review, and publishing.
---

# Design and build a website

Take one marketing website from an explicit business objective to a verified release. Keep implementation
with the current agent; use separate agents only for research isolation or independent review.

## Start with context

1. Follow mandatory lifecycle rules from any active project builder or hosting skill before starting this
   workflow, including required initialization or preview setup.
2. Read the repository instructions and inspect the existing stack, routes, components, tokens, content,
   assets, checks, and hosting configuration.
3. Determine whether the request is a new build, a redesign, or a focused page. Preserve useful existing
   patterns instead of replacing them reflexively.
4. Establish the working mode:
   - **Autonomous:** make reversible decisions from available context and state important assumptions.
   - **Collaborative:** pause at strategy, wireframe, and visual-direction gates for user input.
5. Ask only for missing facts that would materially change the result. Never invent customer quotes,
   performance claims, certifications, prices, or legal promises.
6. For an interaction-heavy product application rather than a marketing surface, use a product-design
   workflow instead of forcing this conversion-oriented process.

## Compose with specialists

Treat this skill as the process owner, not a replacement for narrower capabilities:

- Let an active website builder or hosting skill own setup, preview, build, and deployment mechanics. Its
  tool-specific constraints and sequencing take precedence.
- Use `conduct-user-research` when audience, job, objections, language, or usability claims require evidence.
- Use `define-brand-foundation` when positioning, voice, visual identity, or proof principles are missing.
- Use `evolve-design-system` when the work changes a shared system rather than merely consuming its tokens
  and components.
- Use `audit-accessibility` for a dedicated audit and remediation plan, and
  `measure-product-experiments` for analytics contracts, experiments, or post-launch learning.
- Use visual implementation, component scaffolding, image generation, and browser automation capabilities
  only for their bounded phases.
- Use review and verification agents as independent lenses; do not have the author impersonate them.
- Reuse their results in this workflow instead of repeating the same work.

## Run the workflow

Complete the phases in order. Reuse accepted artifacts instead of reopening settled decisions without new
evidence.

### 1. Define the role and strategy

Read [references/strategy.md](references/strategy.md). Produce a compact brief covering the audience, job,
site purpose, primary conversion, value proposition, proof, success measure, brand position, scope, and
constraints. Copy [assets/website-brief-template.md](assets/website-brief-template.md) when a durable brief
will help a multi-page or multi-turn project.

Do not proceed until every proposed page has a clear audience job and desired action.

### 2. Build the structure and wireframes

Read [references/structure-and-wireframes.md](references/structure-and-wireframes.md). Define the sitemap,
user journey, page hierarchy, section order, responsive text wireframes, component inventory, and required
states. Use [assets/page-spec-template.md](assets/page-spec-template.md) for each substantial page.

Validate the content hierarchy before applying visual polish.

### 3. Write conversion copy

Read [references/conversion-copy.md](references/conversion-copy.md). Write real section-level copy before
building decorative layouts. Connect the promise, evidence, objections, and calls to action in one message
hierarchy. Mark missing proof as a content requirement; never manufacture it.

### 4. Choose the visual direction and build component by component

Read [references/visual-direction.md](references/visual-direction.md), then
[references/componentwise-build.md](references/componentwise-build.md). Derive a visual system from the
brand and strategy, express it as reusable tokens, and implement in this order:

1. Page shell, layout, typography, tokens, and focus behavior.
2. Reusable primitives and navigation.
3. Content sections with final or clearly marked draft copy.
4. Complete pages and cross-page flows.
5. Loading, empty, error, success, long-content, and narrow-screen states where relevant.

When a hero, demo, screenshot, report, terminal, chart, or other visual represents the product, also read
[references/authentic-product-visuals.md](references/authentic-product-visuals.md). Base it on real product
behavior and truthful content rather than decorative marketing fiction.

Render and inspect each meaningful vertical slice. Use an installed component scaffolder, frontend-design
skill, image generator, or browser tool when available, but do not make the workflow depend on a particular
harness or framework.

### 5. Test and refine

Read [references/qa-and-publishing.md](references/qa-and-publishing.md). Run the project checks and inspect
the rendered site with supported preview or browser tooling at representative narrow, medium, and wide
viewports. Follow any active builder's browser restrictions. Exercise links, forms, keyboard navigation,
focus, reduced motion, overflow, and meaningful UI states. Use
[assets/qa-matrix-template.md](assets/qa-matrix-template.md) for larger projects.

Fix root causes, rerun the affected checks, and retain evidence such as command output and screenshots.

### 6. Review, export, and publish

Use an independent design-review agent after UI changes and a verifier agent for final acceptance when those
roles are available. Add security review for forms, authentication, payments, uploads, or other untrusted
input. Use an accessibility-review agent for material interaction or content changes and after accessibility
remediation. Resolve material findings before release.

Discover the repository's existing build and hosting path. Prefer an installed hosting/deployment skill when
one matches. Let that skill govern access-level approvals and deployment mechanics. Treat an explicit request
to publish or deploy as authorization for the named target; otherwise obtain authorization before creating
or changing a live deployment. After publishing, smoke-test the live URL and report the version, URL, checks,
known limitations, and rollback path.

## Apply quality rules

- Give each page one primary job and each section one reason to exist.
- Prefer a distinctive concept tied to the brand over generic gradients, interchangeable cards, and
  decoration without meaning.
- Use semantic HTML, accessible names, visible focus, sufficient contrast, resilient layout, and reduced
  motion from the start.
- Preserve framework, design-system, and repository conventions unless changing them is part of the task.
- Treat mobile as a content-priority test, not a shrunken desktop.
- Test rendered behavior as well as source code.
- Never claim completion from a successful build alone.

## Finish with evidence

Report the strategy followed, pages and components delivered, checks run and results, independent review
status, deployment state, and any remaining content or operational dependencies.
