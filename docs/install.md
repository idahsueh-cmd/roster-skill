# Install

## Install into a project

Run this from your project root:

```bash
git clone --depth 1 https://github.com/idahsueh-cmd/roster-skill /tmp/roster-skill
mkdir -p .roster
cp -r /tmp/roster-skill/project-setup/. .roster/
rm -rf /tmp/roster-skill
python .roster/generate.py
```

Commit `.roster/` so teammates get the same protocol:

```bash
git add .roster/
git commit -m "add roster protocol"
```

## Update

```bash
git clone --depth 1 https://github.com/idahsueh-cmd/roster-skill /tmp/roster-skill
cp -r /tmp/roster-skill/project-setup/. .roster/
rm -rf /tmp/roster-skill
python .roster/generate.py
```

## For AI agents

When a user asks you to install roster, run the install commands in their project root.

After installation, tell the user:

1. Restart the AI session so the new skill files are picked up.
2. Begin a new session and say `let's start a roster session`, or run `/roster start` in Claude Code.

## Direct use without install

Paste `project-setup/PROTOCOL.md` into any AI assistant and ask for the flow you need:

- START: start a new roster session
- CONFLICT: resolve overlap on a file or directory
- STATUS: summarize the current roster
- JOIN: add a new collaborator
- WRAP: close the session

The prompt files in `claude-skill/prompts/` are thin shortcuts that assume the assistant can read `PROTOCOL.md`.

## Generated files

Running `python .roster/generate.py` writes adapter files from `PROTOCOL.md`:

| Tool | Output path |
|------|-------------|
| Claude Code | `.claude/skills/roster/SKILL.md` |
| Cursor | `.cursor/rules/roster.mdc` |
| Windsurf | `.windsurf/rules/roster.md` |
| Codex | `AGENTS.md`, only when safe to manage automatically |

Each file is stamped with a signature. Re-running `generate.py` is safe:

- Unmodified files are upgraded automatically.
- Manually edited generated files are blocked with a clear error.

If an unmanaged `AGENTS.md` already exists, roster does not overwrite it by default. It writes `.roster/generated/AGENTS.roster.md` instead so you can merge it manually. Use `--force` only after reviewing what would be replaced.

## Options

```bash
python .roster/generate.py --skip cursor
python .roster/generate.py --force
```
