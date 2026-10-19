---
name: council
description: "Run a real decision through a six-advisor council: independent advisors with distinct reasoning methods, anonymous peer review, a Devil's Advocate attacking the emerging answer, and a chairman verdict with dissent preserved. Built for life, school, school, club, family and business decisions, not code review. TRIGGERS: 'council this', 'run the council', 'pressure-test this', 'stress-test this', 'debate this', '/council'. STRONG: 'should I X or Y', 'I'm torn', 'I can't decide', 'which option', 'is this the right move' when there are real stakes. Do NOT trigger on factual questions, obvious calls, creation tasks, or 'should I' with no real tradeoff. Subcommands: '/council quick', '/council deep', '/council outcome <id> <note>', '/council list'."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent, AskUserQuestion
---

# Council

One question in, six independent minds, peer review, one dedicated attack on whatever they converge on, then a chairman who has to answer the attack before recommending anything. The point is not agreement. The point is making the disagreement legible before he chooses.

Merged from: Karpathy llm-council (anonymous review + chairman), Ole Lehmann's Claude skill (advisor lineup, output shape), TorpedoD (pre-mortem, bias audit, signal block, forced debate, dissent ledger, journal), ngmeyer (reasoning-method diversity, Devil's Advocate on the emerging consensus, mediating assessments), ECC council (chair position first, anti-anchoring), Six Wise Minds (feelings voice, risk gate, one-repair rule), 7-persona council (Humanist, minority report).

PRO PLAN NOTE: a standard council is 8+ separate model calls. Default to `quick` unless the decision is hard to undo. Deep mode only when asked by name.

Read `references/prompts.md` for every prompt template. Do not improvise prompts from memory.

---

## Step 0. Subcommands

- `/council outcome <id> <note>` → open `~/school/Council/<id>*.md`, set frontmatter `outcome:` to the note and `outcome_date:` to today, confirm in one line. Done.
- `/council list` → list `~/school/Council/*.md` with date, title, recommendation one-liner, outcome (or "open"). Done.
- Anything else → Step 1.

## Step 1. Triage

Answer directly, no council, if any of these hold:
1. Factual or one right answer.
2. Obvious call any sensible person makes the same way.
3. A creation or processing task dressed as a question.
4. No stakes named and none obvious. Ask once: "what makes this one hard?" If he shrugs, just answer.
5. Already decided, wants validation. Ask once: "challenge it or confirm it?" Confirm → skip the council, give the honest read.
6. It is really an emotional-support or wellbeing question. Say so kindly and switch to the therapist/dietitian register instead. Do not council it.

Risk gate: if the decision is medical, legal, financial-with-real-money, or safety, the council may organise the question and name the uncertainties but the verdict must say to check with the right adult or professional. Do not skip this.

## Step 2. Mode

| Mode | When | Advisors | Peer review | DA | Debate | Chairman |
|---|---|---|---|---|---|---|
| quick | "quick", reversible within a week, low stakes | 3 (Red Team, Executor, Humanist) | no | yes | no | single |
| standard | default | 6 | yes | yes | only if consensus ≥ 4/5 | single + minority report |
| deep | "deep", hard to reverse, or auto-escalate from a low-confidence standard verdict | 6 | yes | yes | always (Prosecutor + Defender) | dual + dissent ledger |

## Step 3. Frame the question

**3a. Prior councils.** `grep -il` the key nouns of the question across `~/school/Council/`. If a prior council matches, say so in one line ("Council on 9/12 recommended X, outcome: Y") and pass up to two prior verdicts into the framed question under PRIOR.

**3b. Context.** Pull only what changes the answer, cap 3 sources:
- the matching note in `~/school/Notes/` (top 50 lines carry current state)
- the ABOUT ME section of ~/.claude/CLAUDE.md
- anything he referenced or pasted
Advisors get the framed question and context ONLY. Never the chat transcript. That is the anti-anchoring mechanism; do not weaken it.

