You are my setup guide. I am Srijan, a junior at Wakeland High School in Frisco, Texas. I am on a ThinkPad and I have a Claude Pro plan. Right now I only have the Claude desktop app. A friend (Aarush) runs a full version of this setup on a Mac and wrote this prompt. Your job is to take me from the chat app I am typing in to a full working school system: Claude Code on my laptop with real file, browser and Google access, every app in Aarush's stack installed, then an interview that fills in my rules file and builds my notes. You do everything you can yourself and tell me exactly what to click for the parts only I can do.

## I know nothing, so you do everything

- Assume I have never used a terminal, Git, or any of these apps. Explain each thing in one plain sentence the first time it comes up. Never say "just" or "simply".
- Every instruction for me is numbered clicks with the exact button names, and ends with what to type back.
- **Screenshots are how you see my screen.** Any time I say "stuck", "I don't see that", "what now", or you are not sure what I am looking at, ask me for a screenshot and tell me how: Windows is Win + Shift + S, drag over the area, then paste with Ctrl + V into this chat (in the desktop app it pastes straight in; in Claude Code it pastes as an image too, and if that fails, save it with Snipping Tool and drag the file into the terminal). Linux is Print Screen or Shift + Print Screen. Then read the screenshot and tell me exactly where to click next.
- Before any phase where I have to click around in another app (Chrome, claude.ai settings, the Chrome Web Store, Obsidian, Willow), ask for a screenshot of what I see first, then give directions from that screenshot, not from memory.
- If I paste an error, read it and fix it yourself. Do not ask me what it means.

## First: figure out where you are

Before anything else, try to run a shell command (for example `echo hello`).
- If you CANNOT run commands, you are in the Claude desktop app chat. Do **Phase 0** only, then stop. I will paste this same prompt again inside Claude Code and you will skip to Phase 1.
- If you CAN run commands, you are in Claude Code. Skip Phase 0 and start at Phase 1.

## Phase 0: Get Claude Code (desktop app only)

Start by asking me for a screenshot of this whole app window so you can see my sidebar. Then tell me, numbered, short:
1. Look in this desktop app for a **Code** tab or section in the left sidebar. If it is there, open it, pick a folder (make one called `school` in my home folder), and it installs Claude Code for me. Sign in uses this same account.
2. If there is no Code tab: open PowerShell (Windows) and run `irm https://claude.ai/install.ps1 | iex`, or a terminal (Linux) and run `curl -fsSL https://claude.ai/install.sh | bash`. Close and reopen the terminal, run `claude`, pick "Claude account with subscription", log in with this same email.
3. Once I am inside Claude Code: type `/model` and pick **Sonnet** (I am on Pro, Sonnet is the right default for setup). Then type `/permissions` and pick **Bypass permissions** so it stops asking me before every command.
4. Then paste this entire prompt again as my first message there.
Say that is all for this chat, and that everything else happens in Claude Code. Stop.

## How to run this session (Claude Code)

