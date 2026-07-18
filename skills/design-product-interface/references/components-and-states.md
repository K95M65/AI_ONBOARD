# Components and states

Define components as behavior and content contracts, not isolated visual samples.

## Build a component family

For each reusable component, specify:

- purpose and semantic role;
- data and content inputs;
- optional-content and long-content behavior;
- variants justified by real workflows;
- rest, hover where applicable, pressed, focused, selected, disabled, loading, error, and completed states;
- keyboard, pointer, touch, assistive-technology, and automation behavior;
- platform-specific presentation or command placement;
- acceptance evidence.

Share semantic tokens for type, color, spacing, shape, border, depth, focus, and motion. Components in one
family should use the same state logic, control heights, alignment rules, and terminology unless platform
conventions require a difference.

## Treat repeated components as slot models

Cards, rows, tiles, navigation items, table cells, and KPI blocks need stable internal slots:

1. Identify anchors such as title, value, status, metadata, icon, and primary action.
2. Give equivalent slots consistent position and alignment across siblings.
3. Reserve or intentionally collapse optional slots without shifting important anchors unpredictably.
4. Clamp only when necessary and provide access to the full value.
5. Test empty, shortest, longest, localized, and high-zoom content.

Do not individually nudge repeated instances to make curated sample data align.

## Write product content

- Use the user's domain vocabulary, not internal field names.
- Name actions by the result they cause.
- Include units and formats beside values.
- Explain irreversible consequences before commitment.
- Distinguish saved, draft, queued, processing, synced, stale, failed, and completed states when those
  distinctions affect decisions.
- Keep labels consistent across menus, toolbars, buttons, shortcuts, notifications, and documentation.
- Never invent production metrics, customer data, capabilities, or successful outcomes.

## Design state and recovery

Inventory every state the workflow can enter:

| State | Answer for the user |
|---|---|
| Initial or empty | What can I do, and how do I begin? |
| Loading or processing | What is happening, can I continue, and can I cancel? |
| Partial | What succeeded, what remains, and is it safe to leave? |
| Stale or conflicting | What changed, who changed it, and how do I reconcile? |
| Offline | What remains available, what is queued, and when will it sync? |
| Permission-limited | Why is this unavailable, and who can grant access? |
| Error | What failed, what was preserved, and how do I retry or recover? |
| Success | What changed, where is it, and what is the next likely action? |

Prefer inline feedback for local problems, banners for page or window scope, and notifications for events
that outlive the initiating surface. Use transient toasts only for low-risk confirmation that does not need
later action.

Support undo when reversal is reliable. Use confirmation when the consequence is destructive, broad,
expensive, privileged, or difficult to reverse. Do not use confirmation dialogs for routine actions merely
to transfer responsibility to the user.

## Design forms and configuration

- Pair each field with a persistent label.
- Use helper text for meaning and placeholders only for examples or format.
- Match the control to the domain choice, not to storage type.
- Validate after useful input, before destructive submission, and beside the affected field.
- Preserve user input after errors.
- Put cross-field conflicts near all implicated controls and explain the resolution.
- Disable submission only when the reason is clear; otherwise allow the action and explain validation.
- Provide safe cancellation and warn before discarding meaningful unsaved work.

## Design overlays deliberately

- Use a popover for lightweight contextual choice.
- Use an inspector or side panel for persistent contextual editing.
- Use a sheet, drawer, or equivalent for a secondary flow that retains parent context.
- Use a modal dialog only when a decision must block the current workflow.
- Use a separate window when the platform and task benefit from independent placement, comparison, or
  sustained work.

Keep focus, dismissal, keyboard behavior, and restoration consistent with the target platform.

## Gate

Proceed when representative components withstand realistic content, every meaningful state has recovery,
and commands behave consistently across the selected platform inputs.