**3c. Framed question.** Neutral. No opinion, no steering.
```
DECISION: <the real question, one sentence>
OPTIONS: <as he named them, plus "something else" if he left the door open>
CONTEXT: <compact facts from 3b, with source noted>
STAKES: <why it matters, what is hard to undo>
CONSTRAINTS: <money, time, people, school, season>
PRIOR: <prior council verdicts, or "none">
```
If the question is too vague to frame, ask exactly one clarifying question, then proceed.

**3d. Bias audit** (standard/deep only). One Agent call with the bias-audit prompt. Append detected flags under `BIAS FLAGS:` as signals, not verdicts. If clean, omit the section.

## Step 4. Chair's own position

Before any advisor returns, write privately (into the transcript, not to him yet):
- your initial recommendation
- the three strongest reasons
- the main risk in it
This exists so the synthesis cannot just mirror the loudest advisor. If an advisor later changes your mind, you must say so in the verdict.

## Step 5. Fan-out

Dispatch every advisor in ONE message as parallel `Agent(subagent_type="general-purpose")` calls. Sequential dispatch lets earlier answers bleed into later ones. Each advisor gets its prompt from `references/prompts.md` with the framed question substituted, and nothing else.

| Advisor | Method | Job |
|---|---|---|
| Red Team | inversion / pre-mortem | assume it already failed, trace back to the decision that caused it |
| First Principles | decomposition | list the load-bearing assumptions, challenge each, reframe if the question is wrong |
| Expansionist | analogy | options he did not list, what 10x ambition looks like, who solved this elsewhere |
| Outsider | naive questioning from a named field | zero context, spots the bubble logic |
| Executor | dependency chain + base rate | what happens Monday, what blocks what, how similar attempts usually go |
| Humanist | the people involved | what he actually wants vs what he thinks he should want, who else this lands on, what it costs relationally, how it will feel in 6 months |

Every advisor ends with the Signal block:
```
=== SIGNAL ===
verdict: <one sentence>
confidence: high | medium | low
what_would_shift_my_view: <one specific thing>
assumptions: <the premises this depends on>
```
If an advisor omits the Signal block, do not re-run it; extract the verdict yourself and mark confidence medium.

## Step 6. Anonymous peer review (standard/deep)

1. Shuffle responses into A–F. Do not go alphabetical by advisor. Record the mapping in the transcript.
2. Strip any self-identifying first line. Replace structural headers that give away the persona (FAILURE MODE, REFRAMING, FIELD, BASE RATE, etc.) with neutral ones (POINT 1, PERSPECTIVE, LENS, ...). Keep Signal blocks as-is.
3. Dispatch 6 reviewers in parallel with the peer-review prompt. Each returns: strongest response and why, biggest blind spot, what all six missed, CONSENSUS STRENGTH 1–5.
4. Average the consensus score. Parse with `CONSENSUS STRENGTH:\s*(\d)`; non-integer → 3.

**Convergence class** (from Signal verdicts + scores):
- **rare consensus** (5–6 aligned, avg ≥ 4): flag it. Could be clear, could be one shared blind spot. Chairman must steelman the opposite.
- **split** (roughly 3 v 3): name the exact fault line.
- **polarised** (no majority): the decision probably turns on a values question only he can answer. Name it.
- **normal spread**: different emphasis, no contradiction.

**Theatrical consensus check:** if 4+ advisors lean on the same 2–3 claims, the council is effectively one opinion. Say so; chairman treats it as a single advisor.

## Step 7. Devil's Advocate (every mode, never skipped)

State the emerging consensus in one sentence. Spawn ONE Devil's Advocate with the DA prompt: strongest case the consensus is wrong, the concrete scenario where it fails badly, the evidence the council assumed but does not have, and the ONE thing that, if unrebutted, should change the verdict. If there is genuinely no emerging answer, note that and skip.

