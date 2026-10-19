#!/bin/bash
# One shot installer for Srijan's Claude Code setup.
# Works in Git Bash (Windows), WSL, or any Linux shell. Run from inside this folder:
#   bash install.sh
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
CL="$HOME/.claude"

echo "==> Installing into $CL"
mkdir -p "$CL/skills" "$CL/hooks" "$CL/bin" "$CL/state" "$HOME/school/Notes/drills" "$HOME/school/Writing" "$HOME/school/.config"

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
echo "    hooks: notes_index.sh, project_index.sh, note_drift.py, guard.py, context_size_check.py, statusline.py, model_effort_check.py, callout_detect.py"

# 3b. Scripts (school clock, Canvas watchers, weak notes, unblock, notifier, task scheduler setup)
cp "$HERE"/bin/* "$CL/bin/"
chmod +x "$CL"/bin/*.py "$CL"/bin/*.sh 2>/dev/null || true
echo "    bin: school_clock, canvas_watch, assess_watch, weak_notes, unblock, notify, schedule_tasks"

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
# status line, model effort defaults, skill list: add only what is missing, never replace his choices
cur.setdefault("statusLine", new["statusLine"])
for k in ("modelSettings", "skillOverrides"):
    if k not in new:
        continue
    d = cur.setdefault(k, {})
    for name, val in new[k].items():
        d.setdefault(name, val)
# bypass permissions as the default mode
cur.setdefault("permissions", {})["defaultMode"] = "bypassPermissions"
cur["skipDangerousModePermissionPrompt"] = True
json.dump(cur, open(dst, "w"), indent=2)
print("    settings.json merged (hooks, status line, model settings, skill list, bypass permissions default)")
EOF

# 5. Vault skeleton: copy vault/ into ~/school, never overwrite an existing file
added=0; kept=0
cd "$HERE/vault"
while IFS= read -r p; do
  mkdir -p "$HOME/school/$(dirname "$p")"
  if [ -e "$HOME/school/$p" ]; then
    kept=$((kept+1))
  else
    # stamp new notes with today's date so the staleness check starts clean
    sed "s/^updated: 2026-01-01/updated: $(date +%Y-%m-%d)/" "$p" > "$HOME/school/$p"; added=$((added+1))
  fi
done < <(find . -type f | sed 's|^\./||')
cd "$HERE"
mkdir -p "$HOME/school"/{Projects,Notes,Classes,Daily,Drafts,Council,Templates}
[ -f "$HOME/school/Notes/Week.md" ] || printf '# Week\n\n## Current state\n(nothing yet)\n\n## Log\n' > "$HOME/school/Notes/Week.md"
echo "    vault: ~/school is the Obsidian vault ($added files added, $kept already there and left alone)"
# 5b. Config files: real bells.json by default, canvas.json.example for the token. Never overwritten (the loop above skips existing files).
[ -f "$HOME/school/.config/bells.json" ] && echo "    config: ~/school/.config/bells.json (Wakeland bell schedule + A/B days), canvas.json.example, README.md"
echo "    folders: Projects, Notes, Classes, Daily, Drafts, Council, Templates, .obsidian"

echo
echo "==> Done. Next:"
echo "    1. Edit ~/.claude/CLAUDE.md, fill in ABOUT ME."
echo "    2. cd ~/school && claude"
echo "    3. Open Obsidian > Open folder as vault > ~/school, then install Dataview (see ~/school/Start Here.md)."
echo "    4. Type /plugin, pick Discover, install the Anthropic skills pack (docs, pdf, pptx, xlsx) and anything else that looks useful."
echo "    5. Paste the first message from SETUP.md section 6."
echo "    6. Canvas alerts: Claude sets them up for you in BOOTSTRAP Phase 8b (needs your Canvas token)."
