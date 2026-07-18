---
name: agents-md-init
description: Bootstraps an AGENTS.md file for a project by detecting its stack, package manager, and build/test/lint commands. Use when a repo has no AGENTS.md (or CLAUDE.md) yet and the user wants to onboard AI tools, or asks to create/generate agent instructions for the project.
---

# AGENTS.md init

Create a first-draft [`AGENTS.md`](https://agents.md) grounded in what the repository actually contains,
not in guesses.

## When to use

A project has no `AGENTS.md` yet and the user wants to set up AI-tool onboarding, or asks you to "generate
an AGENTS.md / agent instructions" for the repo.

## Steps

1. **Detect the stack and commands** — run the detector instead of assuming:

   ```bash
   bash scripts/detect-stack.sh
   ```

   It reports the language/ecosystem, package manager, and the real `build` / `test` / `lint` scripts it
   finds in manifests (`package.json`, `pyproject.toml`, `Makefile`, `go.mod`, `Cargo.toml`, etc.).
   For Apple projects it also reports Xcode projects/workspaces, SwiftPM, Tuist, Swift version files,
   shared schemes, and formatter/linter configuration.

2. **Skim the structure** — list top-level dirs and note what each holds (`src/`, `tests/`, `packages/`…).
   Read the existing `README.md` for setup steps and conventions already documented.

3. **Draft `AGENTS.md`** from the template in this repo's [`../../AGENTS.md`](../../AGENTS.md), filling in:
   - Overview (stack, what it is) — 1–2 sentences.
   - Setup, build, test, lint — use the **exact commands the detector found**.
   - Structure — the real directories.
   - Conventions — only ones you can verify (formatter config present, lint rules, naming actually used).
   - For Swift/Apple projects — the project system, shared schemes, supported platforms and deployment
     targets, Swift language/concurrency settings, exact destinations used by CI, generated-project
     ownership, and distribution/signing references. Never copy signing identities or credential values.

4. **Only claim what's true.** If you can't confirm a convention from config or code, leave it out rather
   than inventing it. A wrong `AGENTS.md` misleads every agent that reads it.

5. **Keep it short.** It's loaded every session. Cut anything the code already makes obvious.

6. **Offer to wire up tools** — mention that `CLAUDE.md` can `@AGENTS.md`, `GEMINI.md` can symlink to it,
   and Codex/opencode/Cursor read it natively. (See the tool matrix / `link.sh` in AI_ONBOARD.)

## Rules

- Prefer editing an existing `AGENTS.md` over clobbering it — merge, don't overwrite.
- Don't include secrets, tokens, or environment-specific paths.
- Commands must be copy-paste runnable; verify names against the manifest, don't paraphrase.
