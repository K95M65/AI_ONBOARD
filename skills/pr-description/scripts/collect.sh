#!/usr/bin/env bash
# collect.sh — gather the raw material for a PR description: commits + changed-file stat for base..HEAD.
#
# Usage: bash collect.sh [base]   (defaults to origin/main, then main)
set -uo pipefail

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Not a git repository." >&2; exit 1
fi

BASE="${1:-origin/main}"
if ! git rev-parse --verify --quiet "$BASE" >/dev/null; then
  if git rev-parse --verify --quiet main >/dev/null; then BASE="main"
  elif git rev-parse --verify --quiet master >/dev/null; then BASE="master"
  else echo "Could not resolve a base branch (tried $1/origin/main/main/master)." >&2; exit 1; fi
fi

echo "Base: $BASE   Head: $(git rev-parse --abbrev-ref HEAD)"
echo
echo "### Commits ($BASE..HEAD)"
git log --pretty='- %s' "$BASE..HEAD" || echo "  (none)"
echo
echo "### Files changed"
git diff --stat "$BASE...HEAD" || echo "  (none)"
