#!/usr/bin/env bash
# scan.sh — detect the project's ecosystem and run the matching dependency vulnerability scanner.
# Degrades gracefully: if a scanner isn't installed, print how to get it and continue.
#
# Usage: bash scan.sh [path]   (defaults to .)
set -uo pipefail

ROOT="${1:-.}"
cd "$ROOT" 2>/dev/null || { echo "No such path: $ROOT" >&2; exit 1; }
have() { command -v "$1" >/dev/null 2>&1; }
ran=0

if [ -f package.json ]; then
  ran=1
  echo "### Node dependencies"
  if [ -f pnpm-lock.yaml ] && have pnpm; then pnpm audit || true
  elif [ -f yarn.lock ] && have yarn; then yarn npm audit 2>/dev/null || yarn audit || true
  elif have npm; then npm audit || true
  else echo "  npm/pnpm/yarn not found — install Node tooling to scan."; fi
  echo
fi

if [ -f go.mod ]; then
  ran=1
  echo "### Go dependencies"
  if have govulncheck; then govulncheck ./... || true
  else echo "  govulncheck not found — install: go install golang.org/x/vuln/cmd/govulncheck@latest"; fi
  echo
fi

if have osv-scanner; then
  ran=1
  echo "### osv-scanner (cross-ecosystem)"
  osv-scanner scan "$PWD" || true
  echo
fi

if [ "$ran" -eq 0 ]; then
  echo "No recognized manifest (package.json, go.mod) here, and osv-scanner is not installed."
  echo "Install osv-scanner for broad coverage: https://google.github.io/osv-scanner/"
fi
