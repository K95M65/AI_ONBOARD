# Manual, optional workflow foundations

`goal-contract` and `grill-requirements` normalize two useful workflows without pretending every harness
needs the same replacement. They are portable skills, but they are excluded from capability profiles
because some tools already provide equivalent native capabilities.

Both are original AI_ONBOARD skills and are **manual by contract**: an agent may select them only after the
user explicitly asks for goal-backed work or a requirements grill. They do not auto-run before ordinary
planning, implementation, review, or verification.

Manual invocation may be a direct skill name or unambiguous natural language such as “run this as a goal”
or “grill me on the requirements.” It does not require the user to know the internal skill name.

## Capability selection

| Need | Native capability exists | Native capability is absent |
|------|--------------------------|-----------------------------|
| Durable goal state | Use the harness's native goal lifecycle | Use `goal-contract` as an honest conversation fallback |
| Structured questions | Let `grill-requirements` use the native question UI | Ask one decision at a time in normal conversation |
| Persistent fallback artifact | Do not create a parallel ledger | Write a goal file only when the user explicitly requests resumability |

Install both optional skills:

```bash
python3 /path/to/AI_ONBOARD/scripts/ai_onboard.py \
  --target /path/to/project \
  install \
  --harness claude,codex,opencode \
  --profile core \
  --agents \
  --workflow-foundations
```

For an already managed project, set `"workflow_foundations": true` in `ai-onboard.json` and run
`python3 .ai-onboard/bin/ai_onboard.py sync`. The legacy copy path remains
`bash templates/link.sh --workflow-foundations`.

## GOAL boundary

`goal-contract` defines outcome, evidence, scope, constraints, and a stop condition. A request to define
criteria presents the contract without creating lifecycle state; only an explicit create, run, resume, or
continue request activates a goal. On activation it inspects and prefers native goal state, avoids duplicate
goals, and never claims that a conversation fallback provides automatic continuation or enforcement.

It is not a general planning skill and must not activate for ordinary implementation requests.

## GRILL boundary

`grill-requirements` is an explicit pre-planning interview. It explores the repository before asking
answerable questions, resolves one consequential decision branch at a time, recommends an answer, and ends
with a shared decision brief.

It is not an implicit clarification tax, an implementation workflow, or a post-build review. Durable
glossaries, ADRs, and specifications remain separate opt-in outputs.

## Composition

```text
request
  → manually invoke GRILL when the user explicitly wants assumptions pressure-tested
  → manually invoke GOAL when the user explicitly wants measurable or resumable work
  → plan and execute
  → independent review
  → verification against the goal evidence
```

The two foundations remain skills because they are on-demand procedures. Project facts still belong in
`AGENTS.md`; independent review still belongs with a separate subagent.

A harness may match the user's explicit natural-language intent to either skill, but ordinary ambiguity is
not a trigger and selection is not permission to cross the skill's activation gate.

## Provenance

The native-first GOAL boundary is informed by OpenAI's `define-goal` workflow. The explicit, one-decision-
at-a-time GRILL pattern is informed by Matt Pocock's MIT-licensed `grill-me` and shared `grilling`
workflows. These AI_ONBOARD skills are original portable implementations with narrower trigger and
persistence boundaries.
