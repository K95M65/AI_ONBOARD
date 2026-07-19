# Apple development workflow

AI_ONBOARD's `apple` profile is a routed workflow rather than a flat bundle of interchangeable prompts.
The `develop-apple-platform-app` skill owns project discovery, implementation, runtime verification, and
the distribution boundary. It loads only the specialist needed for the current risk.

## Route work through the profile

| Need | Skill |
|------|-------|
| End-to-end native app implementation or review | `develop-apple-platform-app` |
| State ownership, modules, dependencies, or navigation boundaries | `swift-architecture` |
| Tasks, actors, isolation, cancellation, or `Sendable` | `swift-concurrency` |
| SwiftUI state, navigation, scenes, components, settings, or commands | `swiftui-ui-patterns` |
| Public or reusable Swift API shape and naming | `swift-api-design-guidelines` |
| Unit, integration, UI, async, flaky, or performance tests | `swift-testing-expert` |
| SwiftData schemas, contexts, queries, migrations, or CloudKit | `swiftdata-expert` |
| Existing or deliberately selected Core Data stacks | `core-data-expert` |
| SwiftUI accessibility audit or remediation | `swiftui-accessibility-auditor` |
| AppKit accessibility audit or remediation | `appkit-accessibility-auditor` |
| Measured SwiftUI runtime performance work | `swiftui-performance-audit` |

Do not load every specialist for every Apple task. Start with the orchestrator, preserve the repository's
real Xcode or SwiftPM contract, and add a specialist only when the requested change crosses its boundary.

## Apple Development skill-set assessment

The separately maintained Apple Development folder contains the same eleven skill names as the canonical
AI_ONBOARD `apple` profile. The copies are concise and emphasize current Apple documentation, the closest
Apple-authored sample, and an explicit record of what was adapted. The canonical AI_ONBOARD skills retain
broader implementation playbooks, packaged references, licenses, and notices.

The integration policy is:

1. Keep `skills/` in AI_ONBOARD canonical; do not copy duplicate skill directories over it.
2. Preserve the canonical specialist playbooks and their existing reference routers.
3. Apply the Apple folder's source-selection discipline through
   `develop-apple-platform-app/references/apple-source-selection.md`.
4. Ship UI metadata for every Apple skill through `agents/openai.yaml`.
5. Review future Apple-folder changes as candidate improvements, then port the smallest useful delta into
   the canonical skill with its license and validation evidence.

This avoids two same-named global skills drifting apart while retaining the strongest material from both
sets.

## Verify an Apple change

Record the actual workspace or project, scheme, target, configuration, destination, Swift language mode,
deployment targets, entitlements, and distribution channel. Then report:

- the official symbol, framework page, or Apple sample that materially informed the change;
- the local technique adopted and any sample assumptions rejected;
- exact build and test commands;
- the runtime scenario exercised;
- accessibility, persistence, concurrency, or performance evidence relevant to the change; and
- signing, notarization, store, or production actions that remain outside current authorization.
