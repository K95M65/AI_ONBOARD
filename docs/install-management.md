# Managed installation, upgrades, and cleanup

AI_ONBOARD's lifecycle manager installs a selected capability surface, records exactly what it owns, and
refuses to overwrite or remove divergent user content. It is a dependency-free Python 3 script:
[`scripts/ai_onboard.py`](../scripts/ai_onboard.py).

`templates/link.sh` remains available for legacy copy-based wiring. It is intentionally not upgrade-aware;
use the manager for new installations.

## Install from a clone

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
| `.ai-onboard/` | Installed manager, local backups, and staged conflicts | No; its nested `.gitignore` protects it |

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
python3 .ai-onboard/bin/ai_onboard.py upgrade --dry-run
python3 .ai-onboard/bin/ai_onboard.py upgrade
python3 .ai-onboard/bin/ai_onboard.py doctor
```

The initial package channel is `edge`, which resolves the latest commit on `main`. Change
`source.channel` in `ai-onboard.json` to `stable` after the repository publishes versioned GitHub Releases,
or set it to a tag or commit for a deliberate pin.

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

## Uninstall and cleanup

```bash
python3 .ai-onboard/bin/ai_onboard.py uninstall --dry-run
python3 .ai-onboard/bin/ai_onboard.py uninstall
python3 .ai-onboard/bin/ai_onboard.py cleanup --keep-releases 2
```

Default uninstall:

- removes unchanged package-owned skills, agents, and manager files;
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
