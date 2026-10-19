You are my setup guide. I am Srijan, a junior at Wakeland High School in Frisco, Texas. I am on a ThinkPad and I have a Claude Pro plan. Right now I only have the Claude desktop app. A friend (Aarush) runs a full version of this setup on a Mac and wrote this prompt. Your job is to take me from the chat app I am typing in to a full working school system: Claude Code on my laptop with real file, browser and Google access, every app in Aarush's stack installed, then an interview that fills in my rules file and builds my notes. You do everything you can yourself and tell me exactly what to click for the parts only I can do.

## First: figure out where you are

Before anything else, try to run a shell command (for example `echo hello`).
- If you CANNOT run commands, you are in the Claude desktop app chat. Do **Phase 0** only, then stop. I will paste this same prompt again inside Claude Code and you will skip to Phase 1.
- If you CAN run commands, you are in Claude Code. Skip Phase 0 and start at Phase 1.

## Phase 0: Get Claude Code (desktop app only)

Tell me, numbered, short:
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
- Keep a log at ~/school/SETUP_LOG.md: one line per phase and per app, PASS / SKIP / FAIL, plus anything to fix later. Create it in Phase 1.
- Short messages. I am reading this in a terminal.
- I am on Pro. Do not spawn subagents. Do not read files you do not need. If this chat gets long, tell me to run /compact.
- Never run anything that deletes, force pushes, or wipes. Never sign my school Google account into anything Claude. School account lives in Chrome only. Personal Gmail is my Claude login.

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
| 8 | Obsidian | Obsidian | Windows: `winget install --id Obsidian.Obsidian -e`. Linux: snap `sudo snap install obsidian --classic`, or the AppImage/.deb from https://obsidian.md/download. Then tell me: open Obsidian > Open folder as vault > pick `~/school/Notes`. That folder is where you write my notes, so I can read them there. |
| 9 | Willow Voice (dictation, Aarush talks to Claude instead of typing) | Windows: **Willow Voice** (it has an official Windows app). Linux: no Willow; try Wispr Flow if it has a Linux build when I check, else SKIP and I type. | Windows: download from https://willowvoice.com (Students page: https://willowvoice.com/students for the student plan). Install, open, allow Microphone and Input/typing permissions, learn the hotkey it shows. Test: tell me to dictate one sentence into this terminal. |
| 10 | Granola (records classes) | Windows: **Granola**. Linux: none, SKIP. | Decided in Phase 7, not here. Just note it in the log as "pending Phase 7". |
| 11 | Grammarly | Windows: Grammarly desktop. Linux: the Grammarly Chrome extension only. | Optional. Windows: `winget install --id Grammarly.Grammarly -e`; if not found, https://www.grammarly.com/desktop/windows. Ask me yes/no first; skip if I say no. |
| 12 | Ollama (local models) | Ollama | Optional and only if the ThinkPad has 16 GB RAM or more (check first). Windows: `winget install --id Ollama.Ollama -e`. Linux: `curl -fsSL https://ollama.com/install.sh | sh`. If RAM is under 16 GB, SKIP and say why. |

Rules for this phase: one app per message, run the command, show me the result, then the next. Do not install anything not on this list. If winget asks me to accept terms, tell me what to type. Restart the terminal at the end of this phase if PATH changed (tell me to type `exit`, reopen, run `claude --resume` and pick this session, then "continue phase 3").
Check: `git --version`, `python3 --version`, `node --version`, `gh --version` all print, Chrome and Obsidian open, Willow Voice dictated one sentence. Log it.

## Phase 3: Starter pack (rules, skills, hooks)

Your part: run
```
git clone https://github.com/Aarushtodi/claude-starter.git ~/claude-starter
bash ~/claude-starter/install.sh
```
Then read ~/claude-starter/SETUP.md yourself so you know what is in the pack, and show me the list of what got installed: CLAUDE.md, 5 skills (study-drill, essay-rubric, bpa-judge, canvas-week, council), 2 hooks (notes index, command guard), bypass permissions default, ~/school/Notes.
Check: `ls ~/.claude/skills` shows the 5 skills and ~/.claude/CLAUDE.md exists. Tell me the hooks only turn on after a restart and that we restart in the last phase.

## Phase 4: Claude desktop app check

I already use it. Tell me where Settings and Connectors are in it (we need them in Phase 6) and confirm the account matches. Log PASS.

## Phase 5: Claude in Chrome

My part, numbered:
1. Open Chrome. My personal Google account is the Chrome profile I use for Claude. My school Google account is also signed into Chrome (for Canvas and school Docs), either in the same profile or a second one. Ask me which and remember it for CLAUDE.md.
2. Install the "Claude" extension by Anthropic from the Chrome Web Store. Sign in to it with my personal Claude account.
3. Pin it to the toolbar.
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

## Phase 9: Interview and CLAUDE.md

Read ~/.claude/CLAUDE.md. The ABOUT ME section has blanks. Interview me, one question at a time, 8 to 12 questions, until the blanks are filled: my 8 classes with teacher names and A/B period, which classes have tests soon, my BPA team (who, roles, next deadline), how I study best, when I usually do homework, which Chrome profile has the school account, whether I dictate with Willow or type, anything you must never do. Stop when my answers stop changing what you would write.
Then: rewrite ABOUT ME with what you learned. Show me the full new section. I say "save", you save it with Edit (not by overwriting the file).
Then: create one note per class in ~/school/Notes/<Class>.md plus BPA.md, each with `## Current state` and `## Log` headings and whatever I told you. Show me `ls ~/school/Notes` and tell me to look at them in Obsidian.
Check: CLAUDE.md has no blanks left in ABOUT ME. Log it.

## Phase 10: Memory

Explain in 3 lines: starting a message with `#` tells you to remember something permanently, and you put it in CLAUDE.md after showing me the line. Facts that change (grades, deadlines) go in the notes, rules go in CLAUDE.md. Then have me try it once with something real. Log it.

## Phase 11: Restart and first real job

1. Show me SETUP_LOG.md with every PASS / SKIP / FAIL, apps included.
2. Tell me to type `/exit`, open my terminal (Windows Terminal or Ghostty), `cd ~/school`, and run `claude`. Hooks turn on now.
3. Tell me the first message to paste in the new session, exactly this:
   "Read the notes index above and CLAUDE.md. Run /canvas-week. Then tell me the 3 things you would do for me first this week, and start on the first one."
4. If anything is FAIL in the log, give me a one line fix for each I can try tomorrow, and say "text Aarush" for anything you could not solve.

That is the whole session. Start now: try the shell command, then Phase 0 or Phase 1.
