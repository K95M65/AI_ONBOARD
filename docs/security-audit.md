# Security audit methodology

How we run a security audit in this framework — the **standard** the [`security-audit`](../skills/security-audit/)
skill operationalizes. This doc is the human-facing reference: scoping, severity, and reporting. The skill is
the agent-facing procedure; the [`security-review`](../agents/security-review.md) subagent is the delivery
vehicle for the *diff-sized* version.

## Two sizes, one method

| | `security-review` subagent | `security-audit` skill |
|---|---|---|
| **Scope** | one change (a diff) | a whole codebase, service, or feature |
| **Delivery** | delegated, independent lens (grader ≠ author) | the driver or the subagent runs the methodology inline |
| **Same** | threat-model → categories → confirm → severity-ranked report | ← identical |

They share this doc's rubric and report format. The subagent *invokes* the skill's checklist for anything
bigger than a trivial diff. (See [`mechanisms.md`](mechanisms.md) for why one's a subagent and one's a skill.)

## Scoping: own code vs external code

- **Your own pre-release code** — you have `AGENTS.md`, tests, and architectural context. Lean on them; focus
  on what changed since the last audit and on the highest-value assets.
- **Unfamiliar external / client code** — assume nothing. Spend the first pass purely on **orientation**
  (surface-scan + reading entry points) before judging anything. Timebox orientation so you don't rabbit-hole.

The skill is written codebase-agnostic so it serves both; the only difference is how much context you start
with.

## Severity rubric

**Severity = impact × exploitability.** Rate, don't guess:

| Severity | Meaning |
|----------|---------|
| **Critical** | Trivially exploitable + severe impact (RCE, auth bypass, mass data exposure, secret leak to attacker). Fix before ship. |
| **High** | Real exploit path to significant impact, but needs some condition (auth'd user, specific input). |
| **Medium** | Exploitable but limited impact, or significant impact behind a hard precondition. |
| **Low** | Weakness with minor impact or requiring implausible conditions; defense-in-depth. |
| **Info** | Not exploitable now; hygiene/hardening worth noting. |

Down-rate anything you **could not trace** to a concrete path — an unconfirmed suspicion is at most a
Medium labeled "unconfirmed", never a Critical.

## Report format

One finding per issue, **highest severity first**:

```markdown
### [SEVERITY] Short title
- **Location:** path/to/file.ext:LINE (and related sites)
- **Category:** authz | injection | secrets | crypto | …
- **Exploit scenario:** concrete steps — who does what, and the outcome.
- **Confidence:** confirmed (traced) | plausible (needs confirmation)
- **Fix:** the specific change that closes it.
```

End with a one-paragraph summary: counts by severity, the single most important thing to fix, and what was
**out of scope / not reviewed** (never let silence imply "everything else is clean").

## Rules of engagement

- **Read and report only.** Never run a found exploit against a live system, never exfiltrate data.
- **Confirmed over comprehensive.** A traced Critical is worth more than a long list of maybes.
- **State coverage honestly.** What you didn't look at is part of the report.
- Worked example of the output: [`../examples/notes-app/SECURITY-AUDIT.md`](../examples/notes-app/SECURITY-AUDIT.md).
