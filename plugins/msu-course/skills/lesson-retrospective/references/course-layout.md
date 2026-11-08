# Course vault layout

Read this only when Step 1 or Step 3 doesn't resolve cleanly — a missing folder, an ambiguous
session number, a template that isn't there.

## Finding the active course

Use `$COURSE_ROOT` if set; otherwise the current working directory if it contains `course-calendar.md`
(run from the course repo root).

Don't hardcode a semester. To resolve generally: list the sibling course folders next to the course root, read each
`course-calendar.md`, and prefer the one whose semester brackets today's date. Confirm your pick
before writing.

**The pilot course folder (the frozen Spring 2026 SSC 493 record; `$PILOT_ROOT` if set) is read-only.** Read it, never write to it. Its value
is being an honest record of what happened, including where the plan broke, and that depends on not
being retconned. It is also where the four good retros live, if you want to see the target quality.

## Layout

```
<course-root>/
├── course-calendar.md      ← authoritative: dates, session numbers, units, milestones
├── course-facts.md         ← enrollment, staffing, the Archie/Reggie/Eve agents
├── course-arc.md
├── whiteboard.md           ← unresolved ideas; a reasonable home for future-cohort notes
├── Syllabus.md             ← student-facing
├── templates/
│   ├── retrospective-template.md   ← the retro output shape
│   ├── session-plan-template.md
│   ├── assignment-template.md
│   └── unit-overview-template.md
├── units/
│   ├── 00-foundations/
│   │   ├── Unit Overview.md
│   │   ├── 01-course-framework-team-formation.md   ← lesson plan, GLOBAL session number
│   │   ├── 01-assignment-*.md
│   │   ├── 01-retro.md                              ← written after teaching — what you create
│   │   └── evals/
│   ├── 01-inventory-and-map/
│   ├── 02-process-and-anchor/
│   ├── 03-compose/
│   └── 04-track-and-handoff/
├── carried-over/           ← curated pilot assets; includes get-back-on-track.md
├── partners/
└── admin/
```

## Session numbers are global

Session files carry the global number **01–28**, not a within-unit number, no matter which unit
folder they live in. So the lesson plan for session 8 is `units/*/08-*.md` and the retro is
`units/<same folder>/08-retro.md`.

This exists because the pilot renamed `unit-N-topic/` to `week-NN-topic/` mid-semester and orphaned
files across both schemes. Global numbers mean moving a session between units is a `mv`, not a
renumber.

**Find the unit folder by globbing for the lesson plan**, not by mapping the calendar's unit label.
The plan's location is ground truth for where the retro goes. If no lesson plan exists (a session
taught from slides alone — the pilot had several), fall back to the calendar's Unit column:

| Calendar label | Folder |
|---|---|
| Foundations | `00-foundations` |
| I·M | `01-inventory-and-map` |
| P·A | `02-process-and-anchor` |
| C | `03-compose` |
| T | `04-track-and-handoff` |

## Retro template fallback

Always prefer reading `templates/retrospective-template.md` — it's the source of truth and may
change. Only if it's genuinely missing, use this shape:

```markdown
---
tags:
  - ssc490
  - retrospective
  - fall2026
session:
date:
---

# Retro — Session {{session}}: {{title}}

## 1. What actually happened vs. planned

## 2. What worked — keep it

## 3. What didn't — change it

## 4. Who's off track

## 5. Carry forward to next session

---

**Downstream edits needed:**
```

## Calendar facts worth knowing

- 28 sessions, Tue/Thu, 80 minutes. Sep 1 – Dec 10, 2026.
- **Dates and session numbers are confirmed and do not move.** Content moves between fixed slots.
- Weeks 9 and 13 are single-session (Fall Break Oct 26–27; Thanksgiving Nov 26–27).
- Milestones: M1 · S6 Sep 17 (individual) · M2 · S14 Oct 15 · M3 · S19 Nov 5 · M4 · S24 Nov 24 ·
  M5 · S27 Dec 8. M2–M5 go to partners.
- Many Fall session titles are still blank past S8 — the calendar says titles are firm through S7
  and unit-level after that. Filling one in from what was actually taught is a real improvement.

## Cohort facts that shape prompt 4

- **30 students, roughly 8–10 teams** (the pilot was 19 students, 5 teams).
- Pass/No Pass. GWC framework (Get it / Want it / Capacity), rated `+` / `+/-` / `-`.
- Partners: several community/business partners (listed in `course-facts.md`), with multiple teams per partner.
- The pilot's failure mode was **invisible students** — some had zero n8n executions and were found
  only by a post-class audit, and peer evaluation surfaced team problems far too late. At 8–10
  teams, detection has to be systematic rather than observational. That's why every lesson plan
  carries **Steering checkpoints** (when · artifact the instructor looks at · trigger to step in), including
  checks between classes. Plans written before Oct 2026 call this **Off-Track Detection**.

## The student-facing agents

Live outside the vault; distributed to students by QR code in slides.

- **Reggie** — individual reflection / pre-retrospective interview. The instructor reads Reggie transcripts
  before facilitating a live retro, to surface common themes. Student-reported data, not ground truth.
- **Eve** — peer evaluation.
- **Archie** — learning recovery, paired with `carried-over/get-back-on-track.md`.

## Slides

Reveal.js decks live in a **separate repo**, not the vault (`$SLIDES_DIR` if set; ask otherwise).
Don't write there from this skill.
Worth knowing because in the pilot the slides were a more accurate record of what was actually
taught than the lesson plans were — so if the instructor can't remember what he covered, the deck is the
better memory aid to point him at.
