---
name: lesson-planning
description: "Plan or rework one class session (or a multi-session milestone sprint) for MSU SSC 490-005 (AI Workflows & Organizational Intelligence). Reads the authoritative course calendar, unit overview, adjacent sessions and the previous session's retro, writes a six-part outcome/steering plan (Outcome, Roadmap, Tracking, Team operating model, Steering checkpoints, Student docs) into the course vault, then runs a sync pass over everything the new plan invalidates. Use when asked to plan, draft, rework, revise or fill in a session, sprint, lesson plan, class day or session assignment for SSC 490 / SSC 493 / 'the MSU course' - by number ('plan session 9'), date ('what am I teaching Thursday'), topic, or when a session moved and other docs must change. Student-facing docs the plan links are written with the course-student-docs skill. Not for post-class retrospectives (use lesson-retrospective) or scaffolding a new course."
---

# Lesson Planning — SSC 490-005

> **Setup.** Part of the `msu-course` plugin with its siblings `lesson-retrospective` and
> `course-student-docs` (invoked as `/msu-course:<skill>` when installed as a plugin). Set
> `COURSE_ROOT` to your course repo (the vault folder holding `course-calendar.md`) or run from its
> root. Optional: `SLIDES_DIR` (slide-deck markdown), `PILOT_ROOT` (frozen pilot record, read-only).

Produce an **outcome/steering plan** for one session or a milestone sprint, then run a **sync pass**
over everything that plan just made stale.

SSC 490 runs like a client project, not a lecture. Teams deliver real artifacts to real partners;
the instructor is the meta-PM. A plan says **what teams produce, by when, how the work is tracked, and where
the instructor steers** — never how the instructor should teach. No lines to say, no call-and-response prompts, no
circulating questions, no minute-by-minute blocks. In his words: *"I really need you not to tell me
how to teach; what I need are paths to outcomes."*

Two pilot failures still shape this skill: nobody reconciled plans against the calendar (three
contradicting schedules ran at once), and off-track teams were invisible until a post-hoc audit. So
the sync pass is required, and every plan names **steering checkpoints**: what the instructor looks at, when,
and what makes him step in.

## Before you start

Read `references/course-context.md` — frameworks, stance, scale, pilot failures. Orientation only;
the vault is the source of truth, read fresh at runtime.

Read `references/writing-guide.md` before writing anything. It defines the six parts, the voice, and
the rejected patterns, from the instructor's own corrections.

Read the approved reference plan: `units/01-inventory-and-map/11-inventory-sprint.md`.

## Step 1 — Locate the course and the session

```bash
ROOT="${COURSE_ROOT:-$PWD}"   # set COURSE_ROOT to your course repo, or run from its root
[ -f "$ROOT/course-calendar.md" ] || ROOT=$(dirname "$(find "$ROOT/.." -maxdepth 2 -name course-calendar.md | sort | tail -1)")
```

If more than one candidate exists, ask which course.

**The session number is the input** — global, 1–28. If the user gave a date, weekday or topic,
resolve it against the calendar grid and confirm: *"Thursday Oct 1 is Session 10, Inventory & Map —
that one?"* When the work is a milestone sprint (e.g. S11–S14 → M2), plan the whole sprint in the
first session's file; later sessions in the sprint get short delta plans that link it.

## Step 2 — Gather context, in this order

```bash
bash <this-skill-dir>/scripts/session-context.sh <NN> [course-root]   # path relative to this SKILL.md
```

Fall back to reading by hand if it fails — the order matters more than the tool:

| # | Read | Why it matters |
|---|------|----------------|
| 1 | `course-calendar.md` | **Authoritative.** Date, unit, title, `M#` due dates, Zoom/partner/guest days, single-session weeks. |
| 2 | `units/<NN-unit>/Unit Overview.md` | The unit outcome this session serves. |
| 3 | **Previous session's `NN-retro.md`** | Carry-forward items are requirements. Off-track teams named there set today's steering. |
| 4 | Previous + next session plans | Teams' real starting state; what the next session assumes exists. |
| 5 | Team SOWs, `partners/`, team project folders | What each team is actually building. Steering is per team. |
| 6 | `course-facts.md` | Teams, partners, infra, open ⚠️ items. |
| 7 | `CARRIED-*.md` in the unit | Pilot material. Mine it; don't schedule it as-is. |
| 8 | `templates/session-plan-template.md` | The output shape. Read it each run. |
| 9 | `course-arc.md`, `Syllabus.md` | Only as needed. |

**No retro for a taught session?** Ask first: *"S8 was taught Sep 24 and has no retro. Anything I
should know, or run the lesson-retrospective skill on S8 first?"*

## Step 3 — Rework or write fresh?

