#!/usr/bin/env python3
"""Bedtime block: blocks Instagram, TikTok and YouTube on this laptop at night by editing the hosts file.
Zero Claude usage. Stdlib only. Windows (Git Bash) and Linux.

  python3 bedtime_block.py on        add the block (needs admin / root)
  python3 bedtime_block.py off       remove it (refused between 21:00 and 06:00 while the block is due)
  python3 bedtime_block.py status    what is blocked, tonight's time, skips used this week
  python3 bedtime_block.py skip      take tonight off (only before 21:00, max 2 per week)
  python3 bedtime_block.py check     make the block match the clock (the scheduled failsafe)
  python3 bedtime_block.py schedule  register the scheduled jobs (needs admin / root); add --remove to undo, --dry to preview

Config: ~/school/.config/bedtime.json, written by Claude in the Phase 8c interview:
  {"bedtime": "22:00", "weekend_bedtime": null, "wake": "06:00", "sites": ["instagram.com","tiktok.com","youtube.com"],
   "skip_cap": 2, "say_rule": true}
  bedtime = Sun to Thu nights. weekend_bedtime = Fri and Sat nights ("23:00"), null = no block on Fri/Sat.
  sites = base domains to block (www, m and known api hosts are added for each). skip_cap is clamped to 2.
State:  ~/school/.config/bedtime_state.json (skips). Test overrides: HOSTS_FILE, BEDTIME_NOW="YYYY-MM-DD HH:MM", BEDTIME_PLATFORM=windows|linux.
Aarush's rules, kept: never lift after 21:00, skips only before 21:00, max 2 per ISO week.
"""
import json, os, re, shutil, subprocess, sys
from datetime import datetime, timedelta
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

START = "# BEDTIME-BLOCK START"
END = "# BEDTIME-BLOCK END"
DEFAULT_SITES = ["instagram.com", "tiktok.com", "youtube.com"]
EXTRA_HOSTS = {  # hosts Aarush's block also covers for the three defaults
    "instagram.com": ["i.instagram.com", "l.instagram.com", "api.instagram.com"],
    "tiktok.com": ["vm.tiktok.com", "api.tiktok.com"],
    "youtube.com": ["youtu.be", "youtubei.googleapis.com"],
}
HOST_LINE = re.compile(r"^(0\.0\.0\.0|::) [A-Za-z0-9.-]+$")
DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
SCHOOL_NIGHTS = ["sun", "mon", "tue", "wed", "thu"]
CUTOFF_HOUR = 21
HARD_MAX_SKIPS = 2
RULE = "Rule: the block stays after 9pm. Skips are only before 9pm, max 2 a week."
TAG = "claude-starter-bedtime"
ALL_TASKS = ("ClaudeBedtimeOn", "ClaudeBedtimeOnWeekend", "ClaudeBedtimeOff", "ClaudeBedtimeCheck")


def tasks():
    return [n for n in ALL_TASKS if n != "ClaudeBedtimeOnWeekend" or conf()["weekend"]]


def platform():
    p = os.environ.get("BEDTIME_PLATFORM", "").lower()
    if p in ("windows", "linux"):
        return p
    return "windows" if os.name == "nt" else "linux"


def home():
    if os.environ.get("BEDTIME_HOME"):
        return Path(os.environ["BEDTIME_HOME"])
    if os.name != "nt" and os.environ.get("SUDO_USER") and os.geteuid() == 0:
        try:
            import pwd
            return Path(pwd.getpwnam(os.environ["SUDO_USER"]).pw_dir)
        except Exception:
            pass
    return Path.home()


CONF_DIR = home() / "school" / ".config"
CONF_FILE = CONF_DIR / "bedtime.json"
STATE_FILE = CONF_DIR / "bedtime_state.json"
LOG_FILE = home() / ".claude" / "state" / "bedtime.log"


