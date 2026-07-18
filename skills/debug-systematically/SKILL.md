---
name: debug-systematically
description: Reproduces software failures, isolates causal conditions, tests competing hypotheses, and either reports the supported diagnosis or implements and verifies the smallest authorized root-cause fix. Use for diagnosis or repair when the cause of a bug, crash, flaky test, incorrect output, performance regression, race condition, integration failure, or environment-specific behavior is unknown; do not use for feature development or a known-cause change that the user explicitly wants implemented test-first.
---

# Debug systematically

Replace guess-and-check editing with a reproducible chain from symptom to cause to verified correction.

## Reproduce the failure

Capture the exact command or user path, expected result, observed result, environment, versions, input,
frequency, and earliest known good state. Reduce nondeterminism where possible. If the failure cannot be
reproduced, gather discriminating evidence instead of changing code speculatively.

## Narrow the causal surface

1. Identify the boundary where correct state first becomes incorrect.
2. Compare passing and failing inputs, environments, commits, timing, or dependencies.
3. Trace data and control flow across that boundary.
4. Form one falsifiable hypothesis at a time.
5. Run the smallest experiment that could disprove it.
6. Record rejected hypotheses so they are not repeated.

Use logs, assertions, traces, profilers, debuggers, or temporary instrumentation only where they distinguish
competing causes. Remove temporary instrumentation before finishing unless it has lasting operational value.

## Respect the request boundary

For a diagnosis-only request, stop after identifying the supported cause, evidence, and likely correction.
Implement only when the user asks to fix the bug or the request clearly includes repair.

## Fix the cause

- Add or refine a regression test that fails for the reproduced defect.
- Make the smallest coherent correction at the causal boundary.
- Do not suppress errors, weaken assertions, add arbitrary sleeps or retries, broaden timeouts, or upgrade
  dependencies without evidence that the change addresses the cause.
- Preserve unrelated behavior and existing architecture.

## Verify

Confirm the original reproduction now passes, the regression test detects the old behavior, and the
relevant broader checks remain green. Exercise nearby edge cases implied by the cause. For intermittent
failures, run enough repetitions to support the stability claim and report the sample.

Compose with `test-browser-workflows` for browser failures, a platform-specific testing skill where one
exists, and a verifier agent for independent acceptance. When the cause and intended behavior are already
known and the user wants a regression-first implementation, hand the change to `develop-test-first`
instead of repeating its red-green-refactor loop here.

Finish a diagnosis-only request with the supported cause, decisive evidence, likely correction, commands
run, and residual uncertainty. When repair was authorized, also report the implemented fix and regression
coverage.
