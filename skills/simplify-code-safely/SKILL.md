---
name: simplify-code-safely
description: Simplifies existing code while preserving externally observable behavior, public contracts, and required performance. Use when reducing accidental complexity, removing dead or duplicated logic, clarifying control flow, shrinking an over-engineered change, or performing a focused behavior-preserving refactor; do not use for feature development, architecture replacement, or read-only code review.
---

# Simplify code safely

Make the code easier to understand without quietly changing what it does.

## Establish the behavior boundary

Read the project instructions, callers, tests, public interfaces, error behavior, side effects, data formats,
performance constraints, and compatibility requirements. State the simplification target and what must not
change. If behavior is unclear, characterize it with focused tests before refactoring.

## Find accidental complexity

Look for:

- dead code, unreachable branches, stale flags, and unused indirection;
- duplicated rules that represent the same concept;
- conditionals that can become early exits or explicit state transitions;
- abstractions with one caller and no meaningful policy boundary;
- misleading names, hidden side effects, and values recomputed across layers;
- comments that compensate for unclear structure rather than explain intent.

Do not collapse distinct domain concepts merely because their current implementations look similar.

## Simplify in small steps

1. Record a passing baseline for the relevant checks.
2. Make one coherent transformation at a time.
3. Prefer deletion, direct control flow, precise names, and existing language features.
4. Preserve public APIs, error semantics, ordering, concurrency, persistence, and security checks unless the
   user explicitly includes them in scope.
5. Run the narrow checks after each risky transformation.
6. Review the final diff for accidental behavior changes and unnecessary churn.

Avoid speculative frameworks, generic helpers without a stable concept, broad formatting changes, and
dependency upgrades unrelated to the simplification.

## Prove the result

Run focused tests and the relevant broader suite. Compare before/after behavior, and measure performance only
when performance is part of the contract. Report what became simpler—deleted branches, reduced state,
removed duplication, or clearer ownership—without using line count as the only quality measure.

Use a separate reviewer agent when independent code review is requested. This skill edits code; the reviewer
remains read-only.

Finish when the behavior boundary still holds, the diff is smaller or conceptually clearer, and every
claimed improvement is visible in the code rather than asserted from taste.
