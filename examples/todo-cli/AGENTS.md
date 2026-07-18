# AGENTS.md

## Project overview

`todo` — a single-binary task manager CLI written in **Go**. Cobra for commands; tasks persisted as JSON
under `~/.todo/`. No network, no server, no UI.

## Setup

```bash
go mod download
go build -o bin/todo ./cmd/todo
./bin/todo --help
```

## Build, test, and lint

Run the checks relevant to files you changed before considering a task done.

```bash
go build ./...
go test ./...                 # full suite
go test -race ./internal/...  # core packages, race detector on
golangci-lint run             # lint (falls back to: go vet ./...)
```

## How to work

> Not project-specific — the default working style, kept as-is from the AI_ONBOARD template.

- **Understand before you change.** Read the relevant code first; if unsure, open the file — don't guess.
- **Plan when it's non-trivial.** One-sentence diff → just do it; otherwise outline steps first.
- **Be persistent within scope.** Finish and verify before handing back, but check in first before expanding
  scope or doing anything irreversible (rewriting the saved-tasks format, deleting a user's `~/.todo`).
- **Verify, then claim.** Run the checks above and show the command + output; don't assert success.
- **Fix causes, not symptoms.** Don't suppress an error or weaken a check to make it pass.
- **Match the surroundings.** Follow the conventions below and nearby code.
- **Delegate deliberately.** Subagent only for isolation, parallelism, or an independent lens. Layer rules
  live in the nearest `AGENTS.md`.
- **Report honestly.** Say plainly if tests fail, a step was skipped, or you got blocked.

## Project structure

- `cmd/todo/` — CLI entrypoint + Cobra commands. Has its own `AGENTS.md` (command-layer profile).
- `internal/task/` — task domain model + business logic (no I/O). Has its own `AGENTS.md` (core-layer profile).
- `internal/store/` — JSON persistence; the only package that touches the filesystem.

## Conventions

- **Go style:** `gofmt` (CI enforces — run it). Errors wrapped with `fmt.Errorf("...: %w", err)`, never
  swallowed.
- **Layering:** commands stay thin; business logic lives in `internal/`. Dependencies point one way
  (`cmd/` → `internal/`, never back).
- No new dependencies without discussion.

## Security & safety

- **Never log secrets.** (This tool has none by design — keep it that way.)
- Treat file paths from flags/args as **untrusted**: constrain them to the todo directory, never let `..`
  escape it, and never shell out with them.
