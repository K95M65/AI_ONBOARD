---
name: audit-accessibility
description: Audits and remediates accessibility barriers across web, desktop, and mobile products, including interaction, assistive technology, visual presentation, motion, cognitive load, content, localization, and platform conventions. Use when reviewing an experience for accessibility, investigating an access failure, preparing remediation, or verifying that accessibility defects were fixed.
---

# Audit accessibility

Assess whether people with different access needs can understand, operate, recover from, and complete real
tasks. Treat conformance as a floor and automated checks as evidence, not as proof of accessibility.

## Establish scope and authority

1. Read project instructions, supported platforms, target versions, user workflows, design-system guidance,
   known access needs, and prior findings.
2. Identify the applicable legal, contractual, policy, and platform requirements. Check current official
   sources when exact criteria or API behavior matters.
3. Define representative users, assistive technologies, input methods, languages, display settings,
   environments, and critical tasks.
4. Include success, loading, empty, validation, error, permission, destructive, offline, and recovery states.
5. Record what cannot be tested in the available environment.

Use [assets/accessibility-audit-template.md](assets/accessibility-audit-template.md) for a formal audit.

## Inspect the implementation and rendered behavior

Read [references/platform-checks.md](references/platform-checks.md), then load only the relevant platform
section.

Combine available evidence:

- structure, semantics, names, roles, values, states, and relationships;
- keyboard, pointer, touch, switch, voice, and automation behavior as applicable;
- screen-reader order, announcements, actions, focus, and rotor or navigation structures;
- color, contrast, text scaling, zoom, reflow, system appearance, and forced settings;
- animation, flashing, vestibular effects, reduced motion, and timing;
- plain language, error recovery, consistency, cognitive load, and interruption;
- long, translated, bidirectional, and user-generated content;
- platform accessibility APIs and native control behavior.

Run automated scanners when available, but reproduce and verify findings manually. Do not infer rendered
accessibility from source code alone.

## Exercise complete tasks

1. Start from the platform's expected entry point.
2. Complete representative tasks without relying on sight, pointer precision, color alone, audio alone, or
   memory of hidden state.
3. Trigger validation and failure conditions; confirm that focus and announcements lead to recovery.
4. Change text size, contrast, appearance, motion, orientation, window or viewport size, and input method
   where supported.
5. Confirm that authentication, consent, payments, uploads, and destructive actions remain understandable
   and operable.
6. Test realistic content extremes and localization rather than ideal placeholder text.

For participant-based accessibility research, compose with `conduct-user-research`; do not ask disabled
participants to substitute for basic conformance testing.

## Report reproducible findings

For every issue, capture:

- concise barrier and affected people;
- platform, version, environment, assistive technology, and settings;
- exact location and reproduction steps;
- expected and actual behavior;
- user impact and blocked or degraded task;
- evidence, applicable requirement, and confidence;
- suspected cause, remediation direction, and verification method.

Prioritize from task impact, reach, frequency, persistence, recoverability, safety, and availability of an
alternative—not cosmetic discomfort alone. Use:

- **Critical:** prevents a critical task or creates serious safety, privacy, or financial risk.
- **High:** blocks a common task or a substantial group with no reasonable workaround.
- **Medium:** materially degrades a task but recovery or an alternative exists.
- **Low:** limited friction, inconsistency, or robustness risk.

Do not downgrade an issue merely because the affected population is smaller.

## Remediate causes

1. Prefer correct native or semantic behavior before custom accessibility overrides.
2. Fix shared primitives when the defect is systemic, then assess every consumer.
3. Preserve useful information and interaction; do not “solve” access by removing required capability.
4. Use equivalent alternatives only when direct access is not technically possible.
5. Add regression coverage at the most reliable layer without replacing task-level verification.
6. Retest the exact scenario and adjacent workflows with the original settings and assistive technology.

Route design-system-wide defects to `evolve-design-system` and product language defects to
`design-product-content`.

## Finish with evidence

Report scope, standards and platforms considered, tasks and configurations exercised, findings by severity,
fixes made, retest evidence, untested areas, accepted risks, and owners for remaining work. Never claim that
an experience is “fully accessible.”
