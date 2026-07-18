# Product strategy and workflows

Define what work the product enables before choosing screens or controls.

## Build the product brief

Capture:

1. **Primary users:** Name their role, expertise, authority, and relevant accessibility needs.
2. **Environment:** Record where, when, and under what interruptions, connectivity, lighting, mobility, or
   device constraints the work happens.
3. **Jobs and outcomes:** Complete, "When ___, this user needs to ___, so they can ___."
4. **Frequency and duration:** Distinguish first-use, occasional, repeated, and all-day expert work.
5. **Stakes:** State the cost of delay, confusion, accidental action, data loss, or incorrect output.
6. **Domain objects:** Name the entities users recognize, their relationships, lifecycle, and ownership.
7. **Permissions and scope:** Identify who may view, create, change, approve, export, or delete each object.
8. **Success measures:** Prefer task completion, accuracy, recovery, time-to-value, retention, or reduced
   support burden over screen-level engagement.
9. **Platforms:** List operating systems, form factors, input methods, windowing, offline behavior, and
   distribution channels.
10. **Constraints and non-goals:** Record technical, regulatory, brand, schedule, compatibility, and migration
    limits.

Separate known facts, hypotheses, and open research questions.

## Map real work

For each important job:

1. Identify the trigger and required context.
2. List the user's current steps, decisions, inputs, collaborators, and handoffs.
3. Mark delays, repeated entry, hidden dependencies, risky decisions, and recovery points.
4. Define the smallest successful completion and what must remain visible afterward.
5. Include interruption, resume, cancellation, conflict, stale data, and partial-completion paths.

Design around user decisions rather than mirroring backend endpoints or database tables. Preserve domain
concepts that help users predict the system; hide implementation concepts that do not.

## Prioritize workflows

Choose:

- one primary workflow that demonstrates the product's core value;
- one high-risk workflow where mistakes matter;
- one edge workflow that stresses content, permissions, or recovery;
- one onboarding or first-use path when learnability matters.

Use these as representative design and implementation slices. Do not start with a dashboard if it is only a
summary of work that has not yet been designed.

## Define the command model

Inventory actions and classify them:

- global application commands;
- navigation and view commands;
- object-level commands;
- selection-level bulk commands;
- transient editing commands;
- destructive or privileged commands.

Decide where each command is discoverable on every target platform: menu, toolbar, contextual menu, command
palette, keyboard shortcut, touch action, or inline control. A shortcut accelerates a visible command; it
should not be the only way to discover essential behavior.

## Gate

Proceed when the primary users, platform, objects, workflows, states, permissions, and success criteria are
explicit enough to explain why each proposed surface exists.