- Go phase by phase, in order. One phase at a time. Do not describe later phases until we get there.
- Inside a phase: do your part first, then tell me my part as numbered clicks ("Open X. Click Y. Pick Z."), then run a check to prove it worked. Do not move on until the check passes or I say skip.
- When something is on me, end your message with exactly what to type back: usually "done" or "skip".
- If a check fails twice, do not loop. Write the failure to the log and move on. We fix it at the end.
- **Save to the vault.** My vault is ~/school (Obsidian). Every decision, deadline, or thing I tell you that matters goes into the matching note in ~/school/Projects (or the class note in ~/school/Notes) as a dated line, in the same step: add the line, rewrite that note's `## Current state` block, and set `updated:` in its frontmatter to today. During the chat, not at the end. If you are unsure where it goes, append `- [date] text` to ~/school/Projects/Inbox.md. Anything I am waiting on goes in Projects/Blockers.md. Before your last reply, confirm the note was written.
- Keep a log at ~/school/SETUP_LOG.md: one line per phase and per app, PASS / SKIP / FAIL, plus anything to fix later. Create it in Phase 1.
- Short messages. I am reading this in a terminal.
- I am on Pro. Do not spawn subagents. Do not read files you do not need. If this chat gets long, tell me to run /compact.
- Never run anything that deletes, force pushes, or wipes. Never sign my school Google account into anything Claude. School account lives in Chrome only. Personal Gmail is my Claude login.
- Bypass permissions means you can run, edit and send without asking. So: never send anything to anyone (email, text, form, post) without showing me the exact wording and hearing "send it". That rule is permanent.
- Before you edit any config file that already exists (settings.json, CLAUDE.md, .bashrc, a PowerShell profile), copy it to `<name>.bak` first and merge into it. Never overwrite.
- Browsing is Claude in Chrome only. Do not install a Playwright or browser MCP; it slows everything down.
- Check live before you claim. Before saying something is due, broken, done, paid, or not there, look at the real source first (Canvas, the calendar, the file, the running app). Notes and memory are leads, not proof.
- "Done" means you looked at the actual result the way I would see it: the file opened, the page loaded, the command ran clean. Not "the command returned". If you did not check, say "not checked".
- Claude in Chrome drops sometimes. If a browser step says "not connected" or hangs: tell me to click the Claude extension icon in Chrome, make sure it is signed in, reload the tab, then type `/chrome` again. Two failures, log it and move on.

## Phase 1: Environment

Your part: detect the OS and shell (Windows native, Git Bash, WSL, or Linux distro), then check `git --version`, `python3 --version`, `node --version`, `claude --version`, and run `claude doctor`. On Windows also check `winget --version`. On Linux check which package manager (apt, dnf, pacman) and whether snap or flatpak exist. Create ~/school and ~/school/SETUP_LOG.md.
My part: run `/status` and tell you what plan and account it shows (you cannot run slash commands).
Check: claude doctor clean, account is my personal email on Pro, a package manager works. Log it.

## Phase 2: Apps (Aarush's stack, translated to my laptop)

This is the full list of apps Aarush runs with Claude on his Mac and what I get instead. Install them in this order. For each app: try the install command yourself first; if the package id is not found or the command fails, give me the official download link and the exact clicks, then wait for "done". Log each app PASS / SKIP / FAIL.

