# Managed installation, upgrades, and cleanup

AI_ONBOARD's lifecycle manager installs a selected capability surface, records exactly what it owns, and
refuses to overwrite or remove divergent user content. It is a dependency-free Python 3 script:
[`scripts/ai_onboard.py`](../scripts/ai_onboard.py).

`templates/link.sh` remains available for legacy copy-based wiring. It is intentionally not upgrade-aware;
use the manager for new installations.

## Install globally for one user

Use an explicit global scope when the selected skills and optional reference agents should be available
across repositories:

```bash
python3 /path/to/AI_ONBOARD/scripts/ai_onboard.py \
  --global \
  install \
  --harness claude,codex,opencode \
  --profile core \
  --profile apple \
  --agents
```

The global install uses native user-level discovery paths:

| Harness surface | Managed destination |
|-----------------|---------------------|
| Codex and OpenCode portable skills | `~/.agents/skills/` |
| Claude Code skills | `~/.claude/skills/` |
| Codex reference agents | `~/.codex/agents/` |
| Claude Code reference agents | `~/.claude/agents/` |
| OpenCode reference agents | `~/.config/opencode/agents/` |
| Desired state and lock | `~/.ai-onboard/` |
| User command | `~/.local/bin/ai-onboard` |

Add `~/.local/bin` to `PATH` when the installer reports that it is missing. The installed command defaults
to global scope:

```bash
ai-onboard status
ai-onboard doctor
ai-onboard upgrade --check --json
ai-onboard uninstall --dry-run
```

Global installs deliberately do not install `AGENTS.md`, harness configuration, project slash commands,
scheduled GitHub workflows, or macOS project notifications. Keep shared project facts in each repository's
`AGENTS.md`; use a project install for managed configuration or notification assets. `--configs` and
`--notifications` therefore fail closed with `--global`.

Global and project installs use separate desired-state and lockfile locations. A global upgrade cannot
silently rewrite a project's managed copies, and a project upgrade cannot change the user-global package.

## Install into a project from a clone

Start with a project `AGENTS.md`. Copy [`templates/AGENTS.md`](../templates/AGENTS.md) or generate one with
the `agents-md-init` skill, then run:

```bash
python3 /path/to/AI_ONBOARD/scripts/ai_onboard.py \
  --target /path/to/project \
  install \
  --harness claude,codex,opencode \
  --profile core \
  --profile product \
  --agents \
  --configs
```

The manager installs itself into `.ai-onboard/bin/ai_onboard.py`, so subsequent commands run from the
managed project:

```bash
python3 .ai-onboard/bin/ai_onboard.py status
python3 .ai-onboard/bin/ai_onboard.py doctor
```

Add `--dry-run` to `install`, `adopt`, `sync`, `upgrade`, `profile`, `uninstall`, or `cleanup` to preview
without changing the project.

## Capability profiles

Profiles keep the installed skill listing relevant and reduce discovery-context cost. Combine only the
capabilities a project needs:

| Profile | Capability surface |
|---------|--------------------|
| `core` | Repository delivery, testing, debugging, review, and maintenance |
| `product` | Websites, product interfaces, brand, content, design systems, accessibility, and measurement |
| `apple` | Swift, SwiftUI, AppKit, persistence, architecture, testing, and Apple accessibility |
| `security` | Threat models, attack surfaces, controls, vulnerabilities, identity, and hardening |
| `cloudflare` | Workers, Agents, Durable Objects, Zero Trust, deployment, and platform workflows |
| `research` | Research, analysis, OSINT, evidence, markets, visualization, and communication |

GOAL and GRILL remain separately selected manual foundations:

```bash
python3 .ai-onboard/bin/ai_onboard.py \
  profile add security

# For a first install:
python3 scripts/ai_onboard.py install \
  --profile core \
  --workflow-foundations
```

Remove an unneeded profile with `profile remove <name>`. The manager removes only unchanged package-owned
artifacts; modified or adopted content becomes user-owned and remains.

## Desired state, lock, and local runtime

The installation has three layers:

| Path | Purpose | Commit? |
|------|---------|:-------:|
| `ai-onboard.json` | Desired harnesses, profiles, features, repository, and update channel | Yes |
| `.ai-onboard.lock.json` | Exact package version, source revision, checksums, ownership, and managed config keys | Yes |
| `.ai-onboard/` | Installed manager, cached update status, local backups, and staged conflicts | No; its nested `.gitignore` protects it |

Commit the desired state and lockfile with the project. A teammate can reproduce the locked state with:

```bash
python3 .ai-onboard/bin/ai_onboard.py sync
```

