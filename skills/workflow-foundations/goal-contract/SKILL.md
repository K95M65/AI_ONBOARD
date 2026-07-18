---
name: goal-contract
description: Defines a concrete, measurable execution goal and, for activation requests, hands it to native goal state when the agent harness supports that capability. Use only when the user explicitly asks to create or run a goal, requests goal-backed or resumable work, or wants fuzzy intent converted into verified completion criteria; do not invoke for ordinary implementation tasks.
---

# Goal contract

Turn explicit goal intent into an honest execution contract. Prefer native goal state; use a
conversation-local contract only when the harness has no equivalent capability.

## Select the state mechanism

1. Decide whether the user asked to **define** a contract or to **create, run, resume, or continue** a goal.
2. For definition-only requests, present the contract without activating lifecycle state.
3. For activation requests, check whether the harness exposes native goal creation, inspection,
   continuation, or lifecycle state.
4. Use native goal state when available. Do not create a parallel file or second goal ledger.
5. When native goal state is unavailable, keep the contract in the current conversation by default.
6. Create or update a repository goal file only when the user explicitly requests durable, file-backed
   resumability. Confirm the path and preserve existing project conventions before writing it.
7. Never claim that a conversation contract supplies automatic continuation, persistence, budget control,
   or lifecycle enforcement that the harness does not provide.

## Define the contract

Write one concise objective that establishes:

- **Outcome** — the concrete condition that will be true.
- **Evidence** — the checks, artifacts, observations, or thresholds that prove completion.
- **Scope** — the systems, files, environments, or decisions included.
- **Constraints** — safety boundaries, forbidden changes, budgets, deadlines, or blast-radius limits.
- **Stop condition** — the ambiguity, repeated blocker, or external dependency that requires user input.

Add non-goals only when they prevent a plausible scope mistake. Use quantitative thresholds when they
represent real success; do not invent decorative precision. When the user asks only for a draft and has
not supplied a threshold, label any useful numeric target as **proposed for confirmation** rather than an
accepted constraint.

## Repair weak goals

- Replace activity statements such as “make progress” or “improve this” with observable outcomes.
- Inspect available project context before asking the user for facts the repository can answer.
- Ask one concise question only when the missing answer would materially change the outcome, evidence, or
  scope. Recommend the safest reasonable answer when helpful.
- Do not force goal creation onto a bounded request that can be completed normally.
- Include a token, cost, or time budget only when the user explicitly sets one.

## Activate without duplication

1. Inspect existing native or file-backed goal state before creating anything.
2. Continue an active matching goal instead of creating a duplicate.
3. Surface a conflicting active goal and ask the user which objective should own the work.
4. Create or present the contract once it passes this quality bar:
   - the completion condition is binary or measurably bounded;
   - the required evidence is named;
   - material scope boundaries are explicit;
   - the stop condition is honest and actionable.

Treat an unambiguous request to create, run, resume, or continue a goal as authorization to activate it.
Requests to define criteria or draft a contract authorize presentation only. Do not add a redundant
confirmation gate to either path.

## Close honestly

- Evaluate completion against the contract, not effort expended.
- Use only lifecycle states the active harness actually supports.
- Mark a native goal complete only when every required outcome and validator is satisfied.
- Use native blocked semantics only under that harness's rules; otherwise report the blocker without
  inventing durable state.
- For conversation-only fallback, close with satisfied evidence, unmet criteria, and any remaining external
  dependency. Do not imply that the contract will resume itself later.

## Contract format

```markdown
Objective: <one outcome-focused sentence>
Evidence:
- <validator or observable result>
Scope: <included surface>
Constraints: <material boundaries>
Stop and ask when: <specific escalation condition>
State mechanism: <native goal | conversation fallback | user-authorized file>
```
