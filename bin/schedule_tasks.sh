#!/bin/bash
# Linux: register the school automations in cron. Safe to re-run (replaces its own lines).
#   bash schedule_tasks.sh           install
#   bash schedule_tasks.sh --remove  take them out
# canvas_watch every 30 min, assess_watch Sundays 17:00, weak_notes daily 16:40.
BIN="$HOME/.claude/bin"
LOG="$HOME/.claude/state/cron.log"
TAG="# claude-starter"
command -v crontab >/dev/null 2>&1 || { echo "crontab not found. Install cron (sudo apt install cron) and re-run."; exit 1; }
PY="$(command -v python3 || command -v python)"
[ -n "$PY" ] || { echo "python3 not found"; exit 1; }
mkdir -p "$HOME/.claude/state"
CUR="$(crontab -l 2>/dev/null | grep -v "$TAG")"
if [ "$1" = "--remove" ]; then
  printf '%s\n' "$CUR" | crontab -
  echo "removed the claude-starter cron lines"
  exit 0
fi
NEW="$CUR
*/30 * * * * $PY $BIN/canvas_watch.py >> $LOG 2>&1 $TAG canvas_watch
0 17 * * 0 $PY $BIN/assess_watch.py >> $LOG 2>&1 $TAG assess_watch
40 16 * * * $PY $BIN/weak_notes.py >> $LOG 2>&1 $TAG weak_notes"
printf '%s\n' "$NEW" | sed '/^$/d' | crontab -
echo "registered 3 cron jobs:"
crontab -l | grep "$TAG"
