#!/usr/bin/env python3
"""Status line: shows the live model and effort at the bottom of Claude Code, and saves them
so the model_effort_check hook can read the real state of this chat. Zero tokens."""
import json, os, sys, time
try:
    d = json.load(sys.stdin)
except Exception:
    d = {}
m = d.get("model") or {}
mid, name = m.get("id", ""), m.get("display_name", "?")
effort = d.get("effort") or d.get("effort_level") or m.get("effort")
if isinstance(effort, dict):
    effort = effort.get("level")
if not effort:
    try:
        with open(os.path.expanduser("~/.claude/settings.json"), encoding="utf-8-sig") as f:
            s = json.load(f)
        effort = (s.get("modelSettings", {}).get(mid, {}) or {}).get("effortLevel")
        effort = (effort or "default") + "*"   # * = from settings, not live
    except Exception:
        effort = "?"
try:
    # one file per chat so another session's model never leaks into this one
    sid = d.get("session_id") or "unknown"
    os.makedirs(os.path.expanduser("~/.claude/state/live_model"), exist_ok=True)
    with open(os.path.expanduser("~/.claude/state/live_model/%s.json" % sid), "w", encoding="utf-8") as f:
        json.dump({"id": mid, "name": name, "effort": effort, "session_id": sid, "ts": time.time()}, f)
except Exception:
    pass
print("%s | effort %s" % (name, effort))