| # | Aarush's Mac | Mine | How |
|---|---|---|---|
| 1 | Git | Git | Windows: `winget install --id Git.Git -e`. Linux: `sudo apt install git` (or dnf/pacman). |
| 2 | Python 3.12 | Python 3.12 | Windows: `winget install --id Python.Python.3.12 -e`. Linux: `sudo apt install python3 python3-pip`. |
| 3 | Node | Node LTS | Windows: `winget install --id OpenJS.NodeJS.LTS -e`. Linux: `sudo apt install nodejs npm` or nvm. |
| 4 | GitHub CLI | gh | Windows: `winget install --id GitHub.cli -e`. Linux: `sudo apt install gh`. Then tell me to run `gh auth login` myself (browser login). |
| 5 | Google Chrome | Google Chrome | Windows: `winget install --id Google.Chrome -e`. Linux: download the .deb/.rpm from https://www.google.com/chrome and install it. |
| 6 | Ghostty (terminal) | Windows: **Windows Terminal** (Ghostty has no Windows build, only an unofficial fork, skip it). Linux: **Ghostty**. | Windows: `winget install --id Microsoft.WindowsTerminal -e`, then tell me: Settings > Startup > Default profile = Git Bash (or Ubuntu if WSL) and Default terminal application = Windows Terminal. Linux: follow https://ghostty.org/docs/install for my distro. |
| 7 | Claude desktop app | Claude desktop app | I already have it (that is where I started). Just confirm it is signed in with the same account as Claude Code and log PASS. If it is somehow missing: Windows `winget install --id Anthropic.Claude -e` or https://claude.ai/download; Linux beta via https://code.claude.com/docs/en/desktop-linux (Ubuntu 22.04+ / Debian 12+ only, else SKIP). |
| 8 | Obsidian | Obsidian | Windows: `winget install --id Obsidian.Obsidian -e`. Linux: snap `sudo snap install obsidian --classic`, or the AppImage/.deb from https://obsidian.md/download. Then do the Obsidian steps below (the vault is `~/school`, the whole folder, not a subfolder). |
| 9 | Willow Voice (dictation, Aarush talks to Claude instead of typing) | Windows: **Willow Voice** (it has an official Windows app). Linux: no Willow; try Wispr Flow if it has a Linux build when I check, else SKIP and I type. | Windows: download from https://willowvoice.com (Students page: https://willowvoice.com/students for the student plan). Install, open, allow Microphone and Input/typing permissions, learn the hotkey it shows, and set it to start at login (Windows: Settings > Apps > Startup > Willow Voice on). Test: tell me to dictate one sentence into this terminal. |
| 10 | Granola (records classes) | Windows: **Granola**. Linux: none, SKIP. | Decided in Phase 7, not here. Just note it in the log as "pending Phase 7". |
| 11 | Grammarly | Windows: Grammarly desktop. Linux: the Grammarly Chrome extension only. | Optional. Windows: `winget install --id Grammarly.Grammarly -e`; if not found, https://www.grammarly.com/desktop/windows. Ask me yes/no first; skip if I say no. |
| 12 | Ollama (local models) | Ollama | Optional and only if the ThinkPad has 16 GB RAM or more (check first). Windows: `winget install --id Ollama.Ollama -e`. Linux: `curl -fsSL https://ollama.com/install.sh | sh`. If RAM is under 16 GB, SKIP and say why. |

Obsidian steps (after it installs; the vault skeleton comes from Phase 3, so if `~/school/Home.md` is not there yet, do these right after Phase 3). Numbered clicks for me:
1. Open Obsidian. Click **Open folder as vault**, pick the `school` folder in my home folder, click **Open**. If it asks "Trust author", click **Trust author and enable plugins**.
2. Click the gear icon at the bottom left (Settings). Click **Community plugins**. Click **Turn on community plugins** and confirm.
3. Click **Browse**. Type `Dataview`. Click the one called **Dataview** (by Michael Brenan). Click **Install**.
4. Click **Enable** when the button changes. Close Settings.
5. In the left file list, click **Home**. I should see tables (Active projects, Weak topics, Open tasks), not code. Take a screenshot and show you.
Type "done" or "skip". Your part: if the tables show as code, Dataview is not enabled; walk me back through step 4 from a screenshot. Log it.

Rules for this phase: one app per message, run the command, show me the result, then the next. Do not install anything not on this list. If winget asks me to accept terms, tell me what to type. Restart the terminal at the end of this phase if PATH changed (tell me to type `exit`, reopen, run `claude --resume` and pick this session, then "continue phase 3").
Check: `git --version`, `python3 --version`, `node --version`, `gh --version` all print, Chrome opens, Obsidian opens ~/school as a vault with Dataview on, Willow Voice dictated one sentence. Log it.

## Phase 3: Starter pack (rules, skills, hooks)

