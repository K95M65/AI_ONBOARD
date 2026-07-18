# Assumptions and experiments

## Write testable assumptions

Use a concrete form:

> We believe **[specific users in a situation]** will **[behavior/change]** because **[mechanism]**. We will
> reconsider if **[observable evidence]** does not meet **[threshold]** by **[time or sample condition]**.

Inspect these risk classes:

- **Value:** the outcome matters enough to change behavior.
- **Usability:** people can understand, complete, and recover from the workflow.
- **Feasibility:** the system and organization can deliver it reliably.
- **Viability:** economics, policy, support, legal, and operations can sustain it.
- **Adoption:** people can discover, access, and integrate it into current work.
- **Accessibility and safety:** the approach does not create unacceptable barriers or harm.
- **Measurement:** the predicted change can be observed without misleading proxies.

## Choose evidence proportional to the claim

| Claim | Small credible test |
|---|---|
| A problem occurs in a workflow | Contextual observation, existing evidence review, targeted interview |
| A concept is understood | Low-fidelity concept task with explanation in the participant's own words |
| A workflow is usable | Representative task test including errors and recovery |
| People will take an action | Concierge, commitment, pilot, or limited release |
| A technical approach works | Spike, benchmark, integration test, or operational rehearsal |
| A change causes an outcome | Randomized experiment where ethical and feasible; otherwise a stated quasi-experimental design |

Preference, comprehension, usability, adoption, and causal impact are different claims. Do not substitute
one for another.

## Precommit the decision

Before the test, record:

- hypothesis and alternative explanations;
- population, context, and exclusions;
- primary evidence and guardrails;
- success, failure, and inconclusive thresholds;
- minimum exposure or stopping rule;
- actions for each result;
- risks created by the test itself.
