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

### Security & audit

| Skill | What it does |
|-------|--------------|
| [`threat-model`](threat-model/) | STRIDE + data-flow threat model — design-time framing |
| [`secure-coding`](secure-coding/) | Write-time defensive practices, per category |
| [`input-sanitization`](input-sanitization/) | Validate-in / encode-out per sink (SQLi, XSS, command, path, SSRF) |
| [`identity-management`](identity-management/) | Authn/authz patterns — sessions, JWT/OAuth, RBAC, MFA, IDOR |
| [`secret-management`](secret-management/) | Store/inject/scope/rotate secrets safely |
| [`vulnerability-hardening`](vulnerability-hardening/) | Config/deploy hardening — headers, TLS, least privilege |
| [`security-audit`](security-audit/) | Systematic whole-codebase audit — threat model, checklist, surface-scan |
| [`dependency-vuln-scan`](dependency-vuln-scan/) | Scan dependencies for known CVEs (npm/Go/osv-scanner) |
| [`secret-scan`](secret-scan/) | Scan for committed secrets incl. git history |
| [`automated-security-review`](automated-security-review/) | Wire the scanners into CI as a PR gate (GitHub Actions) |

### Code scaffolding

| Skill | What it does |
|-------|--------------|
| [`component-scaffold`](component-scaffold/) | Scaffold a React/TS component (component + test + index) |
| [`cobra-command`](cobra-command/) | Scaffold a Go Cobra subcommand + table-driven test |
| [`prisma-migrate`](prisma-migrate/) | Safely create + apply a Prisma migration; guards non-local DBs |

### Dev workflow

| Skill | What it does |
|-------|--------------|
| [`conventional-commit`](conventional-commit/) | Write a Conventional Commits message from staged changes |
| [`pr-description`](pr-description/) | Write a PR description from the branch's commits + diff |
| [`changelog`](changelog/) | Roll Conventional Commits since the last tag into release notes |

### Data & onboarding

| Skill | What it does |
|-------|--------------|
| [`dataviz`](dataviz/) | Correct, readable, accessible charts — choice, color, a11y |
| [`agents-md-init`](agents-md-init/) | Bootstrap an `AGENTS.md` by detecting the stack + commands |

## Authoring a new skill

Follow [docs/skills.md](../docs/skills.md). The short version:

1. `mkdir skills/<name>` with a `SKILL.md`.
2. Frontmatter needs `name` and a trigger-rich `description` (what it does + when to use it).
3. Put deterministic work in `scripts/`; keep `SKILL.md` lean and push depth into referenced files.
4. Make it self-contained so it runs when dropped into any repo.
