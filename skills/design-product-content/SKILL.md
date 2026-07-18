---
name: design-product-content
description: Designs clear, consistent, accessible in-product language and content systems for navigation, actions, onboarding, instructions, forms, validation, errors, empty states, notifications, help, and localization. Use when creating or revising interface copy, terminology, voice and tone in a product workflow, or content patterns across a product or design system.
---

# Design product content

Help people understand their situation, make a decision, complete an action, and recover. Treat interface
content as part of the interaction model, not decoration added after layout.

## Establish context

1. Read project instructions, product and brand foundations, research, domain vocabulary, existing
   interface, support evidence, legal constraints, localization needs, and design-system patterns.
2. Identify the user's goal, knowledge, emotional state, risk, and next decision at each moment.
3. Distinguish in-product content from acquisition and conversion copy. Let `design-and-build-website` own
   marketing-site persuasion.
4. Inventory inconsistent terms, unclear ownership or scope, missing states, support-heavy moments, and
   content embedded in code or images.
5. Mark regulated or legally controlled language; do not silently rewrite it.

Use [assets/content-matrix-template.md](assets/content-matrix-template.md) for multi-state or cross-product
work.

## Define the content model

1. Name domain objects consistently and distinguish easily confused concepts.
2. Define preferred terms, forbidden or deprecated synonyms, grammatical form, and examples.
3. Assign each surface one communication job and a clear hierarchy.
4. Define voice as stable principles and tone as a contextual adjustment.
5. Establish rules for capitalization, punctuation, dates, numbers, units, pronouns, and abbreviations that
   match product and locale conventions.
6. Record content ownership, source of truth, review needs, and update triggers.

Use `define-brand-foundation` when voice, audience, positioning, or product-level identity is unresolved.

## Write for action and state

Read [references/content-patterns.md](references/content-patterns.md) when drafting common interface
patterns.

For each piece of content:

- state what happened or what the user can do;
- use the user's domain vocabulary;
- make action, object, and scope explicit;
- place instructions near the decision or field they support;
- explain consequences before irreversible actions;
- state how to recover from errors;
- disclose limitations, permissions, delays, and costs before commitment;
- preserve necessary nuance while removing internal jargon and filler.

Write the complete state set: default, first use, loading, empty, partial, validation, error, permission,
offline, success, interruption, destructive, and recovery states where applicable.

Do not use blame, false urgency, shame, confirmshaming, hidden consent, or celebratory language for
sensitive outcomes.

## Design for accessibility and localization

- Make link and control labels understandable out of context.
- Do not encode essential meaning in color, icon, position, sound, or illustration alone.
- Prefer short sentences and concrete verbs without oversimplifying expert terminology users need.
- Avoid directional instructions that fail after reflow or bidirectional localization.
- Allow strings to expand; do not solve overflow by writing unnaturally terse English.
- Keep variables, pluralization, grammar, and sentence boundaries safe for translation.
- Avoid idioms, wordplay, and cultural references unless brand value outweighs localization cost.
- Write useful accessible labels and descriptions for meaningful non-text content.

Use `audit-accessibility` for an independent task-level accessibility assessment.

## Validate in the interface

1. Place content in the actual layout with realistic data, long names, zero values, unknown values, and
   translated or expanded strings.
2. Check hierarchy, truncation, repetition, timing, announcements, and behavior across states.
3. Test comprehension and task completion with representative users when stakes or uncertainty justify it.
4. Review support logs, search queries, abandonment, correction, and error patterns after release.
5. Distinguish content problems from workflow, policy, or system problems; do not paper over a broken model
   with clearer sentences.

## Deliver a maintainable result

Report:

- terminology and voice decisions;
- final content by component and state;
- rationale for high-risk or constrained language;
- accessibility and localization considerations;
- unresolved legal, policy, product, or evidence dependencies;
- validation performed and measures to monitor.

Preserve content in the repository's established resource or localization system. Do not introduce a new
content platform merely to complete the writing task.
