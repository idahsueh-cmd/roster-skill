# roster

> Git tracks code. CODEOWNERS tracks review responsibility. roster tracks live intent before a PR exists.

A pre-PR coordination protocol for two or more developers (or AIs, or both) working the same repo at the same time — so you don't overwrite each other before review tools can help.

Works across Claude Code, Cursor, Windsurf, and Codex CLI, so nobody needs to switch tools to participate.

roster does **not** replace CODEOWNERS, branch protection, issue trackers, or PR review. Use CODEOWNERS for long-lived review responsibility and merge requirements. Use roster for the short-lived "who is touching what today?" agreement at the start of a live collaboration session.

---

## Quick demo

```text
User: let's start a roster session

AI: Who is working today, and what is each person building?

User: Codex: admin roster UI / Claude: CSV import API
```

The AI writes `ROSTER.md`:

| File / Directory | Session Owner | Consult / Notify | Notes |
|------------------|---------------|------------------|-------|
| src/pages/admin/ | Codex | Claude | admin UI |
| src/api/import/ | Claude | Codex | CSV import |
| package.json | ALL | ALL | needs agreement before changing |
| src/lib/api.ts | ALL | ALL | shared contract |

Now both agents know what to avoid before a PR exists.

---

## What this isn't

roster is not an AI rules sync tool, a task tracker, or a code review system. If you're solo and only want consistent AI instructions across tools, you probably want something else.

## roster vs CODEOWNERS

| Need | CODEOWNERS | roster |
|------|------------|--------|
| Long-term file responsibility | Yes | No |
| Automatic PR review requests | Yes | No |
| Required owner approval before merge | Yes, with branch protection or rulesets | No |
| Pre-PR session planning | No | Yes |
| Temporary "who touches what today" coordination | No | Yes |
| Multi-agent or multi-person conflict prevention before commits land | No | Yes |

If a repo already has CODEOWNERS, roster should read it as context for sensitive areas and likely reviewers, not as the session plan itself.

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
| Codex CLI  | `AGENTS.md`, only when safe to manage automatically |

Each file is stamped with a signature. Re-running `generate.py` is safe:
- Unmodified files → upgraded automatically
- Manually edited files → blocked with a clear error and three options

For Codex, if an existing unmanaged `AGENTS.md` is present, roster does not overwrite it by default. It writes `.roster/generated/AGENTS.roster.md` instead and tells you to merge the snippet manually. Use `--force` only after reviewing what would be replaced.

### Options

```bash
python .roster/generate.py --skip cursor    # skip one tool
python .roster/generate.py --force          # overwrite everything
```

---

## Test

```bash
python -m unittest tests.test_generate
```

The tests use only Python's standard library.

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
| File / Directory       | Session Owner | Consult / Notify | Notes                           |
|------------------------|---------------|------------------|---------------------------------|
| src/pages/Pricing/     | Ida           | Mei              |                                 |
| src/components/Navbar/ | Jason         | Ida              |                                 |
| theme.css              | ALL           | ALL              | needs agreement before changing |

## Conflict Rules
- Technical detail → Session Owner decides, notifies others
- Design / architecture / shared config → all involved must agree before anyone proceeds
```

All collaborators share this file. It is the single source of truth for the session.

---

## Direct use (no install)

If you just need the protocol without setting up the full tool, paste `project-setup/PROTOCOL.md` into any AI assistant and ask for the flow you need. The prompt files in [`claude-skill/prompts/`](claude-skill/prompts/) are thin shortcuts that assume the assistant can read `PROTOCOL.md`.

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
    ├── README.md          ← explains the installed .roster/ directory
    ├── PROTOCOL.md        ← single source of truth
    ├── generate.py        ← generates adapter files for all tools
    ├── templates/         ← tool-specific wrappers (thin shells)
    └── VERSION
```

---

## License

[MIT](LICENSE)
