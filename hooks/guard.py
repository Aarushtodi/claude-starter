#!/usr/bin/env python3
"""PreToolUse hook for Bash. Blocks commands that wipe things, since bypass
permissions means Claude will not ask first. Exit 2 = block with a reason."""
import json
import re
import sys

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

cmd = (data.get("tool_input") or {}).get("command", "") or ""

BLOCK = [
    (r"\brm\s+-[a-zA-Z]*r[a-zA-Z]*f|\brm\s+-[a-zA-Z]*f[a-zA-Z]*r", "rm -rf"),
    (r"\bgit\s+push\s+.*--force|\bgit\s+push\s+-f\b", "git push --force"),
    (r"\bgit\s+reset\s+--hard", "git reset --hard"),
    (r"\bgit\s+clean\s+-[a-zA-Z]*f", "git clean -f"),
    (r"\bformat\s+[a-zA-Z]:", "format drive"),
    (r"\bdel\s+/[sS]\b|\brmdir\s+/[sS]\b|Remove-Item\s+.*-Recurse", "recursive delete"),
    (r"\bmkfs\b|\bdd\s+if=", "disk wipe"),
    (r">\s*~/\.claude/CLAUDE\.md\b|>\s*\$HOME/\.claude/CLAUDE\.md\b", "overwrite CLAUDE.md (use Edit, show the line first)"),
]

for pat, label in BLOCK:
    if re.search(pat, cmd):
        print(
            f"BLOCKED by guard.py: this looks like '{label}'. "
            "CLAUDE.md says never without asking. Tell Srijan exactly what you want to run and why, "
            "and run it only after he says yes in the chat.",
            file=sys.stderr,
        )
        sys.exit(2)

sys.exit(0)
