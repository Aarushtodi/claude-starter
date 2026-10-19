#!/usr/bin/env python3
"""Canvas watchdog. Zero tokens: plain Canvas API calls, no AI.

Polls Canvas for your active courses, diffs against the last snapshot, keeps a ledger of open
assignments, escalates reminders as due dates get close, and only closes an item when Canvas says it
was submitted or graded. Alerts are desktop notifications (held while school_clock says you are in class).

  canvas_watch.py            poll (the scheduled job; quiet between 22:00 and 07:00)
  canvas_watch.py --digest   print + notify the ledger once (after-school summary)
  canvas_watch.py --status   print the ledger from the last poll
  canvas_watch.py --done TEXT  mark an open item done by hand (paper / in-class work Canvas can't see)
  --dry   print instead of notifying, save nothing     --force  ignore the quiet hours

Config: ~/school/.config/canvas.json   State: ~/.claude/state/canvas/   Ledger note: ~/school/Projects/Canvas Ledger.md
"""
import sys
from datetime import timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sc_common import (SCHOOL, STATE, Canvas, TokenDead, canvas_conf, fmt_due, not_configured, now,  # noqa: E402
                       parse_dt, read_json, school_year_start, strip_html, write_json)

DIR = STATE / "canvas"
STATE_F = DIR / "watch_state.json"
LOG_F = DIR / "watch.log"
LEDGER_NOTE = SCHOOL / "Projects" / "Canvas Ledger.md"
DONE_STATES = {"submitted", "graded", "pending_review"}
UNVERIFIABLE = {"on_paper", "none", "external_tool"}
DRY = "--dry" in sys.argv
NOW = now()


def log(msg):
    DIR.mkdir(parents=True, exist_ok=True)
    with open(LOG_F, "a", encoding="utf-8") as f:
        f.write("%s %s%s\n" % (NOW.strftime("%Y-%m-%d %H:%M:%S"), "DRY " if DRY else "", msg))


def load_state():
    st = read_json(STATE_F)
    if st:
        return st
    return {"init": False, "assign": {}, "ann_seen": [], "mod_seen": [], "stages": {}, "manual_done": []}


def deliver(text):
    if not text.strip():
        return
    log("SEND " + text.replace("\n", " / ")[:300])
    if DRY:
        print("=== WOULD NOTIFY ===\n" + text + "\n====================")
        return
    import notify
    notify.send(text, "Canvas")


def pull_assignments(cv, cid, short, term_start):
    rows = cv.get("/courses/%s/assignments" % cid, {"include[]": ["submission"], "per_page": 100})
    if rows is None:
        return None  # fetch failed, keep the old snapshot
    snap = {}
    for a in rows:
        if not a.get("published", True):
            continue
        due, created = parse_dt(a.get("due_at")), parse_dt(a.get("created_at"))
        if due and due < term_start:
            continue  # imported from a past year
        if not due and created and created < term_start:
            continue
        sub = a.get("submission") or {}
        snap[str(a["id"])] = {
            "cls": short, "name": (a.get("name") or "").strip(), "due": a.get("due_at"), "pts": a.get("points_possible"),
            "types": a.get("submission_types") or [], "state": sub.get("workflow_state", "unsubmitted"),
            "score": sub.get("score"), "excused": bool(sub.get("excused")), "missing": bool(sub.get("missing")),
            "late": bool(sub.get("late")), "url": a.get("html_url"),
        }
    return snap


def pts_str(a):
    return " (%g pts)" % a["pts"] if a.get("pts") else ""


def diff_assignments(st, cid, new):
    ev, first_seen, old = [], cid not in st["assign"], st["assign"].get(cid, {})
    for aid, a in new.items():
        o = old.get(aid)
        due = parse_dt(a["due"])
        if o is None:
            if st["init"] and not first_seen:
                ev.append(("NEW", "NEW %s: %s%s due %s" % (a["cls"], a["name"], pts_str(a), fmt_due(due, NOW))))
            continue
        if o["due"] != a["due"]:
            ev.append(("MOVED", "DUE DATE MOVED %s: %s now %s (was %s)" % (a["cls"], a["name"], fmt_due(due, NOW), fmt_due(parse_dt(o["due"]), NOW))))
        if a["score"] is not None and a["score"] != o["score"] and a["pts"]:
            pct = 100 * a["score"] / a["pts"]
            line = "GRADED %s: %s %g/%g (%.0f%%)" % (a["cls"], a["name"], a["score"], a["pts"], pct)
            if pct < 100:
                line += ". Under 100: find what you missed before the next test."
            ev.append(("GRADE", line))
        if a["missing"] and not o["missing"]:
            ev.append(("FLAG", "MISSING flag %s: %s" % (a["cls"], a["name"])))
        if a["late"] and not o["late"] and a["state"] in DONE_STATES:
            ev.append(("FLAG", "LATE flag %s: %s (submitted late)" % (a["cls"], a["name"])))
        if a["state"] in DONE_STATES and o["state"] not in DONE_STATES:
            ev.append(("CLOSE", "closed %s: %s" % (a["cls"], a["name"])))
    st["assign"][cid] = new
    return ev