Carried pilot plans carry a `> [!warning] Carried from the Spring 2026 pilot` banner and a `Needs
rework:` line — that line is the instructor's spec. Rework into the six-part shape; keep case material and
pacing evidence; drop the pilot's scripted blocks. Move any Spring reflection to the pilot record
(say where). Delete the banner and Spring frontmatter once the plan is genuinely Fall.

**The instructor's review comments** arrive as ` ```jf-note ``` ` blocks (or inline `` `jf-note: …` ``) in the
vault file. Every note is a requirement. Before revising, copy the annotated version to the scratchpad
as `<file>.vN-with-jf-notes.md`, address every note, and leave no notes in the live file.

## Step 4 — Design before you write

On scratch first:

0. **Objectives live at the unit level.** Bloom's-verb Key Learning Objectives belong in the Unit
   Overview (D2L-ready), pitched at the **application layer and above** (apply, configure, research,
   build, evaluate, defend), not remember/understand. A session plan names which unit objective(s)
   it advances in one line under the title; it doesn't write its own objective list. If the unit's
   objectives are still a stub, draft them (application-layer) and propose them in the sync pass.
1. **Outcome.** What artifact does each team hand over, to what standard, on what date? Inside a
   milestone sprint, the outcome is the milestone and this session is a dated step toward it. The
   standard must be checkable by looking at the artifact.
2. **Roadmap.** The process steps a team follows, abstract enough to fit every team's project.
   Organize around real use cases (requirements → can the system do it? Yes / No / Maybe), not
   abstract entities.
3. **Tracking.** Every tracked thing gets one home and a person who updates it.
4. **Team operating model.** Who PMs, how work divides, where tasks and due dates live.
5. **Steering.** For each class day and each between-class check: the artifact the instructor looks at and
   what triggers him stepping in.
6. **Student docs.** Which session doc / milestone doc / step examples / templates / student skills
   exist or must be written.

Hold the stance: *AI belongs inside a process, not independent of one.* Teams automating before the
process exists is a design bug — flag it.

## Step 5 — Write the plan

One instructor-facing file, global session number: `units/<NN-unit>/<SS>-<slug>.md`, following
`templates/session-plan-template.md`.

The student-facing docs it links (session doc, milestone/assignment doc, step examples, templates)
are separate files written with the **course-student-docs** skill. Invoke it; don't write them here.

Do **not** create `NN-retro.md`. The plan links to it; `lesson-retrospective` writes it after class.

## Step 6 — Check before calling it done

- **Six parts, in order**: Outcome · Roadmap · Tracking · Team operating model · Steering
  checkpoints · Student docs.
- **Outcome standard is checkable** — "every requirement answered Yes / No / Maybe with a docs link
  or reason," not "understands APIs."
- **Dated steps** from now to the milestone, including every partner-facing send (PM sends, after
  the instructor's review).
- **Steering checkpoints** name a time, an artifact and a trigger, with at least one check *between*
  classes. Class time is work time; at 8–10 teams the instructor can't see who isn't working by looking.
- **Deck = outline only.** Topic list + vocabulary to define. None of your prose on slides.
- **No script.** Run the scan in `references/writing-guide.md`; it must come back empty.
- **Prep** includes testing the exact student path 24–48h out, publishing student docs, and
  recording the session.
- **Partner milestone** table filled, even when "none."
- **The instructor's own to-dos** (email a partner, decide a tool) are beads assigned to him, cited by ID.
- **Retrospective link only** — `[[NN-retro]]`, empty. Never pre-populate it.

## Step 7 — The sync pass

**Every time.** Read `references/sync-pass.md` and work its checklist: `course-calendar.md`, the unit
overview, adjacent plans, `Syllabus.md` (rare), the slide deck, `course-facts.md`.

- **The calendar wins.** Resolve disagreements; never leave both standing.
- **Propose, don't sneak.** Each downstream edit is a specific diff the instructor approves.

## Step 8 — Report

```
Session <NN>: <Title> — <Date>   (sprint S<NN>–S<MM> → M#, if applicable)
Written:  units/<unit>/<NN>-<slug>.md
Student docs: <exist / written / still needed — via course-student-docs>
Carried:  <from S<NN-1> retro, or "no retro — planned blind">
Outcome: <artifact · standard · due>
Steering: <n> checkpoints, <n> between classes

Sync pass:
  ✅ course-calendar.md — title + deliverable filled (applied)
  ⚠️  S<NN+1> assumes <X>; today doesn't produce it — needs a decision
  🔄 Slides — outline in plan section 2; deck not built

Open questions for you:
  - <what the vault doesn't answer>
```

Never invent course facts. If the vault doesn't say, write `⚠️ TBD` and ask.
