# @RSTHRIVES Portable Agent Workflow Framework website

The [AI_ONBOARD project map](https://k95m65.github.io/AI_ONBOARD/) is the public, visual explanation of the
**@RSTHRIVES Portable Agent Workflow Framework**. `AI_ONBOARD` remains the repository and install-package
name. The site is not a second documentation system: it presents the same workflow framework and reads its
catalog from canonical repository metadata.

## Purpose

The audience is a developer or team lead who feels the cost of instruction drift but does not yet know how
project context, Agent Skills, and subagents should divide responsibility.

The site should answer five questions in order:

1. **What is broken?** Tool-specific instructions fragment and self-review makes “done” ambiguous.
2. **What is the model?** Durable project context, on-demand procedures, and isolated agents solve different
   context problems.
3. **How is it managed?** Capability profiles, desired state, a lockfile, checksums, backups, and staged
   conflicts make install, upgrade, and removal inspectable.
4. **How does a request move?** An interactive router shows the orchestrator, specialists, review lenses,
   evidence, and release boundary for representative work.
5. **What is the result?** A verified handoff records what changed, which checks passed, what shipped, and
   what still needs authority.

The primary action is exploring a request route. The secondary action is installing or inspecting the
repository.

Codex, Claude Code, and OpenCode are first-class supported harnesses and must remain named on the product
page. The site should explain portability without presenting one harness as the framework's owner.

## Information architecture

The single page follows this sequence:

```text
Promise → Problem → Three mechanisms → Managed lifecycle
        → Interactive request router → Shared workflow
        → Generated skill catalog → Verified result
```

The route examples are grouped as **Create & design**, **Build & ship**, and **Research & assess**. They
cover marketing websites, interactive products, Apple applications, security, Cloudflare, market analysis,
open-source investigation, and repository delivery. They demonstrate composition; they are not an
exhaustive or hard-coded router for agent runtime. Route selection is stored in the `route` query parameter
so examples can be bookmarked and browser history restores prior choices.

## Visual direction

The design is an **operating atlas / signal-routing board**:

- warm paper, dark ink, acid lime, safety orange, and signal blue;
- compressed editorial display type paired with monospace system labels;
- visible rails, connectors, indexes, and evidence blocks instead of generic cards;
- strong focus states, semantic structure, usable contrast, reduced-motion support, and responsive layouts
  from small mobile screens through wide desktop displays.

The page uses no application framework and no runtime JavaScript dependency. Google Fonts are an optional
enhancement; local fallbacks preserve the experience if they are unavailable.

## Source and generated data

- `site/index.html` owns structure and public copy.
- `site/styles.css` owns the visual system and responsive behavior.
- `site/app.js` owns request routing, catalog filtering, and quickstart copy behavior.
- `site/data/catalog.json` is generated from canonical `skills/**/SKILL.md` and `agents/*.md` frontmatter.
- `scripts/sync_project_docs.py` generates the catalog and the marked inventory blocks in the root, skills,
  and agents READMEs.

Never edit the generated JSON or text inside a `<!-- generated:… -->` block by hand.

## Documentation maintenance contract

When changing a capability, setup path, public workflow, or repository structure:

1. update the canonical implementation or documentation;
2. update the nearest maintained README;
3. update root `README.md` if the promise, quickstart, or top-level map changed;
4. update website copy or routes if the public process changed;
5. update [`docs/install-management.md`](install-management.md) when lifecycle behavior changes;
6. run `python3 scripts/sync_project_docs.py`; and
7. run the checks below.

Manual workflow foundations remain visible in the generated catalog but are not part of the default
managed profile selection. Keep both boundaries explicit in website copy and setup documentation: GOAL and
GRILL are original AI_ONBOARD skills, are selected separately with `--workflow-foundations`, and run only
after explicit user intent. When they appear in a route, mark them as manual opt-ins that are skipped by
default rather than mandatory linear stages.

Vendored upstream READMEs are excluded from project navigation edits. Preserve their source text and
licenses.

## Local preview and checks

```bash
python3 scripts/sync_project_docs.py
python3 scripts/sync_project_docs.py --check
python3 scripts/check_skills.py
python3 scripts/check_harness_configs.py
python3 -m unittest -v tests/test_ai_onboard.py
python3 scripts/check_site.py
node --check site/app.js
python3 -m http.server 4173 --directory site
```

Then exercise the site in a real browser at <http://localhost:4173>:

- every request button changes the full route and end result;
- search and category filters work together and can be cleared;
- catalog source links point at canonical files;
- keyboard focus remains visible and follows a logical order;
- the page works at 320 px, 768 px, and a wide desktop viewport;
- 200% zoom does not cause horizontal page scrolling; and
- reduced-motion preference does not hide content.

## GitHub Pages

`.github/workflows/pages.yml` validates generated content, packages only `site/`, and deploys that artifact
with the official GitHub Pages actions. The workflow deploys from `main` and also supports manual dispatch.

The publishing target is `https://k95m65.github.io/AI_ONBOARD/`. GitHub Pages should be treated as public
output even when this repository is private; keep internal or sensitive material out of `site/` and its
generated catalog.
