---
name: gh-issue
description: Create, triage, and manage GitHub issues with the gh CLI. Use when filing a bug or feature issue, triaging the backlog, or linking issues to PRs.
---

# GitHub issues

## Create

```bash
gh issue create --title "<title>" --body-file ISSUE.md --label bug
```

A good issue states: **what happened vs. expected**, **repro steps**, **environment**, and the **scope** of
impact. Use the repo's `.github/ISSUE_TEMPLATE` if one exists.

## Triage

```bash
gh issue list --state open --label bug        # scan
gh issue view <n>                             # read
gh issue edit <n> --add-label triaged --assignee @me
gh issue close <n> --reason completed         # or not_planned
```

## Link to work

- Reference in a PR body as `Closes #<n>` / `Fixes #<n>` so merging auto-closes it.
- Cross-link related issues with `#<n>` mentions.

## Notes

- Prefer labels + milestones over ad-hoc conventions so triage is queryable.
- Keep one problem per issue; split omnibus issues so they can be closed independently.
