# cowork — Claude Code Skill

A Claude Code skill for coordinating multi-person development sessions on the same repo.

**The problem it solves:** Two or more developers working the same codebase simultaneously, each with their own Claude Code session, trying not to overwrite each other.

## Install

```bash
claude skill install https://github.com/idahsueh-cmd/cowork-skill
```

## Usage

| Command | What it does |
|---------|-------------|
| `/cowork start` | Set up a session — reads project config, asks who's working on what, produces `COWORK.md` with ownership table |
| `/cowork conflict` | Resolve an ownership dispute — gives a clear ruling based on task ownership |
| `/cowork status` | Summarize the current session state from `COWORK.md` |
| `/cowork join` | Onboard a new collaborator mid-session |
| `/cowork wrap` | Close the session — merge order, checklist, archive `COWORK.md`, trigger `/handoff` |

## How it works

`/cowork start` produces a `COWORK.md` in the project root:

```
# COWORK Session — 2026-06-07
Collaborators: Ida, Jason, Mei

## Tasks
- Ida: new pricing page
- Jason: dark mode toggle
- Mei: CMS API integration

## Ownership
| File / Directory | Owner | Reviewer | Notes |
|-----------------|-------|----------|-------|
| src/pages/Pricing/ | Ida | Mei | |
| src/components/Navbar/ | Jason | Ida | |
| theme.css | ALL | ALL | needs agreement before changing |

## Conflict rules
- Technical detail → Owner decides, notifies others
- Design / architecture / shared config → all involved must agree before proceeding
```

All collaborators share this file as the source of truth for the session.

## Conflict resolution rules

- **Technical detail** (implementation choice that doesn't affect others) → Owner makes the call, notifies everyone
- **Design / architecture / shared config** (affects the whole codebase) → no one proceeds until all agree

## Requirements

- Each collaborator needs their own Claude Code installation
- Everyone needs push access to the repo (GitHub collaborator)

## License

MIT
