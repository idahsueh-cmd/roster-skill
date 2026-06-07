# Cowork — Conflict

Someone needs to touch a file that belongs to another person, or ownership was never defined. Your job is to resolve this fairly and update the shared record.

**Step 1 — Ask me the following in a single message:**
1. What file or directory is in dispute?
2. Why does each person need to touch it? (one sentence per person — list all parties involved)
3. Is this a **technical implementation detail**, or a **design/architecture/shared-config decision** that affects the whole codebase?

**Step 2 — After I answer, apply the rule:**

- **Technical detail** → the Owner (whoever's task depends most on this file) makes the call. They decide, then notify everyone else. No group vote needed.
- **Design / architecture / shared config** → no one proceeds until all involved agree. If async agreement is taking too long, recommend a quick sync call.

**Step 3 — Update `COWORK.md`:**
- If the ruling changes who owns the file, update the Ownership table.
- Log the resolution under `## Open Conflicts` so everyone can see it was handled.

Tell me the ruling and what was updated.
