#!/usr/bin/env bash
# new-migration.sh — safely create + apply a Prisma migration.
# Guards against running against a non-local database (staging/prod) by inspecting DATABASE_URL.
#
# Usage: bash new-migration.sh <migration-name> [--force]
set -euo pipefail

FORCE=0
NAME=""
for a in "$@"; do
  case "$a" in
    --force) FORCE=1 ;;
    -h|--help) echo "Usage: bash new-migration.sh <migration-name> [--force]"; exit 0 ;;
    -*) echo "Unknown option: $a" >&2; exit 2 ;;
    *) NAME="$a" ;;
  esac
done
[ -n "$NAME" ] || { echo "Usage: bash new-migration.sh <migration-name> [--force]" >&2; exit 2; }

# Resolve DATABASE_URL from the environment, falling back to a local .env file.
URL="${DATABASE_URL:-}"
if [ -z "$URL" ] && [ -f .env ]; then
  URL="$(grep -E '^DATABASE_URL=' .env | tail -1 | sed -E 's/^DATABASE_URL=//; s/^"//; s/"$//')"
fi
if [ -z "$URL" ]; then
  echo "DATABASE_URL is not set (checked env and .env). Aborting." >&2
  exit 1
fi

# Extract the host from scheme://[user[:pass]@]host[:port]/db
host="$(printf '%s' "$URL" | sed -E 's#^[a-zA-Z0-9+.-]+://([^/@]*@)?([^:/?]+).*#\2#')"
case "$host" in
  localhost|127.0.0.1|::1|0.0.0.0) local_db=1 ;;
  *) local_db=0 ;;
esac

if [ "$local_db" -eq 0 ] && [ "$FORCE" -eq 0 ]; then
  echo "DATABASE_URL host '$host' does not look local." >&2
  echo "Refusing to migrate a possibly shared/production database." >&2
  echo "If you are certain, re-run with --force." >&2
  exit 1
fi

echo "Creating migration '$NAME' against host '$host'..."
npx prisma migrate dev --name "$NAME"
