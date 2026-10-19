#!/bin/bash
# SessionStart hook: prints the Current state block of every note in ~/school/Notes
# so Claude knows where each class and project stands without being told.
DIR="$HOME/school/Notes"
[ -d "$DIR" ] || exit 0

body=""
for f in "$DIR"/*.md; do
  [ -e "$f" ] || continue
  name=$(basename "$f" .md)
  # single idea notes (type: concept) and the README are not class notes, skip them
  [ "$name" = "README" ] && continue
  tr -d '\r' < "$f" | awk '/^---$/{n++; next} n==1 && /^type:[[:space:]]*(concept|assessment)/{f=1} END{exit !f}' && continue
  # Current state block = lines between "## Current state" and the next "## " heading
  state=$(awk '/^## Current state/{on=1; next} on && /^## /{exit} on && NF{print}' "$f" | head -8)
  [ -z "$state" ] && state="(no Current state block yet)"
  body="${body}### ${name}"$'\n'"${state}"$'\n\n'
done

[ -z "$body" ] && exit 0

cat <<EOF
NOTES INDEX (class notes in ~/school/Notes; project state is in ~/school/Projects. Read the full note before working on that class or project):

${body}
STANDING RULE: when something worth keeping happens in this chat (a decision, a deadline, a grade, a plan, a thing Srijan said), write it into the matching note (class note in Notes/, anything else in Projects/) as a dated line, rewrite its "## Current state" block and set updated: to today, all in the same step. If no note fits, append "- [date] text" to ~/school/Projects/Inbox.md. Do it during the chat, not at the end.
EOF
