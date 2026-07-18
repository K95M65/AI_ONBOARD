# Mobile platform conventions

Design iOS, iPadOS, and Android surfaces for touch, interruption, constrained attention, variable
connectivity, and platform navigation. Check current Apple and Android guidance for exact conventions.

## Choose a navigation model

- Keep the primary destinations few and stable.
- Preserve each platform's back behavior and navigation expectations.
- Use tabs for peer destinations, stacks for drill-in work, and modals for bounded secondary tasks.
- Adapt large-screen tablets through sidebars, split views, panes, keyboard support, and pointer support
  rather than stretching a phone column.
- Keep the current account, object, environment, and unsaved state visible when actions have meaningful
  scope.

## Design for touch and mobility

- Give targets sufficient size and separation.
- Avoid hover dependence and undiscoverable gestures.
- Keep primary actions reachable without obscuring content or system gestures.
- Handle software keyboards, safe areas, rotation, text scaling, and one-handed use.
- Request camera, location, microphone, photos, contacts, or notification access in context and explain the
  benefit before the system prompt.
- Preserve work through interruption, backgrounding, process termination, and connectivity changes.

## Respect platform identity

Share product concepts, data, and brand while allowing navigation, controls, typography, icons, motion,
permissions, and system surfaces to follow the target platform. Do not force pixel-identical iOS and Android
interfaces when it makes either feel foreign.

Use native accessibility semantics and system controls where possible. Provide visible alternatives for
gesture shortcuts and haptic-only feedback.

## Validate

Test small and large phones, tablets where supported, orientation, software keyboards, dynamic text sizes,
screen readers, switch or keyboard access, reduced motion, high contrast, light and dark appearance, slow or
offline networks, background and resume, permission denial, deep links, notifications, and store release
requirements.
