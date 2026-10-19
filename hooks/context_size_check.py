#!/usr/bin/env python3
"""UserPromptSubmit hook (10/14): warn when this chat's context gets long, since every step re-reads all of it.
Fires once per threshold (150k, 300k, 500k) per chat so it doesn't nag."""
import json, os, re, sys
STEPS = [150_000, 300_000, 500_000]
STATE = os.path.expanduser("~/.claude/state/context_warned")
try:
    data = json.load(sys.stdin)
    path = data.get("transcript_path", "")
    session = re.sub(r"[^A-Za-z0-9_-]", "", data.get("session_id", ""))[:64]
    with open(path, "rb") as f:
        f.seek(0, 2); f.seek(max(0, f.tell() - 400_000))
        tail = f.read().decode("utf-8", "ignore").splitlines()
except Exception:
    sys.exit(0)
ctx = 0
for line in reversed(tail):
    if '"usage"' not in line:
        continue
    try:
        d = json.loads(line)
    except Exception:
        continue
    u = d.get("message", {}).get("usage") if d.get("type") == "assistant" and not d.get("isSidechain") else None
    if u:
        ctx = u.get("input_tokens", 0) + u.get("cache_read_input_tokens", 0) + u.get("cache_creation_input_tokens", 0)
        break
hit = max([s for s in STEPS if ctx >= s], default=0)
if not hit or not session:
    sys.exit(0)
mark = os.path.join(STATE, session)
try:
    done = int(open(mark).read().strip() or 0)
except Exception:
    done = 0
if hit <= done:
    sys.exit(0)
try:
    os.makedirs(STATE, exist_ok=True); open(mark, "w").write(str(hit))
except Exception:
    pass
print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext":
    f"CONTEXT SIZE: this chat is at ~{ctx // 1000}k tokens and every step re-reads all of it. "
    "At the end of your reply add ONE line: if the topic changed, 'fresh chat for this one (/clear)'; "
    "if he is mid-task, '/compact would cut the re-reads'. Before /clear, make sure state is saved to your notes in ~/school/Notes."}}))