`sync` resolves the exact locked revision. `upgrade` resolves the current configured channel instead.
The manager refuses a Git source whose installable package content is uncommitted, so a commit lock cannot
misrepresent dirty files. A non-Git source records a `content:` digest; pass
`--source /path/to/source` for later operations because it has no remotely resolvable commit.

## Check and upgrade

```bash
python3 .ai-onboard/bin/ai_onboard.py upgrade --check
python3 .ai-onboard/bin/ai_onboard.py upgrade --check --cache --json
python3 .ai-onboard/bin/ai_onboard.py upgrade --check --cache --notify
python3 .ai-onboard/bin/ai_onboard.py upgrade --dry-run
python3 .ai-onboard/bin/ai_onboard.py upgrade
python3 .ai-onboard/bin/ai_onboard.py doctor
```

The default check only prints a result and does not write to the project. Automation and notification
options are explicit:

| Option | Behavior |
|--------|----------|
| `--json` | Emits current/latest version, revision, digest, release classification, summary, notes URL, and check time |
| `--cache` | Writes `.ai-onboard/update-status.json`; `doctor` surfaces a cached available update |
| `--notify` | Sends a macOS Notification Center or Linux `notify-send` notice when an update exists |
| `--exit-code` | Returns `10` when an update exists, `0` when current, and `2` for a check error |

An applied `sync` or `upgrade` clears the cached notice so `doctor` does not report an update that already
landed. Package release metadata classifies a change as `security`, `fix`, `feature`, or `maintenance`;
the classification and summary come from committed package metadata, not generated marketing copy.

## Protect Git identity

The installed manager can prevent a personal address from entering commit metadata:

```bash
python3 .ai-onboard/bin/ai_onboard.py check-git
```

The default checks the effective `GIT_AUTHOR_IDENT` and `GIT_COMMITTER_IDENT` process values plus every
commit reachable from local refs. `--identity-only` is suitable for a pre-commit hook;
`--history-only` is suitable for CI after a full-history checkout. `--pre-push` consumes the standard Git
pre-push hook input and checks the exact outgoing object ranges, including commits pushed directly by
object ID. A failure identifies the unsafe role and commit ID without printing the address itself. The
command returns `0` when the selected checks pass, `1` for policy violations, and `2` when Git or repository
metadata cannot be inspected.

This policy is explicit rather than part of `doctor`: GitHub no-reply addresses are appropriate for
GitHub-hosted projects but should not be imposed on portable installations that use another forge.
AI_ONBOARD's own checkout activates tracked commit, merge, patch, and pre-push hooks with:

```bash
git config core.hooksPath .githooks
```

The commit-producing hooks catch unsafe process defaults early. The pre-push hook then checks the exact
outgoing commit objects, covering dangling object-ID pushes plus preserved or explicitly overridden authors
before they leave the machine. CI repeats the reachable-history check after a full checkout as defense in
depth.

## Pre-publish deployment smoke tests

Before pushing a package build, test complete isolated project and global deployments for all first-class
harnesses:

```bash
python3 scripts/test_deployments.py
```

Select one harness for a focused or verbose run:

```bash
python3 scripts/test_deployments.py --harness claude
python3 scripts/test_deployments.py --harness codex --verbose
python3 scripts/test_deployments.py --harness opencode
```

Each run snapshots the current package content so uncommitted work remains testable. For every harness it
tests both a temporary project install and an isolated fake-home global install. The project path preserves
seeded user configuration and exercises all profiles, agents, configs, notifications, workflow
foundations, Git identity, updates, previews, and cleanup. The global path verifies native user discovery
locations, launcher behavior, desired state, drift detection, updates, previews, and cleanup. No harness
login, provider credential, or model API call is required. CI runs the same contract as a three-harness
matrix on every push and pull request.

The default package channel is `stable`, which resolves the latest versioned GitHub Release. Use `edge`
only when a project intentionally tracks the latest commit on `main`, or set `source.channel` to a tag or
commit for a deliberate pin. Changing channels is explicit desired-state maintenance; upgrades never
change it silently.

Public repositories update with Python alone. For a private source repository, authenticate the GitHub CLI
with access to that repository or set `GH_TOKEN`/`GITHUB_TOKEN`; the manager uses those credentials without
storing them in desired state or the lockfile.

An upgrade follows these rules:

1. unchanged package-owned artifacts are backed up and replaced;
2. missing package-owned artifacts are restored;
3. divergent files are preserved and the incoming version is staged under `.ai-onboard/conflicts/`;
4. JSON and TOML configuration is merged at managed-key level;
5. the lockfile changes only after reconciliation succeeds.

