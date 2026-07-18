---
name: design-product-interface
description: Guides a research-to-release workflow for interactive product interfaces across web applications, macOS, Windows and Linux desktop, iOS and Android, and cross-platform apps. Use when creating or substantially redesigning an application, dashboard, admin or operational tool, settings surface, or multi-step product workflow; use design-and-build-website instead for conversion-oriented marketing websites.
---

# Design a product interface

Take an interactive product from explicit user work to a platform-appropriate, verified release. Treat the
target platform as part of the product definition, not as a skin applied after designing a generic interface.

## Establish the operating context

1. Read repository instructions and inspect the product, current workflows, data model, UI architecture,
   design system, platform APIs, tests, analytics, support material, and release path.
2. Confirm that the task is an interactive product. For a marketing website whose main job is persuasion
   and conversion, use `design-and-build-website`.
3. Identify every supported platform, form factor, input method, window model, offline requirement,
   accessibility target, and distribution channel.
4. Decide whether the work is:
   - **native-first:** optimize for one operating system and its conventions;
   - **shared product, adapted surfaces:** preserve concepts and workflows while intentionally varying
     navigation, commands, layout, and controls by platform;
   - **cross-platform shell:** share implementation without pretending the platforms are identical.
5. Ask only for missing facts that would materially change the product model. State reversible assumptions
   when autonomous progress is authorized.

Use `conduct-user-research` when important user, environment, workflow, or usability claims need evidence.
Use `shape-product-opportunity` when the desired outcome, opportunity, assumptions, or experiment boundary
is still unclear.

## Load only the relevant platform guidance

- For browser-delivered products, read [references/platform-web-app.md](references/platform-web-app.md).
- For macOS products, read [references/platform-macos.md](references/platform-macos.md).
- For iOS or Android products, read [references/platform-mobile.md](references/platform-mobile.md).
- For Windows, Linux, Electron, Tauri, Qt, or other desktop products, read
  [references/platform-desktop.md](references/platform-desktop.md).
- For a multi-platform product, read every applicable platform reference. Define one shared product model,
  then record deliberate platform deltas. Do not settle for a lowest-common-denominator interface.

Treat these references as durable heuristics. When exact platform behavior, APIs, store requirements, or
accessibility rules matter, check the current official platform guidance.

## Run the workflow

### 1. Define the product role and strategy

Read [references/strategy-and-workflows.md](references/strategy-and-workflows.md). Produce a compact brief
covering users, jobs, environment, task frequency, stakes, domain language, objects, permissions, success
measures, platforms, constraints, and non-goals. Use
[assets/product-interface-brief-template.md](assets/product-interface-brief-template.md) when a durable
artifact will help.

Do not design screens until the primary users, work, and consequences of error are explicit.

For a first-run, adoption, or stalled-user problem, read
[references/activation-and-onboarding.md](references/activation-and-onboarding.md). For a product whose
core behavior uses generative or agentic AI, read
[references/ai-powered-experiences.md](references/ai-powered-experiences.md).

### 2. Model workflows, structure, context, and density

Read [references/layout-context-and-density.md](references/layout-context-and-density.md). Define the
conceptual model, information architecture, task flows, navigation, layout paradigm, command model, content
hierarchy, scope cues, and density. Start with the hardest representative workflow, not a decorative home
screen.

For a table paired with a chart, map, diagram, timeline, canvas, or another representation of the same data,
use `coordinate-data-views`.

### 3. Specify components, content, and states

Read [references/components-and-states.md](references/components-and-states.md). Define component contracts,
domain-language labels, complete interaction states, validation, recovery, permissions, loading, empty
content, long content, and destructive-action behavior. Use realistic data shaped by the real schema.

Use `design-product-content` for a substantial terminology, onboarding, error, help, or localization
problem. Use `evolve-design-system` when the task changes shared tokens, component contracts, governance,
versioning, or migration rather than merely consuming the existing system.

### 4. Establish the visual system and build vertical slices

Derive tokens and visual language from the product role, platform conventions, brand, content density, and
use environment. Preserve sound existing patterns. Use native controls and system behaviors when they
improve familiarity, accessibility, or integration; customize deliberately when product identity or task
performance justifies it.

Use `define-brand-foundation` when brand strategy or voice is missing. For native products, read
[references/native-visual-and-motion.md](references/native-visual-and-motion.md) before establishing visual
direction.

Implement in this order:

1. Data and state model for the chosen workflow.
2. Application shell, navigation, commands, focus, and platform integration.
3. Reusable primitives and one complete representative vertical slice.
4. Remaining workflows and secondary surfaces.
5. Loading, empty, error, partial, success, offline, permission, and recovery states.

Render or run each meaningful slice before multiplying the pattern.

### 5. Test and refine on the target platforms

Read [references/validation-and-release.md](references/validation-and-release.md). Run repository checks and
exercise the actual application with representative data, input methods, window or viewport sizes, system
settings, permissions, and failure conditions. Validate task completion and recovery, not merely visual
similarity.

Use `audit-accessibility` for a dedicated cross-platform audit and remediation plan. Use
`measure-product-experiments` when success requires an event contract, baseline, experiment, or post-release
learning loop.

### 6. Review, export, and release

Use an independent design-review agent after UI changes and a verifier agent for final acceptance when those
roles are available. Add security review for authentication, authorization, sensitive data, payments,
uploads, external input, privileged operations, or cross-account administration.
Use an accessibility-review agent when accessibility behavior is material, after remediation, or before a
high-impact release.

Follow the repository's established packaging, signing, notarization, store, deployment, or distribution
path. Obtain authorization before a live release unless the user explicitly requested it. Smoke-test the
released artifact or environment and report the version, target, evidence, limitations, and rollback path.

## Compose with specialists

- Let native UI, frontend implementation, component scaffolding, data visualization, browser automation,
  security, and deployment skills own their bounded mechanics.
- Use `develop-apple-platform-app` for Swift, SwiftUI, AppKit, Apple persistence, testing, profiling,
  packaging, signing, or distribution work.
- Use platform SDK guidance that matches the repository rather than adding a framework merely because it is
  familiar.
- Preserve accepted artifacts and decisions across phases. Reopen them only when implementation or testing
  provides new evidence.

## Apply quality rules

- Optimize for the user's work, not the number of visible features.
- Use the user's domain vocabulary and make action scope unmistakable.
- Match information density to expertise, frequency, screen size, and consequence of error.
- Make keyboard, pointer, touch, assistive technology, and automation behavior appropriate to the target.
- Keep repeated components aligned through stable slots and shared tokens.
- Expose commands through the platform's expected discovery paths.
- Design recovery alongside success.
- Never claim completion from a successful compile or attractive static screen alone.

## Finish with evidence

Report the product model, platform decisions, workflows and components delivered, checks and task scenarios
run, accessibility and independent-review status, release state, and remaining product or operational
dependencies.
