# Advanced

## Current design

`project-setup/PROTOCOL.md` is the single source of truth. It defines the START, CONFLICT, STATUS, JOIN, and WRAP flows, plus the `ROSTER.md` format.

The prompt files in `claude-skill/prompts/` are intentionally thin. They do not duplicate the workflow; each one only tells the assistant to execute the matching flow from `PROTOCOL.md`.

When installed into a project, `.roster/README.md` explains the installed directory:

- `.roster/PROTOCOL.md` is the core rulebook
- `.roster/generate.py` creates the AI-tool adapter files
- `ROSTER.md` is the per-session collaboration artifact created at the project root

## How it works

Every session produces a `ROSTER.md` at the repo root:

```md
# ROSTER Session - 2026-06-07
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
- Technical detail -> Session Owner decides, notifies others
- Design / architecture / shared config -> all involved must agree before anyone proceeds
```

All collaborators share this file. It is the single source of truth for the current session.

## Repo structure

```text
roster-skill/
|-- README.md
|-- claude-skill/
|   |-- SKILL.md
|   `-- prompts/
|-- docs/
|   |-- advanced.md
|   `-- install.md
|-- project-setup/
|   |-- README.md
|   |-- PROTOCOL.md
|   |-- generate.py
|   |-- templates/
|   `-- VERSION
`-- tests/
    `-- test_generate.py
```

## Tests

```bash
python -m unittest tests.test_generate
```

The tests use only Python's standard library and cover:

- all tool adapters generate successfully
- unmanaged `AGENTS.md` is not overwritten
- manually modified managed files block regeneration
