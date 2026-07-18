# Tracking and experiments

## Event contract

Define an event with:

- semantic name and version;
- business meaning;
- trigger and exclusions;
- actor, object, context, result, and source;
- required and optional properties with types and allowed values;
- identity and anonymous-to-known behavior;
- timestamp source, retry, deduplication, ordering, and offline behavior;
- consent category, sensitivity, retention, and access;
- validation examples and owner.

Prefer events that describe meaningful domain occurrences over UI implementation details. A renamed button
should not change the meaning of a completed-order event.

## Metric contract

Specify:

> Among **[eligible population]**, the **[aggregation]** of **[event or state]** per **[unit]** during
> **[window]**, excluding **[rules]**, segmented by **[predeclared dimensions]**.

Include source tables or events, join keys, late-arrival policy, version, owner, and known biases.

## Experiment integrity

Before outcome analysis, verify:

- deterministic assignment and allocation;
- eligibility applied before assignment where intended;
- stable treatment and control experiences;
- exposure logic and contamination;
- sample-ratio balance;
- identifier and join integrity;
- event completeness and equivalent logging across variants;
- no unplanned early stopping or variant redefinition.

## Interpret results

Report:

- participants assigned and exposed;
- baseline and observed values;
- absolute and relative effect;
- interval or uncertainty appropriate to the method;
- guardrail effects;
- planned segment results;
- data-quality or protocol issues;
- practical significance and decision.

An inconclusive result is not evidence of no effect. A statistically detectable effect is not necessarily
worth its cost or harm.
