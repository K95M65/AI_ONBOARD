# How agents should work — the behavioral contract

The `## How to work` section of [`AGENTS.md`](../AGENTS.md) is a small, opinionated set of defaults for
*how* an agent should behave on any project — separate from the project-specific facts (stack, commands,
conventions) that make up the rest of the file.

It isn't invented here. Every rule below is something **both OpenAI and Anthropic publish as official
guidance**. Where they converge, we adopt it verbatim in spirit. Where they diverge — mainly on how
autonomous an agent should be — we make one deliberate choice and explain it.

Keep the `AGENTS.md` section short; keep the reasoning here.

---

## The principles and where they come from

### Understand before you change — don't guess
An agent that guesses at file contents or structure hallucinates. Both vendors say the same thing:

- **OpenAI** (GPT-4.1 Prompting Guide, agentic reminders): *"If you are not sure about file content or
  codebase structure pertaining to the user's request, use your tools to read files and gather the relevant
  information: do NOT guess or make up an answer."*
- **Anthropic** (Claude Code best practices): *"Claude can infer intent, but it can't read your mind"* —
  reference specific files and gather context before acting.

### Plan when it's non-trivial
Investigate before implementing, but don't ceremony-ize trivial edits.

- **OpenAI** (Practical Guide to Building Agents / GPT-4.1 guide): emphasize "thorough investigation before
  implementation" and break problems into incremental steps.
- **Anthropic** (best practices): explore → plan → code, but *"if you could describe the diff in one
  sentence, skip the plan."*

### Be persistent within scope — the one deliberate choice
This is where the two camps pull in different directions, and where we make a call:

- **OpenAI dials autonomy up.** Their headline agentic reminder: *"You are an agent — please keep going
  until the user's query is completely resolved… Only terminate your turn when you are sure that the problem
  is solved."* That single instruction moved their internal SWE-bench score ~20%. (Context: tuned for
  GPT-4.1, a non-reasoning model that tends to yield too early.)
- **Anthropic dials it down.** *"Overeager behavior"* is a **named threat** in their auto-mode model; they
  push scoping investigations narrowly, course-correcting early, and asking the user rather than barreling
  ahead. (Context: aimed at capable reasoning models that tend to over-reach.)

**Our default — "persistent within scope":** finish the task fully and verify before yielding (OpenAI's
persistence), but treat *scope expansion* and *irreversible/destructive actions* as the hard stop where you
check in first (Anthropic's guardrail). It's model-agnostic and takes the defensible half of each.

### Verify, then claim — show evidence
The single strongest, most-repeated theme in both vendors' guidance.

- **OpenAI** (Codex best practices): define **success criteria** — "what done looks like and how to verify
  it" — and run the relevant tests/lint/typecheck before finishing.
- **Anthropic** (Agent SDK + best practices): the core loop is *"gather context → take action → verify work
  → repeat,"* and *"show evidence rather than asserting success"* — the command you ran and what it returned,
  not a claim. *"If you can't verify it, don't ship it."*

### Fix causes, not symptoms
- **Anthropic** (best practices): address root causes; *"don't suppress the error."*
- Consistent with OpenAI's success-criteria framing — a check that's been weakened to pass no longer
  verifies anything.

### Match the surroundings
- **Anthropic**: match the style of surrounding code; prefer editing existing files over adding new ones.
- **OpenAI**: derive behavior from existing conventions/SOPs rather than inventing new ones.

### Report honestly
- **Anthropic**: the "trust-then-verify gap" — plausible-looking work that misses edge cases; show the test
  output, name what was skipped, surface blockers.
- **OpenAI**: verification and success criteria are first-class instructions — a silent skip defeats them.

---

## Two meta-rules for maintaining the contract

Both vendors agree on how this file itself should be governed:

1. **Brevity is a hard rule, not a preference.**
   - OpenAI (Codex best practices): *"A short, accurate AGENTS.md is more useful than a long file full of
     vague rules."* Codex stops reading merged instruction files at 32 KiB.
   - Anthropic (memory docs): *"Target under 200 lines… Longer files consume more context and reduce
     adherence."* Test each line: *"Would removing this cause the agent to make mistakes? If not, cut it."*

2. **Grow rules from real friction, not speculation.**
   - OpenAI: *"Add new rules only after observing repeated mistakes."*
   - Anthropic: *"Treat CLAUDE.md like code — prune it regularly, and test changes by observing whether
     behavior actually shifts."*

   → Ship the template lean. Add project-specific rules when an agent actually gets something wrong twice,
   not before.

---

## Guidance vs. enforcement (important caveat)

An instructions file is **advisory**, not a guarantee. Anthropic is explicit: CLAUDE.md/AGENTS.md is
context delivered to the model, *"there's no guarantee of strict compliance."* For steps that **must** happen
every time, use deterministic mechanisms instead:

- **Claude Code:** hooks (PreToolUse / Stop) and `permissions.deny`.
- **Codex:** sandbox modes (`read-only`, `workspace-write`, `danger-full-access`) and approval policies
  (`untrusted`, `on-request`, `never`).

That's why this repo keeps the behavioral *contract* in the portable `AGENTS.md` but documents per-tool
*enforcement* separately under [`setup/`](setup/). The contract sets the intent; the tool config makes the
non-negotiable parts binding.

---

## Sources

- OpenAI — AGENTS.md spec: <https://agents.md>
- OpenAI — Codex custom instructions & best practices: <https://developers.openai.com/codex/guides/agents-md>
- OpenAI — GPT-4.1 Prompting Guide (agentic workflows): <https://cookbook.openai.com/examples/gpt4-1_prompting_guide>
- OpenAI — A Practical Guide to Building Agents (PDF): <https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf>
- Anthropic — Claude Code best practices: <https://code.claude.com/docs/en/best-practices>
- Anthropic — Claude Code memory (CLAUDE.md): <https://code.claude.com/docs/en/memory>
- Anthropic — Building effective agents: <https://www.anthropic.com/engineering/building-effective-agents>
- Anthropic — Building agents with the Claude Agent SDK: <https://claude.com/blog/building-agents-with-the-claude-agent-sdk>

> Both vendors' docs are migrating hosts (OpenAI Codex → `learn.chatgpt.com`; Anthropic → `code.claude.com` /
> `claude.com/blog`) and are version-dependent. Treat specific numbers (e.g. Codex's 32 KiB cap, Claude's
> 200-line target) as current-as-of-writing, and re-check before relying on them.
