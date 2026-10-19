# Claude Code setup for Srijan (ThinkPad, Claude Pro)

**Shortcut:** do sections 1 and 2 below (install + log in), then type `/model` and pick Sonnet, then paste the whole of `BOOTSTRAP.md` from this gist as your first message. Claude walks you through everything else (Ghostty, starter pack, Claude app, Chrome, connectors, Granola, plugins, interview) one step at a time and logs what passed. The rest of this file is the manual version and the reference.

Read this top to bottom once. Takes about 20 minutes. Do the steps in order.

## 0. What you are getting

Claude Code is Claude running in your terminal with real access to your computer: files, browser, Google account. Your Pro plan already includes it, no extra cost. Same usage pool as the claude.ai chat app, so every long session here eats into your chat limits too (see section 7).

## 1. Install

**If the ThinkPad is Windows 11 (most likely):**

1. Install Git for Windows if you do not have it: https://git-scm.com/download/win (defaults are fine).
2. Open PowerShell (not as admin) and run:
   ```
   irm https://claude.ai/install.ps1 | iex
   ```
3. Close PowerShell, open it again, run `claude`. If it says "command not found", restart the laptop once.

Optional but nicer: install WSL (Ubuntu) with `wsl --install` in an admin PowerShell, reboot, then inside Ubuntu run the Linux command below. WSL gives you a proper Linux shell, which Claude Code is happiest in. Not required to start.

**If the ThinkPad is Linux (Ubuntu, Fedora, etc.):**
```
curl -fsSL https://claude.ai/install.sh | bash
```
Then open a new terminal and run `claude`.

## 2. Log in with your Pro account

First time you run `claude` it opens a browser login. Pick **"Claude account with subscription"**, not API key. Sign in with the same Google/email you use for claude.ai. Done when the terminal says you are logged in.

Check: run `claude` then type `/status`. It should show your plan.

## 3. Turn on bypass permissions

By default Claude asks before every file edit and command. For school work that gets annoying fast. Two ways:

**Per session (safest while you learn):**
```
claude --dangerously-skip-permissions
```

**Make it the default:** inside Claude Code type `/permissions`, pick **Bypass permissions**, and it remembers. Or add an alias so plain `claude` always does it:

- PowerShell: run `notepad $PROFILE`, add the line `function cc { claude --dangerously-skip-permissions @args }`, save, reopen PowerShell, use `cc`.
- Linux / WSL: `echo 'alias cc="claude --dangerously-skip-permissions"' >> ~/.bashrc` then `source ~/.bashrc`, use `cc`.

Bypass means Claude will run commands and edit files without asking. The CLAUDE.md file in section 5 is what keeps it from doing dumb stuff. Read that file.

## 4. Chrome + Google access

**Claude in Chrome (Claude drives your real browser, logged in as you):**
1. Install the Chrome extension: search "Claude in Chrome" in the Chrome Web Store, add it, sign in with your claude.ai account.
2. In Claude Code type `/chrome` and turn it on, or start with `claude --chrome`.
3. Test: "open canvas and tell me what is due this week." It should open a new tab in your Chrome and read it.

Keep your school Google account signed into Chrome so Claude can read Canvas, Google Classroom, Docs, Slides through the browser. Do NOT sign the school account into Claude itself (districts can see that). Your personal Gmail is the Claude login.

**Google connectors (Calendar, Drive, Gmail directly, no browser):**
1. Go to https://claude.ai/settings/connectors on your personal account.
2. Connect Google Calendar, Google Drive, Gmail. Use your PERSONAL Google account.
3. Back in Claude Code type `/mcp`. The Google tools show up automatically since you are logged in with the same account.

## 5. Install the CLAUDE.md, skills, and hooks (one command)

Everything is in a repo. Open Git Bash (Windows), or your terminal (WSL / Linux), and run:

```
git clone https://github.com/Aarushtodi/claude-starter.git ~/claude-starter
bash ~/claude-starter/install.sh
```

What that installs:
- `~/.claude/CLAUDE.md`: the rules file Claude reads every session. **Fill in the ABOUT ME section at the top** (teachers, periods, what you are working on). 5 minutes. Claude interviews you for the rest on the first run.
- 5 skills (type `/` in Claude Code to see them):
  - `/study-drill` quizzes you one question at a time and loops on misses
  - `/essay-rubric` finds the rubric first, drafts to it, grades the draft before you see it
  - `/bpa-judge` builds the 505 plan with you or mock judges you with hard follow ups
  - `/canvas-week` reads Canvas through Chrome, lists what is due, puts tests on your calendar
  - `/council` six advisor debate for real decisions (heavy on usage, use `quick` mode)
