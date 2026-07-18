---
name: evolve-design-system
description: Audits and evolves an existing design system through reusable foundations, component contracts, documentation, governance, adoption, versioning, and migration. Use when consolidating inconsistent UI patterns, introducing or changing tokens and components, planning cross-product adoption, deprecating patterns, or establishing a maintainable design-system operating model.
---

# Evolve a design system

Improve a shared system without treating a component library, design file, or token set as the whole system.
Preserve proven local patterns unless evidence supports changing them.

## Define system boundaries

1. Read project instructions and inspect design assets, code libraries, tokens, components, documentation,
   release processes, products, platforms, ownership, and adoption.
2. Identify consumers, supported platforms and frameworks, contribution paths, release channels, and
   compatibility commitments.
3. State the user and organizational outcomes the system should improve.
4. Distinguish:
   - foundations and semantic tokens;
   - interaction and content patterns;
   - components and composition;
   - platform-specific implementations;
   - documentation, governance, and delivery infrastructure.
5. Set non-goals. Let product-design skills own individual product workflows and visual direction.

Use [assets/system-audit-template.md](assets/system-audit-template.md) for a multi-product audit.

## Audit actual use

Inventory both official and local patterns. For each candidate, capture usage, variants, states, quality,
accessibility, ownership, duplication, platform fit, and migration cost. Inspect rendered behavior and real
content rather than relying only on component names.

Classify findings:

- **retain:** coherent, reusable, and meeting current needs;
- **repair:** valid concept with implementation, accessibility, or documentation defects;
- **consolidate:** equivalent patterns with unnecessary divergence;
- **promote:** useful local pattern ready for shared ownership;
- **specialize:** legitimate product or platform-specific exception;
- **deprecate:** harmful, obsolete, or superseded.

Do not force visually similar patterns into one component when their behavior, semantics, or ownership
differ.

## Define the target model

1. Establish principles tied to consumer needs and product outcomes.
2. Define semantic foundations before multiplying components: color roles, typography roles, spacing,
   shape, elevation, motion, iconography, density, and responsive or platform adaptations.
3. Specify component contracts: purpose, anatomy, slots, variants, states, content rules, behavior, input
   methods, accessibility semantics, constraints, and composition boundaries.
4. Separate shared concepts from platform implementations. Native conventions may require deliberate
   differences.
5. Define stable naming based on meaning rather than current appearance.
6. Require representative examples with realistic, long, localized, missing, and error content.

Use `audit-accessibility` for independent accessibility assessment and `design-product-content` for
cross-component terminology and content patterns.

## Plan change as a product

Read [references/governance-and-migration.md](references/governance-and-migration.md) when setting
contribution, release, deprecation, or migration policy.

Prioritize work by consumer value, risk, frequency, accessibility impact, maintenance cost, and dependency
order. Deliver a representative vertical slice before broad expansion:

1. one foundation change;
2. one complete component contract and implementation;
3. documentation and examples;
4. consumer migration;
5. feedback and measured adjustment.

Avoid a long rebuild that produces no adopted capability.

## Govern contributions and releases

Define:

- decision rights and maintainers;
- proposal and review criteria;
- evidence required to add a variant or component;
- accessibility, test, and documentation gates;
- versioning and compatibility policy;
- experimental, stable, deprecated, and removed states;
- support expectations and feedback channels.

Keep exceptions visible and time-bound. A product-specific need is not automatically system debt, and a
shared implementation is not automatically a design system.

## Migrate safely

1. Map old tokens, components, and behaviors to replacements.
2. Separate mechanical migrations from changes requiring product judgment.
3. Provide compatibility layers or staged releases when abrupt change would create excessive risk.
4. State visual, behavioral, accessibility, and API changes.
5. Migrate representative consumers first and use their findings to refine guidance.
6. Verify supported states, platforms, themes, input methods, and content extremes.
7. Define removal criteria and track remaining adoption.

## Measure system health

Use indicators such as adoption in eligible surfaces, task completion for consumers, defect and
accessibility trends, upgrade lag, support demand, contribution throughput, duplicate-pattern reduction,
and product quality. Do not optimize for component count or raw adoption without context.

## Finish with evidence

Report current-state findings, target model, retained exceptions, prioritized roadmap, ownership,
compatibility and migration plan, validation performed, adoption risks, and unresolved decisions.
