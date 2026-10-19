#!/usr/bin/env python3
"""UserPromptSubmit hook: when Srijan calls out a bad answer, remind Claude to log it to Claude Misses first."""
import json, re, sys

PATTERNS = [
    r"\bstupi?d\b", r"\bdumb", r"\bidiot", r"\bwtf\b", r"\bbruh\b",
    r"\bcall(ing)? (you|u) out\b", r"\bcallout\b", r"\bsave (this|that|it) miss\b", r"\bmiss log\b",
    r"\b(that'?s|thats|ur|you'?re|youre) (so )?wrong\b", r"\bnot what i (said|asked|meant)\b",
    r"\bmakes no sense\b", r"\bwhy would you\b", r"\bdid i (say|ask)\b",
]

try:
    prompt = json.load(sys.stdin).get("prompt", "")
except Exception:
    sys.exit(0)

low = prompt.lower()
hit = next((p for p in PATTERNS if re.search(p, low)), None)
if hit:
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "UserPromptSubmit",
        "additionalContext": (
            "CALL-OUT CHECK (callout_detect.py matched '" + hit + "'): if he is calling out something you said, "
            "BEFORE fixing it, append an entry to ~/school/Projects/Claude Misses.md "
            "(date/time, what you said quoted, his words verbatim, why it was wrong, the fix, rule changed). "
            "Update the matching rule in ~/.claude/CLAUDE.md if one applies (show him the line first). "
            "Then confirm 'logged' in one line and fix the answer. "
            "If it is not a call-out at you (for example venting about someone else), ignore this.")}}))
