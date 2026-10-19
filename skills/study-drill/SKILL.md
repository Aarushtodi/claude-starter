---
name: study-drill
description: Drill for a test or quiz instead of lecturing. Use when Srijan says "drill me", "quiz me", "study for", "test on", "help me review", or names a unit or chapter he has a test on. Builds a question bank from his notes, Canvas, or the textbook section, asks one question at a time, tracks misses, and loops back on them until they stick. Also use to make a one page cheat sheet after a drill.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
---

# Study drill

Teaching by asking. Claude does not explain a topic until Srijan gets a question wrong on it.

## 1. Source first
- Find the real scope: the Canvas assignment or announcement for the test, the teacher's slides, the handout, or the note at `~/school/Notes/<Class>.md`. Never drill from general knowledge when a source exists; teachers test what they taught.
- If nothing is on disk and Chrome is on, read Canvas for the unit. Save what you find into the class note under a dated `### Test: <topic>` heading.
- Ask once if the format is MCQ, short answer, essay, or mixed. Match the drill to it.

## 2. Build the bank
- 20 to 40 questions, hardest material weighted heaviest. Mix recall, "why", and "compare X and Y".
- For MCQ tests write real distractors (the wrong answer a half-prepared student would pick).
- Save the bank to `~/school/Notes/drills/<Class> <topic> <date>.md` so it can be rerun.

## 3. Run it
- One question at a time. Wait for his answer. No hints before he answers.
- Right: one word ("Yes.") and the next question. Do not restate the answer.
- Wrong: the correct answer, one sentence on why, one sentence on the trap he fell into. Tag the question `MISS`.
- Every 10 questions: score line, then the MISS questions come back reworded.
- Stop when he says stop or every MISS has been answered right twice in a row.

## 4. Close
- Score, the 3 weakest ideas, and whether he is ready (be honest; "not yet" is a valid answer).
- Offer a one page cheat sheet of only the MISS material. If yes, write it as plain markdown he can print or handwrite.
- Write the result into the class note: date, topic, score, weak spots. Update its Current state block.
