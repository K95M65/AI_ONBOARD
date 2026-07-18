---
name: coordinate-data-views
description: Designs and implements synchronized representations of the same data, such as table plus chart, list plus map, or records plus diagram or timeline. Use when users need to select, inspect, filter, or navigate the same entities across two complementary views in a web, desktop, or mobile product.
---

# Coordinate data views

Design two representations as one interaction system. Use this only when each view supports a distinct user
task; do not add a chart, map, canvas, or diagram merely for visual richness.

## Confirm the pairing

Proceed when:

1. Both views represent the same identifiable entities or aggregates.
2. Each view answers a different important question.
3. Users need to move between the views during one workflow.
4. The added synchronization cost is justified by task value.

Choose which view is primary. A table may lead precise comparison while a map supplies spatial context; a
diagram may lead relationship exploration while a list supplies searchable detail.

## Define the shared interaction model

Read [references/patterns.md](references/patterns.md). Specify:

- stable identity and mapping between representations;
- shared filters, time range, search, and data freshness;
- transient hover or focus, persistent selection, multi-selection, and active detail;
- commands that affect shared data versus one representation only;
- color, symbols, terminology, and legend semantics;
- cross-view navigation and scroll or pan behavior;
- empty, loading, partial, stale, filtered, and error states.

Keep shared state in one authoritative model. Each view reads and changes that state; neither maintains a
private competing selection or filter.

## Choose the platform arrangement

- **Wide web or desktop:** Use side-by-side panes when both views need simultaneous attention. Size the
  primary view generously and allow a useful adjustable split when appropriate.
- **Narrow web or mobile:** Switch between views with a platform-appropriate tab, segmented control, or
  drill-in path while preserving shared state.
- **Windowed desktop:** Consider separate synchronized windows only when independent placement, multiple
  displays, or comparison materially improves the work.
- **Touch:** Do not depend on hover. Make selection, detail, and reset controls explicit.
- **Keyboard and assistive technology:** Make the data representation operable without the visual view and
  announce cross-view selection changes meaningfully.

## Implement in vertical slices

1. Establish canonical IDs, shared state, and one small realistic dataset.
2. Implement selection from the primary view.
3. Reflect selection and focus in the companion view.
4. Implement the reverse direction and bring the counterpart into view.
5. Add shared filters and representation-specific controls.
6. Add large-data performance, complete states, and platform adaptation.

Reuse central formatting and semantic-color definitions. Do not duplicate data interpretation in separate
renderers.

## Validate

Test:

- selection, multi-selection, hover where applicable, focus, clearing, and Escape or platform equivalent;
- filtering, sorting, zooming, panning, time changes, and stale or refreshed data;
- counterpart visibility when the destination is off-screen or outside the visual extent;
- screen reader and keyboard operation without requiring the visual representation;
- narrow, wide, touch, pointer, and supported desktop arrangements;
- empty, one-item, large, overlapping, missing-geometry, and partial datasets;
- rendering and interaction performance with realistic scale.

Report the primary view, shared state contract, platform adaptations, task scenarios exercised, and any
remaining performance or accessibility limitations.
