# Layout, context, and density

Choose structure from the work and platform rather than defaulting to a dashboard grid.

## Choose a layout paradigm

Match the dominant relationship:

| Work | Likely paradigm |
|---|---|
| Scan and compare records | Table or list |
| Move work through states | Board or staged workflow |
| Edit one object with context | Master-detail or inspector |
| Arrange spatial relationships | Canvas, map, or diagram |
| Follow ordered events | Timeline or activity stream |
| Monitor a bounded set of signals | Dashboard |
| Browse visual items | Gallery |
| Concentrate on one artifact | Editor or single-focus workspace |

Combine paradigms only when each supports a distinct user task. Reuse the same page or window skeleton for
equivalent workflows so users can transfer their mental model.

## Establish information architecture

- Name navigation and objects with user vocabulary.
- Make the current location, active object, workspace, account, environment, and selection clear.
- Use hierarchy only where the domain has hierarchy; do not invent nesting to organize navigation.
- Keep global controls separate from controls that affect only a view, selection, or object.
- Preserve stable object identity across search, lists, detail views, notifications, and history.
- Give deep structures a clear back path, breadcrumb, outline, sidebar, or equivalent platform convention.

## Communicate action scope

Before an action, show what it affects:

- Name the active workspace, record, environment, account, or customer.
- Bound the editable region when changes apply only within it.
- State the count and type of selected objects for bulk actions.
- Make cross-account administration or impersonation persistent and unmistakable, with a visible exit.
- Distinguish development, staging, production, internal, and customer-facing surfaces with persistent cues.
- Put the affected object and consequences in destructive confirmations.

Do not rely on color alone for scope or environment distinctions.

## Match density to work

Set density from:

- expertise and task frequency;
- display size and viewing distance;
- comparison and scanning needs;
- pointer, touch, keyboard, and assistive input;
- duration of use;
- consequence of selection errors.

Occasional users need guidance and progressive disclosure. Trained daily users often need compact rows,
stable positions, keyboard access, batch operations, persistent filters, and at-a-glance status. Do not
force consumer-style whitespace onto operational tools or dense desktop layouts onto touch targets.

Provide density modes only when distinct user groups or environments genuinely need them. Preserve content
hierarchy and hit-target safety in every mode.

## Design expert workflows

For operational or domain-expert tools:

- prioritize throughput, accuracy, continuity, and scanability;
- preserve state and selection across repeated operations;
- support keyboard traversal and commands for frequent work;
- keep primary signals visible without opening details;
- allow safe batch action and review;
- show system status, freshness, conflicts, and ownership;
- support interruption, handoff, and resume;
- avoid hiding frequent actions behind decorative menus.

For complex configuration:

- group parameters by domain concept, not implementation module or alphabet;
- use domain-language labels and include units;
- provide visible defaults and reset behavior;
- separate saved defaults from one-time session overrides;
- disclose advanced controls without burying frequently used settings;
- explain conflicts and dependencies beside the affected controls;
- validate in domain terms before submission.

## Handle responsive and adaptive layout

Adapt the interaction model, not merely dimensions:

- reprioritize content and commands for smaller spaces;
- replace simultaneous panes with drill-in navigation or view switching where necessary;
- preserve selection and context when a pane collapses;
- move commands to platform-expected locations;
- avoid nested two-axis scrolling;
- set useful minimum sizes for windows, panes, inspectors, and content.

## Gate

Proceed when a user can identify where they are, what is selected, what actions affect, and how to complete
the primary workflow at every supported size and input mode.
