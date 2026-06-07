#!/usr/bin/env python3
"""roster generate — writes AI tool adapter files from PROTOCOL.md"""

import hashlib
import os
import re
import sys
from datetime import datetime, timezone

SCRIPT_DIR    = os.path.dirname(os.path.abspath(__file__))
PROTOCOL_PATH = os.path.join(SCRIPT_DIR, "PROTOCOL.md")
TEMPLATES_DIR = os.path.join(SCRIPT_DIR, "templates")
VERSION_PATH  = os.path.join(SCRIPT_DIR, "VERSION")

TOOLS = {
    "claude":   ".claude/skills/roster/SKILL.md",
    "cursor":   ".cursor/rules/roster.mdc",
    "windsurf": ".windsurf/rules/roster.md",
    "codex":    "AGENTS.md",
}

CODEX_SNIPPET_PATH = ".roster/generated/AGENTS.roster.md"

ALLOWED = {"{{content}}", "{{name}}", "{{version}}", "{{description}}"}
SIG_RE  = re.compile(
    r'<!-- roster-managed[^>]*gen-hash: ([a-f0-9]{8})[^>]*out-hash: ([a-f0-9]{8})[^>]*-->\n?'
)


def h8(text):
    return hashlib.sha256(text.encode()).hexdigest()[:8]


def parse_meta(text):
    """Parse YAML-like frontmatter between --- delimiters. Returns (meta dict, body str)."""
    m = re.match(r'^---\n(.*?)\n---\n(.*)', text, re.DOTALL)
    if not m:
        return {}, text
    meta, current = {}, None
    for line in m.group(1).splitlines():
        s = line.rstrip()
        if not s or s.startswith('#'):
            current = None
            continue
        if s.startswith('  ') and current:
            k, _, v = s.strip().partition(':')
            if v:
                meta.setdefault(current, {})[k.strip()] = v.strip()
        elif ':' in s:
            k, _, v = s.partition(':')
            k, v = k.strip(), v.strip()
            if v:
                meta[k] = v
            else:
                current = k
    return meta, m.group(2)


def safe_replace(template, values):
    result = template
    for k, v in values.items():
        if k in ALLOWED:
            result = result.replace(k, v)
    for unknown in set(re.findall(r'\{\{[^}]+\}\}', result)):
        print(f"  WARN unknown placeholder {unknown} - left as-is")
    return result


def conflict_error(tool, path):
    print(f"\nERROR Cannot overwrite {path}")
    print( "    This file does not match roster's last output.")
    print( "    Possible reasons: manually edited, or not created by roster.\n")
    print(f"  A. Skip this tool:     python .roster/generate.py --skip {tool}")
    print(f"  B. Force overwrite:    python .roster/generate.py --force")
    print( "     WARN Run `git diff` first to review what you'd lose.")
    print(f"  C. Commit first:       git add {path} && git commit")
    print( "     Then re-run generate.py and use `git diff` to review changes.")


def write_file(path, content):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def main():
    args  = sys.argv[1:]
    force = "--force" in args
    skip  = set()
    for i, a in enumerate(args):
        if a == "--skip" and i + 1 < len(args):
            skip.add(args[i + 1])

    protocol        = read_file(PROTOCOL_PATH)
    version         = read_file(VERSION_PATH).strip() if os.path.exists(VERSION_PATH) else "1.0.0"
    meta, body      = parse_meta(protocol)
    errors          = False
    claude_written  = False

    for tool, out_path in TOOLS.items():
        if tool in skip:
            print(f"  SKIP {tool}: skipped")
            continue

        tpl_path = os.path.join(TEMPLATES_DIR, f"{tool}.md.template")
        if not os.path.exists(tpl_path):
            print(f"  WARN {tool}: template not found, skipping")
            continue

        template  = read_file(tpl_path)
        gen_hash  = h8(protocol + template)
        tool_meta = meta.get(tool, {})
        desc      = tool_meta.get("description", meta.get("description", ""))

        rendered  = safe_replace(template, {
            "{{content}}":     body.strip(),
            "{{name}}":        meta.get("name", "roster"),
            "{{version}}":     version,
            "{{description}}": desc,
        })
        out_hash  = h8(rendered)
        ts        = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        sig_line  = (f"<!-- roster-managed: do not edit. "
                     f"gen-hash: {gen_hash} out-hash: {out_hash} "
                     f"generated-at: {ts} -->\n")
        final     = sig_line + rendered

        if tool == "codex" and os.path.exists(out_path) and not force:
            existing = read_file(out_path)
            if SIG_RE.search(existing) is None:
                write_file(CODEX_SNIPPET_PATH, final)
                print(f"  WARN codex: existing unmanaged {out_path} found")
                print(f"     wrote {CODEX_SNIPPET_PATH} instead; merge it into {out_path} manually, or re-run with --force")
                continue

        if os.path.exists(out_path) and not force:
            existing = read_file(out_path)
            m = SIG_RE.search(existing)
            if m is None:
                conflict_error(tool, out_path)
                errors = True
                continue
            stored_gen, stored_out = m.group(1), m.group(2)
            actual_body = SIG_RE.sub("", existing)
            if h8(actual_body) != stored_out:
                conflict_error(tool, out_path)
                errors = True
                continue
            if stored_gen == gen_hash:
                print(f"  OK {tool}: already up to date")
                continue

        write_file(out_path, final)
        print(f"  OK {tool}: wrote {out_path}")
        if tool == "claude":
            claude_written = True

    if claude_written:
        print()
        print("  TIP If Claude Code doesn't pick up .claude/skills/roster/SKILL.md:")
        print("     1. Restart your Claude Code session")
        print("     2. Make sure you launched claude from this project directory")
        print("     3. WSL users: launch claude from inside WSL, not from Windows")

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
