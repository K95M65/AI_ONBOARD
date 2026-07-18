---
name: measure-product-experiments
description: Defines trustworthy product measurement, event contracts, data-quality checks, and experiments tied to explicit decisions. Use when creating a measurement plan, selecting product metrics and guardrails, specifying analytics instrumentation, evaluating a rollout or product change, or designing an ethical randomized or quasi-experimental test.
---

# Measure product experiments

Design measurement around a decision, not around the volume of events available. Preserve the distinction
between observed association and causal effect.

## Define the decision and causal model

1. Read project instructions, product strategy, research, existing telemetry, data definitions, privacy
   rules, architecture, and prior experiments.
2. State the decision, owner, population, context, alternatives, and date it must be made.
3. Describe how the product change is expected to alter user behavior and the desired outcome.
4. List alternative explanations, possible harms, spillovers, and delayed effects.
5. Record the baseline, current evidence, unknowns, and what result would change the decision.

Use [assets/measurement-plan-template.md](assets/measurement-plan-template.md) for a durable plan.

## Choose measures that match the decision

Define:

- **outcome measure:** the user or business condition the decision ultimately targets;
- **leading measure:** earlier evidence on the proposed mechanism;
- **guardrails:** harms or regressions that make apparent success unacceptable;
- **diagnostics:** measures used to explain implementation and segment differences;
- **data-quality measures:** evidence that exposure, events, joins, and windows are trustworthy.

For every metric, specify numerator, denominator, unit of analysis, eligible population, exclusions, time
window, segmentation, source, owner, and known limitations. Prefer rates and distributions when totals hide
exposure or inequality.

Do not use a convenient proxy without explaining why it should track the intended outcome and how it could
be gamed.

## Specify instrumentation as contracts

Read [references/tracking-and-experiments.md](references/tracking-and-experiments.md) when defining events,
assignment, exposure, or experiment analysis.

For each event, define:

- stable semantic name and business meaning;
- exact trigger and non-trigger cases;
- actor, object, context, and outcome properties;
- identifier, timestamp, deduplication, ordering, and version behavior;
- consent, minimization, retention, and access requirements;
- validation cases and responsible owner.

Capture exposure only when the participant could plausibly experience the treatment. Never include secrets,
unnecessary content, or sensitive attributes merely for possible future analysis.

## Validate the data path

1. Trace the flow from user action to emitted event, transport, storage, transformation, metric, and
   decision surface.
2. Test expected, duplicate, retried, offline, partial, failure, and cross-device cases.
3. Compare telemetry with an independent source where possible.
4. Inspect missingness, impossible values, sample-ratio imbalance, delayed arrival, bot or internal traffic,
   and version drift.
5. Establish alerting or routine checks proportional to the decision risk.

Do not analyze an experiment until assignment, exposure, eligibility, and primary metric integrity pass
their predeclared checks.

## Choose an evaluation design

Prefer a randomized controlled experiment when assignment is ethical, feasible, and unlikely to create
unacceptable interference. Otherwise choose the strongest feasible alternative and state its limitations:
staged rollout, switchback, interrupted time series, matched comparison, difference-in-differences, or a
descriptive pilot.

Predeclare:

- hypothesis and unit of assignment;
- eligibility and exclusion rules;
- treatment, control, exposure, and contamination;
- primary metric, guardrails, segments, and analysis window;
- minimum detectable effect or decision-relevant threshold;
- power or sample rationale, duration, stopping rule, and multiple-comparison handling;
- actions for positive, negative, mixed, harmful, and inconclusive results.

Seek qualified statistical, legal, privacy, or ethics review when stakes or organizational policy require
it. Do not promise a valid sample size or causal claim without the necessary inputs.

## Analyze and decide

1. Report assignment, exposure, data quality, attrition, and protocol deviations before outcomes.
2. Show effect size and uncertainty, not only a significance label.
3. Check guardrails and practically important segment differences without uncontrolled result hunting.
4. Distinguish planned analyses from exploratory findings.
5. Consider novelty, seasonality, interference, survivorship, logging changes, and delayed outcomes.
6. Make the precommitted decision or explain why new evidence invalidates the original rule.
7. Record what was learned, remaining uncertainty, rollout or rollback, and follow-up measurement.

Use `shape-product-opportunity` when results must update the opportunity or product bet.

## Apply quality rules

- Minimize data and respect consent, purpose, retention, access, and deletion obligations.
- Do not define success from engagement alone when the product aims for a user outcome.
- Do not change the primary metric or stopping rule after inspecting results without labeling the analysis
  exploratory.
- Do not report causality from a before-and-after comparison alone.
- Never fabricate telemetry, baselines, sample sizes, statistical results, or experiment outcomes.
