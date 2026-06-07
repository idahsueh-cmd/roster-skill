# roster

> Git tracks code. roster tracks intent.

A coordination protocol for two or more developers (or AIs, or both) working the same repo at the same time — so you don't overwrite each other.

Works across Claude Code, Cursor, Windsurf, and Codex CLI, so nobody needs to switch tools to participate.

---

## What this isn't

roster is not a "sync your AI instructions across tools" wrapper — tools designed to push one config file into Claude's rules, Cursor's `.mdc`, and Windsurf's rules already exist and work fine.

roster solves a different problem: two or more people (or AIs, or both) editing the same repo at the same time without overwriting each other. The multi-tool support is incidental — what matters is that everyone touching the repo agrees on who owns what before the commit lands.

If you're solo and just want consistent AI instructions across multiple AI tools, you probably want one of those other tools. If you're coordinating multiple people (with or without AI help), read on.

---

## For AI agents

When the user asks you to install roster, run these commands in their project root:

```bash
git clone --depth 1 https://github.com/idahsueh-cmd/roster-skill /tmp/roster-skill
mkdir -p .roster
cp -r /tmp/roster-skill/project-setup/. .roster/
rm -rf /tmp/roster-skill
python .roster/generate.py
```

After installation, tell the user:
1. Restart your AI session so the new skill files are picked up
2. Begin a new session and say "let's start a roster session" — or run `/roster start` if you're using Claude Code

---

## For humans

### Install

```bash
git clone --depth 1 https://github.com/idahsueh-cmd/roster-skill /tmp/roster-skill
mkdir -p .roster
cp -r /tmp/roster-skill/project-setup/. .roster/
rm -rf /tmp/roster-skill
python .roster/generate.py
```

Commit the `.roster/` directory so teammates get the same setup when they clone:

```bash
git add .roster/
git commit -m "add roster protocol"
```

### Update

```bash
git clone --depth 1 https://github.com/idahsueh-cmd/roster-skill /tmp/roster-skill
cp -r /tmp/roster-skill/project-setup/. .roster/
rm -rf /tmp/roster-skill
python .roster/generate.py
```

---

## What gets generated

Running `generate.py` writes four adapter files from `PROTOCOL.md`:

| Tool       | Output path                        |
|------------|------------------------------------|
| Claude Code | `.claude/skills/roster/SKILL.md`  |
| Cursor     | `.cursor/rules/roster.mdc`         |
| Windsurf   | `.windsurf/rules/roster.md`        |
| Codex CLI  | `AGENTS.md`                        |

Each file is stamped with a signature. Re-running `generate.py` is safe:
- Unmodified files → upgraded automatically
- Manually edited files → blocked with a clear error and three options

### Options

```bash
python .roster/generate.py --skip cursor    # skip one tool
python .roster/generate.py --force          # overwrite everything
```

---

## How it works

Every session produces a `ROSTER.md` at the repo root:

```
# ROSTER Session — 2026-06-07
Collaborators: Ida, Jason, Mei

## Tasks
- Ida: new pricing page
- Jason: dark mode toggle
- Mei: CMS API integration

## Ownership
| File / Directory       | Owner | Reviewer | Notes                           |
|------------------------|-------|----------|---------------------------------|
| src/pages/Pricing/     | Ida   | Mei      |                                 |
| src/components/Navbar/ | Jason | Ida      |                                 |
| theme.css              | ALL   | ALL      | needs agreement before changing |

## Conflict Rules
- Technical detail → Owner decides, notifies others
- Design / architecture / shared config → all involved must agree before anyone proceeds
```

All collaborators share this file. It is the single source of truth for the session.

---

## Direct use (no install)

If you just need the protocol without setting up the full tool, paste any file from
[`claude-skill/prompts/`](claude-skill/prompts/) into any AI assistant directly.

| Prompt file | When to use |
|-------------|-------------|
| `start.md`    | Starting a new session |
| `conflict.md` | Dispute over a file |
| `status.md`   | Check current state |
| `join.md`     | New person joining |
| `wrap.md`     | Ending the session |

---

## Repo structure

```
roster-skill/
├── README.md
├── claude-skill/          ← direct Claude Code skill install
│   ├── SKILL.md
│   └── prompts/
└── project-setup/         ← copy this into your project as .roster/
    ├── PROTOCOL.md        ← single source of truth
    ├── generate.py        ← generates adapter files for all tools
    ├── templates/         ← tool-specific wrappers (thin shells)
    └── VERSION
```

---

## License

[MIT](LICENSE)
