---
name: canvas-week
description: Pull what is due and what is coming from Canvas through the browser. Use when Srijan says "what's due", "canvas", "this week", "what do I have", "any tests coming", or at the start of a planning session. Reads the Canvas dashboard and each course's upcoming items through Claude in Chrome, lists them by date, adds test dates to Google Calendar, and writes the week into the notes.
allowed-tools: Read, Write, Edit, Bash, mcp__claude-in-chrome__*, mcp__claude_ai_Google_Calendar__*
---

# Canvas week

Needs Claude in Chrome on (`/chrome`) and the school Google account signed into Chrome.

## 1. Read
- Open a NEW tab to the district Canvas (Frisco ISD: https://friscoisd.instructure.com). Never reuse one of his open tabs.
- Dashboard first: the To Do and Coming Up panels. Then each course card: Assignments sorted by due date, plus Announcements from the last 7 days (teachers put test dates there).
- Pull: title, course, due date and time, points, and whether it is submitted.
- Close every tab you opened when done.

## 2. Report
One list, by date, nearest first. Format:
```
Mon 10/20  APUSH    Unit 4 reading quiz          10 pts   not submitted
Tue 10/21  Precal   HW 3.4                       completion
Thu 10/23  AP Lang  TEST: rhetorical analysis    major
```
Then: anything overdue, anything with no due date but 50+ points, and any announcement that mentions a test, quiz, project, or deadline.

## 3. Calendar
- Tests, quizzes, projects, and major grades go on his Google Calendar (personal account) as `TEST: <class> <topic>`, `QUIZ: ...`, or `DUE: <class> <title>`. Check for an existing event first so nothing doubles.
- For a test: also add a 1 hour `Study: <class>` block two evenings before, avoiding anything already on the calendar.

## 4. Notes
- Write the week into `~/school/Notes/Week.md` (overwrite, dated at top).
- Any new test or deadline also goes into that class's note as a dated line, and its Current state block gets updated.
