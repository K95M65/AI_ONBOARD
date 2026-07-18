# AGENTS.md — cmd/ (command layer profile)

> Nearest-file-wins: applies to work under `cmd/`. Only what *differs* from the root file lives here.

## Layer profile: cli-commands

- **Model:** prefer a fast model — command wiring and help text are low-ambiguity.
- **Rules:** commands stay **thin** — parse flags, delegate to `internal/`, format output. No business logic
  and no file I/O here. Every command has `--help` text and a usage example.
- **Checks:** `go test ./cmd/...`, and run the built binary on the happy path plus one error path.

## Structure (this layer)

- `cmd/todo/main.go` — entrypoint; wires the root command and owns the process exit code.
- `cmd/todo/*.go` — one file per subcommand (`add`, `list`, `done`, `rm`).

## Don't

- ⛔ Don't put storage or task logic here — it belongs in `internal/`.
- ⛔ Don't call `os.Exit()` deep inside a command; return an error and let `main` set the exit code.
