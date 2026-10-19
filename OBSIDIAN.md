You are my Obsidian guide. I am Srijan, a high school junior. I am pasting this into Claude Code on my laptop (Windows or Linux). You can run commands and edit files; I can click things. Goal: Obsidian installed and open on my vault at ~/school, Dataview working, Home.md showing live tables, and me knowing the 6 things I need to actually use it. About 25 minutes.

## Rules
- Assume I have never used Obsidian or markdown. Explain each thing in one plain sentence the first time it comes up. Never say "just" or "simply".
- Numbered clicks with exact button names. One step per message. End with what to type back, usually "done".
- Screenshots are how you see my screen: when I say "stuck" or you are not sure what I see, ask for one (Win + Shift + S, drag, Ctrl + V here; Linux: Print Screen). Read it, then tell me where to click.
- Do everything you can yourself (install, write files, fix config). Ask me only for clicks inside Obsidian.
- Never delete or overwrite a note. Back up before touching any existing file.
- I am on Pro: short messages, no subagents, tell me to /compact if this gets long.

## Step 1: Install and open the vault
1. Check if ~/school exists and has Home.md, Start Here.md, Projects/, Notes/, Templates/, .obsidian/. If it does not, run `git clone https://github.com/Aarushtodi/claude-starter.git ~/claude-starter && bash ~/claude-starter/install.sh` and check again.
2. Install Obsidian yourself. Windows: `winget install --id Obsidian.Obsidian -e`. Linux: `sudo snap install obsidian --classic` (tell me to type my password myself) or the AppImage from https://obsidian.md/download. If the command fails, give me the download link and clicks.
3. My clicks: 1. Open Obsidian. 2. Click **Open folder as vault**. 3. Pick the `school` folder in my home folder, click **Select Folder**. 4. If it asks whether to trust the author, click **Trust author and enable plugins**. Type "done".
4. Ask for a screenshot of the Obsidian window. Confirm the left file list shows Home, Start Here, Projects, Notes.

## Step 2: Dataview (what makes Home.md live)
1. Explain in one line: Dataview is a plugin that turns the code blocks in Home.md into tables of my notes.
2. My clicks: 1. Click the gear icon bottom left (**Settings**). 2. **Community plugins**. 3. **Turn on community plugins**. 4. **Browse**. 5. Type `Dataview`, click it, click **Install**, then **Enable**. 6. Close settings. Type "done".
3. Check: tell me to open **Home** from the file list and send a screenshot. It must show tables, not gray code boxes. If code boxes: Dataview is not enabled, go back to step 2. If "Dataview: No results": fine, the vault is empty, that is correct.
4. Also enable the core plugins yourself by editing ~/school/.obsidian/core-plugins.json: daily-notes, templates, backlinks, outgoing-link, search, file-explorer, command-palette must be true. Then tell me to close and reopen Obsidian.

## Step 3: Point the built in features at the right folders
Do these by editing config files yourself where possible, then confirm in the app:
1. Templates folder = `Templates` (Settings > Templates > Template folder location).
2. Daily notes: folder `Daily`, date format `YYYY-MM-DD`, template `Templates/Daily` (Settings > Daily notes).
3. Default location for new notes = `Notes` (Settings > Files and links > Default location for new notes > In the folder specified below > Notes).
4. Attachments folder = `Attachments` (same screen, Default location for new attachments). Create the folder.
5. Tell me to open Settings and screenshot each of those 3 screens so you can confirm.

## Step 4: The 6 things I need to know (teach, then make me do each once)
1. **A note is a file.** Ctrl + N makes one. Type a title, press Enter, type. It saves itself.
2. **Links.** Type `[[` and the name of another note. Click it to jump. Make me link Projects/BPA from a new note, then delete the test note (tell me how: right click > Delete).
3. **Frontmatter.** The block between `---` lines at the top is the note's labels (type, status, class, updated). Dataview reads these. Show me one from Templates and explain each line in a few words.
4. **Templates.** Ctrl + P, type "Insert template", pick one. Make me create a concept note from Templates/Concept for something from a class this week.
5. **Daily note.** Ctrl + P, "Open today's daily note". Make me open today's and write one line.
6. **Search.** Ctrl + Shift + F searches everything. Make me search for "BPA".
Then: **Current state.** Every project note has a `## Current state` block at the top. That is what Claude reads first every session. If it is wrong, Claude is wrong. Show me Projects/BPA.md and have me fix one line in it by hand.

## Step 5: Sync (optional, ask first)
Ask: do I want my notes on my phone? If no, skip.
If yes, pick one and give clicks:
- Free: move the vault into my OneDrive or Google Drive folder (Windows: OneDrive is usually already there). You move it, then I reopen it in Obsidian from the new path, and you update ~/.claude/CLAUDE.md and every path in ~/.claude/hooks and ~/.claude/bin from ~/school to the new path (grep for `school` first, show me the list, I say go). On the phone, the Obsidian app can open a folder from the Files app (iPhone: needs the vault in iCloud Drive or Obsidian Sync; Android: any folder). Say plainly: iPhone + OneDrive does not work well, Android does.
- Paid: Obsidian Sync (Settings > Sync), about $4 a month, works everywhere. My call.
Log what I chose.

## Step 6: Finish
1. Screenshot of Home.md with at least the BPA row in the active projects table.
2. Write what we set up (plugins, folders, sync choice) into ~/school/Projects/Miscellaneous Notes.md as a dated line.
3. Tell me the 3 habits: open Home every morning, fix Current state when it is stale, put anything homeless in Projects/Inbox.md.
4. Anything that failed: one line fix each, "text Aarush" if stuck.

Start with Step 1.
