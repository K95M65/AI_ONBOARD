---
name: develop-test-first
description: Implements a known behavior change through a focused failing test, the smallest passing production change, and a verified refactor. Use when the user requests test-driven development, a known-cause regression-first bug fix, or new testable domain logic; do not use for unknown-cause diagnosis, behavior-preserving legacy characterization or refactoring, documentation-only work, generated artifacts, exploratory spikes, or UI polish whose value cannot be expressed as stable behavior.
---

# Develop test first

Use a red-green-refactor loop to clarify behavior and protect the change, not to maximize test count.

## Define the behavior

State the observable outcome, boundary, representative input, expected result, and meaningful failure case.
Follow the repository's existing test framework, naming, fixture, and placement conventions. Use a
platform-specific testing skill when it provides more precise guidance.

## Establish the baseline

Run the nearest existing tests before editing. Confirm whether the requested behavior is absent, broken, or
already covered. If the request is only to characterize and preserve existing legacy behavior, route to
`simplify-code-safely`; a passing characterization test is not the Red step for a new behavior.

## Run the loop

1. **Red** — add the smallest test that expresses one missing behavior.
2. Run it and confirm it fails for the intended product reason, not syntax, setup, or fixture failure.
3. **Green** — make the smallest coherent production change that satisfies the behavior.
4. Run the focused test and relevant neighboring tests.
5. **Refactor** — simplify names, duplication, control flow, and test setup while all tests stay green.
6. Repeat for the next independently valuable behavior.

Assert public outcomes, state transitions, outputs, or boundary interactions. Avoid tests coupled to private
method order, incidental DOM structure, arbitrary timing, or excessive mocks.

## Handle exceptions honestly

If the work requires a discovery spike, keep it disposable and translate the learned contract into a test
before shipping production code. If a reliable automated test is impractical, explain why and define the
strongest repeatable manual or integration evidence instead of pretending the loop occurred.

## Finish with evidence

Run the focused test, relevant suite, and any required typecheck, lint, build, or integration checks. Report
the initial failing behavior, production change, refactor, and final commands.

Use `debug-systematically` first when the cause is unknown, then return here only after the intended
correction is supported. Use `simplify-code-safely` for characterization and behavior-preserving cleanup.
Use an independent reviewer and verifier after implementation when available.