def hosts_path():
    if os.environ.get("HOSTS_FILE"):
        return Path(os.environ["HOSTS_FILE"])
    if platform() == "windows":
        return Path(os.environ.get("SystemRoot", r"C:\Windows")) / "System32" / "drivers" / "etc" / "hosts"
    return Path("/etc/hosts")


def now():
    v = os.environ.get("BEDTIME_NOW")
    if v:
        return datetime.strptime(v, "%Y-%m-%d %H:%M")
    return datetime.now().replace(second=0, microsecond=0)


def log(msg):
    try:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write("%s %s\n" % (datetime.now().strftime("%F %T"), msg))
    except Exception:
        pass


def load_json(p, default):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8-sig"))
    except Exception:
        return default


def hhmm(s, fallback):
    m = re.fullmatch(r"([01]?\d|2[0-3]):([0-5]\d)", str(s).strip())
    return (int(m.group(1)), int(m.group(2))) if m else fallback


def domain_list(sites):
    out = []
    for b in sites:
        for d in [b, "www." + b, "m." + b] + EXTRA_HOSTS.get(b, []):
            if d not in out:
                out.append(d)
    return out


def conf():
    c = load_json(CONF_FILE, {})
    if not isinstance(c, dict):
        c = {}
    bed = hhmm(c.get("bedtime", ""), (22, 0))
    if bed[0] < 19:
        bed = (22, 0)
    wk = c.get("weekend_bedtime")
    weekend = hhmm(wk, None) if wk else None
    if weekend and weekend[0] < 19:
        weekend = None
    wake = hhmm(c.get("wake", ""), (6, 0))
    sites = c.get("sites")
    if isinstance(sites, list):
        sites = [str(x).lower().strip() for x in sites if re.fullmatch(r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}", str(x).strip())]
        sites = [x[4:] if x.startswith("www.") else x for x in sites]
    else:
        sites = []
    try:
        cap = max(0, min(HARD_MAX_SKIPS, int(c.get("skip_cap", HARD_MAX_SKIPS))))
    except Exception:
        cap = HARD_MAX_SKIPS
    return {"bed": bed, "weekend": weekend, "wake": wake, "sites": sites or DEFAULT_SITES,
            "cap": cap, "say_rule": c.get("say_rule", True) is not False}


def night_bed(cf, night):
    """Bedtime for this night, or None when that night has no block."""
    return cf["bed"] if DAYS[night.weekday()] in SCHOOL_NIGHTS else cf["weekend"]


def refuse(msg):
    print("REFUSED: %s%s" % (msg, (" " + RULE) if conf()["say_rule"] else ""))


def state():
    s = load_json(STATE_FILE, {})
    if not isinstance(s, dict) or not isinstance(s.get("skips"), list):
        s = {"skips": []}
    return s


def week_key(d):
    iso = d.isocalendar()
    return (iso[0], iso[1])


def skips_this_week(night):
    n = 0
    for s in state()["skips"]:
        try:
            if week_key(datetime.strptime(s, "%Y-%m-%d").date()) == week_key(night):
                n += 1
        except Exception:
            pass
    return n


def block_due(t):
    """(due, night, why). Due = inside tonight's window on a block night that was not skipped.
    A night is the date the evening started; times before wake belong to the night before."""
    cf = conf()
    cur = (t.hour, t.minute)
    night = t.date() - timedelta(days=1) if cur < cf["wake"] else t.date()
    bed = night_bed(cf, night)
    if bed is None:
        return False, night, "no block tonight"
    if night.strftime("%Y-%m-%d") in state()["skips"]:
        return False, night, "tonight is skipped"
    if cur >= bed or cur < cf["wake"]:
        return True, night, "in window"
    return False, night, "before bedtime"


# ---------- hosts file ----------

def read_hosts():
    p = hosts_path()
    return p.read_bytes().decode("utf-8", errors="surrogateescape") if p.exists() else ""


def has_block(text):
    return START in text


def strip_block(text):
    """Remove only our own marker section; every other line stays byte for byte."""
    out, inside = [], False
    for line in text.splitlines(keepends=True):
        bare = line.strip()
        if not inside and bare == START:
            inside = True
            continue
        if inside:
            if bare == END:
                inside = False
                continue
            if HOST_LINE.match(bare):
                continue
            inside = False  # damaged section: keep this line and stop dropping
        out.append(line)
    return "".join(out)


def make_block(nl):
    lines = [START]
    for d in domain_list(conf()["sites"]):
        lines += ["0.0.0.0 " + d, ":: " + d]
    lines.append(END)
    return nl.join(lines) + nl


def write_hosts(text):
    p = hosts_path()
    try:
        bak = p.with_name(p.name + ".bedtime.bak")
        if p.exists() and not bak.exists():
            shutil.copyfile(str(p), str(bak))
        p.write_bytes(text.encode("utf-8", errors="surrogateescape"))
    except PermissionError:
        who = "an administrator PowerShell" if platform() == "windows" else "sudo"
        print("NEEDS ADMIN: can't edit the hosts file from here. The scheduled job does it; manual runs need %s." % who)
        sys.exit(2)


def flush_dns():
    if os.environ.get("HOSTS_FILE"):
        return
    try:
        if platform() == "windows":
            subprocess.run(["ipconfig", "/flushdns"], capture_output=True, timeout=20)
        elif shutil.which("resolvectl"):
            subprocess.run(["resolvectl", "flush-caches"], capture_output=True, timeout=20)
        elif shutil.which("systemd-resolve"):
            subprocess.run(["systemd-resolve", "--flush-caches"], capture_output=True, timeout=20)
    except Exception:
        pass


def do_on():
    text = read_hosts()
    if has_block(text):
        print("block already on (nothing changed)")
        return
    nl = "\r\n" if "\r\n" in text else "\n"
    if text and not text.endswith("\n"):
        text += nl
    write_hosts(text + make_block(nl))
    flush_dns()
    log("BLOCK ON")
    cf = conf()
    print("block ON: %s blocked until %02d:%02d" % (", ".join(cf["sites"]), cf["wake"][0], cf["wake"][1]))


def do_off():
    text = read_hosts()
    if not has_block(text):
        print("block already off (nothing changed)")
        return
    write_hosts(strip_block(text))
    flush_dns()
    log("BLOCK OFF")
    print("block OFF")


# ---------- commands ----------

def cmd_on(a):
    _, night, why = block_due(now())
    if why == "tonight is skipped":
        print("tonight (%s) is skipped, block not added" % night)
        return 0
    do_on()
    return 0


def cmd_off(a):
    t = now()
    due, night, why = block_due(t)
    if has_block(read_hosts()) and due and (t.hour >= CUTOFF_HOUR or (t.hour, t.minute) < conf()["wake"]):
        refuse("it is %s and the block is due tonight." % t.strftime("%H:%M"))
        log("off REFUSED at %s" % t.strftime("%F %H:%M"))
        return 3
    do_off()
    return 0


def cmd_check(a):
    due, night, why = block_due(now())
    has = has_block(read_hosts())
    if due and not has:
        do_on()
    elif not due and has:
        do_off()
    else:
        print("check: nothing to change (%s)" % why)
    return 0


def cmd_skip(a):
    t = now()
    cf = conf()
    if t.hour >= CUTOFF_HOUR or (t.hour, t.minute) < cf["wake"]:
        refuse("it is %s." % t.strftime("%H:%M"))
        log("skip REFUSED (late) at %s" % t.strftime("%F %H:%M"))
        return 3
    night = t.date()
    key = night.strftime("%Y-%m-%d")
    if night_bed(cf, night) is None:
        print("tonight is not a block night, nothing to skip")
        return 0
    st = state()
    if key in st["skips"]:
        print("tonight is already skipped")
        return 0
    used = skips_this_week(night)
    if used >= cf["cap"]:
        refuse("%d of %d skips already used this week." % (used, cf["cap"]))
        log("skip REFUSED (limit) %s" % key)
        return 3
    st["skips"] = (st["skips"] + [key])[-60:]
    CONF_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(st, indent=1), encoding="utf-8")
    log("skip granted %s" % key)
    print("skipped tonight (%s). Skips used this week: %d of %d" % (key, used + 1, cf["cap"]))
    return 0


