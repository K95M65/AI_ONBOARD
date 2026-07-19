#!/usr/bin/env bash
# Retrieves the secret for an existing Turnstile widget via the Cloudflare API.
# Used by the recovery flow so the agent can wire canonical server-side
# siteverify against an existing widget without rotating the sitekey.
#
# Reads:
#   $CLOUDFLARE_API_TOKEN (required)
#
# Args:
#   --account-id <id>   Cloudflare account ID
#   --sitekey <key>     Widget sitekey to look up
#   --secret-file <path> New restricted file that receives the widget secret
#
# Outputs JSON. Exit 0 on success, 1 on failure.
#   ok:        {"status":"ok","clearance_level":"<level>","domains":[<list>]}
#   no_scope:  {"status":"missing_read_scope","detail":"token lacks Account.Turnstile:Read"}
#   not_found: {"status":"error","reason":"widget_not_found","http_code":<code>}
#
# The agent uses clearance_level to enforce the pre-clearance scope boundary
# (Spin only applies to widgets where clearance_level == "no_clearance"; for
# other levels siteverify is optional and the recovery flow should exit).
#
# Never propose recreating the widget to get a fresh secret; that breaks
# the existing sitekey everywhere the user has it deployed in their frontend.

set -uo pipefail
set +x

curl_with_auth() {
  local token_value="$1"
  shift
  printf 'header = "Authorization: Bearer %s"\n' "$token_value" \
    | env -u CLOUDFLARE_API_TOKEN curl --config - "$@"
}

while [[ $# -gt 0 ]]; do
  case $1 in
    --account-id) ACCOUNT_ID="$2"; shift 2 ;;
    --sitekey)    SITEKEY="$2"; shift 2 ;;
    --secret-file) SECRET_FILE="$2"; shift 2 ;;
    *) echo "fetch-secret: unknown arg $1" >&2; exit 2 ;;
  esac
done

: "${CLOUDFLARE_API_TOKEN:?CLOUDFLARE_API_TOKEN must be set}"
: "${ACCOUNT_ID:?--account-id required}"
: "${SITEKEY:?--sitekey required}"
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
    {
        "status": "ok",
        "clearance_level": result.get("clearance_level", "no_clearance"),
        "domains": result.get("domains", []),
    },
    separators=(",", ":"),
))
PY
  then
    echo "fetch-secret: could not create restricted secret file." >&2
    return 1
  fi
}

tmp=$(mktemp)
chmod 600 "$tmp"
trap 'rm -f "$tmp"' EXIT
http_code=$(curl_with_auth "$cloudflare_api_token" -sS -w "%{http_code}" -o "$tmp" \
  "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/challenges/widgets/$SITEKEY" \
  2>/dev/null || echo "000")

if [ "$http_code" = "200" ]; then
  has_secret=$(jq -r '(.result.secret // "") != ""' "$tmp" 2>/dev/null || python3 -c "import sys,json; print(str(bool(json.load(open(sys.argv[1])).get('result',{}).get('secret'))).lower())" "$tmp")
  if [ "$has_secret" = "true" ]; then
    write_result "$tmp" "$SECRET_FILE" || exit 1
    rm -f "$tmp"
    exit 0
  fi
fi

if [ "$http_code" = "403" ]; then
  code=$(jq -r '.errors[0].code // 0' "$tmp" 2>/dev/null || echo "0")
  if [ "$code" = "10000" ]; then
    rm -f "$tmp"
    echo "fetch-secret: token can edit Turnstile widgets but cannot read this one's secret." >&2
    echo "fetch-secret: add Account.Turnstile:Read or retrieve it through the dashboard secret flow." >&2
    echo "{\"status\":\"missing_read_scope\",\"detail\":\"token lacks Account.Turnstile:Read\"}"
    exit 1
  fi
fi

rm -f "$tmp"
echo "fetch-secret: widget lookup failed (HTTP $http_code)." >&2
echo "{\"status\":\"error\",\"reason\":\"widget_not_found\",\"http_code\":$http_code}"
exit 1
