# Governance and migration

## Contribution lifecycle

Use a lightweight lifecycle:

1. **Need:** show repeated consumer evidence or a strategically important unmet case.
2. **Explore:** compare composition, extension, local ownership, and a new shared primitive.
3. **Specify:** define contract, states, accessibility, content, platform deltas, tests, and ownership.
4. **Pilot:** adopt in representative consumers and record exceptions.
5. **Stabilize:** publish documentation, compatibility commitment, release notes, and support path.
6. **Maintain or retire:** monitor use, defects, and changing platform guidance.

Require stronger evidence for permanent public API than for an experimental pattern.

## Version change by consumer impact

- **Patch:** compatible correction with no intentional contract change.
- **Minor:** additive capability or opt-in behavior.
- **Major:** removal, renamed contract, changed default, or behavior requiring consumer judgment.

Visual or accessibility changes can be behavior changes even when the code API is unchanged. State them
explicitly.

## Deprecation record

Document:

- deprecated item and rationale;
- supported replacement and gaps;
- first deprecated and intended removal versions or dates;
- automated migration, if safe;
- manual decisions required;
- known consumers and owner;
- escape hatch for legitimate exceptions.

## Migration plan

Sequence dependencies first: foundations, primitives, composed components, then product surfaces. For each
consumer, record compatibility, visual review, interaction tests, accessibility checks, product owner, and
rollback. Never run a mechanical replacement where semantics, information hierarchy, or user behavior may
change.
