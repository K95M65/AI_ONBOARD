#!/usr/bin/env bash
# new-note.sh — create an Obsidian note with YAML frontmatter (title/date/tags).
# Keeps spaces in the filename so [[Title]] wikilinks resolve. Refuses to overwrite.
#
# Usage: bash new-note.sh "<Title>" [folder] [tag ...]
set -euo pipefail

[ "$#" -ge 1 ] || { echo 'Usage: bash new-note.sh "<Title>" [folder] [tag ...]' >&2; exit 2; }
TITLE="$1"; shift

# Optional folder = first remaining arg that isn't a tag (tags start with #, or just treat first as folder).
FOLDER="."
if [ "$#" -ge 1 ] && [ "${1#\#}" = "$1" ]; then FOLDER="$1"; shift; fi

DATE="$(date +%F)"
# Sanitize only path-illegal characters; keep spaces (Obsidian filenames allow them).
SLUG="$(printf '%s' "$TITLE" | tr '\/:' '---')"
DEST="$FOLDER/$SLUG.md"

mkdir -p "$FOLDER"
[ -e "$DEST" ] && { echo "Refusing to overwrite $DEST" >&2; exit 1; }

yaml_quote() {
  local value="$1"
  value="${value//\\/\\\\}"
  value="${value//\"/\\\"}"
  value="${value//$'\n'/\\n}"
  value="${value//$'\r'/\\r}"
  value="${value//$'\t'/\\t}"
  printf '"%s"' "$value"
}

{
  echo "---"
  printf 'title: '; yaml_quote "$TITLE"; echo
  printf 'date: '; yaml_quote "$DATE"; echo
  if [ "$#" -ge 1 ]; then
    echo "tags:"
    for t in "$@"; do
      printf '  - '; yaml_quote "${t#\#}"; echo
    done
  fi
  echo "---"
  echo
  echo "# $TITLE"
  echo
} > "$DEST"

echo "Created $DEST"
