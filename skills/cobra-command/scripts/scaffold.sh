#!/usr/bin/env bash
# scaffold.sh — create a new Cobra subcommand (command + table-driven test) from templates/.
# Self-locating: resolves templates relative to this script. Portable to bash 3.2 (macOS).
#
# Usage: bash scaffold.sh <command-name> [target-dir]
set -euo pipefail

usage() { echo "Usage: bash scaffold.sh <command-name> [target-dir]" >&2; exit 2; }
[ "$#" -ge 1 ] || usage

NAME="$1"
DIR="${2:-.}"

# Command names are lowercase (letters, digits, hyphen).
if ! printf '%s' "$NAME" | grep -qE '^[a-z][a-z0-9-]*$'; then
  echo "Command name must be lowercase (e.g. add, list, my-cmd). Got: '$NAME'" >&2
  exit 1
fi

# Capitalize the first letter for the Go identifier (bash-3.2-safe, no ${x^}).
CAP="$(printf '%s' "$NAME" | awk '{print toupper(substr($0,1,1)) substr($0,2)}' | tr -d '-')"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TPL="$SCRIPT_DIR/../templates"
GO="$DIR/$NAME.go"
TEST="$DIR/${NAME}_test.go"

for f in "$GO" "$TEST"; do
  [ -e "$f" ] && { echo "Refusing to overwrite existing $f" >&2; exit 1; }
done

render() { sed -e "s/__NAME__/$NAME/g" -e "s/__CAP__/$CAP/g" "$1"; }
mkdir -p "$DIR"
render "$TPL/command.go.tmpl"      > "$GO"
render "$TPL/command_test.go.tmpl" > "$TEST"

echo "Created:"
echo "  $GO"
echo "  $TEST"
echo "Register it on the root command: root.AddCommand(new${CAP}Cmd())"
