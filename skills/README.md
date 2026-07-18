# Skills library

Portable, reusable [Agent Skills](../docs/skills.md) — an open standard, so each folder works **as-is in both
Claude Code and Codex** (and 30+ other tools). Copy or symlink a folder into a harness's skills directory:

| Harness | Personal | Project (team-shared) |
|---------|----------|-----------------------|
| Claude Code | `~/.claude/skills/<name>/` | `.claude/skills/<name>/` |
| Codex | `~/.agents/skills/<name>/` | `.agents/skills/<name>/` (vendor-neutral — **not** `.codex/skills`) |

## Installing a skill

```bash
# Claude Code (project, team-shared)
mkdir -p .claude/skills && cp -R skills/dataviz .claude/skills/

# Codex (project) — same folder, different directory
mkdir -p .agents/skills && cp -R skills/dataviz .agents/skills/

# Use it in both without duplicating: one canonical copy, symlinked into each tree
ln -s "$PWD/skills/dataviz" .claude/skills/dataviz
ln -s "$PWD/skills/dataviz" .agents/skills/dataviz
```

## Skills in this library

| Skill | What it does |
|-------|--------------|
| [`conventional-commit`](conventional-commit/) | Writes a Conventional Commits message from your staged changes |
| [`agents-md-init`](agents-md-init/) | Bootstraps an `AGENTS.md` by detecting your project's stack and commands |
| [`dataviz`](dataviz/) | Guidance for correct, readable, accessible charts — chart choice, color, a11y |
| [`component-scaffold`](component-scaffold/) | Scaffolds a React/TS component (component + test + index) from templates |
| [`prisma-migrate`](prisma-migrate/) | Safely creates + applies a Prisma migration; guards against non-local databases |
| [`security-audit`](security-audit/) | Systematic whole-codebase security audit — threat model, category checklist, surface-scan |
| [`dependency-vuln-scan`](dependency-vuln-scan/) | Scans dependencies for known CVEs (npm/pnpm/yarn, Go, osv-scanner); degrades gracefully |
| [`secret-scan`](secret-scan/) | Scans for committed secrets incl. git history (gitleaks/trufflehog, grep fallback) |
| [`threat-model`](threat-model/) | STRIDE + data-flow threat model of a feature — design-time companion to `security-audit` |
| [`cobra-command`](cobra-command/) | Scaffolds a Go Cobra subcommand + table-driven test (CLI counterpart to `component-scaffold`) |
| [`pr-description`](pr-description/) | Writes a PR description from the branch's commits + diff |
| [`changelog`](changelog/) | Rolls Conventional Commits since the last tag into release notes |

## Authoring a new skill

Follow [docs/skills.md](../docs/skills.md). The short version:

1. `mkdir skills/<name>` with a `SKILL.md`.
2. Frontmatter needs `name` and a trigger-rich `description` (what it does + when to use it).
3. Put deterministic work in `scripts/`; keep `SKILL.md` lean and push depth into referenced files.
4. Make it self-contained so it runs when dropped into any repo.