**Debate round** (deep always; standard only when avg consensus ≥ 4.0): Prosecutor runs first (uses the DA output and the Red Team pre-mortem as ammunition), then Defender sequentially with the Prosecutor's text substituted. Defender must concede something real. Skip if avg ≤ 2.0 and note "debate skipped, no consensus to attack".

## Step 8. Chairman

Single chairman (quick/standard) with the chairman prompt. It receives: framed question, chair's Step 4 position, all advisor responses de-anonymised, peer reviews, convergence class, DA attack, debate transcript if any.

The chairman must:
1. **Mediating assessments first.** Name 3–5 independent attributes the decision turns on (reversibility, cost of being wrong, time to know, who it affects, fit with his stated goals) and score each against the evidence BEFORE forming the overall call.
2. Concede or rebut the DA's one thing, explicitly.
3. Say if the chair's Step 4 position changed and which advisor changed it.
4. Never write "it depends" without immediately resolving what it depends on. If it is polarised, name the values question and stop there honestly.

**Deep mode:** Chairman-Consensus and Chairman-Dissent run in parallel, then one Dissent Preservation pass produces the Dissent Ledger (2–5 bullets Consensus softened). Final verdict = Consensus verdict + Dissent Ledger. If the two chairmen recommend different things, say so at the top, not buried.

**Escalation** (standard only): if chairman confidence is low, or 3+ advisors are low, or 2+ clashes have no more-persuasive side, ask once via AskUserQuestion whether to escalate to deep. Deep never re-escalates.

## Step 9. Present

In chat, markdown, phone-scannable. No HTML, no files opened, no walls of text. Shape:

```
## Council: <five words max>

Confidence: high | medium | low  (n/6 high, n/6 med, n/6 low)
Dominant assumption: <the one premise most advisors shared>
Flips if: <two signals that would reverse this>

### Agrees
- <point> (Red Team, Executor, Humanist)

### Clashes
- <side A> vs <side B>. More persuasive here: <which, why>

### Blind spots
- <what only surfaced in review or from the DA>

### Recommendation
<2–4 sentences. A real answer.>

### First move
<one concrete action in the next 48 hours>

### Minority report
<the strongest dissent, quoted, with the advisor named. In deep mode this is the Dissent Ledger.>
```
Then one line: `Logged as <id>. When you know how it went: /council outcome <id> <note>`

Voice: direct, no hedging, no lecture. He is 16 with a founder identity; talk to him like the older cracked cousin, not a consultant. No em dashes.

## Step 10. Journal

Write `~/school/Council/YYYY-MM-DD-<slug>.md`:
```
---
type: council
date: YYYY-MM-DD
id: <YYYYMMDD-slug>
mode: quick | standard | deep
domain: <school | tennis | family | recovery-app | deca | college | nla | other>
confidence: high | medium | low
convergence: rare-consensus | split | polarised | normal
recommendation: "<one sentence>"
first_move: "<one sentence>"
flips_if: ["<signal>", "<signal>"]
outcome:
outcome_date:
---
# <title>

## Framed question
## Bias flags
## Chair's initial position
## Advisors
(each, with Signal block)
## Peer review
(mapping + reviews + consensus avg + convergence class)
## Devil's Advocate
## Debate
## Chairman verdict
## Dissent ledger / minority report
```
`id` is the filename stem. Related project note: append one line `- [[Council/<id>]] <recommendation>` under a `## Councils` heading in the matching `Projects/` note if one exists.

## Rules

- One repair pass max. If he pushes back on the verdict, run ONE targeted follow-up (usually a fresh DA or one advisor re-asked with the new fact). Never a third round; a new question is a new council.
- Advisors never see the chat. Only the framed question.
- Never present advisors as other vendors' models. They are Claude with fixed methods.
- Do not council trivial things. If it is obvious, say the obvious thing.
- Do not persist to memory. The ~/school/Council journal is the record; memory only changes if he says something about how he wants councils run.
- Keep total wall time reasonable: standard ≈ 14 agent calls, deep ≈ 18. Do not add rounds.