def tasks_registered():
    if platform() == "windows":
        if os.environ.get("BEDTIME_PLATFORM"):
            return None
        try:
            return all(subprocess.run(["schtasks", "/query", "/tn", n], capture_output=True, timeout=20).returncode == 0
                       for n in tasks())
        except Exception:
            return None
    return (CONF_DIR / "bedtime_scheduled").exists()


def cmd_status(a):
    t = now()
    cf = conf()
    due, night, why = block_due(t)
    on = has_block(read_hosts())
    print("hosts block: %s" % ("ON" if on else "off"))
    print("block window: %02d:%02d to %02d:%02d Sun to Thu nights; Fri and Sat: %s" % (
        cf["bed"] + cf["wake"] + (("from %02d:%02d" % cf["weekend"]) if cf["weekend"] else "no block",)))
    print("blocked sites: %s" % ", ".join(cf["sites"]))
    print("tonight (%s): %s" % (night, "due now" if due else why))
    print("skips used this week: %d of %d" % (skips_this_week(night), cf["cap"]))
    r = tasks_registered()
    print("scheduled jobs: %s" % ("registered" if r else ("not registered" if r is False else "unknown")))
    if on != due:
        print("note: block does not match the clock yet; the scheduled `check` fixes it")
    return 0


def is_admin():
    if platform() == "windows":
        try:
            import ctypes
            return bool(ctypes.windll.shell32.IsUserAnAdmin())
        except Exception:
            return False
    return os.geteuid() == 0


