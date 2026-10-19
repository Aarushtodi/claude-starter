#!/usr/bin/env python3
"""Daily 16:40. Every Canvas grade under full points from the last 7 days gets a pre-filled "weak" note in
~/school/Notes, so the one note per missed question habit starts from a stub instead of a blank page. Zero tokens.

  weak_notes.py [--dry]
Reads scores through the Canvas API (submissions with score below points possible). If your token cannot read
scores it says so and exits 0. Config: ~/school/.config/canvas.json. State: ~/.claude/state/weak_notes.json
"""
import re, sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sc_common import (SCHOOL, STATE, Canvas, TokenDead, canvas_conf, not_configured, now, parse_dt,  # noqa: E402
                       read_json, write_json)

DRY = "--dry" in sys.argv
STATE_F = STATE / "weak_notes.json"
NOTES = SCHOOL / "Notes"


def safe(s):
    return re.sub(r'[\\/:*?"<>|]+', "-", s).strip()[:70]


def note_text(cls, name, score, when, url):
    return ("---\nclass: %s\nunit: \nstatus: weak\ntype: concept\ndate: %s\nscore: %s\nsource: Canvas\n---\n"
            "# %s | %s | %s\n\n## What I missed\n- [ ] q: ___ | why: ___\n- [ ] q: ___ | why: ___\n\n"
            "## Next\n- one concept note per missed question (Templates/Concept Note.md), each `status: weak`\n"
            "- then set this note to `status: solid`\n%s" % (
                cls, when, score, cls, name, score, ("- Canvas: %s\n" % url) if url else ""))


def main():
    cc = canvas_conf()
    if not cc:
        return not_configured("weak_notes")
    token, base, conf = cc
    cv = Canvas(token, base)
    t0 = now()
    since = (t0 - timedelta(days=7))
    state = read_json(STATE_F, {}) or {}
    made, seen_any, denied = [], False, []
    for cid, short in cv.courses(conf):
        rows = cv.get("/courses/%s/students/submissions" % cid,
                      {"student_ids[]": "self", "include[]": "assignment", "graded_since": since.isoformat(), "per_page": 100})
        if rows is None:
            denied.append("%s (HTTP %s)" % (short, getattr(cv, "last_error", "?")))
            continue
        seen_any = True
        for s in rows:
            a = s.get("assignment") or {}
            pts, score = a.get("points_possible"), s.get("score")
            if score is None or not pts or s.get("excused") or score >= pts:
                continue
            graded = parse_dt(s.get("graded_at"))
            if graded and graded < since:
                continue
            key = "%s|%s" % (cid, a.get("id"))
            name = (a.get("name") or "assignment").strip()
            path = NOTES / ("Weak - %s %s.md" % (safe(short), safe(name)))
            if key in state or path.exists():
                continue
            state[key] = t0.strftime("%Y-%m-%d")
            when = (parse_dt(s.get("graded_at")) or t0).strftime("%Y-%m-%d")
            if DRY:
                print("WOULD WRITE %s" % path)
            else:
                NOTES.mkdir(parents=True, exist_ok=True)
                path.write_text(note_text(safe(short), name, "%g/%g" % (score, pts), when, a.get("html_url")), encoding="utf-8")
            made.append("%s %s %g/%g" % (short, name, score, pts))
    if not DRY:
        write_json(STATE_F, state)
    if denied and not seen_any:
        print("weak_notes: Canvas would not return scores for any course: %s. Your token may not be allowed to read grades, so nothing was "
              "created. Ask Claude to read the grades in Chrome instead." % ", ".join(denied))
        return
    if denied:
        print("weak_notes: skipped (no score access): %s" % ", ".join(denied))
    if made:
        print("weak_notes: %d new weak note(s) in ~/school/Notes to fill in: %s" % (len(made), "; ".join(made)))
    else:
        print("weak_notes: nothing new under 100 in the last 7 days" if seen_any else "weak_notes: no courses found")


if __name__ == "__main__":
    try:
        main()
    except TokenDead:
        print("weak_notes: Canvas token is dead (401). Make a new one: Canvas > Account > Settings > New Access Token, then tell Claude.")
    except Exception as e:
        print("weak_notes: failed (%s)" % e)
    sys.exit(0)
