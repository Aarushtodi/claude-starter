#!/usr/bin/env python3
"""unblock.py <id>: a blocker resolved. Every `BLOCKED-BY: <id>` in ~/school (.md) and ~/.claude/CLAUDE.md
becomes `UNBLOCKED <date> (<id>)`, the row in Projects/Blockers.md is marked resolved, and the change is logged there.
Prints every file it touched so Claude can re-read those notes and update them."""
import re, sys
from datetime import datetime
from pathlib import Path

HOME = Path.home()
SCHOOL = HOME / "school"


def main():
    if len(sys.argv) != 2 or not sys.argv[1].strip():
        sys.exit("usage: unblock.py <id>")
    bid = sys.argv[1].strip()
    today = datetime.now().strftime("%Y-%m-%d")
    pat = re.compile(r"BLOCKED-BY:\s*" + re.escape(bid) + r"(?![\w-])")
    files = [p for p in SCHOOL.rglob("*.md") if ".obsidian" not in p.parts and ".git" not in p.parts] if SCHOOL.exists() else []
    cm = HOME / ".claude" / "CLAUDE.md"
    if cm.exists():
        files.append(cm)
    touched = 0
    for p in files:
        try:
            text = p.read_bytes().decode("utf-8-sig")  # bytes in, bytes out: CRLF survives
        except Exception:
            continue
        new, n = pat.subn("UNBLOCKED %s (%s)" % (today, bid), text)
        if n:
            p.write_bytes(new.encode("utf-8"))
            touched += n
            print("updated %d line(s): %s" % (n, p))
    bl = SCHOOL / "Projects" / "Blockers.md"
    row = False
    if bl.exists():
        text = bl.read_bytes().decode("utf-8-sig")
        nl = "\r\n" if "\r\n" in text else "\n"
        out = []
        for line in text.splitlines(keepends=True):  # each line keeps its own ending
            body = line.rstrip("\r\n")
            end = line[len(body):]
            cells = body.split("|")
            if body.startswith("|") and len(cells) >= 6 and cells[1].strip() == bid:
                cells[4] = " resolved %s " % today
                body = "|".join(cells)
                row = True
            out.append(body + end)
        text = "".join(out)
        if not text.endswith("\n"):
            text += nl
        text = text + nl + "- [%s] UNBLOCKED %s: %d line(s) swapped%s" % (today, bid, touched, "" if row else ", no table row found") + nl
        text = re.sub(r"^updated:.*$", "updated: " + today, text, count=1, flags=re.M)
        bl.write_bytes(text.encode("utf-8"))
        print("logged in %s (table row %s)" % (bl, "marked resolved" if row else "not found"))
    else:
        print("no Blockers.md at %s" % bl)
    print("done: %d BLOCKED-BY line(s) for '%s' swapped" % (touched, bid))
    return 0


if __name__ == "__main__":
    sys.exit(main())
