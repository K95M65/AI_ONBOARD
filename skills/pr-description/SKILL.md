---
name: pr-description
description: Write a clear pull-request description from the branch's commits and diff. Use when opening a PR or when asked to summarize a branch's changes for review.
---

# PR description

## When to use

Opening a PR, or summarizing a branch's changes for reviewers.

## Steps

1. Gather the raw material: `bash scripts/collect.sh [base]` (base defaults to `origin/main`, falling back to
   `main`). It prints the commit subjects and the changed-file stat for `base..HEAD`.
2. Write the description from that material using the template below — **explain the why**, not just the what;
   the diff already shows the what.
3. Keep it honest: call out risk, follow-ups, and anything not covered by tests.

## Template

```markdown
## Summary
<1–3 sentences: what this PR does and why.>

## Changes
- <the notable changes, grouped; not a commit dump>

## Testing
- <what you ran / added, and the result>

## Risk & follow-ups
- <blast radius, migrations, anything deferred>
```

## Notes

- Lead with the problem being solved, not the implementation.
- If the branch does several unrelated things, that's a signal to split the PR, not to write a longer summary.
