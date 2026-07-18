---
name: shape-product-opportunity
description: Turns a desired product outcome and available evidence into prioritized opportunities, explicit assumptions, and testable bets. Use when deciding what product problem to pursue, framing discovery, evaluating solution options, reducing product risk, or defining experiments before committing to delivery.
---

# Shape a product opportunity

Create a defensible product bet without smuggling a preferred feature into the problem statement.

## Anchor on an outcome

1. Read project instructions, strategy, research, analytics, support evidence, constraints, and active
   commitments.
2. State the desired user behavior or condition and the business or mission outcome it should support.
3. Define the affected users, situation, baseline, time horizon, and exclusions.
4. Separate the outcome from output. “Release feature X” is an output; state the change it is meant to
   create.
5. Record evidence, assumptions, unresolved contradictions, and non-goals.

Use [assets/opportunity-brief-template.md](assets/opportunity-brief-template.md) when the decision needs a
durable artifact.

## Map opportunities before solutions

1. Express opportunities as user needs, obstacles, or desires grounded in evidence.
2. Organize parent and child opportunities only where the relationship is supported.
3. Keep solutions out of opportunity labels.
4. Note affected segments and contexts; do not average away materially different needs.
5. Mark evidence source, recency, confidence, and gaps for every material branch.

Use `conduct-user-research` when the map relies mainly on stakeholder belief or evidence is too weak to
support a decision.

## Select a promising opportunity

Compare opportunities using:

- expected contribution to the outcome;
- user importance and current dissatisfaction;
- reach and frequency in the relevant population;
- strategic fit and differentiation;
- confidence and quality of evidence;
- cost of delay, reversibility, dependencies, and downside;
- accessibility, safety, privacy, operational, and equity implications.

Do not collapse these into a precise score unless the inputs deserve that precision. Show tradeoffs and why
the selected opportunity outranks plausible alternatives.

## Generate and compare solution approaches

Generate meaningfully different approaches, including process, policy, content, service, or removal options
when software is not the smallest answer. Compare them against the same opportunity and constraints.

For each candidate, state:

- mechanism by which it could change the outcome;
- users and situations it serves or excludes;
- dependencies and operational effects;
- new failure modes and irreversible choices;
- expected learning value.

Let `design-product-interface` or `design-and-build-website` own detailed design after the opportunity and
bet are accepted.

## Expose assumptions and reduce risk

Read [references/assumptions-and-experiments.md](references/assumptions-and-experiments.md) when ranking
assumptions or choosing a test.

1. Write assumptions across value, usability, feasibility, viability, accessibility, safety, adoption, and
   measurement.
2. Rank them by importance and uncertainty.
3. Test the riskiest assumption with the smallest credible evidence, not the most impressive prototype.
4. Define the prediction, evidence threshold, guardrails, time box, and decision before collecting results.
5. Use `measure-product-experiments` when instrumentation, metric definitions, assignment, or causal
   analysis requires a full measurement plan.

## Decide and bound the bet

Produce:

- target outcome and baseline;
- selected opportunity and evidence;
- alternatives considered;
- solution hypothesis and causal mechanism;
- riskiest assumptions and planned tests;
- leading, outcome, and guardrail measures;
- scope boundaries, dependencies, and stop conditions;
- decision: commit, test, reframe, defer, or stop.

Treat a failed assumption test as useful risk reduction. Do not reinterpret success criteria after seeing
the result.

## Apply quality rules

- Preserve a trace from evidence to opportunity to solution to experiment.
- Distinguish fact, inference, assumption, and decision.
- Prefer reversible learning before expensive commitment.
- Include who may be harmed, excluded, or burdened.
- Do not invent market evidence, customer demand, forecasts, or experiment results.
