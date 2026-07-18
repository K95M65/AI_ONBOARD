---
name: dataviz
description: Guidance for creating charts, graphs, and data visualizations that are correct, readable, and accessible. Use before writing any chart, plot, or dashboard, or when choosing chart types or colors.
---

# Data visualization

## When to use

Read this before writing the first line of chart code (any library, any medium) or choosing chart colors.

## Pick the right chart for the question

- Trend over time → **line**. Comparison across categories → **bar**. Part-to-whole → **stacked bar**
  (avoid pie beyond ~5 slices). Correlation → **scatter**. Distribution → **histogram / box**.
- **One question per chart.** If it needs a paragraph to explain, split it into two charts.

## Color

- **Categorical:** distinct hues, ~7 max; beyond that, group the tail into "other".
- **Sequential / diverging** palettes are for *ordered* data only. Never use a rainbow ramp for magnitude.
- **Never encode by color alone** — add labels, shape, or position. Check contrast and colorblind-safety.

## Make it readable

- Label axes with **units**. Start bar axes at **zero**. Sort categories by value, not alphabetically,
  unless the order is inherently meaningful.
- Prefer **direct labels** on series over a legend when you can. Cut chartjunk (heavy gridlines, 3D,
  redundant borders).

## Before shipping

- State the takeaway in **one sentence**. If the chart doesn't show it, fix the chart, not the caption.
- **Verify the numbers against the source data** before publishing.
- See [`reference.md`](reference.md) for a starter palette and the accessibility checklist.

## Note — name collision on Claude Code

Claude Code ships a **more comprehensive built-in `dataviz` skill** (with a runnable palette validator and
light/dark theming). If you're on Claude Code, prefer that one and **don't install this copy** — two skills
with the same name collide/shadow. This lean, portable version is for **Codex, opencode, and other harnesses**
(or projects) that don't have the built-in. `link.sh --skills` and the global installer copy every skill, so
delete `dataviz` from your Claude Code skills dir if the built-in is present.