- Hooks: a notes index, a project index and a note drift check that load at session start so Claude knows where every class and project stands, a context size warning, and a guard that blocks `rm -rf`, force pushes, and other wipes even in bypass mode.
- A status line at the bottom of Claude Code showing the model and effort (`Sonnet 5.5 | effort medium*`), Pro friendly effort defaults (Sonnet and Opus on medium), and a model fit check: Sonnet by default, Opus only for hard essays, BPA strategy, or something broken.
- A call-out logger: when you tell Claude it was wrong ("stupid", "not what I asked"), it logs the miss to `~/school/Projects/Claude Misses.md` before fixing. Say "misses" to review the patterns.
- A school clock (`SCHOOL CLOCK:` line at session start) using your bell schedule and A/B days from `~/school/.config/bells.json` (Wakeland default). In class means no pings.
- Canvas scripts in `~/.claude/bin`, all zero Claude usage: `canvas_watch` (new, moved and graded work, open ledger, every 30 minutes), `assess_watch` (Sundays, catches teacher edits to test plans, writes them to `Projects/Inbox.md`), `weak_notes` (a stub note for every grade under full points). They need a Canvas token in `~/school/.config/canvas.json`; Claude gets it from you in BOOTSTRAP Phase 8b and registers them with Task Scheduler (Windows) or cron (Linux). Alerts are desktop notifications.
- `unblock.py` and the `BLOCKED-BY: <id>` convention for anything you are waiting on, tracked in `Projects/Blockers.md`.
- Bypass permissions set as the default (so plain `claude` works, no flag needed).
- `~/school/` as an Obsidian vault: Home.md and Start Here.md, Projects/ (BPA, Inbox, Blockers, Miscellaneous Notes), Notes/, Classes/, Daily/, Drafts/, Council/, Templates/, plus two more SessionStart hooks (project index, note drift).

Re-running `install.sh` is safe: it never overwrites a filled in CLAUDE.md.

**Plugins (Anthropic's own skills: Docs, PDF, PowerPoint, Excel, and more):**
Inside Claude Code type `/plugin`, go to **Discover**, and install the Anthropic skills pack and anything else that looks useful for school. These download into Claude Code itself, so they have to be installed from your laptop, not from a file.

## 6. First session

Open a terminal in a folder you want Claude to work in. Make one:
```
mkdir ~/school && cd ~/school
```
(Windows PowerShell: `mkdir $HOME\school; cd $HOME\school`)

Run `cc` (or `claude --dangerously-skip-permissions`) and paste this as your first message:

```
Read your CLAUDE.md. Then interview me with 8 to 10 questions, one at a time, to fill in whatever is still blank or vague about my classes, teachers, BPA, and how I like to work. After the interview, rewrite the ABOUT ME section of CLAUDE.md with what you learned, show me the diff, and save it. Then make one hub per class in ~/school/Classes from the hub template, one class note per class in ~/school/Notes, and fill in ~/school/Projects/BPA.md, each with a Current state block. Finish by telling me the 3 things you would do for me first.
```

## 7. Pro plan reality

- Pro has a usage limit that resets every 5 hours, plus a weekly cap. Claude Code burns through it faster than chat because it reads a lot of files.
- Type `/model` to see what models your plan allows. Use **Sonnet** as default for school work (fast, cheap on limits). Switch to **Opus** only for hard stuff: a long essay you actually care about, a BPA plan, debugging something broken.
- Long chats are the drain. One task per session. `/clear` when you switch topics. `/compact` if a chat gets long but you need to keep going.
- If you hit the limit mid task: it tells you when it resets. Plan long work for right after a reset.
- Do not spawn subagents (the Agent tool) for small jobs. Each one is a full extra conversation.

## 8. Useful commands

| Command | What it does |
|---|---|
| `/clear` | new conversation, keeps CLAUDE.md |
| `/compact` | shrink the chat so you can keep going |
| `/model` | switch Sonnet / Opus |
| `/permissions` | set bypass as default |
| `/chrome` | toggle browser control |
| `/mcp` | see Google and other connectors |
| `/memory` | edit CLAUDE.md from inside Claude |
| `/resume` | pick up an old session |
| `/cost` | see what this session used |
| `#` at the start of a message | tell Claude to remember something permanently |
| `Esc` twice | go back to an earlier message in the chat |
| `Shift+Tab` | cycle permission modes (normal, auto accept, plan) |

## 9. If something breaks

- `claude doctor` checks the install.
- Login loop: `claude logout` then `claude` again.
- Windows "command not found": restart the terminal, then the laptop.
- Chrome not responding: close the Claude in Chrome popup, reload the tab, try again.
- Still stuck: ask Aarush, he has a working build of all of this.
