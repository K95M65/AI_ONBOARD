# Platform accessibility checks

Load the applicable sections and verify exact current requirements against official guidance.

## All platforms

- Give every control an understandable name, role, value, state, and available action.
- Preserve logical reading, navigation, focus, and interaction order.
- Keep targets usable without fine pointer precision or gesture-only knowledge.
- Provide visible and programmatic status, validation, error, and completion feedback.
- Support text enlargement, contrast settings, reduced motion, and alternative input.
- Do not rely on color, shape, location, sound, or motion alone.
- Avoid unexpected context changes, time pressure, flashing, and irreversible action without confirmation.
- Keep language direct, instructions local, terminology consistent, and recovery explicit.
- Test long strings, pluralization, bidirectional text, and layouts that expand.

## Web

- Inspect native HTML semantics before adding ARIA.
- Verify heading and landmark structure, accessible names, relationships, live updates, table semantics,
  dialogs, route changes, and focus management.
- Exercise keyboard-only operation, skip paths, focus visibility, zoom, reflow, high contrast, and reduced
  motion.
- Confirm browser and screen-reader combinations within the product's support policy.

## Apple platforms

- Inspect the accessibility tree, labels, values, hints, traits, actions, grouping, sort priority, and focus.
- Exercise VoiceOver, Full Keyboard Access, Voice Control, Switch Control, Dynamic Type or larger text,
  Increase Contrast, Differentiate Without Color, Reduce Transparency, Reduce Motion, and audio settings
  where supported.
- Prefer standard SwiftUI, AppKit, or UIKit behavior; verify custom drawing and gestures explicitly.
- On macOS, verify menu and command discovery, window and sheet focus, toolbar and sidebar navigation,
  keyboard shortcuts, and accessibility behavior across multiple windows.

## Android

- Inspect semantics, labels, roles, state descriptions, traversal order, live regions, and custom actions.
- Exercise TalkBack, keyboard or switch access, font and display scaling, contrast, magnification, and
  remove-animations settings where supported.
- Verify custom gestures have discoverable, operable alternatives.

## Windows and Linux desktop

- Inspect the platform accessibility tree and automation properties.
- Exercise keyboard and screen-reader navigation, system scaling, high-contrast themes, reduced animation,
  window management, menus, and dialogs.
- Verify custom canvases expose meaningful objects and actions rather than one opaque surface.
