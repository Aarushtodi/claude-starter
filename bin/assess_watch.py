#!/usr/bin/env python3
"""Weekly test-date watcher (Sundays 17:00). Zero tokens: no AI.

Snapshots every Canvas source that tends to carry test dates (front page, modules, unit/calendar pages,
assignments, linked files, public Google Docs) for your active courses and diffs against last week.
When something changed it writes the diff to ~/.claude/state/assess_watch/changes_<date>.md, adds dated
lines to ~/school/Projects/Inbox.md (Claude reads them next session and puts real test dates on your
calendar), and sends a notification.

  assess_watch.py [--dry] [--baseline]
  --dry       diff and print, save nothing
  --baseline  save snapshots, report nothing (first run does this by itself)
Config: ~/school/.config/canvas.json
"""
import difflib, hashlib, re, sys, urllib.error, urllib.request
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sc_common import (STATE, Canvas, TokenDead, canvas_conf, inbox_add, not_configured, parse_dt,  # noqa: E402
                       read_json, school_year_start, strip_html, write_json)

BASE = STATE / "assess_watch"
SNAP = BASE / "snap"
STATE_F = BASE / "state.json"
DOC_RE = re.compile(r"docs\.google\.com/(document|presentation)/d/([A-Za-z0-9_-]{20,})")
FILE_RE = re.compile(r"/courses/\d+/files/(\d+)")
PAGE_RE = re.compile(r'href="[^"]*/courses/\d+/pages/([^"?#/]+)"')
TITLE_RE = re.compile(r"calendar|schedule|unit|test|exam|quiz|assess|plan|syllabus|review|study", re.I)
TESTY = re.compile(r"test|exam|quiz|assessment|final|midterm", re.I)


def table_text(body):
    body = re.sub(r"</t[dh]>", " | ", body or "", flags=re.I)
    body = re.sub(r"</tr>|<br\s*/?>|</p>|</li>", "\n", body, flags=re.I)
    lines = [re.sub(r"\s+", " ", strip_html(l)).strip() for l in body.split("\n")]
    return "\n".join(l for l in lines if l)


def fetch_public(url):
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return r.read().decode("utf-8", "replace")
    except Exception:
        return None


def safe(s):
    return re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_").lower()[:40] or "course"


def course_sources(cv, cid, term_start):
    out, bodies = {}, []
    front = cv.get("/courses/%s/front_page" % cid)
    if isinstance(front, dict) and front.get("body"):
        out["front_page"] = table_text(front["body"])
        bodies.append(front["body"])
    modules = cv.get("/courses/%s/modules" % cid, {"include[]": "items", "per_page": 100})
    if isinstance(modules, list):
        lines = []
        for mod in modules:
            lines.append("## %s" % mod.get("name"))
            lines += ["- %s %s" % (i.get("title"), i.get("page_url") or i.get("external_url") or "") for i in mod.get("items", [])]
        out["modules"] = "\n".join(lines)
    slugs = []
    listing = cv.get("/courses/%s/pages" % cid, {"sort": "updated_at", "order": "desc", "per_page": 50}, paginate=False)
    if isinstance(listing, list):
        slugs += [p["url"] for p in listing if TITLE_RE.search(p.get("title", "")) and (p.get("updated_at") or "") >= term_start.strftime("%Y-%m-%d")][:12]
    if isinstance(front, dict):
        slugs += PAGE_RE.findall(front.get("body") or "")
    seen = set()
    for slug in list(dict.fromkeys(slugs))[:20]:
        page = cv.get("/courses/%s/pages/%s" % (cid, slug))
        if not isinstance(page, dict) or not page.get("body") or page.get("page_id") in seen:
            continue
        seen.add(page["page_id"])
        out["page_%s" % page["url"]] = "# %s\n%s" % (page.get("title"), table_text(page["body"]))
        bodies.append(page["body"])
    assigns = cv.get("/courses/%s/assignments" % cid, {"per_page": 100, "order_by": "due_at"})
    if isinstance(assigns, list):
        floor = term_start.strftime("%Y-%m-%d")
        out["assignments"] = "\n".join("%s | %s | %s pts" % (a.get("due_at") or "no due", a.get("name"), a.get("points_possible"))
                                        for a in assigns if (a.get("due_at") or "9999") >= floor)
    for fid in list(dict.fromkeys(FILE_RE.findall(" ".join(bodies))))[:15]:
        meta = cv.get("/courses/%s/files/%s" % (cid, fid))
        if isinstance(meta, dict) and meta.get("display_name"):
            out["file_%s" % fid] = "%s | updated %s | %s bytes" % (meta["display_name"], meta.get("updated_at"), meta.get("size"))
    for kind, did in list(dict.fromkeys(DOC_RE.findall(" ".join(bodies))))[:10]:
        url = ("https://docs.google.com/document/d/%s/export?format=txt" % did if kind == "document"
               else "https://docs.google.com/presentation/d/%s/export/txt" % did)
        text = fetch_public(url)
        if text and "<html" not in text[:500].lower():  # login walls come back as HTML
            out["gdoc_%s" % did] = "https://docs.google.com/%s/d/%s\n%s" % (kind, did, text)
    return out


