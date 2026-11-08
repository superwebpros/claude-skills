---
name: lesson-retrospective
description: Capture a post-class instructor retrospective for a course session, then push its implications into the plans it affects. Use whenever the instructor has just taught or is debriefing a class — "retro for session 8", "I just taught today's class", "let's debrief", "what actually happened vs. what I planned", "post-class reflection", "log how class went", "capture what happened in class today", "update the lesson plan with what really happened" — and also when he mentions students who fell behind, a block he had to skip, or timing that blew up in a session he just ran. Interviews him on five short prompts, writes units/NN-unit/SS-retro.md from the course template, then derives concrete edits to the next session's plan, course-calendar.md, unit overviews, and any at-risk milestone. Use it even when he only has two minutes — a three-line retro beats none, and the downstream pass is where the value is.
---

# Lesson Retrospective

> **Setup.** Part of the `msu-course` plugin with its siblings `lesson-planning` and
> `course-student-docs` (invoked as `/msu-course:<skill>` when installed as a plugin). Set
> `COURSE_ROOT` to your course repo (the vault folder holding `course-calendar.md`) or run from its
> root. Optional: `PILOT_ROOT` (frozen pilot record, read-only).

The instructor teaches SSC 490-005 at Michigan State and runs a retro after nearly every class. In the
Spring 2026 pilot the habit collapsed — 4 of 23 sessions got one — and those four turned out to
be the most valuable documents in the entire course record. Everything in this skill is shaped by
one question: **will this retro still get written on a Thursday night when he's tired?**

Two consequences that govern how you behave:

**His time is the scarce resource, not yours.** Keep the interview short and accept terse answers.
Do the expensive thinking yourself, afterward, and hand him decisions rather than homework.

**A retro that changes nothing was not worth writing.** The pilot's Session 15 retro said
*"Session 16 needs to account for this — can't assume pillars are done."* Session 16 did not
account for it. Preventing exactly that is the point of this skill. The downstream pass in
Step 6 is the centerpiece; the interview is just how you get the inputs for it.

## Ground rule: never invent what happened in a class

You were not there. Every factual claim in a retro comes from the instructor or from an artifact you
actually read. If he doesn't answer a prompt, **leave that section blank** — a blank section is
honest and is a visible signal that a topic went unexamined. Inferring "what probably happened"
from the lesson plan produces a document that reads fine and is worthless, because its whole
value is being the record of where the plan and reality diverged.

Never write into the retro: what the lesson plan said students would do, plausible-sounding
timings, or student reactions nobody reported. You may *ask* about those things.

---

## Step 1 — Locate the course

