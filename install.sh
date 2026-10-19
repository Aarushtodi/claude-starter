#!/bin/bash
# One shot installer for Srijan's Claude Code setup.
# Works in Git Bash (Windows), WSL, or any Linux shell. Run from inside this folder:
#   bash install.sh
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
CL="$HOME/.claude"

echo "==> Installing into $CL"
mkdir -p "$CL/skills" "$CL/hooks" "$HOME/school/Notes/drills" "$HOME/school/Council" "$HOME/school/Writing"

# 1. CLAUDE.md (never overwrite a filled in one)
if [ -f "$CL/CLAUDE.md" ]; then
  cp "$HERE/CLAUDE.md" "$CL/CLAUDE.md.new"
  echo "    CLAUDE.md already exists, saved the new one as CLAUDE.md.new (merge by hand)"
else
  cp "$HERE/CLAUDE.md" "$CL/CLAUDE.md"
  echo "    CLAUDE.md installed. Fill in ABOUT ME."
fi

# 2. Skills
for s in "$HERE"/skills/*/; do
  n="$(basename "$s")"
  rm -rf "$CL/skills/$n"
  cp -R "$s" "$CL/skills/$n"
  echo "    skill: $n"
done

# 3. Hooks
cp "$HERE"/hooks/*.sh "$HERE"/hooks/*.py "$CL/hooks/"; mkdir -p "$CL/state"
chmod +x "$CL"/hooks/*.sh "$CL"/hooks/*.py 2>/dev/null || true
echo "    hooks: notes_index.sh, guard.py, context_size_check.py"

# 4. settings.json: merge hooks in, keep whatever is already there
python3 - "$CL/settings.json" "$HERE/settings.json" <<'EOF'
import json, sys, os
dst, src = sys.argv[1], sys.argv[2]
new = json.load(open(src))
cur = {}
if os.path.exists(dst):
    try:
        cur = json.load(open(dst))
    except Exception:
        cur = {}
hooks = cur.setdefault("hooks", {})
for event, entries in new["hooks"].items():
    have = json.dumps(hooks.get(event, []))
    for e in entries:
        if json.dumps(e) not in have:
            hooks.setdefault(event, []).append(e)
# bypass permissions as the default mode
cur.setdefault("permissions", {})["defaultMode"] = "bypassPermissions"
cur["skipDangerousModePermissionPrompt"] = True
json.dump(cur, open(dst, "w"), indent=2)
print("    settings.json merged (hooks + bypass permissions default)")
EOF

# 5. Starter notes
for n in BPA Inbox Week; do
  f="$HOME/school/Notes/$n.md"
  [ -f "$f" ] || printf '# %s\n\n## Current state\n(nothing yet)\n\n## Log\n' "$n" > "$f"
done
echo "    notes folder: ~/school/Notes (BPA.md, Inbox.md, Week.md)"

echo
echo "==> Done. Next:"
echo "    1. Edit ~/.claude/CLAUDE.md, fill in ABOUT ME."
echo "    2. cd ~/school && claude"
echo "    3. Type /plugin, pick Discover, install the Anthropic skills pack (docs, pdf, pptx, xlsx) and anything else that looks useful."
echo "    4. Paste the first message from SETUP.md section 6."
