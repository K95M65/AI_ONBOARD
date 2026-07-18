# AI-powered product experiences

Design generative and agentic behavior as a variable, inspectable system rather than a magical text box.

## Define the role and autonomy

- State the user outcome, the AI's bounded job, and what remains the user's responsibility.
- Choose an autonomy level: suggest, draft, transform, execute with preview, execute with confirmation, or
  act within explicit standing authority.
- Make data access, tools, side effects, costs, latency, and escalation paths visible at the decision point.
- Preserve a non-AI or manual path for high-stakes work when feasible.

Do not imply certainty, completion, or authority the system does not have.

## Make work legible

Show progress at the level useful for intervention: queued, gathering context, using a tool, waiting for
permission, producing output, partially completed, blocked, or failed. Let users cancel long-running work
and understand what cancellation preserves.

For consequential outputs:

- distinguish source material, model inference, and user-provided facts;
- expose citations or evidence where the product can support them;
- preview intended external actions, affected objects, recipients, or costs;
- show partial success and failed steps rather than collapsing them into one status;
- retain an audit trail and reversal path proportional to impact.

## Support correction

Design for edit, retry, regenerate, compare, constrain, provide feedback, and resume. Preserve useful user
changes across regeneration. Let users correct the source context or instruction, not only rate the output.

When the model lacks required information, prefer a focused request, bounded alternative, or explicit
uncertainty over fabricated completion. Distinguish a model limitation from a permissions, tool, network,
policy, or data-quality failure.

## Evaluate the experience

Define representative tasks, expected qualities, unacceptable failures, and human review criteria. Test
variation, adversarial or ambiguous inputs, partial context, tool failure, latency, and recovery. Measure
task outcome and correction burden, not only response preference.

Use `measure-product-experiments` for event and experiment design. Add security review when prompts,
retrieval, tools, external actions, sensitive data, tenancy, or delegated authority are involved.
