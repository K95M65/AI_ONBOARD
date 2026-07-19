# @RSTHRIVES Portable Agent Workflow Framework

**AI_ONBOARD** is universal onboarding configuration for AI coding tools — **write your agent instructions
once, use them across every harness.**

Codex, Claude Code, OpenCode, Cursor, Gemini CLI, Aider, Windsurf and friends each look for their *own* config file. Maintaining a separate `CLAUDE.md`, `GEMINI.md`, `.cursorrules`, and `AGENTS.md` by hand means they drift apart within a week. This repo treats **`AGENTS.md` as the single source of truth** and wires every other tool to it.

**Codex, Claude Code, and OpenCode are first-class supported harnesses.** Each gets a conservative,
project-level config and native agent realization without baking personal models, providers, credentials, or
UI preferences into the shared framework.

[Explore the interactive project map](https://k95m65.github.io/AI_ONBOARD/) for the public explanation of
the **@RSTHRIVES Portable Agent Workflow Framework** and route example requests through project context,
focused skills, independent review, verification, and release.

The framework is built in public by [@rsthrive](https://x.com/rsthrive); `AI_ONBOARD` remains the repository
and install-package name.

> **Manual workflow foundations:** `goal-contract` (GOAL) and `grill-requirements` (GRILL) are original
> AI_ONBOARD skills that run only when the user explicitly invokes their intent. GOAL is for explicitly
> goal-backed, measurable, or resumable work; GRILL is for an explicitly requested requirements interview.
> Neither runs automatically during ordinary implementation, and both are installed separately with
> `--workflow-foundations`. “Manual” means explicit natural-language intent or direct
> skill invocation; the user does not need to type the exact skill name.

<!-- generated:project-inventory:start -->
- **68** portable skills across **7** capability groups
- **6** independent reference subagents for research, review, and verification
- **3** composable mechanisms: project context, on-demand skills, and isolated subagents
<!-- generated:project-inventory:end -->

---

## The idea

```
                 ┌─────────────────┐
                 │    AGENTS.md    │   ← you edit this, and only this
                 │ (source of truth)│
                 └────────┬────────┘
          ┌───────────────┼────────────────┐
          │               │                │
     CLAUDE.md        GEMINI.md      read natively
    (@import)        (symlink)       (no wiring)
          │               │                │
     Claude Code      Gemini CLI   Codex · Cursor · OpenCode
```

- **[AGENTS.md](https://agents.md)** is an open, tool-agnostic standard already read natively by Codex, OpenCode, Cursor, Jules, Zed, Aider, and 20k+ repos.
- Tools that use a *different* filename are pointed back at `AGENTS.md` via a **symlink** or a **one-line import**, so there is exactly one file to maintain.

## Repository layout

| Path | What it is |
|------|------------|
| [`AGENTS.md`](AGENTS.md) | This repository's shared working contract and portability example |
| [`templates/AGENTS.md`](templates/AGENTS.md) | Drop-in shared project-contract starter |
| [`docs/tool-matrix.md`](docs/tool-matrix.md) | Which config file *each* AI tool actually reads (start here) |
| [`docs/agents-md.md`](docs/agents-md.md) | The `AGENTS.md` format, sections, and precedence rules |
| [`docs/agent-behavior.md`](docs/agent-behavior.md) | The behavioral contract — how agents should work, with OpenAI/Anthropic citations |
| [`docs/delegation.md`](docs/delegation.md) | How agents delegate to subagents (by function) and specialize by layer (profiles) |
| [`docs/mechanisms.md`](docs/mechanisms.md) | Which mechanism to use — AGENTS.md vs Skills vs Subagents |
| [`docs/install-management.md`](docs/install-management.md) | Managed installation, profiles, upgrades, adoption, cleanup, and uninstall |
| [`docs/workflow-foundations.md`](docs/workflow-foundations.md) | Manually invoked, native-first GOAL and explicit GRILL compatibility workflows |
| [`docs/capability-expansion.md`](docs/capability-expansion.md) | Browser testing, web preservation, current docs, Obsidian, code quality, Superpowers, and frontend-design gap decisions |
| [`docs/security-audit.md`](docs/security-audit.md) | Security audit methodology — severity rubric, report format, skill + subagent |
| [`docs/security-consulting.md`](docs/security-consulting.md) | Internal/external attack-surface, vulnerability-risk, and control-assessment workflow |
| [`docs/skills.md`](docs/skills.md) | The Agent Skills format (`SKILL.md`) and how to author portable skills |
| [`docs/website.md`](docs/website.md) | Website strategy, information architecture, generated-data contract, and publishing workflow |
| `docs/setup/` | Per-tool setup guides (Claude Code, Codex, OpenCode, Cursor, Gemini CLI) |
| `templates/configs/` | Conservative project-config starters for Claude Code, Codex, and OpenCode |
| `templates/commands/` | Portable update-check slash commands and the optional Codex compatibility prompt |
| `templates/notifications/` | Opt-in scheduled GitHub notification workflow |
| [`agents/`](agents/) | Reference subagents (researcher, reviewer, verifier, security/design lenses) |
| [`examples/`](examples/) | Worked end-to-end setups — a full-stack monorepo wired for Claude Code + Codex |
| `skills/` | A library of reusable, portable skills |
| `templates/` | Drop-in starter files |
| [`site/`](site/) | Dependency-free source for the interactive GitHub Pages website |
| [`package-manifest.json`](package-manifest.json) | Version, update channel, and capability-profile definitions |
| [`scripts/ai_onboard.py`](scripts/ai_onboard.py) | Dependency-free lifecycle manager |
| [`scripts/install_macos_update_notifier.py`](scripts/install_macos_update_notifier.py) | Reversible, opt-in macOS Notification Center scheduler |
| [`scripts/test_deployments.py`](scripts/test_deployments.py) | Full temporary deployment smoke tests for Claude, Codex, and OpenCode |
| [`scripts/sync_project_docs.py`](scripts/sync_project_docs.py) | Generates the live skill catalog and synchronizes README inventory counts |

## Quickstart

1. Start the target project with an `AGENTS.md`: copy [`templates/AGENTS.md`](templates/AGENTS.md), or
   invoke `agents-md-init` to generate a stack-aware version.
2. Clone AI_ONBOARD and install only the capability profiles the project needs:

   ```bash
   git clone https://github.com/K95M65/AI_ONBOARD.git
   python3 AI_ONBOARD/scripts/ai_onboard.py \
     --target /path/to/project \
     install \
     --harness claude,codex,opencode \
     --profile core \
     --profile product \
     --agents \
     --configs
   ```

   Add `--workflow-foundations` only when the project wants the manual GOAL and GRILL compatibility layer.
   Profiles keep skill discovery focused; available profiles are `core`, `product`, `apple`, `security`,
   `cloudflare`, and `research`.
3. Commit `ai-onboard.json`, `.ai-onboard.lock.json`, and the installed project files. The target now carries
   its own manager:

   ```bash
   python3 .ai-onboard/bin/ai_onboard.py status
   python3 .ai-onboard/bin/ai_onboard.py upgrade --check --cache --json
   python3 .ai-onboard/bin/ai_onboard.py uninstall --dry-run
   ```

The manager preserves divergent user files, merges only owned configuration keys, stages incoming conflicts,
and removes only unchanged managed content. See [`docs/install-management.md`](docs/install-management.md)
for adoption, locked sync, upgrades, cleanup, recovery, and uninstall behavior.

Add `--notifications` to the install command to opt into `/ai-onboard-update` for Claude Code and
OpenCode, a Codex compatibility prompt,
and a weekly GitHub Actions check. The portable `check-ai-onboard-updates` skill remains the preferred
cross-harness workflow. Codex users who specifically want a slash prompt can copy the installed template
to `~/.codex/prompts/` and invoke `/prompts:ai-onboard-update`; Codex custom prompts are user-scoped and
deprecated in favor of skills, so the manager never writes there silently.

For a free local macOS notification:

```bash
python3 .ai-onboard/bin/install_macos_update_notifier.py \
  install --target . --interval weekly
```

Update checks classify releases as `security`, `fix`, `feature`, or `maintenance`. Plain
`upgrade --check` stays read-only; `--cache` records the result for `doctor`, `--notify` sends a desktop
notice when supported, `--json` provides a stable machine contract, and `--exit-code` returns `10` when an
update is available.

[`templates/link.sh`](templates/link.sh) remains as a legacy copy-based compatibility path. It is useful for
simple wiring but does not provide lifecycle tracking.

### Deployment smoke tests

Exercise a complete managed install for every first-class harness before publishing a build:

```bash
python3 scripts/test_deployments.py
python3 scripts/test_deployments.py --harness codex --verbose
```

Each isolated temporary project installs every capability profile plus agents, configs, notifications, and
manual workflow foundations. The script validates the harness-specific layout, desired state, lockfile,
user-config preservation, `status`, `doctor`, local-source update checks, sync and uninstall previews, and
real cleanup. It does not require harness credentials or make model API calls. GitHub Actions runs the same
contract as a Claude, Codex, and OpenCode matrix on every push and pull request.

## Website and documentation

The website is a static artifact generated from the same repository people and agents inspect. Skill names,
descriptions, categories, and inventory counts come from canonical `skills/**/SKILL.md` and `agents/*.md`
frontmatter; do not edit [`site/data/catalog.json`](site/data/catalog.json) by hand.

```bash
python3 scripts/sync_project_docs.py          # regenerate catalog + README counts
python3 scripts/sync_project_docs.py --check  # fail when they are stale
python3 scripts/check_skills.py               # validate skill structure, links, and lexical trigger overlap
python3 scripts/check_harness_configs.py       # validate Claude, Codex, and OpenCode project boundaries
python3 -m unittest discover -v tests           # validate lifecycle and deployment contracts
python3 scripts/test_deployments.py             # smoke-test all three complete harness deployments
python3 -m http.server 4173 --directory site  # preview at http://localhost:4173
```

When user-facing behavior, capabilities, setup, or repository structure changes, update the nearest README
and the website narrative in the same change. See [`docs/website.md`](docs/website.md) for the maintenance
and GitHub Pages publishing contract.

## Scope

This repo covers **project-level onboarding files** (what an agent should know when it opens your repo),
**portable skills** (reusable capabilities), and **independent reference subagents** (bounded research and
review lenses). It is intentionally tool-agnostic: tool-specific power features (Claude Code hooks, Codex
`config.toml`, etc.) are documented in `docs/setup/` but kept *out* of the shared `AGENTS.md` so it stays
portable.

## License

**MIT** — see [`LICENSE`](LICENSE). Free to use, copy, modify, and distribute; just keep the notice.

The vendored Cloudflare skills in [`skills/cloudflare/`](skills/cloudflare/) are **Apache-2.0** (their upstream license) — see [`skills/cloudflare/NOTICE.md`](skills/cloudflare/NOTICE.md).

---

*Status: active. Core docs, multi-harness setup, the behavioral and delegation model, six reference
subagents, the portable skills library, two worked examples, and the generated interactive project map are
in place.*
