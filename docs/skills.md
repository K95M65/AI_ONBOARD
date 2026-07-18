# Agent Skills (`SKILL.md`)

Where `AGENTS.md` tells an agent *how this project works*, a **Skill** teaches an agent *how to perform a
specific task* — and only loads when that task comes up. Skills are a **progressive-disclosure** format:
the agent sees a one-line description of every available skill up front, and pulls in the full instructions
(and any bundled scripts) only when it decides the skill is relevant. That keeps context cheap while giving
the agent deep, on-demand expertise.

Skills began at Anthropic but are now an **open, cross-vendor standard** ([agentskills.io](https://agentskills.io),
Dec 2025): the *same* `SKILL.md` folder runs in **Claude Code and Codex** (and 30+ other tools) with no
wrapper and no translation. That makes a skill the most portable artifact in this repo — author it once,
install it into each harness's skills directory.

## Anatomy

A skill is a **folder** containing a `SKILL.md`, plus optional supporting files:

```
my-skill/
├── SKILL.md            # required — frontmatter + instructions
├── reference.md        # optional — deeper docs loaded on demand
├── scripts/
│   └── run.py          # optional — executable helpers the agent can call
└── templates/
    └── example.txt     # optional — assets the skill uses
```

## `SKILL.md` frontmatter

```markdown
---
name: pdf-form-filler
description: Fills PDF forms from a JSON data file. Use when the user needs to populate a fillable PDF, or asks to batch-fill form templates.
---

# PDF Form Filler

## When to use
Use this when the user provides a fillable PDF and structured data to put into it.

## Steps
1. Inspect the form fields: `python scripts/inspect.py <file.pdf>`.
2. Map the user's data to field names.
3. Fill and save: `python scripts/fill.py <file.pdf> <data.json> <out.pdf>`.

## Notes
- If the PDF is flattened (no fillable fields), say so and offer to overlay text instead.
```

**The two fields that matter:**

- **`name`** — lowercase, hyphenated, unique. This is the skill's identifier.
- **`description`** — the single most important line in the file. It's the *only* text the agent sees when
  deciding whether to invoke the skill, so it must state **what the skill does** *and* **when to use it**.
  Write it in the third person. Vague descriptions ("helps with PDFs") never get triggered; specific
  trigger-laden ones ("Use when the user needs to fill a fillable PDF form from JSON") do.

Some harnesses support extra optional fields (e.g. `allowed-tools` to restrict what the skill may run). Keep
these tool-specific extras minimal if you want the skill to stay portable.

## Design principles

1. **One skill, one job.** A skill that does three things gets triggered for none of them well. Split it.
2. **Front-load the trigger in `description`.** The agent matches on it — spell out the *when*.
3. **Keep `SKILL.md` lean; push depth into referenced files.** The body is loaded when triggered; a linked
   `reference.md` is loaded only if the agent needs it. This is the progressive-disclosure payoff.
4. **Prefer scripts for deterministic work.** If a step is "parse this format" or "do this math," ship a
   script and have the skill call it, rather than asking the model to do it by hand.
5. **Write instructions, not prose.** Numbered steps and exact commands. The agent is following, not reading.
6. **Make it self-contained.** Bundle the templates and scripts it needs so it works dropped into any repo.

## Where skills live

The same skill folder is discovered from different directories per harness:

| Harness | Personal (all projects) | Project (team-shared) |
|---------|-------------------------|-----------------------|
| **Claude Code** | `~/.claude/skills/<name>/` | `.claude/skills/<name>/` |
| **Codex** | `~/.agents/skills/<name>/` | `.agents/skills/<name>/` |

> Codex uses the **vendor-neutral `.agents/skills/`** path — **not** `.codex/skills/` (a common third-party
> error). It scans `.agents/skills` from the cwd up to the repo root, then `~/.agents/skills`.

This repo's [`skills/`](../skills/) directory holds portable, reusable skills. Copy — or symlink — a folder
into the paths above; a symlink from one canonical copy into both trees keeps them in sync with zero
duplication.

## Portable across harnesses — three things to get right

1. **Keep frontmatter to the shared subset.** Only `name` + `description` are universal. Avoid tool-specific
   frontmatter keys in `SKILL.md` if you want one file to serve both harnesses.
2. **Make scripts self-locating.** Resolve paths relative to the script
   (`SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"`), never the caller's cwd — the harness that
   invokes the skill sets a different working directory. This is the one real portability gotcha.
3. **Codex-only extras are optional and ignorable.** Codex supports an `agents/openai.yaml` sidecar (UI
   metadata, `allow_implicit_invocation`) and a `[[skills.config]]` enable/disable list in its config. Claude
   Code ignores the sidecar. Note: per-subagent `skills.config` scoping is currently unreliable in Codex
   ([#14161](https://github.com/openai/codex/issues/14161)) — assume skills are **session-global** for now.

## Skills vs. AGENTS.md — when to use which

| | `AGENTS.md` | Skill |
|---|-------------|-------|
| **Loaded** | Every session, always | On demand, when triggered |
| **Answers** | "How does *this project* work?" | "How do I *do this task*?" |
| **Scope** | This repository | Reusable across repositories |
| **Cost** | Paid every session | Paid only when used |

Put durable, project-wide facts in `AGENTS.md`. Package a repeatable procedure — especially one with scripts
or a specific workflow — as a Skill.

For the full decision — including **skill vs *subagent*** (same expertise, different delivery) — see
[`mechanisms.md`](mechanisms.md).