Review and resolve conflicts manually, then run `doctor` again. Never put credentials or private data in
the desired state, lockfile, or package templates.

## Slash-command checks

Install notification assets by adding `--notifications` to `install` or `adopt`.

| Harness | Invocation | Installed source |
|---------|------------|------------------|
| Claude Code | `/ai-onboard-update` | `.claude/commands/ai-onboard-update.md` |
| OpenCode | `/ai-onboard-update` | `.opencode/commands/ai-onboard-update.md` |
| Codex | `$check-ai-onboard-updates` or natural language | Portable skill |
| Codex compatibility prompt | `/prompts:ai-onboard-update` | Copy from `.ai-onboard/share/codex-prompts/ai-onboard-update.md` to `${CODEX_HOME:-~/.codex}/prompts/` |

Codex custom prompts are deprecated, user-scoped, and loaded only when Codex starts. AI_ONBOARD therefore
keeps the shared update workflow as a skill and does not write outside the project automatically. If the
compatibility prompt is copied, restart Codex or open a new task before invoking it.

Every command checks health, caches a structured update result, reports fixes separately from local drift,
and previews an available upgrade. It never applies the upgrade without an explicit follow-up request.

## Scheduled notifications

`--notifications` installs `.github/workflows/ai-onboard-update-check.yml`. It runs weekly and on manual
dispatch, writes the structured result to the job summary, and emits a failing warning when an update is
available so normal GitHub Actions notifications can alert maintainers. Because `K95M65/AI_ONBOARD` is
private, downstream repositories must add an `AI_ONBOARD_TOKEN` Actions secret with read access; no paid
service is required.

The workflow is copied on first install, but later package changes to an active workflow are always staged
under `.ai-onboard/conflicts/` for human review rather than activated automatically.

On macOS, install a project-scoped LaunchAgent:

```bash
python3 .ai-onboard/bin/install_macos_update_notifier.py \
  install --target . --interval weekly

python3 .ai-onboard/bin/install_macos_update_notifier.py \
  status --target .

python3 .ai-onboard/bin/install_macos_update_notifier.py \
  uninstall --target .
```

The LaunchAgent runs the installed manager directly—without a shell—caches the result, and requests a
Notification Center notice only when an update exists. Its label includes a hash of the absolute project
path, so multiple projects do not collide. Run the notifier's `uninstall` action before moving the project.
The main AI_ONBOARD uninstall automatically unloads and removes a matching notifier while the project
remains at the same path; unrecognized or modified LaunchAgent files are preserved. If launchd still
reports the notifier as loaded, uninstall stops before removing the manager and tells you which
`launchctl bootout` command to retry.

## Adopt a legacy installation

Use adoption to place an existing copy-based installation under lifecycle management:

```bash
python3 /path/to/AI_ONBOARD/scripts/ai_onboard.py \
  --target /path/to/project \
  adopt \
  --harness claude,codex,opencode \
  --profile core \
  --profile product \
  --agents \
  --configs
```

Adoption does not change product files. Exact matches are recorded as `adopted`; divergent files remain
unmanaged. Default uninstall preserves adopted content.

For a legacy full-bundle installation, select all six profiles and add `--workflow-foundations`.
Add `--notifications` only when the existing project should also adopt matching notification assets.

## Uninstall and cleanup

```bash
python3 .ai-onboard/bin/ai_onboard.py uninstall --dry-run
python3 .ai-onboard/bin/ai_onboard.py uninstall
python3 .ai-onboard/bin/ai_onboard.py cleanup --keep-releases 2
```

Default uninstall:

- removes unchanged package-owned skills, agents, and manager files;
- removes the cached update status and a matching project-scoped macOS notifier;
- reverses only unchanged config keys or list entries that AI_ONBOARD added;
- preserves `AGENTS.md`, desired state, adopted content, modified files, backups, and conflicts.

`uninstall --purge` additionally removes unchanged adopted artifacts and `ai-onboard.json`. It still
preserves divergent files. `cleanup` prunes old backup sets; it does not delete unresolved conflicts.

## Recovery

If an operation is interrupted:

1. run `status` to identify missing or modified managed artifacts;
2. run `sync` to restore the locked release;
3. inspect `.ai-onboard/conflicts/` before accepting incoming content;
4. recover a prior unchanged artifact from `.ai-onboard/backups/<timestamp>/`; and
5. run `doctor` and the repository's normal checks.

The manager never treats a successful copy as proof that the installed project works. Projects retain their
own build, test, lint, browser, security, and release checks in `AGENTS.md`.
