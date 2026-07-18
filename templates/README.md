# Templates

Drop-in starter files. Copy what you need into a project root.

| File | For | What it does |
|------|-----|--------------|
| [`CLAUDE.md`](CLAUDE.md) | Claude Code | One-line `@AGENTS.md` import + room for Claude-only notes |
| [`AGENTS.layer.md`](AGENTS.layer.md) | All tools | Nested layer-profile starter — drop in a subdir (`web/`, `api/`…) as `AGENTS.md` |
| [`.aider.conf.yml`](.aider.conf.yml) | Aider | Points Aider at `AGENTS.md` as read-only context |
| [`link.sh`](link.sh) | All tools | Auto-wires every tool's config to `AGENTS.md`; `--agents` / `--skills` also install the reference subagents and skills |

The universal [`AGENTS.md`](../AGENTS.md) template lives at the repo root, not here — it's the source of
truth every other file points back to.

## Fastest path

From a project that already has an `AGENTS.md` at its root:

```bash
# copy link.sh in and run it
curl -fsSL https://raw.githubusercontent.com/K95M65/AI_ONBOARD/main/templates/link.sh -o link.sh
bash link.sh            # wires Claude Code, Gemini, Copilot, Aider to AGENTS.md
bash link.sh --agents   # also copy the reference subagents into .claude/agents + .codex/agents
bash link.sh --skills   # also copy the skills into .claude/skills + .agents/skills (Codex)
bash link.sh --dry-run  # preview without touching anything
```

`link.sh` is idempotent and backs up any real file it would replace. `--agents` needs the
`AI_ONBOARD/agents/` directory alongside the script (i.e. run it from a clone); otherwise it prints the
manual copy commands. Symlink steps degrade gracefully on Windows without Developer Mode (warn + skip).
