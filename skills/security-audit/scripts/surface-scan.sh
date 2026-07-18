#!/usr/bin/env bash
# surface-scan.sh — grep a codebase for common security risk indicators to orient an audit.
# NOT a scanner and NOT exhaustive: it surfaces starting points to investigate, with false positives
# expected. Read every hit in context before treating it as a finding.
#
# Usage: bash surface-scan.sh [path]   (defaults to .)
set -uo pipefail

ROOT="${1:-.}"
EXCLUDES=(--exclude-dir=.git --exclude-dir=node_modules --exclude-dir=vendor --exclude-dir=dist
          --exclude-dir=build --exclude-dir=.next --exclude-dir=target --exclude-dir=__pycache__)

# label|regex — extended-regex, case-insensitive.
CHECKS=(
  "Hardcoded secrets|(api[_-]?key|secret|passwd|password|client[_-]?secret)[[:space:]]*[:=][[:space:]]*[\"'][^\"']"
  "AWS access key|AKIA[0-9A-Z]{16}"
  "Private key blocks|BEGIN (RSA |EC |OPENSSH |DSA )?PRIVATE KEY"
  "Shell / command exec|(os/exec|exec\.Command|subprocess\.|child_process|os\.system|popen|\bexec[lv]p?\(|shell=True)"
  "Dynamic eval|(\beval\(|new Function\(|Function\(['\"])"
  "Possible SQL string-building|(SELECT|INSERT|UPDATE|DELETE)[^;]*(\\+|\\\$\{|%s|\.format\(|f\"|f')"
  "Unsafe deserialization|(pickle\.load|yaml\.load\(|readObject|unserialize\(|Marshal\.load)"
  "Disabled TLS verification|(InsecureSkipVerify|verify[[:space:]]*=[[:space:]]*False|rejectUnauthorized[[:space:]]*:[[:space:]]*false)"
  "Weak crypto|(\bMD5\b|\bSHA1\b|\bDES\b|\bRC4\b|ECB|Math\.random\(\))"
  "Permissive CORS|Access-Control-Allow-Origin[^A-Za-z0-9]{1,10}\*"
  "Path from input / traversal|(\.\./|path\.join\([^)]*req|filepath\.Join\([^)]*r\.)"
)

echo "Security surface scan of: $ROOT"
echo "(starting points to investigate — expect false positives; confirm each in context)"
found_any=0
for entry in "${CHECKS[@]}"; do
  label="${entry%%|*}"
  regex="${entry#*|}"
  hits="$(grep -rIEni "${EXCLUDES[@]}" -e "$regex" "$ROOT" 2>/dev/null || true)"
  if [ -n "$hits" ]; then
    found_any=1
    echo
    echo "### $label"
    printf '%s\n' "$hits" | head -n 40 | sed 's/^/  /'
    count="$(printf '%s\n' "$hits" | wc -l | tr -d ' ')"
    [ "$count" -gt 40 ] && echo "  … and $((count - 40)) more"
  fi
done

echo
if [ "$found_any" -eq 0 ]; then
  echo "No risk indicators matched. That is NOT an all-clear — walk reference.md by hand."
else
  echo "Review each hit against reference.md. Absence of a category here does not mean it's safe."
fi
