---
name: cowork
description: "Invoke this skill any time two or more developers are working the same repo simultaneously and need to coordinate — the scenario where we are coding together today and do not want to overwrite each other. Handles the full lifecycle — dividing ownership before work starts, briefing a new person who joins mid-session, summarizing who currently has what, resolving disputes when two people need the same file, and closing the session. Produces a shared COWORK.md that all collaborators reference. Trigger on cowork, 協作, 分工, 一起做, collaborate, working together, 同時改, pair coding, split the work, two of us on this repo. Not for PR reviews, GitHub settings changes, or solo development tasks."
---

# cowork

Read `PROTOCOL.md` (located in the same directory as this skill) and execute the flow that matches `$ARGUMENTS`.

## Route

| $ARGUMENTS | Flow to execute |
|------------|-----------------|
| `start`    | START flow      |
| `conflict` | CONFLICT flow   |
| `status`   | STATUS flow     |
| `join`     | JOIN flow       |
| `wrap`     | WRAP flow       |
| empty      | Ask the user which mode they want, then execute it |

All logic, steps, rules, and the COWORK.md format are defined in `PROTOCOL.md`. Do not deviate from them.
