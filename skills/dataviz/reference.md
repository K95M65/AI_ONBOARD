# Data visualization — reference

Loaded on demand. Keep the [`SKILL.md`](SKILL.md) lean; the depth lives here.

## Starter categorical palette

A brand-neutral, colorblind-considerate set — swap for your design tokens. Distinct in hue and lightness so
series stay separable in grayscale:

| # | Hex | Note |
|---|-----|------|
| 1 | `#4E79A7` | blue |
| 2 | `#F28E2B` | orange |
| 3 | `#59A14F` | green |
| 4 | `#E15759` | red |
| 5 | `#B07AA1` | purple |
| 6 | `#76B7B2` | teal |
| 7 | `#EDC948` | yellow |

- **Sequential** (one hue, light→dark) for magnitude; **diverging** (two hues around a neutral midpoint) for
  data with a meaningful center (e.g. +/- change).

## Accessibility checklist

- [ ] Contrast ≥ 3:1 for graphical objects against their background (WCAG 1.4.11).
- [ ] Information is not conveyed by **color alone** — labels, patterns, or direct annotation back it up.
- [ ] Palette is distinguishable under deuteranopia/protanopia (test with a simulator).
- [ ] Text (axis, labels) meets ≥ 4.5:1 contrast.
- [ ] Interactive charts are keyboard-navigable and expose values to a screen reader (data table fallback).

## Common mistakes

- Truncated bar axes that exaggerate differences (bars must start at zero; lines may not).
- Dual y-axes implying a correlation that isn't there.
- Too many series — if you can't direct-label them, you have too many.
- Pie/donut for comparison — humans read angles poorly; use a bar.
