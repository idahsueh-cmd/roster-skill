---
name: roster
version: 1.0.0
description: Pre-PR coordination protocol for project-local AI tools.

claude:
  description: "Invoke this skill any time two or more developers are working the same repo simultaneously and need to coordinate before a PR exists — the scenario where we are coding together today and do not want to overwrite each other. Handles the full lifecycle — dividing session ownership before work starts, briefing a new person who joins mid-session, summarizing who currently has what, resolving disputes when two people need the same file, and closing the session. Produces a shared ROSTER.md that all collaborators reference. Trigger on roster, cowork, 協作, 分工, 一起做, collaborate, working together, 同時改, pair coding, split the work, two of us on this repo. Not for CODEOWNERS replacement, PR reviews, GitHub settings changes, or solo development tasks."
cursor:
  description: "Use when coordinating multi-person development on the same repo before PR review. Trigger on: roster, cowork, collaborate, split the work, working together, two of us on this, session ownership, who is touching what."
windsurf:
  description: "Roster protocol — activate when multiple developers need to coordinate pre-PR work on the same repository without overwriting each other."
codex:
  description: "Multi-developer coordination protocol. Use when two or more people are working the same repo simultaneously and need to divide temporary session ownership."
---

# Roster Protocol v1.0

Tool-agnostic coordination rules for two or more people working the same repo simultaneously before PR review begins. Any AI assistant (Claude Code, Cursor, Gemini, Copilot, plain ChatGPT) can execute this protocol by following the steps below.

Roster does not replace CODEOWNERS, branch protection, issue trackers, or PR review. CODEOWNERS tracks long-lived review responsibility and can enforce approval before merge. Roster tracks short-lived session intent: who is touching what today, before a PR exists.

---

## ROSTER.md — The Shared Artifact

Every session produces one `ROSTER.md` at the repo root. All collaborators read from this file. It is the single source of truth for who is touching what during the current session.

### Format

```markdown
# ROSTER Session — <YYYY-MM-DD>
Collaborators: <name>, <name>, ...

## Tasks
- <Name>: <one-sentence description of what they're building today>

## Ownership
| File / Directory         | Session Owner | Consult / Notify | Notes                              |
|--------------------------|---------------|------------------|------------------------------------|
| src/feature-x/           | Alice         | Bob              |                                    |
| src/feature-y/           | Bob           | Alice            |                                    |
| package.json             | ALL           | ALL              | needs agreement before changing    |
| src/styles/theme.css     | ALL           | ALL              | needs agreement before changing    |

## Open Conflicts
<!-- Log any unresolved disputes here during the session -->

## Conflict Rules
- Technical detail → Session Owner decides, notifies others
- Design / architecture / shared config → all involved must agree before anyone proceeds

## Wrap
When done: each person creates a handoff / summary independently, then opens a PR.
```

**When to split into `ROSTER-detail.md`:** If the session ownership table exceeds 60 rows (typically 3+ collaborators with large tasks), move detailed rows to `ROSTER-detail.md` and keep `ROSTER.md` as a summary index pointing to it.

---

## Flows

### START

**Purpose:** Kick off a roster session before anyone writes code. Target: under 30 seconds.

**Steps:**

1. **Scan silently** — read `CLAUDE.md`, `README.md`, CODEOWNERS, and any rules files. Run `git log --oneline -20` to see recent contributors and active areas. Survey the top-level directory structure. If CODEOWNERS exists, use it as background context for sensitive areas and likely review responsibility, not as the session plan.

2. **Ask one question:**
   > Who is working today, and what is each person building? (one line per person)
   > Example: "Ida: new pricing page / Jason: dark mode toggle / Mei: CMS API"

3. **Draft the session ownership table** — from each person's description, infer the files and directories they will likely touch. Do not ask the user to fill this in. Auto-assign shared infrastructure (`package.json`, lockfiles, config files, design tokens, CI files, `CLAUDE.md`, `AGENTS.md`, CODEOWNERS) as `ALL`.