def pull_announcements(cv, st, cid, short):
    ev = []
    rows = cv.get("/announcements", {"context_codes[]": "course_%s" % cid, "per_page": 15,
                                     "start_date": (NOW - timedelta(days=10)).strftime("%Y-%m-%d")}, paginate=False)
    for a in rows or []:
        key = "%s:%s" % (cid, a["id"])
        if key in st["ann_seen"]:
            continue
        st["ann_seen"].append(key)
        if not st["init"]:
            continue
        posted = parse_dt(a.get("posted_at"))
        if posted and posted < NOW - timedelta(days=10):
            continue
        body = strip_html(a.get("message"))[:140]
        ev.append(("ANN", "ANNOUNCEMENT %s: %s. %s (read it for a task or date)" % (short, (a.get("title") or "").strip(), body)))
    st["ann_seen"] = st["ann_seen"][-400:]
    return ev


def pull_modules(cv, st, cid, short):
    fresh = []
    for m in cv.get("/courses/%s/modules" % cid, {"include[]": ["items"], "per_page": 50}) or []:
        for it in m.get("items") or []:
            key = "%s:%s" % (cid, it["id"])
            if key in st["mod_seen"]:
                continue
            st["mod_seen"].append(key)
            if st["init"] and it.get("published", True):
                fresh.append("%s [%s]" % ((it.get("title") or "").strip(), (m.get("name") or "").strip()))
    st["mod_seen"] = st["mod_seen"][-3000:]
    if not fresh:
        return []
    shown = "; ".join(fresh[:4]) + ("; +%d more" % (len(fresh) - 4) if len(fresh) > 4 else "")
    return [("MOD", "NEW in %s modules: %s" % (short, shown))]


def open_items(st, floor):
    items = []
    for cid, snap in st["assign"].items():
        for aid, a in snap.items():
            if a["state"] in DONE_STATES or a["excused"] or aid in st["manual_done"]:
                continue
            due = parse_dt(a["due"])
            if due and due < floor:
                continue
            if not due and not a["missing"]:
                continue  # undated shells
            if a["types"] == ["external_tool"] and not a["pts"]:
                continue
            items.append((aid, a, due))
    items.sort(key=lambda x: (x[2] is None, x[2] or NOW))
    return items


def escalation(st, floor):
    lines = []
    for aid, a, due in open_items(st, floor):
        stg = st["stages"].setdefault(aid, [])
        name = "%s: %s" % (a["cls"], a["name"])
        if not due:
            continue
        left = due - NOW
        if left.total_seconds() < 0:
            days_late = (NOW.date() - due.date()).days
            if days_late >= 3:
                if "stuck" not in stg:
                    stg.append("stuck")
                    lines.append("%s is %d days late. I will stop pinging; it stays on the ledger until it is in." % (name, days_late))
                continue
            key = "late-%s-%s" % ("am" if NOW.hour < 12 else "pm", NOW.strftime("%Y-%m-%d"))
            if key not in stg:
                stg.append(key)
                lines.append("LATE %s, was due %s. Submit it, then ask about late credit." % (name, fmt_due(due, NOW)))
            continue
        for label, span in [("3h", timedelta(hours=3)), ("day", None), ("24h", timedelta(hours=24)), ("48h", timedelta(hours=48))]:
            if label in stg:
                continue
            if (due.date() == NOW.date()) if span is None else (left <= span):
                stg.append(label)
                how = {"3h": "3 hours", "day": "today", "24h": "tomorrow", "48h": "in 2 days"}[label]
                lines.append("%s due %s (%s)." % (name, fmt_due(due, NOW), how))
                break
    return lines


