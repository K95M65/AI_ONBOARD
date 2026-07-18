# Product content patterns

## Actions

Use a specific verb and object when context does not make the object unmistakable. Match the label to the
result, not the gesture: “Save report,” not “Continue,” when saving is the consequential action. Reserve
“Yes” and “No” for actual yes-or-no questions.

## Forms and validation

- Use labels for identity; use helper text for format, consequence, or why information is needed.
- State requirements before submission.
- Write an error as problem + affected field or object + recovery.
- Preserve entered values and focus the first actionable problem without hiding the rest.

## Empty and first-use states

Distinguish:

- no data exists yet;
- filters or search have no match;
- data is unavailable;
- permission prevents access;
- content was removed or expired.

Explain the condition and offer the next useful action only when one exists.

## Loading and progress

Name the operation when delay matters. Do not promise a duration the system cannot support. For long work,
explain whether users may leave, how progress persists, and where results will appear.

## Errors and interruptions

State what failed, what remains safe, and what to do next. Avoid raw implementation errors in user-facing
content. Preserve a trace or reference for support when useful without exposing secrets.

## Confirmation and destructive action

Before commitment, name the object, scope, consequence, reversibility, and any delay. Use stronger
confirmation only when risk warrants the extra friction.

## Notifications

Include enough context to understand the event away from the originating screen. Respect privacy on lock
screens, shared devices, email, and other external channels. Avoid duplicate notifications across channels.

## Help and disclosure

Put task-critical guidance in the workflow, not behind help. Use progressive disclosure for rare detail,
examples, policy, or advanced explanation. Keep help synchronized with current behavior.