Use `$COURSE_ROOT` if set, else the current directory (run from the course repo root). Confirm
`course-calendar.md` exists there. If it doesn't, look for the current semester's folder among the
sibling course folders (prefer one whose `course-calendar.md` brackets today's date) and confirm your pick with the instructor before writing anything.

Never write into the pilot course folder (`$PILOT_ROOT`) — that's the frozen Spring pilot record.

## Step 2 — Resolve which session

- **Given a number** ("retro for session 8") — use it.
- **"the session I just taught" / "today's class"** — match today's date against the Session Grid
  in `course-calendar.md`.
- **No date match** (he's catching up on a retro from last week) — offer the most recent past
  session that has no `SS-retro.md` file yet.

Then confirm in one line before going further, because writing to the wrong session number is
expensive to unwind:

> Session 8 — APIs & data sources, Thu Sep 24, Unit I·M. Right one?

If a retro file already exists for that session, say so and ask whether to add to it or replace it.

## Step 3 — Read the context (quietly, before asking anything)

Read these yourself so the interview can be specific instead of generic. Don't narrate the
reading and don't summarize it back at him.

| File | What you need from it |
|---|---|
| `units/*/SS-*.md` (the lesson plan) | The Outcome / dated steps, and the **Steering checkpoints** table (older plans: **Off-Track Detection**) — the artifacts he said he'd check and the triggers |
| `course-calendar.md` | Date, unit, session title, whether a milestone lands on or near this session |
| `units/<unit>/Unit Overview.md` | The unit's deliverables and outcome |
| The **next** session's plan, if it exists | Its **Prerequisite Deliverables** — the thing most likely to be invalidated by what happened today |
| `templates/retrospective-template.md` | The output shape. Read it rather than reproducing it from memory; it's the source of truth and it can change |

The lesson plan file is found by glob on the global session number: `units/*/08-*.md`. Session
numbers are global (01–28) and units are folders, so the number identifies the session no matter
which unit folder it sits in.

If any of this is missing (an unwritten next-session plan is common), note it and move on. A
missing file is not a blocker for a retro.

## Step 4 — Interview

Five prompts. Ask **one or two at a time**, conversationally. Do not paste all five as a wall of
questions — that's a form, and forms are what he skips.

1. **What actually happened vs. planned.** Timing overruns, blocks skipped, pivots. Push once for
   specific minutes ("the plan had 15 for the build — what did it actually take?") because
   "it ran long" doesn't help future-the instructor and "20 min, needed 30" does. Push *once*, then let it go.
2. **What worked — keep it.**
3. **What didn't — change it.**
4. **Who's off track.** Names, and the artifact that revealed it. Outreach needed by when? See below.
5. **Carry forward to next session.**

Prompts 4 and 5 have a second reader: the `lesson-planning` skill treats the previous session's
retro as its highest-value input, reading prompt 5 as requirements for the next plan and prompt 4
as who needs outreach and who shapes the opening. That's the mechanism by which a retro reaches
next week. Worth knowing when you're deciding how hard to press on a vague answer — specificity in
4 and 5 pays off twice.

**Accept terse answers.** "Fine, ran 10 over on the build" is a complete answer to prompt 1. Ask
your one follow-up where it's genuinely load-bearing, then write it down. Pressing a tired
instructor for richer prose is how you teach him that retros are expensive.

**Don't expand scope.** No sixth prompt, no sub-questions you invented, no "while we're here."
If he answers three of five and stops, write those three and leave the rest blank.

### Prompt 4 has a specific job

At 30 students across 8–10 teams the instructor cannot see who isn't working. The pilot found students
with zero n8n executions only through a post-class audit, and peer evaluation surfaced team
problems far too late to fix them. So prompt 4 is not "any concerns?" — it's an audit.

Quote the lesson plan's **Steering checkpoints** row for this session (older plans: **Off-Track Detection**) back to him and ask whether he's checked it:

> Plan says check n8n execution logs, threshold = zero executions. Have you looked yet — and who's on the list?

If he hasn't checked, that's fine and worth recording as such ("not yet checked — do before
Thursday"). Record names and the specific artifact that revealed each one. Vague worry ("a couple
teams seem behind") is worth writing down too, but ask which teams.

Capture a **by-when** for outreach. An off-track student named in a retro with no date attached is
how the pilot lost people.

### Reggie transcripts

Reggie is the AI agent that runs individual student reflection interviews ahead of retrospectives;
the instructor reads them to surface common themes before facilitating a live retro. If he mentions Reggie
output, or points you at a transcript, offer to fold it in.

Treat it as **student-reported data, not ground truth** — it's what students said about their own
experience. Attribute it in the retro (*"Reggie: three students reported losing the thread during
the API block"*) rather than stating it as fact. Where it contradicts the instructor's read, record both;
the disagreement is itself the useful signal. Never use Reggie themes to fill in prompts the instructor
left blank.

## Step 5 — Write the retro

Write `units/<NN-unit>/<SS>-retro.md` using `templates/retrospective-template.md`. Fill the
frontmatter `session:` and `date:` from the calendar. Keep the file short — his words, tightened,
not expanded into paragraphs.

**Write this file before starting the downstream pass**, not after. If he gets pulled away
mid-conversation, the retro exists. That ordering is the whole insurance policy.

Then show him the file — it's short enough to read in the terminal — so he can correct anything
you misheard before it hardens into the record.

## Step 6 — The downstream pass

**This is the part that makes the retro worth writing.** Read
`references/downstream-pass.md` and work through it now.

In short: derive what the retro *implies* for the rest of the course, and present it as a
specific, actionable list with file paths and proposed edits. Then offer to make them. **Never
make these edits silently** — several of them are the instructor's judgment calls about scope and the
partner relationship, not clerical fixes.

The cost asymmetry is the point: the interview costs him five minutes and the downstream pass
costs him a yes or no per item, while the analysis behind it costs him nothing. That's why
"keep it short" and "do the full downstream pass" aren't in tension.

## Step 7 — Offer to annotate the lesson plan

Ask — don't do it unprompted:

> Want me to mark up the Session 8 plan too? Strikethrough on the blocks that didn't happen, callouts for the pivots.

If yes, read `references/annotating-lesson-plans.md`. The instructor has documented conventions for this
(`~~strikethrough~~` for planned-but-not-done, `> [!note] What Actually Happened`,
`> [!warning] Timing Issue`, `> [!tip] For Next Time`) and they are his — preserve them exactly.

The retro file is the primary record; annotating the plan is a bonus that makes the plan
trustworthy for the next cohort. Skipping it is a fine outcome.

## Closing

End with the outreach list and dates, if there is one — that's the only part of a retro with a
clock on it:

> Written: `units/01-inventory-and-map/08-retro.md`. Updated the S9 plan and the calendar.
> Outstanding: email the three students with no n8n executions by Wednesday.

## References

- `references/downstream-pass.md` — the derivation checklist. **Read in Step 6, every time.**
- `references/annotating-lesson-plans.md` — the instructor's markup conventions. Read in Step 7 if he says yes.
- `references/course-layout.md` — vault paths, unit mapping, calendar structure, template fallback.
  Read only if Step 1 or Step 3 doesn't resolve cleanly.
