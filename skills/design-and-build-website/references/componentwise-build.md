# Componentwise build

Implement the approved hierarchy and visual system in small, rendered slices.

## Fit the repository

- Read the nearest project instructions and existing component, routing, styling, data, and test patterns.
- Use the current framework and package manager unless changing them is explicitly in scope.
- Reuse sound primitives and tokens before adding variants.
- Keep content and data ownership consistent with the existing architecture.
- Avoid broad dependency upgrades during a website build.

## Build in layers

1. Establish semantic page structure, global styles, tokens, fonts, containers, and focus behavior.
2. Implement navigation, footer, buttons, links, form controls, media, and repeated content primitives.
3. Build one complete representative section and inspect it before multiplying the pattern.
4. Assemble pages in the approved content order.
5. Connect real routes, content sources, forms, analytics, and integrations.
6. Add relevant loading, empty, error, success, disabled, hover, focus, long-content, and narrow-screen
   states.

## Align repeated components

Treat repeated cards, tiles, rows, pricing blocks, testimonials, and navigation items as stable slot models:

- identify equivalent slots such as title, media, metadata, value, proof, and action;
- align equivalent slots across siblings instead of letting each instance size itself independently;
- reserve or intentionally collapse optional slots without shifting primary anchors unpredictably;
- clamp content only when necessary and make the full value available;
- test the shortest, longest, missing, localized, and high-zoom content;
- fix alignment in the shared component contract rather than nudging individual instances.

## Define done per component

Confirm:

- semantic purpose and accessible name;
- content inputs and optional-content behavior;
- variants justified by real use cases;
- keyboard and pointer behavior;
- narrow, medium, and wide layout behavior;
- long labels, zoom, text wrapping, and overflow;
- test or rendered evidence appropriate to risk.

## Inspect continuously

Render after each meaningful vertical slice. Compare the result to the page specification, not to an
imagined final polish pass. Correct hierarchy, copy, tokens, and component contracts at their source rather
than patching each occurrence.

Optimize only after the intended experience works. Keep client-side JavaScript, font payloads, and media
cost proportional to their value.
