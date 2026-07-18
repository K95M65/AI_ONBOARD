# Verification and distribution

Verify the actual product on supported destinations and keep release operations separate from ordinary
implementation.

## Build and test

1. Run the repository's formatter, linter, generator checks, and narrow affected tests.
2. Build the affected scheme or Swift package with its supported configuration.
3. Run unit and integration tests. Keep Swift Testing and XCTest according to target capability and existing
   suites; UI automation remains XCTest-based unless the project establishes another runner.
4. Exercise the representative workflow in the running app, including cancellation, failure, empty,
   permission-denied, interruption, restoration, and recovery paths that the change affects.
5. Repeat on the oldest supported OS or a representative compatibility destination when availability or
   behavior differs by version.

Do not report a generic “tests passed.” Record the command, scheme, configuration, destination, and result.

## Inspect quality

- Use the relevant SwiftUI or AppKit accessibility auditor and test keyboard-only and VoiceOver operation.
- Check concurrency warnings and runtime diagnostics; reproduce suspected races or hangs rather than
  suppressing diagnostics.
- Profile before optimizing. Use Instruments or signposts appropriate to the symptom, and retain a
  before/after trace or metric for a claimed performance improvement.
- Test persistence migrations against representative copies and verify rollback or compatibility behavior.
- For files and sandbox access, test first grant, retained access, denial, relocation, and revocation.

## Prepare a release artifact

Determine the actual channel:

- Mac App Store or iOS-family App Store;
- Developer ID signed and notarized direct distribution;
- TestFlight, internal enterprise or managed distribution;
- Swift package, framework, command-line product, or local-only app.

Verify version/build numbers, archive configuration, entitlements, privacy declarations, signing identity,
provisioning, hardened runtime, package contents, migrations, update compatibility, and release notes.

Signing, notarization, TestFlight upload, store submission, pricing, phased release, and update-feed
publication require credentials and external authority. Dry-run or inspect when that authority is absent.
After an authorized release, validate the distributed artifact—not only the pre-archive debug build—and
record the rollback or previous-version path.
