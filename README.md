# cowork

A coordination protocol for two or more developers working the same repo at the same time — so you don't overwrite each other.

Supports **Claude Code, Cursor, Windsurf, and Codex CLI** from a single source of truth.

---

## For AI agents

When the user asks you to install cowork, run these commands in their project root:

```bash
git clone --depth 1 https://github.com/idahsueh-cmd/cowork-skill /tmp/cowork-skill
mkdir -p .cowork
cp -r /tmp/cowork-skill/project-setup/. .cowork/
rm -rf /tmp/cowork-skill
python .cowork/generate.py
```

Then tell the user to restart their AI session (so the new skill files are picked up).

---

## For humans

### Install

```bash
git clone --depth 1 https://github.com/idahsueh-cmd/cowork-skill /tmp/cowork-skill
mkdir -p .cowork
cp -r /tmp/cowork-skill/project-setup/. .cowork/
rm -rf /tmp/cowork-skill
python .cowork/generate.py
```

Commit the `.cowork/` directory so teammates get the same setup when they clone:

```bash
git add .cowork/
git commit -m "add cowork protocol"
```

### Update

```bash
git clone --depth 1 https://github.com/idahsueh-cmd/cowork-skill /tmp/cowork-skill
cp -r /tmp/cowork-skill/project-setup/. .cowork/
rm -rf /tmp/cowork-skill
python .cowork/generate.py
```

---

## What gets generated

Running `generate.py` writes four adapter files from `PROTOCOL.md`:

| Tool       | Output path                        |
|------------|------------------------------------|
| Claude Code | `.claude/skills/cowork/SKILL.md`  |
| Cursor     | `.cursor/rules/cowork.mdc`         |
| Windsurf   | `.windsurf/rules/cowork.md`        |
| Codex CLI  | `AGENTS.md`                        |

Each file is stamped with a signature. Re-running `generate.py` is safe:
- Unmodified files → upgraded automatically
- Manually edited files → blocked with a clear error and three options

### Options

```bash
python .cowork/generate.py --skip cursor    # skip one tool
python .cowork/generate.py --force          # overwrite everything
```

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
cowork-skill/
├── README.md
├── claude-skill/          ← direct Claude Code skill install
│   ├── SKILL.md
│   └── prompts/
└── project-setup/         ← copy this into your project as .cowork/
    ├── PROTOCOL.md        ← single source of truth
    ├── generate.py        ← generates adapter files for all tools
    ├── templates/         ← tool-specific wrappers (thin shells)
    └── VERSION
```

---

## License

MIT
