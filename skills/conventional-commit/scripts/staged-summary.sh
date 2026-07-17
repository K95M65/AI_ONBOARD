#!/usr/bin/env bash
# staged-summary.sh — summarize staged git changes for drafting a commit message.
# Prints: branch, staged file list with status, diffstat, and the staged diff (truncated).
set -euo pipefail

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Not inside a git repository." >&2
  exit 1
fi

if git diff --cached --quiet; then
  echo "No staged changes. Stage files with 'git add <paths>' first."
  exit 0
fi

echo "=== Branch ==="
git rev-parse --abbrev-ref HEAD

echo
echo "=== Staged files (status) ==="
git diff --cached --name-status

echo
echo "=== Diffstat ==="
git diff --cached --stat

echo
echo "=== Staged diff (first 400 lines) ==="
git diff --cached | head -n 400
