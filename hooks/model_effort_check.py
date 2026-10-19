#!/usr/bin/env python3
"""UserPromptSubmit hook: tell Claude which model and effort this chat is on, so it can flag a bad fit
in one line. Reads only this chat's own state file written by statusline.py. If missing or stale, says nothing."""
import json, os, sys, time
try:
    sid = json.load(sys.stdin).get("session_id")
    with open(os.path.expanduser("~/.claude/state/live_model/%s.json" % sid), encoding="utf-8") as f:
        st = json.load(f)
    if not sid or st.get("session_id") != sid or time.time() - st.get("ts", 0) > 1800:
        raise ValueError("stale")
except Exception:
    sys.exit(0)  # unknown model: no line beats a wrong line
cur = "%s (%s), effort %s" % (st.get("name", "?"), st.get("id", "?"), st.get("effort", "?"))
print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext":
    "MODEL/EFFORT MONITOR: this chat is on " + cur + " (from this chat's status line). "
    "Rule from CLAUDE.md: Sonnet default, Opus only for hard essays, BPA strategy, or something broken. "
    "If this message does not fit the model, say so in ONE line, for example 'worth /model opus for this' or "
    "'sonnet is plenty here'. If it fits, say nothing. Before flagging, check the model named in your own "
    "system prompt; if it disagrees with this line, trust the system prompt and do not flag."}}))
