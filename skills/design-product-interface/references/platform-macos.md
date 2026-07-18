# macOS conventions

Design for macOS as a windowed, keyboard-and-pointer operating system. Check the current Apple Human
Interface Guidelines and SDK documentation when exact behavior or APIs matter.

## Model the application

- Decide whether the product is document-based, library-based, utility-like, menu-bar based, or a persistent
  workspace. Let that model govern windows, save behavior, reopening, and navigation.
- Support window resizing, full screen, multiple displays, and multiple windows when the work benefits from
  comparison or independent placement.
- Set useful minimum sizes and define how sidebars, inspectors, toolbars, and content adapt as space changes.
- Preserve window, pane, column, and selection state when that helps users resume work.

## Put commands where macOS users expect them

- Expose application-wide and document commands in the menu bar.
- Use standard command names, ordering, roles, and keyboard shortcuts where equivalents exist.
- Keep frequent contextual actions in toolbars, inspectors, or contextual menus without hiding their menu
  equivalents.
- Support undo and redo for meaningful editing operations.
- Make keyboard focus, traversal, default actions, cancellation, and shortcut conflicts deliberate.
- Use the system settings location and terminology appropriate to the app architecture.

Do not transplant mobile bottom navigation, browser-style page chrome, or custom window controls into a
desktop app without a product-specific reason.

## Use native structure deliberately

- Use sidebars for stable collections or top-level destinations.
- Use toolbars for frequent commands that affect the window or current content.
- Use inspectors for properties of the current selection.
- Use sheets or alerts for decisions scoped to a window or document.
- Use separate windows for sustained tasks that need independent placement.
- Prefer native controls, typography, symbols, materials, selection, menus, and drag-and-drop behavior when
  they improve familiarity and accessibility.

Brand the content and visual system without making system controls unrecognizable.

## Integrate with the operating system

Consider only integrations the product needs: files and documents, drag and drop, clipboard, services,
Quick Look, share actions, notifications, menu-bar presence, dock behavior, recent items, restoration,
Spotlight, shortcuts, and automation.

Ask for permissions in context, explain their purpose, handle denial, and keep the useful non-permissioned
path available where possible.

## Validate

Test:

- keyboard-only operation, menus, shortcuts, focus, VoiceOver, reduced motion, increased contrast, and text
  or display scaling;
- small and large windows, full screen, multiple displays, light and dark appearance, and accent changes;
- file open, save, autosave, duplicate, rename, move, close, reopen, crash recovery, and conflicts when
  applicable;
- pointer, trackpad, drag and drop, contextual menus, clipboard, and system permission denial;
- packaging, signing, notarization, sandbox entitlements, update behavior, and distribution requirements
  through the repository's release process.