def main():
    dry, baseline = "--dry" in sys.argv, "--baseline" in sys.argv
    cc = canvas_conf()
    if not cc:
        return not_configured("assess_watch")
    token, base, conf = cc
    cv = Canvas(token, base)
    term_start = parse_dt(conf.get("term_start")) if conf.get("term_start") else school_year_start()
    old_state = read_json(STATE_F)
    if old_state is None:
        baseline = True  # first run: just remember what is there
    old_state = old_state or {}
    courses = cv.courses(conf)
    if not courses:
        print("assess_watch: Canvas answered but no active courses were found (check base_url and token)")
        return
    new_state, report, testy = {}, [], 0
    for cid, short in courses:
        name = safe(short)
        for key, text in course_sources(cv, cid, term_start).items():
            sk = "%s/%s" % (name, key)
            h = hashlib.sha256(text.encode("utf-8")).hexdigest()
            new_state[sk] = h
            snap = SNAP / name / ("%s.txt" % key)
            if old_state.get(sk) != h and not baseline:
                old = snap.read_text(encoding="utf-8").splitlines() if snap.exists() else []
                diff = list(difflib.unified_diff(old, text.splitlines(), "last week", "now", lineterm="", n=2))
                added = [l[1:].strip() for l in diff if l.startswith("+") and not l.startswith("+++") and l[1:].strip()]
                if old and not added:
                    pass  # only removals (an old assignment fell off): not news
                else:
                    kind = "NEW" if not old else "CHANGED"
                    hits = [l for l in added if TESTY.search(l)]
                    testy += len(hits)
                    report.append((short, key, kind, hits or added, "### %s / %s (%s)\n%s" % (short, key, kind, "\n".join(diff[:300]))))
            if not dry:
                snap.parent.mkdir(parents=True, exist_ok=True)
                snap.write_text(text, encoding="utf-8")
    if dry:
        print("\n\n".join(r[4] for r in report) or "assess_watch: no changes")
        return
    write_json(STATE_F, new_state)
    if baseline:
        print("assess_watch: baseline saved (%d sources). Changes show up from next week." % len(new_state))
        return
    if not report:
        print("assess_watch: no Canvas plan changes this week")
        return
    today = datetime.now().strftime("%Y-%m-%d")
    changes = BASE / ("changes_%s.md" % today)
    changes.write_text("# Canvas assessment source changes %s\n\n%s\n" % (today, "\n\n".join(r[4] for r in report)), encoding="utf-8")
    lines = []
    for short, key, kind, shown, _ in report:
        snippet = " | ".join(s[:110] for s in shown[:4])
        lines.append("CANVAS PLAN CHANGED %s / %s (%s). Added: %s" % (short, key, kind, snippet))
    lines.append("Check those for test or quiz dates, put real ones on the calendar as TEST: lines, then sort these. Full diff: %s" % changes)
    inbox_add(lines)
    msg = "%d Canvas plan change(s) this week%s. Details in Projects/Inbox.md." % (len(report), (", %d mention a test or quiz" % testy) if testy else "")
    import notify
    notify.send(msg, "Canvas plan")


if __name__ == "__main__":
    try:
        main()
    except TokenDead:
        print("assess_watch: Canvas token is dead (401). Make a new one: Canvas > Account > Settings > New Access Token, then tell Claude.")
    except Exception as e:
        print("assess_watch: failed (%s)" % e)
    sys.exit(0)
