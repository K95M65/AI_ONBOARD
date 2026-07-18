# AGENTS.md — internal/ (core layer profile)

> Nearest-file-wins: applies to work under `internal/`. Only what *differs* from the root file lives here.

## Layer profile: core

- **Model:** prefer a strong model — this is the business logic and the data integrity.
- **Rules:** pure, testable functions; don't print to stdout (return values/errors, let `cmd/` format).
  Validate and constrain any filesystem path to the todo directory — never let it escape. Every exported
  function gets a table-driven test.
- **Checks:** `go test -race ./internal/...`.

## Structure (this layer)

- `internal/task/` — domain model + business logic. No I/O.
- `internal/store/` — JSON load/save; the only package that touches the filesystem.

## Don't

- ⛔ Don't import `cmd/` from `internal/` — the dependency points one way.
- ⛔ Don't build a file path from user input without constraining it to the todo dir (path traversal).
- ⛔ Don't change the on-disk JSON shape without a migration path — it corrupts existing `~/.todo` files.
