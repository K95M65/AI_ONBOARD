#!/usr/bin/env bash
# gen-workflow.sh — install a starter GitHub Actions security workflow (security.yml) from templates/.
# Self-locating; refuses to overwrite an existing workflow.
#
# Usage: bash gen-workflow.sh [target-dir]   (defaults to .github/workflows)
set -euo pipefail

DIR="${1:-.github/workflows}"
DEST="$DIR/security.yml"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TPL="$SCRIPT_DIR/../templates/security.yml.tmpl"

[ -f "$TPL" ] || { echo "Template not found: $TPL" >&2; exit 1; }
[ -e "$DEST" ] && { echo "Refusing to overwrite existing $DEST" >&2; exit 1; }

mkdir -p "$DIR"
cp "$TPL" "$DEST"
echo "Created $DEST"
echo "Next: enable the jobs for your stack, then require the check in branch protection."
