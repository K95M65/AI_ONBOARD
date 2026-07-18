# Coordinated-view patterns

Use one canonical interaction state across every representation.

## State contract

A typical model includes:

```text
entitiesById
visibleIds
focusedId
selectedIds
activeDetailId
filters
sort
timeRange
dataVersion
```

Keep identity stable through filtering and refresh. Define how aggregates, clusters, ranges, or visual marks
map to one or many entity IDs.

## Interaction matrix

Specify expected behavior before implementation:

| Interaction | Origin view | Companion view |
|---|---|---|
| Focus or pointer hover | Show transient emphasis | Emphasize counterpart without changing selection |
| Select | Persist selected state | Emphasize and bring counterpart into view |
| Multi-select | Update one selected-ID set | Reflect the same set or meaningful aggregate |
| Clear | Remove persistent selection | Restore default emphasis |
| Filter or time change | Update shared visible set | Render the same filtered data |
| Open detail | Identify active entity | Preserve the corresponding context |

Keep transient focus separate from persistent selection. Do not let pointer movement overwrite a deliberate
selection.

## Control ownership

- Put filters, search, time range, and data scope outside both views when they affect both.
- Put zoom, pan, layers, visual extent, and visual labels inside the visual representation.
- Put columns, row density, grouping, and sorting inside the table or list.
- Show one shared legend when color or symbols have the same meaning.
- Use identical terms, number formatting, units, status semantics, and category colors.

## Cross-view navigation

When a counterpart is not visible:

- scroll a list or table row into view;
- pan or zoom a map, canvas, or timeline to the mark;
- expand a collapsed group when doing so will not destroy user context;
- explain when filtering or missing data prevents navigation;
- preserve the user's prior extent so clearing selection can return predictably.

Avoid disorienting animated travel across large visual extents. Respect reduced-motion preferences.

## Accessibility

- Provide a complete nonvisual path through the data.
- Give visual marks accessible names that match the table or list terminology.
- Move keyboard focus only when the user initiated navigation that implies it.
- Announce meaningful selection or filter results without narrating every hover.
- Do not use color as the only cross-view mapping.
- Keep focus indicators distinct from selected and highlighted states.

## Performance

- Virtualize long tables and lists.
- Update existing canvas or WebGL marks rather than reconstructing the entire scene for focus changes.
- Debounce high-frequency pointer updates without delaying deliberate selection.
- Compute shared filters and derived values once.
- Use progressive rendering or clustering only when users can still understand what is represented.
- Test with realistic item counts and worst-case overlap, not only sample data.
