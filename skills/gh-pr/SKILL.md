---
name: gh-pr
description: Create or update a GitHub pull request with the gh CLI. Use when opening a PR from the current branch or updating an existing one. Pairs with the pr-description skill for the body.
---

# GitHub PR

## When to use

Opening or updating a pull request from the command line.

## Steps

1. Push the branch: `git push -u origin HEAD`.
2. Write the body with the `pr-description` skill (save it to `PR.md`).
3. Create the PR:
   ```bash
   gh pr create --base main --title "<title>" --body-file PR.md
   ```
   - Draft: add `--draft`. Request review: `--reviewer <user>`. Self-assign: `--assignee @me`.
   - Fill fields interactively instead: `gh pr create --web`.
4. Update an existing PR: `gh pr edit --title <t> --body-file PR.md`, or just push more commits — the PR
   tracks the branch.
5. Check status: `gh pr checks` (CI) and `gh pr view --web`.

## Notes

- One logical change per PR — if the diff spans unrelated work, split it.
- Don't force-push a shared PR branch without coordinating with reviewers.
- Put `Closes #<n>` in the body to auto-close the linked issue on merge.
