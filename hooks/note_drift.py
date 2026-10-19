#!/usr/bin/env python3
"""SessionStart hook: flag ~/school/Projects notes whose `updated:` is older than their newest
dated log line, notes stalled 7+ days, passed plan dates, and unsorted Inbox items.
Free (no LLM). Prints hook JSON only if something needs attention. Plain python3, any OS."""
import json, re, sys, datetime as dt
from pathlib import Path

P = Path.home() / "school" / "Projects"
TODAY = dt.date.today()
YEAR = TODAY.year
SKIP = ("Inbox.md", "Miscellaneous Notes.md", "Blockers.md")
DATE_LINE = re.compile(r"^\s*(?:[-*>]\s*)?(?:\[)?(?:\*\*)?(?:(\d{4})-(\d{2})-(\d{2})|(\d{1,2})/(\d{1,2}))\b")
ANY_DATE = re.compile(r"(\d{4})-(\d{2})-(\d{2})|\b(1[0-2]|[1-9])/(\d{1,2})(?:\s*[-–]\s*(?:(1[0-2]|[1-9])/)?(\d{1,2}))?(?![\d/])")


def md(d):
    return "%d/%d" % (d.month, d.day)


def read(f):
    return f.read_text(encoding="utf-8", errors="ignore").replace("\r\n", "\n")


def log_dates(text):
    out = []
    for line in text.splitlines():
        m = DATE_LINE.match(line)
        if not m:
            continue
        try:
            d = dt.date(int(m[1]), int(m[2]), int(m[3])) if m[1] else dt.date(YEAR, int(m[4]), int(m[5]))
        except ValueError:
            continue
        if d <= TODAY:
            out.append(d)
    return out


def fm(text):
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    return dict(l.split(":", 1) for l in m[1].splitlines() if ":" in l) if m else {}


def line_deadline(line):
    """Latest date on a line (M/D assumed this year, or YYYY-MM-DD); ranges use their end."""
    best = None
    for m in ANY_DATE.finditer(line):
        try:
            if m[1]:
                d = dt.date(int(m[1]), int(m[2]), int(m[3]))
            else:
                mon, day = int(m[4]), int(m[5])
                if m[7]:
                    mon, day = (int(m[6]) if m[6] else mon), int(m[7])
                d = dt.date(YEAR, mon, day)
        except ValueError:
            continue
        if best is None or d > best:
            best = d
    return best


def plan_passed(text, logs):
    """Worst unresolved past plan date under a Plan/Timeline heading, or any unchecked box."""
    worst = None
    in_plan = False
    for line in text.splitlines():
        h = re.match(r"^#+\s+(.*)", line)
        if h:
            in_plan = bool(re.search(r"plan|timeline", h[1], re.I))
            continue
        s = line.strip()
        is_row = in_plan and s.startswith("|") and not re.match(r"^\|[\s:|-]+$", s)
        is_box = bool(re.match(r"^[-*]\s*\[ \]", s))
        if not (is_row or is_box) or "~~" in s or re.search(r"\[[xX]\]", s):
            continue
        d = line_deadline(s)
        if not d or d >= TODAY or any(l > d for l in logs):
            continue
        if worst is None or d < worst[0]:
            worst = (d, s)
    return worst


def label(line):
    txt = line.strip("|").split("|")[-1] if line.startswith("|") else re.sub(r"^[-*]\s*\[ \]\s*", "", line)
    txt = re.sub(r"\(.*?\)|\*\*|\[\[|\]\]", "", txt).strip(" *`")
    return txt[:40].rstrip(" ,.:;-") or "plan"


def inbox_count(path):
    if not path.exists():
        return 0
    n, on = 0, False
    for l in read(path).splitlines():
        if l.startswith("## "):
            on = l.strip().lower().startswith("## unsorted")
        elif on and l.startswith("- ["):
            n += 1
    return n


def main():
    global TODAY
    if "--today" in sys.argv:
        TODAY = dt.date.fromisoformat(sys.argv[sys.argv.index("--today") + 1])
    if not P.is_dir():
        return
    stale, stalled, passed = [], [], []
    for f in sorted(P.rglob("*.md")):
        rel = f.relative_to(P)
        if f.name in SKIP or any("archive" in p.lower() for p in rel.parts):
            continue
        t = read(f)
        meta = fm(t)
        if meta.get("status", "").strip() != "active" or meta.get("type", "").strip() != "project":
            continue
        name = f.stem
        logs = log_dates(t)
        log = max(logs) if logs else None
        try:
            upd = dt.date.fromisoformat(meta.get("updated", "").strip())
        except ValueError:
            upd = None
        if upd and upd > TODAY:
            upd = None
        if log and (upd is None or (log - upd).days >= 2):
            stale.append(((log - upd).days if upd else 999, name, log))
        last = log or upd
        if last and (TODAY - last).days >= 7:
            stalled.append(((TODAY - last).days, name))
        pp = plan_passed(t, logs)
        if pp:
            passed.append(((TODAY - pp[0]).days, name, pp[0], pp[1]))
    stale.sort(reverse=True)
    stalled.sort(reverse=True)
    passed.sort(reverse=True)
    n_inbox = inbox_count(P / "Inbox.md")
    if not (stale or stalled or passed or n_inbox):
        return
    msg = []
    if stalled:
        msg.append("STALLED 7d+: %d (worst: %s)." % (len(stalled), ", ".join("%s %dd" % (n, d) for d, n in stalled[:3])))
    if passed:
        msg.append("PLAN DATES PASSED: %d (worst: %s)." % (len(passed), "; ".join("%s, %s %s" % (n, label(l), md(d)) for _, n, d, l in passed[:3])))
    if stale:
        names = ", ".join("%s (log %s)" % (s[1], md(s[2])) for s in stale[:3])
        msg.append("NOTE DRIFT: %d project notes have a newer log than their top state. Worst: %s. If you touch one, rewrite its Current state block + updated: in the same step." % (len(stale), names))
    if n_inbox:
        msg.append("INBOX: %d unsorted items in Projects/Inbox.md. Sort each into the right note's log now and move it under Sorted." % n_inbox)
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": " ".join(msg)}}))


if __name__ == "__main__":
    main()
