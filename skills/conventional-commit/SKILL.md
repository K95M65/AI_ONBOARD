---
name: conventional-commit
description: Writes a Conventional Commits message from the currently staged git changes. Use when the user asks to commit, wants a commit message drafted, or asks you to figure out the right commit type/scope for staged work.
---

# Conventional Commit

Draft a well-formed [Conventional Commits](https://www.conventionalcommits.org/) message from what's
currently staged, then commit it.

## When to use

The user has staged changes (or asks you to stage them) and wants a properly formatted commit — e.g.
"commit this", "write a commit message", "what type should this commit be?".

## Steps

1. **Inspect the staged changes** — do not guess from memory:

   ```bash
   bash scripts/staged-summary.sh
   ```

   If it reports nothing staged, ask whether to `git add` the intended files first. Never `git add -A`
   without confirming scope.

2. **Choose the type** from the diff:

   | Type | Use when |
   |------|----------|
   | `feat` | A new feature / capability |
   | `fix` | A bug fix |
   | `docs` | Docs only |
   | `refactor` | Behavior-preserving code change |
   | `test` | Adding/adjusting tests |
   | `chore` | Tooling, deps, config, build |
   | `perf` | Performance improvement |
   | `ci` | CI config/scripts |

3. **Pick a scope** (optional) — the package/area touched, from the file paths (e.g. `api`, `auth`, `ui`).

4. **Write the subject** — imperative mood, lowercase, ≤ ~72 chars, no trailing period:
   `type(scope): do the thing`. Add a body only if the *why* isn't obvious. Add `BREAKING CHANGE:` footer
   (or `!` after the type) for breaking changes.

5. **Commit** — show the message first, then:

   ```bash
   git commit -m "type(scope): subject" -m "optional body"
   ```

## Rules

- Base the type/scope on the **actual diff**, not the user's phrasing.
- One logical change per commit — if the diff spans unrelated concerns, say so and suggest splitting.
- Never invent a co-author or trailer the user didn't ask for.
