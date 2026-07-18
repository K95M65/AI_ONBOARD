---
name: component-scaffold
description: Scaffolds a new React/TypeScript UI component (component + test + index) from a consistent template. Use when creating a new frontend component and you want the standard file layout without hand-copying boilerplate.
---

# Component scaffold

## When to use

Creating a new UI component. Skip it for one-off inline elements — this is for components that get their own
folder, test, and export.

## Steps

1. Run the scaffold script:
   ```bash
   bash scripts/scaffold.sh <ComponentName> [target-dir]
   ```
   - `<ComponentName>` must be **PascalCase** (e.g. `UserCard`).
   - `target-dir` defaults to `components`.
2. It creates `<target-dir>/<ComponentName>/` with `<ComponentName>.tsx`, `<ComponentName>.test.tsx`, and
   `index.ts`.
3. Fill in the props interface and the render body. Use the project's **design tokens** — no hard-coded hex,
   spacing, or font sizes.
4. Run the frontend tests to confirm it compiles and the placeholder test passes.

## Notes

- Refuses to overwrite an existing component directory.
- Templates live in [`templates/`](templates/). Adapt them to your stack once (styling approach, test
  library) and every future scaffold follows suit.
