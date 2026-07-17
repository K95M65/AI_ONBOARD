# Cursor setup

Cursor reads `AGENTS.md` natively, so your shared [`AGENTS.md`](../../AGENTS.md) already provides project
context. Cursor's *own* rules system (`.cursor/rules/`) is for something `AGENTS.md` can't do: **scoped
rules that attach only to matching files.** Use both — `AGENTS.md` for the always-on project brief,
`.cursor/rules/` for glob-targeted specifics.

## Wiring

Nothing required — Cursor picks up `AGENTS.md`. (The old `.cursorrules` single-file format is deprecated;
prefer `AGENTS.md` + `.cursor/rules/`.)

## Power features (`.cursor/rules/*.mdc`)

Each rule is an `.mdc` file with frontmatter that decides **when** it loads:

```
.cursor/
└── rules/
    ├── always.mdc
    ├── api-conventions.mdc
    └── react-components.mdc
```

```markdown
---
description: Conventions for the REST API layer
globs: ["packages/api/**/*.ts"]
alwaysApply: false
---
- All handlers return `Result<T, ApiError>`, never throw across the boundary.
- Validate input with the Zod schemas in `packages/api/schemas`.
```

### The four rule types

| Type | Frontmatter | Loads when… |
|------|-------------|-------------|
| **Always** | `alwaysApply: true` | Every request (like `AGENTS.md`) |
| **Auto Attached** | `globs: [...]`, `alwaysApply: false` | An edited/referenced file matches a glob |
| **Agent Requested** | `description:` set, no globs | The agent decides it's relevant from the description |
| **Manual** | none of the above | You `@`-mention the rule explicitly |

**Rule of thumb:** keep truly global rules in `AGENTS.md`; use **Auto Attached** rules for
directory/framework-specific guidance so it only costs context when relevant. This mirrors nested
`AGENTS.md` files but with glob precision.

### `.cursorignore`

Exclude files from indexing/context (secrets, generated code, huge fixtures):

```
.env*
dist/
**/*.generated.ts
```

## Recommended baseline

```bash
mkdir -p .cursor/rules
# AGENTS.md already covers the global brief. Add scoped rules as the codebase grows.
```

> Cursor's rules format has evolved (`.cursorrules` → `.cursor/rules/*.mdc`). Verify against current Cursor
> docs if frontmatter keys differ.
