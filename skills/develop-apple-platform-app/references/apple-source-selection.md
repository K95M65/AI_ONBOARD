# Apple source selection

Use live primary sources because Xcode, Swift, and Apple SDK behavior changes.

## Source order

1. The repository's checked-in project, build settings, resolved dependencies, tests, and instructions.
2. The installed toolchain and SDK declarations used by the affected target.
3. The narrow current Apple or Swift symbol, framework, migration, or distribution documentation.
4. The closest current Apple-authored sample for the same platform and technical problem.
5. WWDC sessions or archived samples only when current documentation does not cover a required legacy
   behavior.

Useful starting points:

- [Apple Developer Documentation](https://developer.apple.com/documentation/)
- [Apple Sample Code Library](https://developer.apple.com/documentation/samplecode/)
- [Xcode documentation](https://developer.apple.com/documentation/xcode)
- [SwiftUI](https://developer.apple.com/documentation/swiftui)
- [Swift language documentation](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/)
- [Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
- [Accessibility](https://developer.apple.com/documentation/accessibility/)

## Verify source compatibility

For every materially selected API or sample, confirm:

- required Xcode and Swift versions;
- supported platforms and minimum OS versions;
- capabilities, entitlements, privacy declarations, accounts, hardware, and signing requirements;
- lifecycle, ownership, isolation, persistence, error, and cancellation assumptions;
- whether the source is current, beta, deprecated, or archived; and
- whether its validation method matches the local runtime and distribution channel.

An installed SDK does not authorize raising a deployment target. A compiling symbol does not prove
availability on every supported OS.

## Record a material sample decision

When a sample materially shapes implementation, report:

- sample title and canonical Apple URL;
- the demonstrated method and its requirements;
- the smallest technique adapted locally;
- differences in architecture, targets, identifiers, entitlements, and data ownership; and
- the build, test, runtime, accessibility, persistence, or distribution evidence used to validate it.

Use a temporary directory when downloading sample code. Never copy sample credentials, identifiers,
container names, generated files, signing settings, or unrelated architecture into the user's project.
