# Templates

Drop-in starter files. Copy what you need into a project root.

[See the complete workflow framework before installing](https://k95m65.github.io/AI_ONBOARD/).

| File | For | What it does |
|------|-----|--------------|
| [`AGENTS.md`](AGENTS.md) | All tools | Concise shared project-contract starter |
| [`CLAUDE.md`](CLAUDE.md) | Claude Code | One-line `@AGENTS.md` import + room for Claude-only notes |
| [`AGENTS.layer.md`](AGENTS.layer.md) | All tools | Nested layer-profile starter — drop in a subdir (`web/`, `api/`…) as `AGENTS.md` |
| [`.aider.conf.yml`](.aider.conf.yml) | Aider | Points Aider at `AGENTS.md` as read-only context |
| [`configs/claude.settings.json`](configs/claude.settings.json) | Claude Code | Conservative permissions and manual GOAL/GRILL activation |
| [`configs/codex.config.toml`](configs/codex.config.toml) | Codex | Bounded project-level agent concurrency |
| [`configs/opencode.json`](configs/opencode.json) | OpenCode | Conservative permissions, compaction, and watcher defaults |
| [`commands/`](commands/) | Claude, Codex, OpenCode | Update-check slash commands and optional Codex compatibility prompt |
| [`notifications/`](notifications/) | GitHub Actions | Free scheduled update notification template |
| [`link.sh`](link.sh) | All tools | Legacy copy-based wiring without upgrade or uninstall tracking |

The universal [`AGENTS.md`](../AGENTS.md) template lives at the repo root, not here — it's the source of
truth every other file points back to.

## Preferred managed path

From a project that already has an `AGENTS.md` at its root:

```bash
python3 /path/to/AI_ONBOARD/scripts/ai_onboard.py \
  --target /path/to/project \
  install \
  --harness claude,codex,opencode \
  --profile core \
  --agents \
  --configs
```

The installed project gets a desired-state file, lockfile, checksums, backups, and its own copy of the
manager. Add capability profiles as needed and preview every lifecycle action:

```bash
python3 .ai-onboard/bin/ai_onboard.py profile add security --dry-run
python3 .ai-onboard/bin/ai_onboard.py upgrade --check --cache --json
python3 .ai-onboard/bin/ai_onboard.py uninstall --dry-run
```

See [managed installation, upgrades, and cleanup](../docs/install-management.md) for profiles, adoption,
conflict handling, notifications, slash commands, and recovery.

## Legacy copy path

`link.sh` remains for simple, copy-based compatibility:

```bash
bash templates/link.sh --agents --skills --configs
bash templates/link.sh --workflow-foundations
bash templates/link.sh --dry-run
```

It is idempotent and backs up any real file it would replace, but it does not create lifecycle state and
cannot perform a managed upgrade or uninstall. `--agents`, `--skills`, `--configs`, and
`--workflow-foundations` require adjacent package files from an AI_ONBOARD clone. Symlink steps degrade
gracefully on Windows without Developer Mode.

The standard skill selection intentionally skips `goal-contract` and `grill-requirements`; select
`--workflow-foundations` when a harness needs those optional, manually invoked compatibility workflows.

`--configs` preserves any existing config instead of overwriting it. The templates set project safety and
workflow boundaries only; they deliberately omit models, providers, credentials, and personal UI settings.

When a template flag or install path changes, update this README, the root quickstart, and website quickstart
together.
