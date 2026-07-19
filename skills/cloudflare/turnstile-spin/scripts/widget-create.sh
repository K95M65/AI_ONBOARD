#!/usr/bin/env bash
# Creates a Turnstile widget via the Cloudflare API.
#
# Reads:
#   $CLOUDFLARE_API_TOKEN (required)
#
# Args:
#   --account-id <id>        Cloudflare account ID
#   --name <name>            Widget name (e.g. "myproject (Spin)")
#   --domains <a,b,c>        Comma-separated domain list (include localhost,127.0.0.1)
#   --mode <managed|invisible|non-interactive>  Default: managed
#   --secret-file <path>     New restricted file that receives the widget secret
#
# Outputs JSON to stdout. Exit 0 on success, 1 on failure. Diagnostics on stderr.
#   ok:    {"status":"ok","sitekey":"<key>"}
#   error: {"status":"error","code":<code>,"http_code":<code>}
#     code 10000 → token lacks Account.Turnstile:Edit

set -uo pipefail
set +x

curl_with_auth() {
  local token_value="$1"
  shift
  printf 'header = "Authorization: Bearer %s"\n' "$token_value" \
    | env -u CLOUDFLARE_API_TOKEN curl --config - "$@"
}

MODE="managed"
while [[ $# -gt 0 ]]; do
  case $1 in
    --account-id) ACCOUNT_ID="$2"; shift 2 ;;
    --name)       NAME="$2"; shift 2 ;;
    --domains)    DOMAINS="$2"; shift 2 ;;
    --mode)       MODE="$2"; shift 2 ;;
    --secret-file) SECRET_FILE="$2"; shift 2 ;;
    *) echo "widget-create: unknown arg $1" >&2; exit 2 ;;
  esac
done

: "${CLOUDFLARE_API_TOKEN:?CLOUDFLARE_API_TOKEN must be set}"
: "${ACCOUNT_ID:?--account-id required}"
: "${NAME:?--name required}"
: "${DOMAINS:?--domains required}"
: "${SECRET_FILE:?--secret-file required}"
cloudflare_api_token="$CLOUDFLARE_API_TOKEN"
unset CLOUDFLARE_API_TOKEN

write_result() {
  local response_file="$1" destination="$2"
  if ! python3 - "$response_file" "$destination" <<'PY'
import json
import os
import stat
import sys

with open(sys.argv[1], encoding="utf-8") as source:
    result = json.load(source)["result"]

path = sys.argv[2]
flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
if hasattr(os, "O_NOFOLLOW"):
    flags |= os.O_NOFOLLOW
fd = os.open(path, flags, 0o600)
try:
    if not stat.S_ISREG(os.fstat(fd).st_mode):
        raise OSError("destination is not a regular file")
    with os.fdopen(fd, "w", encoding="utf-8", closefd=False) as secret_file:
        secret_file.write(result["secret"])
        secret_file.flush()
    os.fchmod(fd, 0o600)
finally:
    os.close(fd)

print(json.dumps(
    {"status": "ok", "sitekey": result["sitekey"]},
    separators=(",", ":"),
))
PY
  then
    echo "widget-create: could not create restricted secret file." >&2
    return 1
  fi
}

domains_json=$(python3 -c "import sys; print(__import__('json').dumps(sys.argv[1].split(',')))" "$DOMAINS")

response_file=$(mktemp)
chmod 600 "$response_file"
trap 'rm -f "$response_file"' EXIT
http_code=$(curl_with_auth "$cloudflare_api_token" -sS -w "%{http_code}" -o "$response_file" -X POST \
  "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/challenges/widgets" \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"$NAME\",\"domains\":$domains_json,\"mode\":\"$MODE\"}" 2>/dev/null || echo "000")

success=$(jq -r '.success' "$response_file" 2>/dev/null || python3 -c "import sys,json; print(str(json.load(open(sys.argv[1])).get('success',False)).lower())" "$response_file")

if [ "$success" = "true" ]; then
  write_result "$response_file" "$SECRET_FILE" || exit 1
  exit 0
fi

code=$(jq -r '.errors[0].code // 0' "$response_file" 2>/dev/null || echo "0")
echo "widget-create: request failed (HTTP $http_code, code=$code)." >&2
printf '{"status":"error","code":%s,"http_code":%s}\n' "$code" "$http_code"
exit 1
