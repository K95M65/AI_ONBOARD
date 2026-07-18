# Apple project context

Discover the build and runtime contract before choosing APIs or patterns.

## Identify the project system

- Find `*.xcodeproj`, `*.xcworkspace`, `Package.swift`, `Project.swift`, `Workspace.swift`, `Tuist.swift`,
  `Package.resolved`, `.swift-version`, and formatter or linter configuration.
- Prefer a workspace over its contained project when both exist.
- Read `Package.swift`, project settings, configuration files, and repository instructions. Do not edit the
  generated Xcode project when a generator such as Tuist owns it.
- If Xcode is available, use `xcodebuild -list -json -workspace <name>.xcworkspace` or
  `xcodebuild -list -json -project <name>.xcodeproj` to enumerate schemes and targets. Do not guess a scheme.
- Use `swift --version`, `xcodebuild -version`, and resolved package state only as evidence about the current
  environment; repository CI may intentionally use another version.

## Record compatibility

Inspect rather than infer:

- `SWIFT_VERSION`, upcoming features, strict-concurrency level, and default actor isolation;
- platform deployment targets and supported device families;
- build configurations, conditional compilation, availability guards, and package platform clauses;
- application, framework, test, UI-test, extension, widget, service, and command-line targets;
- generated sources, macros, plugins, binary dependencies, and build phases.

An SDK being installed does not authorize raising a deployment target. An API compiling against the newest
SDK does not prove it is available on every supported OS.

## Trace architecture and data

Locate:

- app and scene entry points, delegates, documents, windows, commands, settings, and services;
- observable state ownership and dependency injection;
- actors, global actors, tasks, continuations, delegates, callbacks, and notification boundaries;
- SwiftData containers, Core Data models and stores, files, keychain items, network caches, migrations, and
  synchronization;
- unit, integration, UI, snapshot, accessibility, and performance tests.

Match the established architecture unless the user requested a change and migration evidence justifies it.

## Establish commands safely

Prefer exact commands in `AGENTS.md`, the README, CI, Makefile, scripts, or project automation. Otherwise:

- use `swift build` and `swift test` only for a compatible Swift package;
- use an existing shared scheme with `xcodebuild`, an explicit project or workspace, and an explicit
  destination;
- use the repository's formatter, linter, generator, and package-resolution workflow;
- avoid `clean`, deleting Derived Data, resetting packages, or changing signing as a first diagnostic step.

Record signing teams, profiles, keychains, credentials, and secret values only by approved references; never
copy them into instructions or output.
