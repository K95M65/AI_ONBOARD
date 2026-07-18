# Validation and release

Validate the product through representative work on each target platform.

## Run project checks

Run relevant formatting, lint, type, build, unit, integration, UI, and end-to-end checks from repository
instructions. Fix causes and rerun affected checks. Report pre-existing or environment-dependent failures
plainly.

## Test task scenarios

For each representative workflow, verify:

1. A user can discover how to begin.
2. The product preserves context, selection, scope, and unsaved work.
3. Commands behave consistently across the target input methods.
4. Validation prevents or explains invalid states.
5. Loading, empty, partial, stale, conflict, offline, permission, error, and success behavior is coherent.
6. A user can cancel, undo, retry, reconcile, or recover where appropriate.
7. Completion is observable and the next state is clear.

Use realistic data, including zero items, one item, large collections, long values, localized text,
restricted permissions, stale versions, and malformed external input.

## Test platform behavior

Use the selected platform reference as the test matrix. Exercise supported operating systems, window or
viewport sizes, input methods, themes, text and display scaling, reduced motion, high contrast, screen
readers, keyboard navigation, connectivity, permissions, background or resume, deep links or files, and
system integration.

Capture screenshots, recordings, accessibility output, or test logs for important workflows and failures.

## Review independently

Request an independent design review across:

- product-model and platform fit;
- hierarchy, context, scope, density, and command placement;
- component consistency and realistic content;
- complete states and recovery;
- accessibility and input coverage;
- responsive, adaptive, windowed, and system behavior.

Use a verifier for acceptance criteria and commands. Add security review where external input, identity,
authorization, sensitive information, privileged actions, or distribution trust is involved.

## Prepare release

1. Identify versioning, packaging, signing, notarization, store, hosting, update, and rollback paths.
2. Verify environment configuration and secrets through the approved mechanism.
3. Produce the release artifact or deployment through the existing workflow.
4. Record target platforms, compatibility, migrations, permissions, and known limitations.
5. Obtain authorization before a live release unless the user explicitly requested the target.
6. Smoke-test the distributed build or live environment, including the primary workflow and update or
   rollback path.

Report exact artifacts, versions, targets, checks, review status, known limitations, and operational owners.
