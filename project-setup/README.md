# roster project setup

This directory is installed into a project as `.roster/`.

## Files

- `PROTOCOL.md` is the core rulebook and the single source of truth.
- `generate.py` writes thin adapter files for Claude Code, Cursor, Windsurf, and Codex.
- `templates/` contains the wrappers used by `generate.py`.
- `VERSION` records the installed roster protocol version.

## Generated files

Running `python .roster/generate.py` creates tool-specific rules in the project:

- `.claude/skills/roster/SKILL.md`
- `.cursor/rules/roster.mdc`
- `.windsurf/rules/roster.md`
- `AGENTS.md`, when safe to manage automatically

If an unmanaged `AGENTS.md` already exists, roster writes `.roster/generated/AGENTS.roster.md` instead so you can merge it manually.

## Session files

`ROSTER.md` is created at the project root when a roster session starts. It is temporary session state: who is touching what today, what needs agreement, and any open conflicts.

Do not edit generated adapter files directly. Edit `PROTOCOL.md`, then re-run `generate.py`.
