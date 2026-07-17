#!/usr/bin/env bash
# detect-stack.sh — detect a project's ecosystem, package manager, and build/test/lint commands
# by inspecting manifest files. Read-only; prints a summary. Run from the repo root.
set -euo pipefail

root="${1:-.}"
cd "$root"

echo "=== Ecosystem / manifests found ==="
found=0
detect() { if [ -e "$1" ]; then echo "  - $1  ($2)"; found=1; fi; }
detect package.json      "Node.js / JavaScript / TypeScript"
detect pyproject.toml    "Python (PEP 621 / Poetry / uv / Hatch)"
detect requirements.txt  "Python (pip)"
detect setup.py          "Python (setuptools)"
detect go.mod            "Go"
detect Cargo.toml        "Rust"
detect Gemfile           "Ruby"
detect pom.xml           "Java (Maven)"
detect build.gradle      "Java/Kotlin (Gradle)"
detect build.gradle.kts  "Kotlin (Gradle)"
detect composer.json     "PHP (Composer)"
detect Makefile          "Make targets"
detect Taskfile.yml      "Task"
detect justfile          "just"
[ "$found" -eq 0 ] && echo "  (no known manifest found — inspect the repo manually)"

echo
echo "=== Package manager (Node) ==="
if [ -f pnpm-lock.yaml ]; then echo "  pnpm  (pnpm-lock.yaml)"
elif [ -f yarn.lock ]; then    echo "  yarn  (yarn.lock)"
elif [ -f bun.lockb ] || [ -f bun.lock ]; then echo "  bun   (bun lockfile)"
elif [ -f package-lock.json ]; then echo "  npm   (package-lock.json)"
elif [ -f package.json ]; then echo "  npm   (no lockfile — assume npm)"
else echo "  (n/a)"; fi

echo
echo "=== Scripts / commands ==="
if [ -f package.json ]; then
  echo "  package.json scripts:"
  if command -v node >/dev/null 2>&1; then
    node -e 'try{const s=require("./package.json").scripts||{};const k=Object.keys(s);if(!k.length){console.log("    (none)")}else{for(const n of k)console.log("    "+n+": "+s[n])}}catch(e){console.log("    (could not parse)")}'
  else
    echo "    (node not installed — open package.json to read the \"scripts\" block)"
  fi
fi
if [ -f Makefile ]; then
  echo "  Makefile targets:"
  grep -E '^[a-zA-Z0-9_.-]+:' Makefile | sed 's/:.*//' | sort -u | sed 's/^/    /' || true
fi
if [ -f pyproject.toml ]; then
  echo "  pyproject.toml — check [tool.poetry.scripts], [project.scripts],"
  echo "                   and tooling: pytest, ruff, black, mypy, tox."
fi
if [ -f Cargo.toml ]; then
  echo "  Rust: cargo build | cargo test | cargo clippy | cargo fmt"
fi
if [ -f go.mod ]; then
  echo "  Go:   go build ./... | go test ./... | go vet ./... | gofmt -l ."
fi

echo
echo "=== Formatter / linter config present ==="
for f in .prettierrc .prettierrc.json .prettierrc.js .eslintrc .eslintrc.json .eslintrc.cjs \
         ruff.toml .ruff.toml .flake8 .rubocop.yml .editorconfig biome.json rustfmt.toml .golangci.yml; do
  [ -e "$f" ] && echo "  - $f"
done
[ -f package.json ] && command -v node >/dev/null 2>&1 && \
  node -e 'const p=require("./package.json");for(const k of ["prettier","eslintConfig"])if(p[k])console.log("  - package.json#"+k)' 2>/dev/null || true

echo
echo "=== Top-level layout ==="
ls -1p | grep '/$' | head -n 30 | sed 's/^/  /' || true

echo
echo "Use the above to fill Setup / Build-Test-Lint / Structure / Conventions in AGENTS.md."
echo "Only record commands you can confirm exist. Prefer README.md for documented setup steps."
