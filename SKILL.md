---
name: cowork
description: "Invoke this skill any time two or more developers are working the same repo simultaneously and need to coordinate — the scenario where we are coding together today and do not want to overwrite each other. Handles the full lifecycle — dividing ownership before work starts, briefing a new person who joins mid-session, summarizing who currently has what, resolving disputes when two people need the same file, and closing the session. Produces a shared COWORK.md that all collaborators reference. Trigger on cowork, 協作, 分工, 一起做, collaborate, working together, 同時改, pair coding, split the work, two of us on this repo. Not for PR reviews, GitHub settings changes, or solo development tasks."
---

# cowork

Any number of people, each with their own Claude Code, working on the same repo at the same time. This skill coordinates who owns what — so work doesn't collide.

## Route by $ARGUMENTS

- `start` → Setup mode
- `conflict` → Resolve a file/task ownership dispute
- `status` → Summarize current session state
- `join` → Add a new collaborator mid-session
- `wrap` → Finish the session, trigger handoffs
- empty → Ask which mode they want

---

## START mode

**Step 1 — Read the project silently**

Look for and read (if they exist): `CLAUDE.md`, `README.md`, `.claude/rules/`

**Step 2 — Pre-flight check (in one message)**

Ask:
1. Does everyone already have access to this repo on GitHub? (if not: go to repo → Settings → Collaborators → invite them before continuing)
2. List all collaborators and what each person is building today — one line per person, e.g. "Ida: new pricing page / Jason: dark mode toggle"
3. Any files or areas you already know are sensitive — only one person should touch?

**Step 3 — Map task boundaries**

- Map each person's task to files/directories they'll likely touch
- Flag overlap zones where multiple people might need changes
- For each overlap, assign one Owner (whoever's task depends on it most) and one Reviewer
- Mark shared infrastructure as "needs agreement": config files, design tokens, package.json, CLAUDE.md, API contracts

**Step 4 — Write COWORK.md (keep under 100 lines)**

If 3+ people and the ownership table would exceed 60 lines, split details into `COWORK-detail.md` and keep COWORK.md as a summary index only.

```
# COWORK Session — <date>
Collaborators: <all names>

## Tasks
- <Person>: <task>

## Ownership
| File / Directory | Owner | Reviewer | Notes |
|-----------------|-------|----------|-------|
| ...             | ...   | ...      |       |
| <shared files>  | ALL   | ALL      | needs agreement before changing |

## Conflict rules
- Technical detail → Owner decides, notifies others
- Design / architecture / shared config → all involved must agree before proceeding

## Wrap
When done: each person runs /handoff independently, then opens a PR.
```

Tell the user: "Share COWORK.md with all collaborators. Disputes → `/cowork conflict`. Check state anytime → `/cowork status`. New person joining → `/cowork join`."

---

## CONFLICT mode

Someone wants to change something in another person's area, or ownership was undefined.

**Ask in one message:**
1. What file or area is in dispute?
2. Why does each person need to touch it? (list all parties)
3. Is this a technical implementation detail, or a design/architecture decision that affects the whole codebase?

**Rule:**
- **Technical detail** → the Owner (person whose task depends most on this file) makes the call, then notifies everyone else
- **Design / architecture / shared config** → no one proceeds until all involved agree; recommend a quick sync

Update COWORK.md ownership table if the ruling changes anything.

---

## STATUS mode

Read `COWORK.md` (and `COWORK-detail.md` if it exists) and produce a one-screen summary:
- Who owns what
- Any files marked "needs agreement" that haven't been resolved
- Any open conflicts logged in COWORK.md
- Reminder of next step for each person

Do not ask the user anything. Just read and summarize.

---

## JOIN mode

A new collaborator is joining an ongoing session.

**Step 1 — Brief the new person**

Read COWORK.md and explain in plain language:
- What the session is about
- Who is working on what
- What files are off-limits (other people's areas)
- What files need agreement before touching (shared infrastructure)

**Step 2 — Add them to the session**

Ask in one message:
1. New person's name?
2. What are they building? (one sentence)

Map their task to files, assign Owner + Reviewer for their area, update COWORK.md ownership table.

Tell them: "You're in. If you need to touch someone else's area, run `/cowork conflict` first."

---

## WRAP mode

**Step 1 — Merge order (if multiple PRs are ready)**

If more than one PR is open:
- Identify which PRs touch shared files (these go last)
- PRs with no shared file overlap can merge in any order
- Suggest a specific merge sequence to minimize conflicts

**Step 2 — Checklist**

Confirm each item:
1. Branch up to date with main? (`git pull origin main`)
2. Build passes?
3. Any unresolved conflicts in COWORK.md?
4. PR opened?

**Step 3 — Wrap up**

- Remind every collaborator to run `/handoff` independently in their own Claude Code session
- Rename `COWORK.md` → `COWORK-<date>.md` (and `COWORK-detail.md` → `COWORK-detail-<date>.md` if it exists)

Tell everyone: "Session wrapped. Each of you run `/handoff` now."
