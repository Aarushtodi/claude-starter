# Start Here

This is your vault. A vault is just a folder of notes that Obsidian shows nicely. Claude writes into the same folder, so whatever Claude saves, you see here, and whatever you type here, Claude reads next session.

## Turn on Dataview (one time, 2 minutes)
Dataview is what makes the tables on [[Home]] fill themselves in.
1. Click the gear icon at the bottom left (Settings).
2. Click **Community plugins** in the left list.
3. Click **Turn on community plugins**, then confirm.
4. Click **Browse**, type `Dataview`, click the one called **Dataview** (by Michael Brenan), click **Install**.
5. Click **Enable** when the button changes.
6. Close Settings and open [[Home]]. You should see tables, not code.

## The four keys you actually need
- `Ctrl+O` jumps to any note by typing a few letters. Use this instead of clicking folders.
- `Ctrl+P` opens the command palette. Every feature lives there.
- `[[` links to another note. It autocompletes and creates the note if it does not exist.
- `Ctrl+E` switches between editing and reading view.

## What each folder is for
- **Projects/** is where Claude keeps the state of everything you are working on (BPA, a big paper, an application). You rarely edit these by hand.
- **Notes/** is one note per idea, not per unit. `Mercantilism.md`, not `Unit 3 Notes.md`. Small notes that link to each other beat one long doc.
- **Classes/** is one hub per class. These are views, not lists you maintain. Add a note with the right `class:` and it shows up by itself.
- **Daily/** is the dump. `Ctrl+P`, type "daily", pick "Open today's daily note". Capture here with zero filing decisions.
- **Templates/** are blank forms. `Ctrl+P`, type "template", pick "Insert template".
- **Drafts/** is for emails and texts Claude drafts for you before you approve them.
- **Council/** is where the council skill saves its decisions.

## The project notes
Every note in Projects/ starts with this block:

```
---
type: project
status: active
domain: school
updated: 2026-01-31
---
```

Status is `active`, `waiting`, `done` or `archived`. Under it, the `## Current state` block says where things stand right now, and `## Log` is dated lines, newest at the top. At the start of every session Claude is shown the Current state of every active project, so you never have to re-explain.

Two special notes:
- **Inbox.md**: if Claude is unsure where something goes, it drops a dated line here. Sort it into the right note when you see it.
- **Blockers.md**: anything you are waiting on (a teacher reply, a teammate) goes here with who and by when.

## The frontmatter on concept notes
```
---
class: CLASSCODE
unit: Unit 3
status: weak
type: concept
---
```
`status:` goes `weak`, then `learning`, then `solid`. Mark something **weak** the moment you miss it on a check. It shows up on [[Home]] and on the class hub, and disappears when you change it to solid. That is your relearn queue and you never maintain a list.

## Tasks
Any line starting with `- [ ]` anywhere in the vault rolls up into [[Home]]. Add `[class:: APUSH]` on the line to group it under a class.

## Two habits that decide whether this sticks
1. **Capture in the daily note, always.** Deciding where something goes is what kills note systems. Decide never; link later.
2. **After every graded thing, make one note per question you missed** and mark it `weak`.

## Worth adding later
Settings, Community plugins, Browse: **Spaced Repetition** (flashcards inside notes), **Excalidraw** (diagrams), **Calendar** (month view of daily notes).
