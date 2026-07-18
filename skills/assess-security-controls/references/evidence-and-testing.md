# Evidence and testing

Judge a control from evidence that is relevant, reliable, current, and sufficient for the scoped conclusion.

## Evidence hierarchy

Prefer combinations of:

1. Direct configuration, system state, immutable logs, reports, tickets, and artifacts.
2. Reperformance or observation of the control.
3. Population data and risk-based samples.
4. Approved policies, standards, procedures, architecture, and control definitions.
5. Interviews and representations used to understand the process.

No single class is always sufficient. A configuration snapshot can show design but not months of operation;
a policy can show intent but not implementation; a ticket can show activity but not that risk was removed.

## Evidence record

For every material item, capture:

- evidence identifier and protected location;
- source system and owner;
- collection method and collector;
- date produced, date collected, and period covered;
- related requirement, control, asset, and population;
- integrity or authenticity consideration;
- redactions and handling classification;
- limitations, missing context, and expiration.

Avoid copying secrets, tokens, personal data, exploit payloads, or sensitive infrastructure details into a
broadly distributed workbook.

## Test design

Define:

- control objective and failure condition;
- design test;
- operating test and period;
- population and completeness check;
- risk-based sample method and size rationale;
- expected evidence;
- exception criteria;
- dependence on other controls or service providers.

For automated controls, inspect configuration plus representative operation and change control. For manual
controls, inspect performance across the period rather than one ideal example. For inherited controls,
validate the inheritance boundary, customer responsibilities, and relevant assurance period.

## Evidence sufficiency

Use:

- **Strong:** direct, current, representative, and independently reproducible.
- **Moderate:** credible but limited in period, population, independence, or corroboration.
- **Weak:** assertion, stale snapshot, narrow example, incomplete population, or unclear provenance.
- **None:** requested evidence was not provided or could not be validated.

Confidence is not the same as effectiveness. A control can be confidently ineffective or only weakly
supported as effective.

## Exceptions

Record the requirement, affected population, duration, cause, consequence, compensating control, owner, and
correction plan. Distinguish an isolated exception from a systemic failure and explain how the sample
supports that judgment.
