---
name: develop-apple-platform-app
description: Implements and reviews Swift applications for Apple platforms, with special coverage for macOS, using the repository's real Xcode or SwiftPM configuration. Use when building, changing, debugging, testing, profiling, packaging, signing, or distributing a SwiftUI, AppKit, UIKit, mixed-framework, SwiftData, or Core Data application; do not use it for product-interface strategy alone.
---

# Develop an Apple platform app

Implement Apple-platform software from the project's actual targets and settings. Treat Swift language
mode, deployment targets, UI framework, persistence, entitlements, and distribution channel as discovered
constraints rather than universal defaults.

## Establish the project context

Read repository instructions, then inspect the project using
[references/project-context.md](references/project-context.md). Record:

- project system, schemes, targets, products, and build configurations;
- Swift language mode, strict-concurrency settings, and deployment targets;
- SwiftUI, AppKit, UIKit, extensions, and mixed-framework boundaries;
- state, persistence, networking, dependency, and architecture patterns already in use;
- entitlements, sandbox, signing, update, and distribution model;
- exact build, test, lint, formatting, and generation commands.

Do not upgrade targets, replace architecture, migrate persistence, add packages, or alter signing merely to
match a specialist skill's preferred stack.

## Separate product design from engineering

Use `design-product-interface` when the user work, information architecture, workflows, or visual behavior
still need to be designed. Use this skill to realize that product model in Swift and system APIs. Preserve
accepted platform and design decisions unless implementation evidence exposes a conflict.

For macOS lifecycle, window, document, command, settings, integration, and sandbox decisions, read
[references/macos-engineering.md](references/macos-engineering.md).

## Route bounded questions to specialists

Load only the specialists relevant to the detected project and task:

- `swift-api-design-guidelines` for public or reusable Swift APIs and naming;
- `swift-architecture` for a material architecture choice or refactor;
- `swift-concurrency` for isolation, sendability, cancellation, task structure, or async bridging;
- `swiftui-ui-patterns` for SwiftUI composition, state flow, navigation, windows, commands, or settings;
- `swift-testing-expert` for Swift Testing and XCTest selection or implementation;
- `swiftdata-expert` only when SwiftData is present or deliberately selected;
- `core-data-expert` when Core Data is present or compatibility requires it;
- `swiftui-accessibility-auditor` or `appkit-accessibility-auditor` for the implemented UI framework;
- `swiftui-performance-audit` when SwiftUI runtime behavior, rendering, or update cost is in question.

Treat specialist guidance as scoped expertise. Resolve conflicts in favor of repository instructions,
supported targets, official SDK behavior, and evidence from the build or runtime.

## Implement a coherent vertical slice

1. Trace the requested behavior through model, state ownership, UI, platform integration, persistence, and
   tests before editing.
2. Preserve existing dependency direction and framework boundaries unless the task explicitly changes them.
3. Implement one representative path end to end, including error, cancellation, empty, permission, and
   recovery behavior where applicable.
4. Keep UI state derived from authoritative model state. Make actor and thread assumptions explicit at
   boundaries; do not silence concurrency diagnostics with blanket isolation.
5. Prefer Apple framework capabilities already compatible with the deployment target. Add availability
   checks and fallbacks when support spans API generations.
6. Exercise the slice in the real app or preview before repeating its pattern.

## Verify and prepare distribution

Read [references/verification-and-distribution.md](references/verification-and-distribution.md). Run the
narrowest relevant checks while iterating, then the repository's required suite. Verify runtime behavior on
representative supported destinations, not only compilation.

Use an independent design review after UI changes, the relevant implementation-level accessibility auditor,
an accessibility-review agent when an independent lens is warranted, a verifier for final acceptance, and
security review for identity, sensitive data, files, network trust, privileged operations, entitlements, or
release credentials.

Packaging, signing, notarization, TestFlight, App Store submission, update publication, and credential use
change external state. Follow the established release path and obtain any authority not already granted by
the request.

## Finish with evidence

Report the targets and versions preserved, specialists used, behavior implemented, build and test commands,
runtime and accessibility evidence, signing or distribution state, and any target-specific limitations.
