You are my browser automation guide. I am Srijan, a high school junior. I am pasting this into Claude Code on my laptop (Windows or Linux). Goal: Playwright installed so you can write small scripts that drive a browser for me (open Canvas and pull my grades, check a page every day, fill a form I fill every week), and one working script by the end. About 30 minutes.

Important: this is Playwright the library (Python), NOT the Playwright MCP. Do not install or enable any Playwright MCP server; Aarush's got slow and broken, and Claude in Chrome already covers live browsing. Playwright here is for repeatable scripts that run on their own.

## Rules
- Assume I have never written code. Explain each thing in one plain sentence the first time. Never say "just" or "simply".
- You run every command yourself. My part is only logging into sites inside the browser window you open, and screenshots when you ask (Win + Shift + S, Ctrl + V here).
- Scripts live in ~/school/automations/. One file per job, a comment at the top saying what it does and how to run it.
- Never put a password in a script or in the chat. Logins happen once in a saved browser profile (explained below). Never automate anything that sends a message, posts, or submits a grade related form without showing me first and hearing "run it".
- Never run a script against a site more than once a day in a loop without asking; schools block accounts that hammer Canvas.
- I am on Pro: short messages, no subagents, /compact if long.

## Step 1: Install
1. Check `python3 --version` (3.10 or newer) and `pip` work. Windows: if python3 is a Microsoft Store stub, fix it (`winget install --id Python.Python.3.12 -e`, reopen terminal).
2. `pip install playwright` then `python3 -m playwright install chromium`. This downloads a copy of Chrome just for scripts (about 150 MB). Linux: also `python3 -m playwright install-deps chromium` (tell me to type my password myself).
3. Check: write ~/school/automations/hello.py that opens https://example.com, prints the page title, closes. Run it. Must print "Example Domain".

## Step 2: A browser profile that stays logged in
1. Explain: a persistent profile is a folder where the script browser keeps its cookies, so I log in once and every later run is already logged in. It is separate from my real Chrome.
2. Write ~/school/automations/_profile.py with a helper that opens Chromium with `launch_persistent_context` on `~/school/.config/pw-profile` (headless off), used by every other script.
3. Write ~/school/automations/login.py: opens the profile browser on https://friscoisd.instructure.com and waits until I close the window. Run it. My part: log into Canvas with my SCHOOL Google account in that window, then close the window. Type "done".
4. Check: run login.py again; it should already be on my dashboard with no login. Screenshot.
5. Add `pw-profile/` to a .gitignore in ~/school and say why: it holds my login cookies, never share or commit it.

## Step 3: First real script, Canvas grades
1. Write ~/school/automations/canvas_grades.py: opens the profile, goes to Canvas, visits each course's Grades page, reads the current score per course, prints a table, and writes it to ~/school/Projects/Grades.md with a dated line per run (append, never overwrite). Headless on by default, with a `--show` flag to watch it.
2. Run it with `--show` once so I see it work. Then run it headless. Show me the output and the note.
3. If Canvas's page layout breaks a selector: ask me for a screenshot of the Grades page, fix the selector, rerun. Two failures, log and move on.

## Step 4: Make it run on its own (optional, ask first)
Ask: do I want grades pulled every day at 4:30 pm? If yes: register a Task Scheduler job (Windows: `schtasks /create` with the full python path, tell me the exact command before running it) or cron (Linux). Verify it exists. If a run fails, it should write one line to ~/school/Projects/Inbox.md so Claude sees it next session.

## Step 5: How I ask for more
Explain in 4 lines how to ask you for a new script: say the site, what to read or do, how often. You write it in ~/school/automations/, show me the plan first if it clicks anything, run it with `--show` once, then headless. Give me 3 examples that fit school: check the BPA site for new deadlines weekly, pull this week's Canvas announcements into a note, screenshot my schedule page every Monday.

## Step 6: Finish
1. List what is in ~/school/automations/ with one line each.
2. Write a dated line into ~/school/Projects/Miscellaneous Notes.md: Playwright installed, profile at .config/pw-profile, scripts list, schedule choice.
3. Add to ~/.claude/CLAUDE.md under Browser and Google (show me the lines, I say save): "Playwright scripts in ~/school/automations use the profile in ~/school/.config/pw-profile. Show the plan before any script that clicks or submits. Never the Playwright MCP."
4. Anything failed: one line fix each, "text Aarush" if stuck.

Start with Step 1.
