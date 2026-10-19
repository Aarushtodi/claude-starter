#!/usr/bin/env python3
"""Where is he right now, and can Claude ping him?

    school_clock.py            -> JSON state
    school_clock.py --line     -> one line for the SessionStart hook: "SCHOOL CLOCK: ..."
    school_clock.py --can-ping -> exit 0 if a notification may fire now, 1 if it should be held

States: no_school | before | in_class | passing | lunch | activity | evening
In class (and lunch) hold pings. Passing periods, before school, after school, weekends: fine.
Schedule lives in ~/school/.config/bells.json (A/B rotation, periods, lunch, no school days).
"""
import json, sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sc_common import CONF, HINT, read_json  # noqa: E402


def _d(s):
    return datetime.strptime(s, "%Y-%m-%d").date()


def _t(s):
    h, m = s.split(":")
    return int(h) * 60 + int(m)


def is_school_day(day, cfg):
    if day.weekday() >= 5 or day.strftime("%Y-%m-%d") in set(cfg.get("no_school", [])):
        return False
    for a, b in cfg.get("no_school_ranges", []):
        if _d(a) <= day <= _d(b):
            return False
    return True


def ab_day(day, cfg):
    """A or B for a school day, or None. Each quarter restarts the alternation; overrides pin a date."""
    ab = cfg.get("ab") or {}
    over = ab.get("overrides", {})
    for q in ab.get("quarters", []):
        s, e = _d(q["start"]), _d(q["end"])
        if not (s <= day <= e):
            continue
        cur, d = None, s
        while d <= day:
            if is_school_day(d, cfg):
                key = d.strftime("%Y-%m-%d")
                if key in over:
                    cur = over[key]
                elif cur is None:
                    cur = q["first"]
                else:
                    cur = "B" if cur == "A" else "A"
            d += timedelta(days=1)
        return cur if is_school_day(day, cfg) else None
    return None


def state(now=None):
    cfg = read_json(CONF / "bells.json")
    if not isinstance(cfg, dict) or "bells" not in cfg:
        return {"status": "unconfigured", "can_ping": True, "next_ok": None,
                "hint": "not configured yet, %s (bells.json)" % HINT}
    now = now or datetime.now()
    if not is_school_day(now.date(), cfg):
        return {"status": "no_school", "can_ping": True, "next_ok": None}
    ab = ab_day(now.date(), cfg)
    bell = cfg["bells"].get("wednesday") if (now.weekday() == 2 and cfg["bells"].get("wednesday")) else cfg["bells"]["standard"]
    t = now.hour * 60 + now.minute
    base = {"ab_day": ab}
    if t < _t(bell[0]["start"]):
        return dict(base, status="before", can_ping=True, next_ok=None)
    for i, b in enumerate(bell):
        s, e = _t(b["start"]), _t(b["end"])
        if s <= t < e:
            label = b["label"]
            status = "lunch" if label == "lunch" else ("activity" if label == "activity" else "in_class")
            hold = status != "activity"
            end_dt = now.replace(hour=e // 60, minute=e % 60, second=0, microsecond=0)
            return dict(base, status=status, period=label, can_ping=not hold,
                        next_ok=end_dt.isoformat() if hold else None, ends=b["end"])
        if i + 1 < len(bell) and e <= t < _t(bell[i + 1]["start"]):
            return dict(base, status="passing", period="%s->%s" % (b["label"], bell[i + 1]["label"]), can_ping=True, next_ok=None)
    return dict(base, status="evening", can_ping=True, next_ok=None)


def line(st):
    if st["status"] == "unconfigured":
        return "SCHOOL CLOCK: " + st["hint"]
    ab = (" (%s day)" % st["ab_day"]) if st.get("ab_day") else ""
    if st["status"] == "in_class":
        return "SCHOOL CLOCK: in class, %s%s, ends %s. No pings, answer only what he asks." % (st["period"], ab, st["ends"])
    if st["status"] == "lunch":
        return "SCHOOL CLOCK: at lunch%s, ends %s. No pings." % (ab, st["ends"])
    if st["status"] == "no_school":
        return "SCHOOL CLOCK: no school today. Pings are fine."
    name = {"before": "before school", "evening": "after school", "passing": "between classes"}.get(st["status"], st["status"])
    return "SCHOOL CLOCK: %s%s. Pings are fine." % (name, ab)


if __name__ == "__main__":
    try:
        st = state()
    except Exception as e:
        st = {"status": "unconfigured", "can_ping": True, "next_ok": None, "hint": "bells.json unreadable (%s), %s" % (e, HINT)}
    if "--can-ping" in sys.argv:
        sys.exit(0 if st["can_ping"] else 1)
    print(line(st) if "--line" in sys.argv else json.dumps(st))
