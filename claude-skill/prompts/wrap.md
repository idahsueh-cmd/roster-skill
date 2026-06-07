# Cowork — Wrap

The session is ending. Your job is to make sure everyone closes cleanly with no loose ends.

**Step 1 — If multiple PRs are open, determine merge order:**
- PRs that touch shared files (marked `ALL` in COWORK.md) should merge last.
- PRs with no shared-file overlap can merge in any order.
- Suggest a specific merge sequence to minimize conflicts.

**Step 2 — Run through this checklist for each collaborator:**
1. Is their branch up to date with main? (`git pull origin main`)
2. Does the build pass?
3. Are there any unresolved conflicts in `COWORK.md`?
4. Has their PR been opened?

Tell me which items pass and which need attention, per person.

**Step 3 — Remind every collaborator:**
Each person should create their own handoff/session summary independently in their own AI session before ending.

**Step 4 — Archive the session files:**
- Rename `COWORK.md` → `COWORK-<today's date>.md`
- If `COWORK-detail.md` exists, rename it → `COWORK-detail-<today's date>.md`

Tell me what was renamed and that the session is officially wrapped.
