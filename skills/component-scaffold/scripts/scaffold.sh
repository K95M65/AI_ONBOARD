#!/usr/bin/env bash
# scaffold.sh — create a new React/TS component folder (component + test + index) from templates/.
# Self-locating: resolves templates relative to this script, so it runs the same under any harness.
#
# Usage: bash scaffold.sh <ComponentName> [target-dir]
set -euo pipefail

usage() { echo "Usage: bash scaffold.sh <ComponentName> [target-dir]" >&2; exit 2; }
[ "$#" -ge 1 ] || usage

NAME="$1"
DIR="${2:-components}"

# PascalCase only — this becomes a type and a component identifier.
if ! printf '%s' "$NAME" | grep -qE '^[A-Z][A-Za-z0-9]*$'; then
  echo "Component name must be PascalCase (e.g. UserCard). Got: '$NAME'" >&2
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TPL="$SCRIPT_DIR/../templates"
DEST="$DIR/$NAME"

if [ -e "$DEST" ]; then
  echo "Refusing to overwrite existing $DEST" >&2
  exit 1
fi

mkdir -p "$DEST"
render() { sed "s/__NAME__/$NAME/g" "$1"; }
render "$TPL/Component.tsx.tmpl"      > "$DEST/$NAME.tsx"
render "$TPL/Component.test.tsx.tmpl" > "$DEST/$NAME.test.tsx"
render "$TPL/index.ts.tmpl"           > "$DEST/index.ts"

echo "Created:"
echo "  $DEST/$NAME.tsx"
echo "  $DEST/$NAME.test.tsx"
echo "  $DEST/index.ts"
