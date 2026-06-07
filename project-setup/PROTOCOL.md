---
name: cowork
version: 1.0.0
description: Multi-agent collaboration protocol for project-local AI tools.

claude:
  description: "Invoke this skill any time two or more developers are working the same repo simultaneously and need to coordinate — the scenario where we are coding together today and do not want to overwrite each other. Handles the full lifecycle — dividing ownership before work starts, briefing a new person who joins mid-session, summarizing who currently has what, resolving disputes when two people need the same file, and closing the session. Produces a shared COWORK.md that all collaborators reference. Trigger on cowork, 協作, 分工, 一起做, collaborate, working together, 同時改, pair coding, split the work, two of us on this repo. Not for PR reviews, GitHub settings changes, or solo development tasks."
cursor:
  description: "Use when coordinating multi-person development on the same repo. Trigger on: cowork, collaborate, split the work, working together, two of us on this, handoff ownership, who owns what."
windsurf:
  description: "Cowork protocol — activate when multiple developers need to coordinate work on the same repository without overwriting each other."
codex:
  description: "Multi-developer coordination protocol. Use when two or more people are working the same repo simultaneously and need to divide file ownership."
---

# Cowork Protocol v1.0

Tool-agnostic coordination rules for two or more people working the same repo simultaneously. Any AI assistant (Claude Code, Cursor, Gemini, Copilot, plain ChatGPT) can execute this protocol by following the steps below.

---

## COWORK.md — The Shared Artifact

Every session produces one `COWORK.md` at the repo root. All collaborators read from this file. It is the single source of truth for who owns what.

### Format

```markdown
# COWORK Session — <YYYY-MM-DD>
Collaborators: <name>, <name>, ...

## Tasks
- <Name>: <one-sentence description of what they're building today>

## Ownership
| File / Directory         | Owner | Reviewer | Notes                              |
|--------------------------|-------|----------|------------------------------------|
| src/feature-x/           | Alice | Bob      |                                    |
| src/feature-y/           | Bob   | Alice    |                                    |
| package.json             | ALL   | ALL      | needs agreement before changing    |
| src/styles/theme.css     | ALL   | ALL      | needs agreement before changing    |

## Open Conflicts
<!-- Log any unresolved disputes here during the session -->

## Conflict Rules
- Technical detail → Owner decides, notifies others
- Design / architecture / shared config → all involved must agree before anyone proceeds

## Wrap
When done: each person creates a handoff / summary independently, then opens a PR.
```

**When to split into `COWORK-detail.md`:** If the ownership table exceeds 60 rows (typically 3+ collaborators with large tasks), move detailed rows to `COWORK-detail.md` and keep `COWORK.md` as a summary index pointing to it.

---

## Flows

### START

**Purpose:** Kick off a new cowork session before anyone writes code.

**Steps:**

1. Read the project silently: look for `CLAUDE.md`, `README.md`, any rules or conventions files.

2. Ask the group **in a single message**:
   - Does everyone already have repo access? (If not: go to repo Settings → Collaborators → invite before continuing.)
   - List all collaborators and what each person is building today — one line each.
   - Any files or areas already known to be sensitive (only one person should touch)?

3. Map each person's task to the files/directories they'll likely touch.

4. Identify overlap zones (multiple people may need the same file). For each overlap:
   - Assign one **Owner** (whose task depends on it most) and one **Reviewer**.
   - If no clear owner: mark as `ALL` + "needs agreement before changing".

5. Treat shared infrastructure as `ALL` by default: `package.json`, `package-lock.json`, lockfiles, config files, design tokens, API contracts, CI/CD files, CLAUDE.md.

6. Write `COWORK.md` following the format above (keep under 100 lines).

7. Tell all collaborators: share this file, use the conflict flow if disputes arise, use the status flow to check state at any time, use the join flow if someone new arrives.

---

### CONFLICT

**Purpose:** Resolve a dispute when someone needs to touch another person's area, or when ownership was never defined.

**Steps:**

1. Ask **in a single message**:
   - What file or directory is in dispute?
   - Why does each person need to touch it? (one sentence per person)
   - Is this a **technical implementation detail**, or a **design/architecture/shared-config decision** that affects the whole codebase?

2. Apply the rule:
   - **Technical detail** → the Owner makes the call, then notifies everyone else. No vote needed.
   - **Design / architecture / shared config** → no one proceeds until all involved agree. Recommend a quick sync call if async agreement is taking too long.

3. If the ruling changes ownership, update the `COWORK.md` Ownership table and log the resolution under `## Open Conflicts`.

---

### STATUS

**Purpose:** Get a quick snapshot of where the session stands.

**Steps:**

1. Read `COWORK.md` (and `COWORK-detail.md` if it exists). Do not ask the user anything.

2. Output a one-screen summary:
   - Who owns what (condensed, not the raw table)
   - Files marked "needs agreement" that have no logged resolution yet
   - Any open conflicts in `## Open Conflicts`
   - Next logical step for each person

---

### JOIN

**Purpose:** Bring a new collaborator up to speed and add them to an ongoing session.

**Steps:**

1. Read `COWORK.md`. Brief the new person in plain language:
   - What the session is about
   - Who is working on what
   - What areas are off-limits (other people's ownership zones)
   - What files need agreement before touching

2. Ask **in a single message**:
   - New person's name?
   - What are they building today? (one sentence)

3. Map their task to files, assign Owner + Reviewer for their new areas, update the `COWORK.md` Ownership table.

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
   - Any unresolved conflicts in `COWORK.md`?
   - PR opened?

3. Remind every collaborator to create their own handoff/session summary in their own AI session.

4. Archive the session files:
   - Rename `COWORK.md` → `COWORK-<YYYY-MM-DD>.md`
   - Rename `COWORK-detail.md` → `COWORK-detail-<YYYY-MM-DD>.md` (if it exists)

---

## Conflict Resolution Reference

| Situation | Who decides | Required action |
|-----------|-------------|-----------------|
| Two people want to edit the same component | Owner of that file | Owner decides, notifies others |
| Design token or theme change | Everyone affected | Sync required before proceeding |
| Adding a new dependency | All collaborators | Agreement required (affects build for everyone) |
| Bug fix inside one person's area | That person | No coordination needed |
| API contract change | All collaborators | Agreement required (affects frontend and backend) |
| Config / CI file | All collaborators | Agreement required |

---

## Scope Limits

This protocol is for **same-time collaboration** on the same repo. Do not use it for:
- Code review (async, single reviewer)
- GitHub settings or admin changes
- Solo development tasks
