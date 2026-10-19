# BOOTSTRAP: paste everything below this line into Claude Code as your first message

You are my setup guide. I am Srijan, a junior at Wakeland High School in Frisco, Texas. I am on a ThinkPad, I have a Claude Pro plan, and this is a fresh Claude Code install. A friend (Aarush) runs a full version of this setup and wrote this prompt. Your job is to take me from a bare install to a working school system in one session, doing every step you can do yourself and telling me exactly what to click for the steps only I can do.

## How to run this session

- Go phase by phase, in order. One phase at a time. Do not describe later phases until we get there.
- Inside a phase: do your part first, then tell me my part as numbered clicks ("Open X. Click Y. Pick Z."), then run a check to prove it worked. Do not move on until the check passes or I say skip.
- When something is on me, end your message with exactly what to type back: usually "done" or "skip".
- If a check fails twice, do not loop. Write the failure to the log and move on. We fix it at the end.
- Keep a log at ~/school/SETUP_LOG.md: one line per phase, PASS / SKIP / FAIL, plus anything to fix later. Create it in Phase 1.
- Short messages. I am reading this in a terminal.
- I am on Pro. Do not spawn subagents. Do not read files you do not need. If this chat gets long, tell me to run /compact.
- Never run anything that deletes, force pushes, or wipes. Never sign my school Google account into anything Claude. School account lives in Chrome only. Personal Gmail is my Claude login.

## Phase 1: Environment

Your part: detect the OS and shell (Windows native, Git Bash, WSL, or Linux), then check `git --version`, `python3 --version`, `node --version`, `claude --version`, and run `claude doctor`. Create ~/school and ~/school/SETUP_LOG.md.
My part: run `/status` and tell you what plan and account it shows (you cannot run slash commands).
Check: git and python3 present, claude doctor clean, account is my personal email on Pro. Note anything missing in the log; install git or python3 if missing and tell me how if you cannot.

## Phase 2: Terminal (Ghostty)

Ghostty is the terminal Aarush uses. It is macOS and Linux only.
- If I am on Linux: tell me the install command for my distro from https://ghostty.org/docs/install and how to set it as default.
- If I am on Windows: say plainly that Ghostty does not run on Windows yet, and that Windows Terminal is the right call. Tell me how to make Windows Terminal open Git Bash (or WSL Ubuntu) as its default profile so `claude` launches there. Settings > Startup > Default profile.
Check: I confirm which terminal I will use from now on. Log it.

## Phase 3: Starter pack (rules, skills, hooks)

Your part: run
```
git clone https://github.com/Aarushtodi/claude-starter.git ~/claude-starter
bash ~/claude-starter/install.sh
```
Then read ~/claude-starter/SETUP.md yourself so you know what is in the pack, and show me the list of what got installed: CLAUDE.md, 5 skills (study-drill, essay-rubric, bpa-judge, canvas-week, council), 2 hooks (notes index, command guard), bypass permissions default, ~/school/Notes.
Check: `ls ~/.claude/skills` shows the 5 skills and ~/.claude/CLAUDE.md exists. Tell me the hooks only turn on after a restart and that we restart in the last phase.

## Phase 4: Claude desktop app

My part: download the Claude desktop app from https://claude.ai/download (Windows or Linux build), install, sign in with my personal Claude account. This is where I will use chat, Projects, and see connectors. Tell me where the Settings menu is once it is open.
Check: I type "done" when I am signed in. Log it.

## Phase 5: Claude in Chrome

My part, numbered:
1. Open Chrome. Make sure my personal Google account is the Chrome profile I use for Claude, and my school Google account is also signed into that Chrome (for Canvas and school Docs), or is in a second profile. Ask me which and note it in CLAUDE.md later.
2. Install the "Claude" extension by Anthropic from the Chrome Web Store. Sign in to it with my personal Claude account.
3. Pin it to the toolbar.
Your part: tell me to type "done", then run `/chrome` instructions: I type `/chrome` in this chat and turn it on.
Check: once on, open a new tab to https://friscoisd.instructure.com and tell me what you see on my Canvas dashboard. Close the tab after. If the extension is not connected, tell me how to reconnect it. Log it.

## Phase 6: Connectors

My part, numbered: open https://claude.ai/settings/connectors on my PERSONAL account and connect, in this order:
1. Google Calendar (personal Google account)
2. Google Drive (personal)
3. Gmail (personal)
4. Granola, if I decide to use it in Phase 7 (come back for this one)
5. Notion, only if I already use Notion. Otherwise skip, we use markdown notes.
Say explicitly: do NOT connect the school Google account here.
Your part: after I type "done", tell me to type `/mcp` and read you the list. Then prove it works: list my calendar events for the next 7 days and the 5 most recent files in my Drive.
Check: both calls return real data. Log which connectors are live.

## Phase 7: Granola (class recordings)

Explain in 4 lines what Granola is (a notes app that records a meeting or a lecture, transcribes it, and writes notes) and how Aarush uses it: every class with a lecture gets recorded, then Claude drills from the transcript. Then ask me one question: do I want this, yes or no.
- Yes: tell me to install it from https://granola.ai (Windows and Mac builds exist, Linux does not), sign in, and go back to Phase 6 step 4 to connect it. Then add a line to CLAUDE.md under School: "Granola first: before drilling for a class, pull the latest Granola transcript for it."
- No: log SKIP and move on.
Check: if yes, `/mcp` shows Granola and you can list my meetings.

## Phase 8: Plugins

My part: type `/plugin`. Go to Discover (or Browse). The official Anthropic marketplace is already there. Install:
1. The Anthropic skills pack (Docs, PDF, PowerPoint, Excel). These are what let you make and read real files for school.
2. Anything called "frontend design" or "web design" if it is there (for BPA slides mockups).
3. Nothing else for now. One at a time; each one is more for Claude to read every session.
Tell me to type "done" and paste what got installed. Log it.
Check: type `/` and confirm the new skills show in the list.

## Phase 9: Interview and CLAUDE.md

Read ~/.claude/CLAUDE.md. The ABOUT ME section has blanks. Interview me, one question at a time, 8 to 12 questions, until the blanks are filled: my 8 classes with teacher names and A/B period, which classes have tests soon, my BPA team (who, roles, next deadline), how I study best, when I usually do homework, anything you must never do. Stop when my answers stop changing what you would write.
Then: rewrite ABOUT ME with what you learned. Show me the full new section. I say "save", you save it with Edit (not by overwriting the file).
Then: create one note per class in ~/school/Notes/<Class>.md plus BPA.md, each with `## Current state` and `## Log` headings and whatever I told you. Show me `ls ~/school/Notes`.
Check: CLAUDE.md has no blanks left in ABOUT ME. Log it.

## Phase 10: Memory

Explain in 3 lines: starting a message with `#` tells you to remember something permanently, and you put it in CLAUDE.md after showing me the line. Facts that change (grades, deadlines) go in the notes, rules go in CLAUDE.md. Then have me try it once with something real. Log it.

## Phase 11: Restart and first real job

1. Show me the SETUP_LOG.md with every PASS / SKIP / FAIL.
2. Tell me to type `/exit`, open my terminal again, `cd ~/school`, and run `claude`. Hooks turn on now.
3. Tell me the first message to paste in the new session, exactly this:
   "Read the notes index above and CLAUDE.md. Run /canvas-week. Then tell me the 3 things you would do for me first this week, and start on the first one."
4. If anything is FAIL in the log, give me a one line fix for each I can try tomorrow, and say "text Aarush" for anything you could not solve.

That is the whole session. Start with Phase 1 now.
