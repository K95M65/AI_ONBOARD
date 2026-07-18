# AGENTS.md

## Project

[What this project is, who it serves, and its primary stack.]

## Setup

```bash
[Exact fresh-clone setup command]
[Exact local development command]
```

## Required checks

Run the checks relevant to changed files before finishing.

```bash
[Fast targeted test command]
[Full test command]
[Build or typecheck command]
[Lint and format check]
```

## Structure

- `[path/]` — [what belongs here]
- `[path/]` — [what belongs here]
- `[path/]` — [what belongs here]

## Conventions

- [Language, formatting, and naming rules that differ from tool defaults.]
- [Where tests live and how new behavior should be covered.]
- [Imports, architecture, or generated-file boundaries.]

## Working boundaries

- Understand the relevant implementation before editing it.
- Preserve unrelated user changes and match surrounding conventions.
- Verify behavior with the project commands above before claiming completion.
- Never commit secrets, credentials, `.env` files, or private generated data.
- Ask before deployments, releases, destructive operations, or meaningful scope expansion.

## Harness-specific notes

Keep provider, model, credentials, approval mode, and personal UI preferences out of this shared file.
Put those in the relevant Claude Code, Codex, or OpenCode configuration layer.
