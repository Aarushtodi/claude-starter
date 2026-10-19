#!/bin/bash
# SessionStart hook: prints the Current state block of every note in ~/school/Notes
# so Claude knows where each class and project stands without being told.
DIR="$HOME/school/Notes"
[ -d "$DIR" ] || exit 0

body=""
for f in "$DIR"/*.md; do
  [ -e "$f" ] || continue
  name=$(basename "$f" .md)
  # Current state block = lines between "## Current state" and the next "## " heading
  state=$(awk '/^## Current state/{on=1; next} on && /^## /{exit} on && NF{print}' "$f" | head -8)
  [ -z "$state" ] && state="(no Current state block yet)"
  body="${body}### ${name}"$'\n'"${state}"$'\n\n'
done

[ -z "$body" ] && exit 0

cat <<EOF
NOTES INDEX (from ~/school/Notes, read the full note before working on that class or project):

${body}
STANDING RULE: when something worth keeping happens in this chat (a decision, a deadline, a grade, a plan, a thing Srijan said), write it into the matching note as a dated line and update its "## Current state" block in the same step. If no note fits, append a dated line to ~/school/Notes/Inbox.md. Do it during the chat, not at the end.
EOF
