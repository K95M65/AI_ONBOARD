---
name: obsidian
description: Read and write notes in an Obsidian vault — markdown with wikilinks, tags, YAML frontmatter, daily notes, and folder conventions. Use when creating, linking, or organizing notes in an Obsidian vault, or building a note from a template.
---

# Obsidian

An Obsidian vault is just a folder of Markdown files — no lock-in, so work with the files directly. These are
the conventions that keep a vault navigable.

## When to use

Creating, linking, or organizing notes in an Obsidian vault.

## Conventions

- **Wikilinks:** `[[Note Title]]` links by note *name* (not path); `[[Note#Heading]]` targets a heading;
  `[[Note|alias]]` sets display text. Prefer wikilinks over paths so links survive moves.
- **Frontmatter:** YAML between `---` fences at the very top. Obsidian reads `tags:`, `aliases:`, and
  arbitrary keys (queryable via Dataview). Keep it minimal and consistent.
- **Tags:** `#tag` inline or in `tags:` frontmatter; nest with `/` (`#project/ai`). Keep the taxonomy shallow.
- **Daily notes:** one per day (e.g. `Daily/2026-07-18.md`); link out to permanent notes from there.
- **Embeds/attachments:** `![[image.png]]` embeds; keep attachments in a dedicated folder.

## Create a note

```bash
bash scripts/new-note.sh "<Title>" [folder] [tag ...]
```
Creates `<folder>/<Title>.md` with `title`/`date`/`tags` frontmatter, ready to fill. Refuses to overwrite.

## Structure patterns

- **PARA** (Projects/Areas/Resources/Archive) or **Zettelkasten** (atomic notes + dense links). Pick one.
- **One idea per note**; let structure emerge from links, not deep folder trees.

## Rules

- **Prefer links over folders** — the graph is Obsidian's strength.
- When editing files directly, **update wikilinks yourself** (Obsidian's in-app rename updates backlinks; a
  raw file rename does not).
- Keep filenames stable — a note's name *is* its link target.
