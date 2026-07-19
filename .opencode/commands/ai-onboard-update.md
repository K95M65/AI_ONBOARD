---
description: Check AI_ONBOARD for updates, fixes, and security releases
---

Use the `check-ai-onboard-updates` skill.

Run `python3 .ai-onboard/bin/ai_onboard.py doctor`, then run
`python3 .ai-onboard/bin/ai_onboard.py upgrade --check --cache --json`.
Report the current and latest versions, release classification, summary, notes
link, local drift, and conflicts. If an update exists, run
`python3 .ai-onboard/bin/ai_onboard.py upgrade --dry-run` and summarize the
preview. Do not apply the upgrade unless the user explicitly asks.