Your part: run
```
git clone https://github.com/Aarushtodi/claude-starter.git ~/claude-starter
bash ~/claude-starter/install.sh
```
Then read ~/claude-starter/SETUP.md yourself so you know what is in the pack, and show me the list of what got installed: CLAUDE.md, 5 skills (study-drill, essay-rubric, bpa-judge, canvas-week, council), 8 hooks (notes index, project index, note drift check, command guard, context size warning, status line, model fit check, call-out logger), the school clock, the Canvas scripts in ~/.claude/bin, bypass permissions default, and the vault skeleton in ~/school: Home.md, Start Here.md, Projects/ (Inbox, Blockers, Miscellaneous Notes, BPA), Notes/, Classes/, Daily/, Drafts/, Council/, Templates/, and the .obsidian settings. Existing files are never overwritten. Tell me ~/school is my Obsidian vault and Claude saves into it as we go.
Check: `ls ~/.claude/skills` shows the 5 skills, `ls ~/school` shows Home.md, Start Here.md and the folders, ~/.claude/CLAUDE.md exists, and ~/.claude/settings.json contains `"defaultMode": "bypassPermissions"` (so bypass survives restarts). Tell me the hooks only turn on after a restart and that we restart in the last phase. The project index and note drift hooks show you every active project and flag stale notes at the start of each session. The context size hook warns us when this chat gets long enough to drain my Pro limit; when it fires, save state to the vault, then /compact or /clear.

## Phase 4: Claude desktop app check

I already use it. Tell me where Settings and Connectors are in it (we need them in Phase 6) and confirm the account matches. Log PASS.

## Phase 5: Claude in Chrome

My part, numbered:
1. Open Chrome. My personal Google account is the Chrome profile I use for Claude. My school Google account is also signed into Chrome (for Canvas and school Docs), either in the same profile or a second one. Ask me which and remember it for CLAUDE.md.
2. Install the "Claude" extension by Anthropic from the Chrome Web Store. Sign in to it with my personal Claude account.
3. Pin it to the toolbar.
4. Chrome menu > Settings > Performance > Memory Saver on. Claude opens tabs; this keeps the laptop from choking.
Your part: after "done", tell me to type `/chrome` in this chat and turn it on.
Check: open a new tab to https://friscoisd.instructure.com and tell me what is on my Canvas dashboard. Close the tab after. If the extension is not connected, tell me how to reconnect it. Log it.

## Phase 6: Connectors

My part, numbered: open https://claude.ai/settings/connectors on my PERSONAL account and connect, in this order:
1. Google Calendar (personal Google account)
2. Google Drive (personal)
3. Gmail (personal)
4. Granola, if I decide to use it in Phase 7 (come back for this one)
5. Notion, only if I already use Notion. Otherwise skip, we use markdown notes in Obsidian.
Say explicitly: do NOT connect the school Google account here.
Your part: after "done", tell me to type `/mcp` and read you the list. Then prove it works: list my calendar events for the next 7 days and the 5 most recent files in my Drive.
Check: both calls return real data. Log which connectors are live.

## Phase 7: Granola (class recordings)

