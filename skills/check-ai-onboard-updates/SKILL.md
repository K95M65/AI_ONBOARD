---
name: check-ai-onboard-updates
description: Checks a managed AI_ONBOARD installation for package updates, fixes, and security releases, reports drift separately from available releases, and offers a safe preview before applying an upgrade. Use when the user asks whether AI_ONBOARD is current, invokes the update-check workflow, or wants to review and apply an available bundle update.
---

# Check AI_ONBOARD updates

Run this workflow only in a project containing `ai-onboard.json` and
`.ai-onboard.lock.json`.

1. Check installation health without changing the project:

   ```bash
   python3 .ai-onboard/bin/ai_onboard.py doctor
   ```

2. Query the configured update channel and cache the result:

   ```bash
   python3 .ai-onboard/bin/ai_onboard.py upgrade --check --cache --json
   ```

3. Parse the JSON and report:
   - current and latest versions;
   - whether an update is available;
   - release classification (`security`, `fix`, `feature`, or `maintenance`);
   - the release summary and notes link; and
   - any separate local drift or unresolved conflicts reported by `doctor`.

4. If no update exists, stop after reporting the check time and current version.
5. If an update exists, show the user a non-mutating preview:

   ```bash
   python3 .ai-onboard/bin/ai_onboard.py upgrade --dry-run
   ```

6. Apply the upgrade only when the user asks to proceed:

   ```bash
   python3 .ai-onboard/bin/ai_onboard.py upgrade
   python3 .ai-onboard/bin/ai_onboard.py doctor
   ```

Never treat package availability as permission to overwrite conflicts, change
profiles, or purge user-owned content. Preserve the manager's distinction
between an upstream release, local drift, and staged conflicts.
