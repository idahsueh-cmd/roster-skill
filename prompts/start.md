# Cowork — Start

We are about to begin a collaborative coding session. Two or more people will be working on the same repository at the same time. Your job is to coordinate so our work doesn't collide.

**Follow these steps exactly:**

**Step 1 — Read the project silently.**
Look for and read (if they exist): `CLAUDE.md`, `README.md`, any rules or conventions files. Do not tell me what you found — just internalize it.

**Step 2 — Ask me the following in a single message (do not split into multiple turns):**
1. Does everyone already have access to this repo on GitHub? (If not, we need to invite them before continuing: repo Settings → Collaborators.)
2. List all collaborators and what each person is building today — one line per person. Example: "Alice: new pricing page / Bob: dark mode toggle"
3. Are there any files or areas you already know are sensitive — only one person should touch?

**Step 3 — After I answer, map tasks to files.**
- Map each person's task to the files/directories they'll likely touch.
- Identify overlap zones where multiple people might need changes.
- For each overlap: assign one Owner (whose task depends on it most) and one Reviewer.
- Mark shared infrastructure as ALL + "needs agreement before changing": `package.json`, lockfiles, config files, design tokens, API contracts, CI files.

**Step 4 — Write `COWORK.md` at the repo root** using this exact format (keep under 100 lines):

```
# COWORK Session — <today's date>
Collaborators: <all names>

## Tasks
- <Name>: <task>

## Ownership
| File / Directory | Owner | Reviewer | Notes |
|-----------------|-------|----------|-------|
| ...             | ...   | ...      |       |
| <shared files>  | ALL   | ALL      | needs agreement before changing |

## Open Conflicts
<!-- log disputes here during the session -->

## Conflict Rules
- Technical detail → Owner decides, notifies others
- Design / architecture / shared config → all involved must agree before anyone proceeds

## Wrap
When done: each person creates their own handoff summary, then opens a PR.
```

If 3+ people and the table would exceed 60 rows, move details to `COWORK-detail.md` and keep `COWORK.md` as a summary index.

**Step 5 — Tell all collaborators:**
"Share COWORK.md with everyone. Dispute about a file? Run the conflict prompt. Want current state? Run the status prompt. New person joining? Run the join prompt."
