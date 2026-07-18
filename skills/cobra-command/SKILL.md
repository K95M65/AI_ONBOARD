---
name: cobra-command
description: Scaffolds a new Cobra subcommand (command file + table-driven test) for a Go CLI. Use when adding a subcommand to a Cobra-based CLI and you want the standard thin-command layout without hand-copying boilerplate.
---

# Cobra command scaffold

The Go-CLI counterpart to `component-scaffold`. Generates a thin command that delegates to `internal/`.

## When to use

Adding a new subcommand to a Cobra-based Go CLI.

## Steps

1. Run the scaffold script from the package where commands live (e.g. `cmd/todo/`):
   ```bash
   bash scripts/scaffold.sh <command-name> [target-dir]
   ```
   - `<command-name>` is the CLI verb, **lowercase** (e.g. `add`, `list`).
   - `target-dir` defaults to `.` (the current directory).
2. It creates `<name>.go` (a `new<Name>Cmd()` constructor) and `<name>_test.go` (a table-driven test stub).
3. Register the command on the root: `root.AddCommand(new<Name>Cmd())`.
4. Fill in flags and `RunE`. Keep the command **thin** — parse flags, delegate to `internal/`, format output;
   no business logic here.
5. Run `go test ./...` and exercise the built binary.

## Notes

- Refuses to overwrite existing files.
- Templates live in [`templates/`](templates/) — adapt the package name or error style to your CLI once.
