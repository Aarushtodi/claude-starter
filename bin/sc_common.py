"""Shared helpers for the school automations. Stdlib only, runs on Windows (Git Bash) and Linux."""
import json, re, ssl, sys, time, urllib.error, urllib.parse, urllib.request
from datetime import datetime, timedelta
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HOME = Path.home()
SCHOOL = HOME / "school"
CONF = SCHOOL / ".config"
STATE = HOME / ".claude" / "state"
HINT = "see ~/school/.config/README.md"


class TokenDead(Exception):
    pass


def read_json(path, default=None):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8-sig"))
    except Exception:
        return default


def write_json(path, data):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=1), encoding="utf-8")


def canvas_conf():
    """(token, base_url, full config) or None when not set up yet."""
    c = read_json(CONF / "canvas.json")
    if not isinstance(c, dict):
        return None
    token = str(c.get("token", "")).strip()
    if not token or token.upper().startswith(("PASTE", "YOUR")):
        return None
    base = str(c.get("base_url") or "https://friscoisd.instructure.com").rstrip("/")
    return token, base, c


def not_configured(name):
    print("%s: not configured yet, %s (canvas.json needs your Canvas token)" % (name, HINT))


def now():
    return datetime.now().astimezone()


def parse_dt(s):
    if not s:
        return None
    return datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone()


def fmt_due(dt, ref=None):
    if not dt:
        return "no due date"
    ref = ref or now()
    if dt.date() == ref.date():
        day = "today"
    elif dt.date() == (ref + timedelta(days=1)).date():
        day = "tmrw"
    else:
        day = "%s %d/%d" % (dt.strftime("%a"), dt.month, dt.day)
    h = dt.hour % 12 or 12
    return "%s %d:%02d%s" % (day, h, dt.minute, "am" if dt.hour < 12 else "pm")


def strip_html(s):
    s = re.sub(r"<[^>]+>", " ", s or "").replace("&nbsp;", " ").replace("&amp;", "&")
    return re.sub(r"\s+", " ", s).strip()


def school_year_start():
    t = datetime.now()
    y = t.year if t.month >= 7 else t.year - 1
    return datetime(y, 8, 1).astimezone()


class Canvas:
    def __init__(self, token, base, log=None):
        self.token, self.base, self.log = token, base, log or (lambda m: None)
        self.ctx = ssl.create_default_context()

    def get(self, path, params=None, paginate=True):
        url = self.base + "/api/v1" + path
        if params:
            url += ("&" if "?" in url else "?") + urllib.parse.urlencode(params, doseq=True)
        out = []
        while url:
            req = urllib.request.Request(url, headers={"Authorization": "Bearer " + self.token})
            data, link = None, ""
            for attempt in range(3):  # Canvas drops connections now and then
                try:
                    with urllib.request.urlopen(req, context=self.ctx, timeout=45) as r:
                        data = json.loads(r.read().decode("utf-8"))
                        link = r.headers.get("Link", "")
                    break
                except urllib.error.HTTPError as e:
                    if e.code == 401:
                        raise TokenDead()
                    self.log("HTTP %s on %s" % (e.code, path))
                    self.last_error = e.code
                    return None
                except Exception as e:
                    self.log("ERR %s try %d: %s" % (path, attempt + 1, e))
                    time.sleep(1)
            if data is None:
                return None
            if not isinstance(data, list):
                return data
            out.extend(data)
            m = re.search(r'<([^>]+)>; rel="next"', link)
            url = m.group(1) if (m and paginate) else None
        return out

    def courses(self, conf=None):
        """[(course_id str, short name)] for active student courses, or the ids listed in canvas.json."""
        ids = (conf or {}).get("course_ids")
        rows = self.get("/courses", {"enrollment_state": "active", "per_page": 100}) or []
        out = []
        for c in rows:
            if not isinstance(c, dict) or not c.get("name"):
                continue
            if ids and str(c["id"]) not in [str(i) for i in ids]:
                continue
            out.append((str(c["id"]), (c.get("course_code") or c["name"]).strip()[:30]))
        return out


def inbox_add(lines):
    """Append dated lines under '## Unsorted' in ~/school/Projects/Inbox.md (keeps CRLF if the file has it)."""
    p = SCHOOL / "Projects" / "Inbox.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    if not p.exists():
        p.write_text("---\ntype: reference\nstatus: active\nupdated: %s\n---\n# Inbox\n\n## Unsorted\n\n## Sorted\n" % today,
                     encoding="utf-8", newline="")
    text = p.read_bytes().decode("utf-8-sig")
    nl = "\r\n" if "\r\n" in text else "\n"
    add = nl.join("- [%s] %s" % (today, l) for l in lines)
    m = re.search(r"^## Unsorted[ \t]*\r?\n", text, re.M)
    if m:
        text = text[:m.end()] + add + nl + text[m.end():]
    else:
        text = text.rstrip() + nl + nl + "## Unsorted" + nl + add + nl
    text = re.sub(r"^updated:.*$", "updated: " + today, text, count=1, flags=re.M)
    p.write_bytes(text.encode("utf-8"))
