# Templates

Drop-in starter files. Copy what you need into a project root.

| File | For | What it does |
|------|-----|--------------|
| [`CLAUDE.md`](CLAUDE.md) | Claude Code | One-line `@AGENTS.md` import + room for Claude-only notes |
| [`.aider.conf.yml`](.aider.conf.yml) | Aider | Points Aider at `AGENTS.md` as read-only context |
| [`link.sh`](link.sh) | All tools | Auto-wires every tool's config file to your `AGENTS.md` |

The universal [`AGENTS.md`](../AGENTS.md) template lives at the repo root, not here — it's the source of
truth every other file points back to.

## Fastest path

From a project that already has an `AGENTS.md` at its root:

```bash
# copy link.sh in and run it
curl -fsSL https://raw.githubusercontent.com/K95M65/AI_ONBOARD/main/templates/link.sh -o link.sh
bash link.sh          # wires Claude Code, Gemini, Copilot, Aider to AGENTS.md
bash link.sh --dry-run  # preview without touching anything
```

`link.sh` is idempotent and backs up any real file it would replace.
