# Web application conventions

Design a browser product as an application that participates in the web platform.

## Preserve browser expectations

- Give meaningful locations stable URLs when navigation, sharing, bookmarking, refresh, or history matter.
- Preserve Back and Forward behavior; do not create an invisible navigation stack inside one URL.
- Use semantic HTML and native controls before reproducing them with generic containers.
- Make links navigate and buttons act.
- Support keyboard, pointer, touch, zoom, text resizing, reduced motion, forced colors, and assistive
  technology.
- Preserve state intentionally across refresh, reconnect, and multiple tabs.
- Warn about unsaved work only when meaningful work would actually be lost.

## Design responsively

- Start with content and command priority, then define narrow, medium, and wide arrangements.
- Allow panes to collapse into drill-in navigation or explicit view switching.
- Keep touch targets safe without making pointer layouts unnecessarily sparse.
- Test real mobile browsers, software keyboards, viewport resizing, and browser chrome where relevant.
- Avoid hover-only disclosure and essential gestures without visible alternatives.

## Communicate application context

Make organization, workspace, environment, active record, permissions, and save or sync state visible. Use
breadcrumbs, sidebars, tabs, split views, or page headers only when they match the information model.

For installable or offline-capable products, define what installation adds, what works offline, how queued
changes reconcile, and how users recognize update state. Do not imply native capabilities that the browser
experience cannot reliably provide.

## Validate

Test supported browsers, responsive sizes, keyboard-only use, zoom, assistive technology, slow and offline
networks, refresh, history, deep links, multiple tabs, failed requests, and expired sessions.
