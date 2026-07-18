# macOS engineering

Translate the product model into macOS application structure without treating the Mac as a large iPhone.

## Choose the application model

Identify whether the app is document-based, library-based, utility-like, menu-bar based, a persistent
workspace, an agent or service, or a combination. Align lifecycle and restoration with that model:

- define scenes and windows by sustained user tasks;
- use document architecture for user-owned files that need open/save/autosave/recovery semantics;
- preserve window, pane, selection, and document state where resumption matters;
- support multiple windows, tabs, full screen, and external displays only where the work benefits.

Use SwiftUI lifecycle and controls where they satisfy the behavior and deployment targets. Bridge to AppKit
for capabilities that require it, keeping the boundary small and testable. Preserve an existing AppKit
architecture instead of forcing migration.

## Implement commands and settings

- Put application and document commands in standard menu locations with standard roles and names.
- Keep shortcuts discoverable through menus and resolve conflicts deliberately.
- Support undo and redo through the document or model transaction boundary.
- Scope toolbars to the window, inspectors to the selection, sheets to their parent window, and contextual
  menus to the clicked object.
- Use the project's settings scene or AppKit preferences architecture; keep stored defaults separate from
  transient session state.
- Define focus and key-view traversal. Ensure important actions work by keyboard without requiring pointer
  discovery.

## Integrate with macOS deliberately

Implement only integrations required by the product: file coordination and security-scoped URLs, drag and
drop, pasteboard, Services, Quick Look, sharing, notifications, Spotlight, Shortcuts/App Intents, login
items, dock behavior, menu-bar extras, recent items, or automation.

For each integration:

1. Identify the owning process, lifecycle, data boundary, and failure behavior.
2. Request permissions in context and preserve a useful denial path where possible.
3. Add the minimum sandbox entitlement and capability required.
4. Validate from a signed or sandboxed build when debug execution would hide the constraint.

Never weaken the App Sandbox, hardening, library validation, or privacy protections merely to make a debug
path pass.

## Handle system variation

Test light and dark appearance, accent changes, reduced motion, increased contrast, VoiceOver, display
scaling, long and localized content, small and large windows, full screen, multiple displays, sleep/wake,
termination, reopen, and denied permissions as applicable.

Use availability checks for newer APIs and preserve behavior on every declared deployment target. Prefer a
clear reduced capability over an untested imitation of a newer system feature.
