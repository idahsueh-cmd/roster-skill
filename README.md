# cowork

A coordination protocol for two or more developers working the same repo at the same time — so you don't overwrite each other.

**Works with any AI assistant.** The protocol lives in `PROTOCOL.md`. Use it via Claude Code skill, or paste the `prompts/` files directly into Cursor, Gemini, Copilot, or plain ChatGPT.

---

## Option A — Claude Code skill

```bash
claude skill install https://github.com/idahsueh-cmd/cowork-skill
```

Then use:

| Command | What it does |
|---------|--------------|
| `/cowork start` | Set up a session — reads project, asks who's working on what, writes `COWORK.md` |
| `/cowork conflict` | Resolve an ownership dispute — gives a clear ruling |
| `/cowork status` | Summarize current session state from `COWORK.md` |
| `/cowork join` | Onboard a new collaborator mid-session |
| `/cowork wrap` | Close the session — merge order, checklist, archive |

---

## Option B — Any AI assistant (paste a prompt)

Copy the relevant file from `prompts/` and paste it into any AI chat:

| File | When to use |
|------|-------------|
| `prompts/start.md` | Starting a new session |
| `prompts/conflict.md` | Dispute over a file |
| `prompts/status.md` | Check current state |
| `prompts/join.md` | New person joining |
| `prompts/wrap.md` | Ending the session |

---

## How it works

Every session produces a `COWORK.md` at the repo root:

```
# COWORK Session — 2026-06-07
Collaborators: Ida, Jason, Mei

## Tasks
- Ida: new pricing page
- Jason: dark mode toggle
- Mei: CMS API integration

## Ownership
| File / Directory   | Owner | Reviewer | Notes                           |
|--------------------|-------|----------|---------------------------------|
| src/pages/Pricing/ | Ida   | Mei      |                                 |
| src/components/Navbar/ | Jason | Ida  |                                 |
| theme.css          | ALL   | ALL      | needs agreement before changing |

## Conflict Rules
- Technical detail → Owner decides, notifies others
- Design / architecture / shared config → all involved must agree before anyone proceeds
```

All collaborators share this file. It's the single source of truth for the session.

---

## Conflict resolution rules

| Situation | Who decides |
|-----------|-------------|
| Implementation detail inside one person's area | That person (Owner) |
| Design token / theme / shared config change | Everyone affected — sync required |
| New dependency | All collaborators — affects everyone's build |
| API contract change | All collaborators |

---

## Requirements

- Each collaborator needs their own AI assistant session
- Everyone needs push access to the repo

---

## Architecture

```
PROTOCOL.md       ← single source of truth (tool-agnostic)
SKILL.md          ← thin Claude Code interface (reads PROTOCOL.md, runs it)
prompts/          ← copy-paste prompts for any AI
  start.md
  conflict.md
  status.md
  join.md
  wrap.md
```

---

## License

MIT
