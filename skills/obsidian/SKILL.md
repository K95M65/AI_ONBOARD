---
name: obsidian
description: Read and write notes in an Obsidian vault — markdown with wikilinks, tags, YAML frontmatter, daily notes, and folder conventions. Use when creating, linking, or organizing notes in an Obsidian vault, or building a note from a template.
---

# Obsidian

An Obsidian vault is just a folder of Markdown files — no lock-in, so work with the files directly. These are
the conventions that keep a vault navigable.

## Choose the integration level

1. **Direct files (default)** — read and edit Markdown in the vault with normal filesystem tools. This is
   portable, local, and requires no account, plugin, Sync subscription, or API key.
2. **Obsidian URI (optional)** — use the official `obsidian://` actions to open, create, append, or search
   when launching the desktop app improves the workflow.
3. **Local REST or MCP (optional)** — use an already-installed community integration when the user needs
   active-file access, command execution, structured search, or surgical patches. Treat its local API key as
   a secret and do not install or enable a plugin without permission.

Do not require paid Obsidian Sync or Publish. Let the user's existing filesystem or synchronization method
own cross-device transport.

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
- When persisting technical research, include source URLs, the relevant software version, retrieval date,
  and an invalidation condition. Compose with `retrieve-technical-docs` for that workflow.