4. **Confirm, do not fill** — show the draft `ROSTER.md` and ask: "Does this look right? Any files to add, move, or change session ownership on?" Apply corrections. If no corrections, proceed immediately.

5. **Write `ROSTER.md`** to the repo root.

6. **One-line close** — "ROSTER.md is live. Share it with everyone. Use `/roster conflict` if two people need the same file."

---

### CONFLICT

**Purpose:** Resolve a dispute when someone needs to touch another person's session area, or when session ownership was never defined.

**Steps:**

1. Ask **in a single message**:
   - What file or directory is in dispute?
   - Why does each person need to touch it? (one sentence per person)
   - Is this a **technical implementation detail**, or a **design/architecture/shared-config decision** that affects the whole codebase?

2. Apply the rule:
   - **Technical detail** → the Session Owner makes the call, then notifies everyone else. No vote needed.
   - **Design / architecture / shared config** → no one proceeds until all involved agree. Recommend a quick sync call if async agreement is taking too long.

3. If the ruling changes session ownership, update the `ROSTER.md` Ownership table and log the resolution under `## Open Conflicts`.

---

### STATUS

**Purpose:** Get a quick snapshot of where the session stands.

**Steps:**

1. Read `ROSTER.md` (and `ROSTER-detail.md` if it exists). Do not ask the user anything.

2. Output a one-screen summary:
   - Who has session ownership of what (condensed, not the raw table)
   - Files marked "needs agreement" that have no logged resolution yet
   - Any open conflicts in `## Open Conflicts`
   - Next logical step for each person

---

### JOIN

**Purpose:** Bring a new collaborator up to speed and add them to an ongoing session.

**Steps:**

1. Read `ROSTER.md`. Brief the new person in plain language:
   - What the session is about
   - Who is working on what
   - What areas are off-limits (other people's session ownership zones)
   - What files need agreement before touching

2. Ask **in a single message**:
   - New person's name?
   - What are they building today? (one sentence)

3. Map their task to files, assign Session Owner + Consult / Notify for their new areas, update the `ROSTER.md` Ownership table.

4. Remind them: if they need to touch someone else's area, use the conflict flow first.

---

### WRAP

**Purpose:** Close the session cleanly and hand off to the next phase (PRs, merges, handoffs).

**Steps:**

1. **If multiple PRs are open**, determine merge order:
   - PRs that touch shared files (marked `ALL`) go last.
   - PRs with no shared-file overlap can merge in any order.
   - Suggest a specific merge sequence.

2. Run through the checklist for each collaborator:
   - Branch up to date with main? (`git pull origin main`)
   - Build passes?
   - Any unresolved conflicts in `ROSTER.md`?
   - PR opened?

3. Remind every collaborator to create their own handoff/session summary in their own AI session.

4. Archive the session files:
   - Rename `ROSTER.md` → `ROSTER-<YYYY-MM-DD>.md`
   - Rename `ROSTER-detail.md` → `ROSTER-detail-<YYYY-MM-DD>.md` (if it exists)

---

## Conflict Resolution Reference

| Situation | Who decides | Required action |
|-----------|-------------|-----------------|
| Two people want to edit the same component | Session Owner of that file | Session Owner decides, notifies others |
| Design token or theme change | Everyone affected | Sync required before proceeding |
| Adding a new dependency | All collaborators | Agreement required (affects build for everyone) |
| Bug fix inside one person's session area | That person | No coordination needed |
| API contract change | All collaborators | Agreement required (affects frontend and backend) |
| Config / CI / CODEOWNERS file | All collaborators | Agreement required |

---

## Scope Limits

This protocol is for **same-time collaboration** on the same repo. Do not use it for:
- Code review (async, single reviewer)
- GitHub settings or admin changes
- Solo development tasks
- Long-term ownership or required reviewer enforcement; use CODEOWNERS for that