def cmd_schedule(a):
    remove, dry = "--remove" in a, "--dry" in a
    cf = conf()
    bed, wake, weekend = cf["bed"], cf["wake"], cf["weekend"]
    script = str(Path(__file__).resolve())
    if platform() == "windows":
        full = {"mon": "Monday", "tue": "Tuesday", "wed": "Wednesday", "thu": "Thursday", "fri": "Friday",
                "sat": "Saturday", "sun": "Sunday"}
        py = sys.executable or "python"
        w = Path(py).with_name("pythonw.exe")
        if w.exists():
            py = str(w)
        ps = []
        if remove:
            ps += ["Unregister-ScheduledTask -TaskName %s -Confirm:$false -ErrorAction SilentlyContinue" % n for n in ALL_TASKS]
        else:
            ps.append("$p = New-ScheduledTaskPrincipal -UserId \"$env:USERDOMAIN\\$env:USERNAME\" -LogonType Interactive -RunLevel Highest")
            ps.append("$s = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable")

            def task(name, arg, trig):
                ps.append("$a = New-ScheduledTaskAction -Execute '%s' -Argument '\"%s\" %s'" % (py, script, arg))
                ps.append("Register-ScheduledTask -TaskName %s -Action $a -Trigger (%s) -Principal $p -Settings $s -Force | Out-Null" % (name, trig))
            task("ClaudeBedtimeOn", "on", "New-ScheduledTaskTrigger -Weekly -DaysOfWeek %s -At %02d:%02d" % (",".join(full[n] for n in SCHOOL_NIGHTS), bed[0], bed[1]))
            if weekend:
                task("ClaudeBedtimeOnWeekend", "on", "New-ScheduledTaskTrigger -Weekly -DaysOfWeek Friday,Saturday -At %02d:%02d" % weekend)
            task("ClaudeBedtimeOff", "check", "New-ScheduledTaskTrigger -Daily -At %02d:%02d" % wake)
            task("ClaudeBedtimeCheck", "check",
                 "New-ScheduledTaskTrigger -Once -At 00:01 -RepetitionInterval (New-TimeSpan -Minutes 15) -RepetitionDuration (New-TimeSpan -Days 3650)")
        cmd = "\n".join(ps)
        if dry:
            print(cmd)
            return 0
        if not is_admin():
            print("NEEDS ADMIN: Windows only lets an elevated PowerShell create tasks that edit the hosts file.")
            print("Claude: give Srijan these clicks:")
            print("  1. Click Start, type PowerShell. 2. Right click Windows PowerShell, click Run as administrator, click Yes.")
            print('  3. Paste this and press Enter: & "%s" "%s" schedule' % (sys.executable, script))
            return 2
        r = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", cmd], capture_output=True, text=True)
        if r.returncode != 0:
            print("FAIL: " + (r.stderr or r.stdout).strip()[:300])
            return 1
        print("removed the bedtime tasks" if remove else "registered %s (run elevated)" % ", ".join(tasks()))
        return 0
    # Linux: root crontab, because the hosts file is root only
    dmap = {"mon": 1, "tue": 2, "wed": 3, "thu": 4, "fri": 5, "sat": 6, "sun": 0}
    py = shutil.which("python3") or sys.executable
    env = "BEDTIME_HOME=%s" % home()
    lines = [] if remove else [
        "%d %d * * %s %s %s %s on # %s" % (bed[1], bed[0], ",".join(str(dmap[n]) for n in SCHOOL_NIGHTS), env, py, script, TAG),
    ] + ([
        "%d %d * * 5,6 %s %s %s on # %s" % (weekend[1], weekend[0], env, py, script, TAG)] if weekend else []) + [
        "%d %d * * * %s %s %s check # %s" % (wake[1], wake[0], env, py, script, TAG),
        "*/15 * * * * %s %s %s check # %s" % (env, py, script, TAG),
    ]
    if dry:
        print("\n".join(lines) if lines else "(would remove the %s lines)" % TAG)
        return 0
    if not is_admin():
        print("NEEDS ROOT: the hosts file is root only. Claude: tell Srijan to type this himself in his terminal and enter his password:")
        print("  sudo python3 %s schedule" % script)
        return 2
    if not shutil.which("crontab"):
        print("FAIL: crontab not found. Install cron (sudo apt install cron) and rerun.")
        return 1
    cur = subprocess.run(["crontab", "-l"], capture_output=True, text=True).stdout
    keep = [l for l in cur.splitlines() if TAG not in l and l.strip()]
    subprocess.run(["crontab", "-"], input="\n".join(keep + lines) + "\n", text=True)
    marker = CONF_DIR / "bedtime_scheduled"
    if remove:
        if marker.exists():
            marker.unlink()
        print("removed the bedtime cron lines")
    else:
        CONF_DIR.mkdir(parents=True, exist_ok=True)
        marker.write_text("1", encoding="utf-8")
        print("registered root cron lines (verify: sudo crontab -l | grep %s)" % TAG)
    return 0


def main():
    cmds = {"on": cmd_on, "off": cmd_off, "status": cmd_status, "skip": cmd_skip,
            "check": cmd_check, "schedule": cmd_schedule}
    if len(sys.argv) < 2 or sys.argv[1] not in cmds:
        print(__doc__)
        return 1
    if platform() == "linux" and not os.environ.get("HOSTS_FILE"):
        try:
            if "microsoft" in Path("/proc/version").read_text().lower():
                print("WSL note: this edits the Linux hosts file only. Run it from Git Bash on Windows to block Chrome.")
        except Exception:
            pass
    return cmds[sys.argv[1]](sys.argv[2:]) or 0


if __name__ == "__main__":
    sys.exit(main())
