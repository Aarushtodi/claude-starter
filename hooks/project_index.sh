#!/bin/bash
# SessionStart hook: one line per active project note in ~/school/Projects
# (name, status, banner), so Claude knows what is going on without being told.
DIR="$HOME/school/Projects"
[ -d "$DIR" ] || exit 0

body=""
for f in "$DIR"/*.md; do
  [ -e "$f" ] || continue
  name=$(basename "$f" .md)
  # Inbox, Blockers and Miscellaneous Notes are not projects
  case "$name" in Inbox|Blockers|"Miscellaneous Notes") continue ;; esac
  status=$(tr -d '\r' < "$f" | awk '/^---$/{n++; next} n==1 && /^status:[[:space:]]*/{sub(/^status:[[:space:]]*/,""); print; exit}')
  [ -z "$status" ] && status="?"
  case "$status" in done|archived) continue ;; esac
  banner=$(tr -d '\r' < "$f" | awk '/^>[[:space:]]/{sub(/^>[[:space:]]*/,""); gsub(/\*\*/,""); print; exit}')
  if [ -z "$banner" ]; then
    banner=$(tr -d '\r' < "$f" | awk 'BEGIN{fm=0} /^---$/{fm++; next} fm==1{next} /^[[:space:]]*$/{next} /^#/{next} {sub(/^[-*[:space:]]+/,""); gsub(/\*\*/,""); print; exit}')
  fi
  banner=$(printf '%s' "$banner" | cut -c1-120)
  body="${body}- ${name} [${status}] :: ${banner}"$'\n'
done

[ -z "$body" ] && exit 0

ctx="ACTIVE PROJECTS - full state lives in these notes in ~/school/Projects.
Read the relevant note (~/school/Projects/<name>.md) before doing any work on that project; its top ~50 lines carry current state, next actions, and blockers.

STANDING RULE: save as you go. When something worth keeping happens (a decision, deadline, finding, number, plan, or thing Srijan said), write it into the matching Projects note as a dated line, rewrite its Current state block, and set updated: to today, all in the same step. If no project fits, add a dated line to Projects/Inbox.md. Do it during the chat, not only at the end.

${body}"

PY=$(command -v python3 || command -v python) || exit 0
printf '%s' "$ctx" | "$PY" -c 'import json,sys; print(json.dumps({"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":sys.stdin.read()}}))'
