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
detect Package.swift     "Swift Package Manager"
detect Project.swift     "Tuist project"
detect Workspace.swift   "Tuist workspace"
detect Tuist.swift       "Tuist configuration"
detect Gemfile           "Ruby"
detect pom.xml           "Java (Maven)"
detect build.gradle      "Java/Kotlin (Gradle)"
detect build.gradle.kts  "Kotlin (Gradle)"
detect composer.json     "PHP (Composer)"
detect Makefile          "Make targets"
detect Taskfile.yml      "Task"
detect justfile          "just"
for path in *.xcodeproj *.xcworkspace; do
  [ -e "$path" ] || continue
  echo "  - $path  (Apple Xcode project/workspace)"
  found=1
done
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
if [ -f Package.swift ]; then
  echo "  SwiftPM: swift build | swift test"
fi
if [ -f Project.swift ] || [ -f Workspace.swift ] || [ -f Tuist.swift ]; then
  echo "  Tuist: inspect the repository's documented generate/build/test commands"
fi
if find . -maxdepth 1 \( -name '*.xcodeproj' -o -name '*.xcworkspace' \) -print -quit | grep -q .; then
  echo "  Xcode: inspect shared schemes and CI for the exact workspace/project, configuration, and destination"
fi

echo
echo "=== Apple / Swift project details ==="
apple_found=0
if command -v swift >/dev/null 2>&1; then
  swift_version="$(swift --version 2>/dev/null | head -n 1 || true)"
  [ -n "$swift_version" ] && echo "  Swift toolchain: $swift_version"
fi
for f in .swift-version Package.resolved; do
  if [ -e "$f" ]; then
    echo "  - $f"
    apple_found=1
  fi
done
find . -maxdepth 4 -path '*/xcshareddata/xcschemes/*.xcscheme' -type f -print 2>/dev/null \
  | sed 's#^#  shared scheme: #' || true
if find . -maxdepth 1 \( -name '*.xcodeproj' -o -name '*.xcworkspace' -o -name 'Package.swift' \
  -o -name 'Project.swift' -o -name 'Workspace.swift' -o -name 'Tuist.swift' \) -print -quit \
  | grep -q .; then
  apple_found=1
  echo "  Inspect project settings/CI for Swift language mode, strict concurrency, deployment targets,"
  echo "  supported destinations, signing references, entitlements, and generated-project ownership."
fi
[ "$apple_found" -eq 0 ] && echo "  (n/a)"

echo
echo "=== Formatter / linter config present ==="
for f in .prettierrc .prettierrc.json .prettierrc.js .eslintrc .eslintrc.json .eslintrc.cjs \
         ruff.toml .ruff.toml .flake8 .rubocop.yml .editorconfig biome.json rustfmt.toml .golangci.yml \
         .swiftformat .swiftlint.yml .swiftlint.yaml; do
  [ -e "$f" ] && echo "  - $f"
done
if [ -f package.json ] && command -v node >/dev/null 2>&1; then
  node -e 'const p=require("./package.json");for(const k of ["prettier","eslintConfig"])if(p[k])console.log("  - package.json#"+k)' 2>/dev/null || true
fi

echo
echo "=== Top-level layout ==="
for d in */; do [ -d "$d" ] && printf '  %s\n' "$d"; done | head -n 30 || true

echo
echo "Use the above to fill Setup / Build-Test-Lint / Structure / Conventions in AGENTS.md."
echo "Only record commands you can confirm exist. Prefer README.md for documented setup steps."
