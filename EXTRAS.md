# EXTRAS: only if you already pasted an older BOOTSTRAP and are mid-session. Paste this as one message.

Additions to the setup rules, apply from now on and go back for anything already passed:

1. Permanent rule: bypass permissions means you can run, edit and send without asking, so never send anything to anyone (email, text, form, post) without showing me the exact wording and hearing "send it".
2. Before editing any config file that already exists (settings.json, CLAUDE.md, .bashrc, PowerShell profile), copy it to <name>.bak first and merge into it. Never overwrite.
3. Browsing is Claude in Chrome only. Do not install a Playwright or browser MCP.
4. Phase 2, Willow Voice: also set it to start at login (Windows: Settings > Apps > Startup > Willow Voice on).
5. Phase 3 check: confirm ~/.claude/settings.json contains "defaultMode": "bypassPermissions". If the starter pack was installed before tonight, run `cd ~/claude-starter && git pull && bash install.sh` again to get the third hook (context size warning). When that hook fires, save state to the notes, then /compact or /clear.
6. Phase 5: Chrome menu > Settings > Performance > Memory Saver on.
7. Phase 9 interview: also ask whether I want short or detailed answers, and my goals for this semester.
8. Phase 11: before the restart, offer me 3 small demos based on the interview (drill 5 questions on my next test, put my next test on my calendar, draft a teacher email and show it without sending). I pick one, you do it.
9. Check live before you claim. Before saying something is due, broken, done, paid, or not there, look at the real source first (Canvas, calendar, file, running app). Notes and memory are leads, not proof.
10. "Done" means you looked at the actual result the way I would see it, not that a command returned. If you did not check, say "not checked".
11. If Claude in Chrome says "not connected" or hangs: tell me to click the Claude extension icon, confirm it is signed in, reload the tab, then type /chrome again. Two failures, log it and move on.
12. Vault upgrade. Run `cd ~/claude-starter && git pull && bash install.sh`. It adds the Obsidian vault skeleton to ~/school (Home, Start Here, Projects, Notes, Classes, Daily, Drafts, Council, Templates) without overwriting anything, plus two more hooks (project index, note drift). They turn on after a restart.
13. Redo the Obsidian step with the vault at ~/school (the whole folder, not ~/school/Notes). Numbered clicks for me: 1. Open Obsidian, click **Open folder as vault**, pick `school`, click Open (trust the author if asked). 2. Gear icon, **Community plugins**, **Turn on community plugins**. 3. **Browse**, type `Dataview`, click Dataview, **Install**, then **Enable**. 4. Open **Home** in the file list and confirm I see tables, not code. I type "done".
14. Save to the vault, from now on: every decision, deadline, or thing I say that matters goes in the matching ~/school/Projects note (class notes stay in ~/school/Notes) as a dated line, with its `## Current state` block rewritten and `updated:` set to today, in the same step. Unsure where = append `- [date] text` to ~/school/Projects/Inbox.md. Anything I am waiting on goes in Projects/Blockers.md. Move any old ~/school/Notes/BPA.md and Notes/Inbox.md content into Projects/BPA.md and Projects/Inbox.md (copy first, keep the old files).
15. If Phase 9 is not done yet, do it with the new steps: after the interview make a Classes/<Class>.md hub from `Classes/_Class Hub Template.md` per class (fill CLASSCODE, CLASSNAME, TEACHER, PERIOD), a class note Notes/<Class>.md with `type: class-notes`, fill Projects/BPA.md, and fill the Goal and Classes lines in Home.md.

16. New automations. Run `cd ~/claude-starter && git pull && bash install.sh` again. It adds a status line (bottom of the terminal, shows the model and effort), model and effort defaults for Pro, a model fit check, a call-out logger (Projects/Claude Misses.md), a school clock (tells you if I am in class), a blockers script, and three Canvas scripts in ~/.claude/bin. It never overwrites my files. They turn on after a restart.
17. Merge the new rules from the fresh ~/.claude/CLAUDE.md.new (or the repo CLAUDE.md) into my CLAUDE.md: the call-out rule, the model rule, BLOCKED-BY, school clock, Canvas automations. Show me each new line, I say "save", you Edit them in. Back up CLAUDE.md to CLAUDE.md.bak first.
18. Do Phase 8b: Automations from the latest BOOTSTRAP.md (read ~/claude-starter/BOOTSTRAP.md for it). It gets my Canvas token, tests the Canvas scripts once, and registers the scheduled jobs. Log PASS, SKIP or FAIL.
19. Check that the status line shows at the bottom after the restart, and explain the model line to me in 2 lines.

Tell me which phase we are in and continue.
