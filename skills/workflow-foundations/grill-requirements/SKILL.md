---
name: grill-requirements
description: Runs an explicit, repository-informed interview that pressure-tests a request, plan, or design one consequential decision at a time before implementation. Use only when the user asks to be grilled, interviewed, challenged, or wants assumptions and requirements stress-tested; do not invoke implicitly for routine ambiguity or ordinary clarifying questions.
---

# Grill requirements

Resolve consequential ambiguity before planning or implementation. Keep the interview demanding but
constructive, and end with a shared decision brief rather than code.

## Hold the boundary

- Do not implement, edit files, or enact the plan during the grill.
- Do not silently turn every unclear task into an interview. The user must explicitly request this mode.
- Use the harness's native structured-question interface when available; otherwise ask in normal
  conversation.
- Write a glossary, ADR, specification, or other durable artifact only when the user explicitly requests
  documentation.
- Let the user pause or end the interview at any time.

## Prepare from evidence

1. Read the supplied request, plans, documents, and relevant repository context.
2. Resolve questions from code, configuration, existing decisions, or documentation before asking the user.
3. Identify the unresolved decision branches and their dependencies.
4. Start with the highest-leverage decision that constrains the most downstream choices.

Do not ask the user to recite discoverable repository facts. Surface conflicts between the request and
existing evidence directly.

## Run the interview loop

For each unresolved branch:

1. State the decision and why it matters in one concise sentence.
2. Ask one primary question at a time. A native question UI may present two or three mutually exclusive
   options for that single decision.
3. Put the recommended answer first and explain its main consequence or tradeoff.
4. Avoid neutral option dumps, false dichotomies, leading questions, and questions whose answers do not
   change the plan.
5. Wait for the answer before moving to a dependent branch.
6. Record the accepted decision, rejected alternatives that matter, and new downstream implications.
7. Challenge contradictions, unsafe assumptions, hidden actors, missing states, and untestable success
   claims instead of merely collecting preferences.

When an answer opens a new material branch, add it to the decision map and resolve it in dependency order.
Keep the map concise; do not overwhelm the user with the entire tree.

## Cover the material surfaces

Adapt the interview to the work. Resolve only surfaces that could materially change the result:

- intended outcome, audience, and primary job;
- scope, non-goals, ownership, and authority;
- terminology and domain invariants;
- workflows, actors, states, and permissions;
- inputs, outputs, data boundaries, integrations, and migrations;
- failure, recovery, edge cases, compatibility, and rollout;
- quality thresholds, acceptance evidence, and operational constraints.

Depth should follow risk and reversibility. A small reversible choice needs less grilling than an
architecture, security boundary, data migration, or costly product direction.

## Know when to stop

End the grill when:

- no unresolved decision could materially change the objective, architecture, behavior, safety, or
  acceptance evidence;
- remaining unknowns are explicitly deferred with an owner or validation path; or
- the user asks to stop.

Do not continue asking questions to perform thoroughness.

## Return the decision brief

Conclude with:

```markdown
Shared objective:
Accepted decisions:
Rejected alternatives that matter:
Assumptions still in force:
Open questions or deferred validation:
Non-goals:
Completion evidence:
Recommended next mechanism:
```

Recommend `goal-contract` for substantial, resumable, or goal-backed work. Recommend direct planning for a
bounded task, or a one-off prompt when no persistent mechanism is warranted.