def ledger_text(st, floor, full=False):
    items = open_items(st, floor)
    today = [i for i in items if i[2] and i[2].date() == NOW.date()]
    late = [i for i in items if i[2] and i[2] < NOW]
    head = "%d open, %d due today, %d late" % (len(items), len(today), len(late))
    body = ["%s%s: %s (%s)" % ("LATE " if d and d < NOW else "", a["cls"], a["name"], fmt_due(d, NOW))
            for _, a, d in items[: (None if full else 8)]]
    if not full and len(items) > 8:
        body.append("+%d more in Projects/Canvas Ledger.md" % (len(items) - 8))
    return head, body


def write_ledger_note(st, floor):
    head, body = ledger_text(st, floor, full=True)
    text = ("---\ntype: reference\nstatus: active\nupdated: %s\n---\n# Canvas Ledger\n\n"
            "> Written by canvas_watch.py every poll. Do not edit by hand. Open work Canvas says is not submitted yet.\n\n"
            "## Current state\n%s (as of %s)\n\n## Open\n" % (NOW.strftime("%Y-%m-%d"), head, NOW.strftime("%Y-%m-%d %H:%M")))
    text += "".join("- [ ] %s\n" % b for b in body) or "- nothing open\n"
    try:
        LEDGER_NOTE.parent.mkdir(parents=True, exist_ok=True)
        LEDGER_NOTE.write_text(text, encoding="utf-8")
    except Exception as e:
        log("ledger note failed: %s" % e)


def run(args):
    st = load_state()
    cc = canvas_conf()
    floor = NOW - timedelta(days=14)  # anything due before this is long gone
    if "--status" in args:
        head, body = ledger_text(st, floor, full=True)
        print(head)
        print("\n".join(body))
        return
    if "--done" in args:
        needle = " ".join(args[args.index("--done") + 1:]).lower()
        hit = [(aid, a) for aid, a, _ in open_items(st, floor) if needle and needle in a["name"].lower()]
        for aid, a in hit[:1]:
            st["manual_done"].append(aid)
            print("marked done: %s: %s" % (a["cls"], a["name"]))
        if not hit:
            print("no open item matches '%s'" % needle)
        save(st)
        return
    if not cc:
        return not_configured("canvas_watch")
    token, base, conf = cc
    if not DRY and "--force" not in args and not (7 <= NOW.hour < 22) and "--digest" not in args:
        return
    cv = Canvas(token, base, log)
    term_start = parse_dt(conf.get("term_start")) if conf.get("term_start") else school_year_start()
    courses = cv.courses(conf)
    if not courses:
        print("canvas_watch: Canvas answered but no active courses were found (check base_url and token)")
        return
    if "--digest" in args:
        head, body = ledger_text(st, floor)
        deliver("After school. %s.\n%s" % (head, "\n".join(body) or "Nothing open."))
        return
    events = []
    for cid, short in courses:
        snap = pull_assignments(cv, cid, short, term_start)
        if snap is not None:
            events += diff_assignments(st, cid, snap)
        events += pull_announcements(cv, st, cid, short)
        events += pull_modules(cv, st, cid, short)
    lines = [e[1] for e in events if e[0] != "CLOSE"]
    if not st["init"]:
        st["init"] = True
        head, body = ledger_text(st, floor)
        deliver("Canvas watchdog is live. %s.\n%s" % (head, "\n".join(body)))
        write_ledger_note(st, floor)
        save(st)
        return
    lines += escalation(st, floor)
    if lines:
        head, _ = ledger_text(st, floor)
        deliver("\n".join(lines) + "\n(%s)" % head)
    else:
        print("canvas_watch: nothing new (%s)" % ledger_text(st, floor)[0])
    write_ledger_note(st, floor)
    save(st)


def save(st):
    if not DRY:
        write_json(STATE_F, st)


def main():
    try:
        run(sys.argv[1:])
    except TokenDead:
        deliver("Canvas token is dead (401). The watchdog is blind until you make a new one: Canvas > Account > Settings > New Access Token, then tell Claude.")
    except Exception as e:  # a scheduled job must never crash loudly
        log("crash: %s" % e)
        print("canvas_watch: failed (%s), see %s" % (e, LOG_F))
    return 0


if __name__ == "__main__":
    sys.exit(main())
