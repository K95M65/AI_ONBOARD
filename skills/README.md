# Skills library

Portable, reusable [Agent Skills](../docs/skills.md). Each folder is self-contained — copy it into any
skills location and it works:

| Skill location | Scope |
|----------------|-------|
| `~/.claude/skills/<name>/` | Personal, all projects (Claude Code) |
| `.claude/skills/<name>/` | Team-shared, committed to a repo (Claude Code) |
| anywhere you run the scripts by hand | Any tool — the scripts are plain shell/Python |

## Installing a skill

```bash
# personal
cp -R skills/conventional-commit ~/.claude/skills/

# project (team-shared)
mkdir -p .claude/skills && cp -R skills/conventional-commit .claude/skills/
```

## Skills in this library

| Skill | What it does |
|-------|--------------|
| [`conventional-commit`](conventional-commit/) | Writes a Conventional Commits message from your staged changes |
| [`agents-md-init`](agents-md-init/) | Bootstraps an `AGENTS.md` by detecting your project's stack and commands |

## Authoring a new skill

Follow [docs/skills.md](../docs/skills.md). The short version:

1. `mkdir skills/<name>` with a `SKILL.md`.
2. Frontmatter needs `name` and a trigger-rich `description` (what it does + when to use it).
3. Put deterministic work in `scripts/`; keep `SKILL.md` lean and push depth into referenced files.
4. Make it self-contained so it runs when dropped into any repo.
