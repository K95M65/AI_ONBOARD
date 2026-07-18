# Desktop and cross-platform conventions

Design Windows, Linux, Electron, Tauri, Qt, and other desktop applications around sustained work,
resizable windows, keyboard and pointer input, and operating-system integration.

## Establish the desktop model

- Define whether the app is document-based, library-based, a utility, or a persistent workspace.
- Support useful resizing, minimum sizes, multiple displays, and multiple windows where appropriate.
- Preserve window geometry, pane proportions, navigation, selection, and recent work when it helps users
  resume.
- Use space for comparison, persistent context, and efficient commands rather than simply enlarging mobile
  layouts.

## Adapt by operating system

Keep the shared product model stable while allowing each target to vary:

- menu structure, command names, shortcuts, and modifier keys;
- title bars, window controls, dialogs, notifications, settings locations, and file pickers;
- typography, icons, focus treatment, selection, density, and system themes;
- installation, updates, permissions, packaging, and accessibility APIs.

Use framework abstractions where they preserve expected behavior. Add platform-specific implementation when
an abstraction makes the product feel foreign, blocks accessibility, or hides essential integration.

## Support efficient work

- Make frequent commands visible and give them shortcuts.
- Support contextual menus as accelerators, not the sole discovery path.
- Design reliable focus order, selection, multi-selection, drag and drop, clipboard, undo, and redo.
- Separate navigation, object commands, view controls, and selection-level bulk actions.
- Use toolbars, sidebars, inspectors, status areas, command palettes, and separate windows according to task
  scope.

## Validate

Test every supported operating system rather than assuming cross-platform rendering means cross-platform
behavior. Exercise keyboard and pointer use, screen readers, scaling, high contrast, system themes, window
resizing, multiple displays, file and clipboard integration, permission denial, install, update, uninstall,
crash recovery, and the repository's packaging and signing workflow.
