#!/usr/bin/env bash
# collect.sh — group Conventional Commits by type for a changelog entry.
#
# Usage: bash collect.sh [from-ref]   (defaults to the most recent tag; else full history)
set -uo pipefail

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Not a git repository." >&2; exit 1
fi

FROM="${1:-}"
if [ -z "$FROM" ]; then
  FROM="$(git describe --tags --abbrev=0 2>/dev/null || true)"
fi
if [ -n "$FROM" ] && git rev-parse --verify --quiet "$FROM" >/dev/null; then
  RANGE="$FROM..HEAD"; label="$FROM..HEAD"
else
  RANGE="HEAD"; label="full history (no tag found)"
fi

echo "Changes in $label:"

# Breaking changes: subject with '!' before ':' or a BREAKING CHANGE footer.
breaking="$(git log --pretty='%s' "$RANGE" 2>/dev/null | grep -E '^[a-z]+(\(.+\))?!:' || true)"
if [ -n "$breaking" ]; then
  echo
  echo "## ⚠ Breaking"
  printf '%s\n' "$breaking" | sed -E 's/^[a-z]+(\(.+\))?!:[[:space:]]*/- /'
fi

for type in feat fix perf refactor deprecate remove docs test build ci chore; do
  matches="$(git log --pretty='%s' "$RANGE" 2>/dev/null | grep -E "^${type}(\(.+\))?!?:" || true)"
  if [ -n "$matches" ]; then
    echo
    echo "## $type"
    printf '%s\n' "$matches" | sed -E "s/^${type}(\(.+\))?!?:[[:space:]]*/- /"
  fi
done
