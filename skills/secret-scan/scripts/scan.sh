#!/usr/bin/env bash
# scan.sh — scan for committed secrets. Prefers gitleaks (tree + history), then trufflehog,
# then a best-effort grep over the working tree (history NOT covered).
#
# Usage: bash scan.sh [path]   (defaults to .)
set -uo pipefail

ROOT="${1:-.}"
cd "$ROOT" 2>/dev/null || { echo "No such path: $ROOT" >&2; exit 1; }
have() { command -v "$1" >/dev/null 2>&1; }

if have gitleaks; then
  echo "### gitleaks (tree + history)"
  gitleaks detect --no-banner --redact || true
  exit 0
fi

if have trufflehog; then
  echo "### trufflehog (filesystem)"
  trufflehog filesystem "$PWD" --results=verified,unknown || true
  exit 0
fi

echo "### grep fallback — TREE ONLY (history not covered)"
echo "  Install gitleaks for history coverage: https://github.com/gitleaks/gitleaks"
echo
pats='(api[_-]?key|secret|passwd|password|token|client[_-]?secret)[[:space:]]*[:=]|AKIA[0-9A-Z]{16}|BEGIN[[:space:]]+(RSA|EC|OPENSSH|DSA)?[[:space:]]*PRIVATE KEY|ghp_[0-9A-Za-z]{36}|xox[baprs]-[0-9A-Za-z-]+'
if grep -rHInEi --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=vendor -e "$pats" "$PWD" 2>/dev/null; then
  echo
  echo "Confirm each hit in context — placeholders and test fixtures are common false positives."
else
  echo "  (no matches in the working tree — NOT an all-clear; history is uncovered here)"
fi