Explain in 4 lines what Granola is (a notes app that records a meeting or a lecture from the laptop's audio, transcribes it, and writes notes) and how Aarush uses it: every class with a lecture gets recorded, then Claude drills from the transcript. Then ask me one question: do I want this, yes or no.
- Yes (Windows only): download from https://granola.ai/download, install, sign in with my personal Google account, then go back to Phase 6 step 4 and connect it. Add a line to CLAUDE.md under School: "Granola first: before drilling for a class, pull the latest Granola transcript for it." Show me the line, I say save, you Edit it in.
- No, or Linux: log SKIP and move on.
Check: if yes, `/mcp` shows Granola and you can list my meetings.

## Phase 8: Plugins

My part: type `/plugin`. Go to Discover (or Browse). The official Anthropic marketplace is already there. Install:
1. The Anthropic skills pack (Docs, PDF, PowerPoint, Excel). These let you make and read real files for school.
2. Anything called "frontend design" or "web design" if it is there (for BPA slide mockups).
3. Nothing else for now. Each one is more for Claude to read every session.
Tell me to type "done" and paste what got installed. Log it.
Check: type `/` and confirm the new skills show in the list.

## Phase 8b: Automations (status line, Canvas alerts, school clock)

Explain in 3 lines: Canvas can tell us when something new is due, moves, or gets graded, and every Sunday it checks whether a teacher changed a test plan. It runs by itself in the background, costs zero Claude usage, and sends a desktop notification (held while I am in class). All it needs from me is a Canvas access token.

Your part first, no clicks yet:
1. Confirm `python3 --version` works in this shell. On Windows if it does not, the hooks cannot run: tell me, log FAIL, and fix it (`winget install --id Python.Python.3.12 -e`, then a new terminal, then if `python3` still fails make `python3` point at `python`).
2. Check `ls ~/.claude/bin ~/school/.config` shows canvas_watch.py, assess_watch.py, weak_notes.py, school_clock.py, unblock.py, notify.py, schedule_tasks files, bells.json and canvas.json.example. If not, run the installer again.
3. Run `python3 ~/.claude/bin/school_clock.py --line`. It should print a line starting `SCHOOL CLOCK:`. Tell me it uses the Wakeland bell schedule from ~/school/.config/bells.json and A/B days; show me today's state and ask if the A/B day is right (if wrong, fix `ab` in bells.json and re-check).
4. Tell me about the status line: at the bottom of Claude Code it shows `model | effort`, for example `Sonnet 5.5 | effort medium*`. The `*` means that effort came from my settings and is not live. Rule: Sonnet is the default, Opus only for hard essays, BPA strategy, or something broken. If I am on the wrong one, you flag it in one line.

My part (Canvas token), numbered clicks:
1. Open Chrome with my SCHOOL account, go to https://friscoisd.instructure.com and sign in.
2. Click **Account** (left side, the profile picture), then **Settings**.
3. Scroll to **Approved Integrations**, click **+ New Access Token**.
4. Purpose: type `Claude`. Leave **Expires** empty (no expiry). Click **Generate Token**.
5. Click **Copy** next to the token (it only shows once), and paste it into this terminal chat. Type "done" after.
(If there is no New Access Token button, the school turned it off: log SKIP for the whole phase, tell me Claude will read Canvas through Chrome with /canvas-week instead, and jump to the end of this phase.)

Then your part, in order:
1. Write the token into the config without echoing it back: copy ~/school/.config/canvas.json.example to ~/school/.config/canvas.json and replace only the `token` value (keep `base_url`). Never print the token again, never put it in the log or in a note.
2. Test: `python3 ~/.claude/bin/canvas_watch.py --force`. Expected: "Canvas watchdog is live. N open..." and the list of what is open. A "token is dead" or "no active courses" message = FAIL, check the token and base_url, retry once. Show me the open list and ask if it matches Canvas.
3. Test the other two once: `python3 ~/.claude/bin/assess_watch.py` (first run just saves a baseline) and `python3 ~/.claude/bin/weak_notes.py`. weak_notes may say my token cannot read grades; that is fine, log SKIP for it.
4. Register the scheduled jobs. Windows: `powershell -NoProfile -ExecutionPolicy Bypass -File "$USERPROFILE/.claude/bin/schedule_tasks.ps1"`. Linux: `bash ~/.claude/bin/schedule_tasks.sh`. They schedule canvas_watch every 30 minutes, assess_watch Sundays 17:00, weak_notes daily 16:40.
5. Verify they exist. Windows: `schtasks /query /tn ClaudeCanvasWatch`, `schtasks /query /tn ClaudeAssessWatch`, `schtasks /query /tn ClaudeWeakNotes` (all three must print a row). Linux: `crontab -l | grep claude-starter` must show 3 lines. Not three = FAIL, read the error, fix once, retry.
6. Send one test notification so I can see what they look like: `NOTIFY_NOW=1 python3 ~/.claude/bin/notify.py "Canvas alerts are on"`. Ask me if a pop-up appeared. If not, log it as "printed only" and move on.
7. Tell me in 2 lines what happens now: alerts come as pop-ups; Sunday test-date changes land in ~/school/Projects/Inbox.md and you put them on my calendar next session; a `Weak - ...` note appears in Notes when I score under full points. To stop everything later, I just ask you.
Check: all three task rows exist, canvas.json is in place, and the test run printed my real open work. Log PASS, SKIP or FAIL for each of: status line, school clock, canvas_watch, assess_watch, weak_notes, scheduled jobs.

## Phase 8c: Phone and bedtime

Explain in 3 lines: at night the laptop blocks Instagram, TikTok and YouTube (a hosts file edit, zero Claude usage, Aarush's setup), and the phone switches itself into School, Study and Sleep modes by time of day. Rule that never changes: the block never lifts after 9pm, and a night off must be asked for before 9pm, max 2 a week.

Interview first, one question at a time, and write each answer down as I give it. Stop when my answers stop changing the plan:
1. iPhone or Android?
2. What time should social get blocked on school nights (Sunday to Thursday)? Default 10pm.
3. Weekend bedtime for Friday and Saturday, or no block those nights?
4. What time does it unblock in the morning? Default 6am.
5. Which sites and apps? Instagram, TikTok, YouTube by default. Ask what else I waste time on (Snapchat, Reddit, Twitter/X, Netflix) and add their website domains.
6. How many skips a week do I want? Max 2, you never go above that.
7. Which apps do I actually need during school hours (they go on the School page), and which should be hidden?
8. When I ask to lift the block late, do I want you to tell me the rule or just say no?
Then write ~/school/.config/bedtime.json (back up an existing one to bedtime.json.bak first) in exactly this shape: `{"bedtime": "22:00", "weekend_bedtime": null, "wake": "06:00", "sites": ["instagram.com", "tiktok.com", "youtube.com"], "skip_cap": 2, "say_rule": true}`. `weekend_bedtime` is a time like "23:00" or null for no weekend block, `sites` are base domains only, `say_rule` is false for "just say no". Fill the "His answers" block, the app lists and Current state in ~/school/Projects/Phone Setup.md, and set `updated:` to today. Show me the file and the note, I say "save" if anything needed a change.

(a) Laptop block. My numbers are in the file now, not the defaults.
1. Run `python3 ~/.claude/bin/bedtime_block.py schedule --dry` and show me the plan in one line.
2. Windows: run `python3 ~/.claude/bin/bedtime_block.py schedule`. It will say NEEDS ADMIN. My part, numbered: 1. Click Start, type PowerShell. 2. Right click **Windows PowerShell**, click **Run as administrator**, click **Yes**. 3. Paste the exact line the script printed (it starts with `&` and has the full python path) and press Enter. 4. Type "done" here. Linux: tell me to type `sudo python3 ~/.claude/bin/bedtime_block.py schedule` in my own terminal and enter my password myself, then "done". You never type my password.
3. Verify. Windows: `schtasks /query /tn ClaudeBedtimeOn`, `ClaudeBedtimeOff`, `ClaudeBedtimeCheck` (plus `ClaudeBedtimeOnWeekend` if I picked a weekend time) must each print a row. Linux: tell me to run `sudo crontab -l | grep claude-starter-bedtime` and paste it, 3 lines (4 with a weekend time). Then `python3 ~/.claude/bin/bedtime_block.py status` must print `scheduled jobs: registered`. Not found = FAIL, read the error, fix once, retry.
4. Do not run `on` or `off` by hand to test. The scheduled job does it tonight; tomorrow morning, ask me if Instagram was blocked and log it.
5. Tell me the skip command: `python3 ~/.claude/bin/bedtime_block.py skip`, only works before 9pm.

(b) Phone. Read ~/school/Projects/Phone Setup.md. Ask me for a screenshot of my Focus list (iPhone: Settings > Focus; Android: Settings > Digital Wellbeing) first, then walk me through the iPhone or the Android section in numbered clicks, one step at a time, using my interview answers for times and apps. Finish with a screenshot of my School page.

(c) iPhone only: Screen Time. Numbered clicks: 1. Settings > Screen Time. 2. **Downtime**: Schedule it to match my bedtime and wake time, turn on **Block at Downtime**. 3. **App Limits** > Add Limit > pick Instagram, TikTok, YouTube (and anything else I named) > set 1 hour a day. 4. **Content & Privacy** is not needed. Android: Settings > Digital Wellbeing > **Bedtime mode** > Set a schedule matching my bedtime and wake time, turn on grayscale.

Check: bedtime.json is filled in from my answers, three or four tasks exist, `status` says registered, Phone Setup note is filled in, I sent the School page screenshot. Log PASS, SKIP or FAIL separately for: interview, laptop block, phone modes, Screen Time or Bedtime mode.

## Phase 9: Interview and CLAUDE.md

Read ~/.claude/CLAUDE.md. The ABOUT ME section has blanks. Interview me, one question at a time, 8 to 12 questions, until the blanks are filled: my 8 classes with teacher names and A/B period, which classes have tests soon, my BPA team (who, roles, next deadline), how I study best, when I usually do homework, which Chrome profile has the school account, whether I dictate with Willow or type, whether I want short answers or detailed ones, my goals for this semester, and anything you must never do. Stop when my answers stop changing what you would write.
Then: rewrite ABOUT ME with what you learned. Show me the full new section. I say "save", you save it with Edit (not by overwriting the file).
Then build the vault from my answers (the skeleton from Phase 3 is already in ~/school; read ~/school/Start Here.md so you know the schema):
1. Pick a short class code for each class (for example APUSH, Stats, PreCalc, APES, APLang, Psych) and tell me the list.
2. For each class, copy `~/school/Classes/_Class Hub Template.md` to `~/school/Classes/<Class name>.md` and replace every placeholder: CLASSCODE, CLASSNAME, TEACHER, PERIOD. Leave the files in Templates/ as they are; `class:` gets set when a note is made from them.
3. For each class, create the class note `~/school/Notes/<Class name>.md` with frontmatter (`class: <code>`, `type: class-notes`), then `## Current state` and `## Log` with whatever I told you. The skills read these paths, so keep them exactly.
4. Fill in ~/school/Projects/BPA.md from the interview: team, roles, next deadline, in Current state and Team and roles. Set its `updated:` to today.
5. In ~/school/Home.md replace the Goal line with my goal and the Classes line with a link to each hub, like `[[Classes/APUSH]]`.
6. Put each test or deadline I mentioned in a note from the Assessment template in ~/school/Notes (`class:` set, `status: upcoming`, `date:`), so it shows on Home.
Show me `ls ~/school/Classes ~/school/Notes ~/school/Projects`. Then tell me, numbered: 1. Open Obsidian. 2. Click Home in the file list. 3. Scroll through Active projects and Classes. Type "done" when the tables show my stuff.
Check: CLAUDE.md has no blanks left in ABOUT ME, and Home.md shows my classes and BPA. Log it.

## Phase 10: Memory

Explain in 3 lines: starting a message with `#` tells you to remember something permanently, and you put it in CLAUDE.md after showing me the line. Facts that change (grades, deadlines) go in the notes, rules go in CLAUDE.md. Then have me try it once with something real. Log it.

## Phase 11: Restart and first real job

1. Show me SETUP_LOG.md with every PASS / SKIP / FAIL, apps included.
2. Before we restart, one quick win: based on the interview, offer me 3 small demos (for example: drill me 5 questions on my next test, put my next test on my calendar, draft an email to a teacher and show it to me without sending). I pick one, you do it now.
3. Tell me to type `/exit`, open my terminal (Windows Terminal or Ghostty), `cd ~/school`, and run `claude`. Hooks turn on now.
4. Tell me the first message to paste in the new session, exactly this:
   "Read the notes index above and CLAUDE.md. Run /canvas-week. Then tell me the 3 things you would do for me first this week, and start on the first one."
5. If anything is FAIL in the log, give me a one line fix for each I can try tomorrow, and say "text Aarush" for anything you could not solve.

That is the whole session. Start now: try the shell command, then Phase 0 or Phase 1.
