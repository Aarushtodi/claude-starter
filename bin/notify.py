#!/usr/bin/env python3
"""notify.py "text" [--title T]   Pop a desktop notification, always also print the text.
Windows: toast via notify.ps1, then msg * as a fallback. Linux: notify-send. Otherwise just prints.
Holds the notification (queues it) while school_clock says he is in class; the next call outside class flushes the queue.
NOTIFY_NOW=1 skips the hold. Never raises, always exits 0."""
import os, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sc_common import STATE  # noqa: E402

QUEUE = STATE / "held_pings.txt"


def _toast(title, text):
    try:
        if sys.platform in ("win32", "cygwin", "msys") or os.name == "nt":
            env = dict(os.environ, CLAUDE_TOAST_TITLE=title, CLAUDE_TOAST_BODY=text)
            ps1 = str(Path(__file__).resolve().parent / "notify.ps1")
            r = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", ps1],
                               env=env, capture_output=True, timeout=20)
            if r.returncode == 0:
                return True
            r = subprocess.run(["msg", "*", "%s: %s" % (title, text)], capture_output=True, timeout=20)
            return r.returncode == 0
        import shutil
        if shutil.which("notify-send"):
            return subprocess.run(["notify-send", title, text], capture_output=True, timeout=10).returncode == 0
    except Exception:
        pass
    return False


def can_ping():
    try:
        import school_clock
        return bool(school_clock.state().get("can_ping", True))
    except Exception:
        return True


def send(text, title="Claude"):
    print(text)
    if os.environ.get("NOTIFY_NOW") != "1" and not can_ping():
        QUEUE.parent.mkdir(parents=True, exist_ok=True)
        with open(QUEUE, "a", encoding="utf-8") as f:
            f.write(text.replace("\n", " / ") + "\n")
        print("(notification held, he is in class; it goes out after the bell)")
        return
    held = ""
    if QUEUE.exists():
        held = QUEUE.read_text(encoding="utf-8").strip()
        QUEUE.unlink()
    if held:
        text = text + "\nHeld earlier: " + held
    if not _toast(title, text[:900]):
        print("(no desktop notification available, printed only)")


if __name__ == "__main__":
    a = sys.argv[1:]
    title = "Claude"
    if "--title" in a:
        i = a.index("--title")
        title = a[i + 1]
        del a[i:i + 2]
    try:
        send(" ".join(a) or "(empty)", title)
    except Exception as e:
        print("notify failed: %s" % e)
    sys.exit(0)
