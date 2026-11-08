# The sync pass

Run this every time a session plan is written or reworked, before you report back.

## Why it exists

The Spring pilot ran **three contradicting plans at once** — the original syllabus, an archived
11-unit plan, and a revised weeks-8-14 plan. None was marked authoritative, and the syllabus was
never updated, so it described a course that had stopped existing in Week 5. Nobody set out to do
that. It happened one un-reconciled session plan at a time.

A session plan is a claim about the course. The moment you write it, other documents may be
lying. Finding out costs five minutes now and a lost class later.

## Two standing rules

**1. `course-calendar.md` is authoritative.** Dates and session numbers are confirmed against the
registrar and do not move. Titles, deliverables and notes are fillable. When the plan and the
calendar disagree, resolve it in one direction or the other — never leave both standing and never
let the plan silently win.

**2. Propose, don't sneak.** Every downstream edit is presented as a specific diff and applied
only after the instructor says yes. He is the one holding the arc in his head; an edit he didn't see is an
edit he can't reconcile. The exception is trivially mechanical and unambiguous (filling an empty
title cell with the title he just approved) — do it, and say you did.

## The checklist

### 1. `course-calendar.md` — the session grid row

Check the row for this session, and the rows around it:

- **Session title** — empty for most sessions past S7. Fill it with the plan's title. Keep it
  short enough for the grid; the plan's H1 can be longer.
- **Unit** — does the session's content actually serve the unit it's filed under? If not, that's
  a real conversation, not a quiet edit. Global session numbering means moving a session between
  units is a `mv`, so it's cheap — but it changes the unit's arc.
- **Notes column** — milestone due (`**M# due**`), partner touchpoint, Zoom/away days, guest
  lecturers, single-session-week flags. If the plan introduces a partner interaction or a
  deliverable to the partner, the calendar should say so.
- **Milestone reality check** — if the session is 1–2 sessions before an `M#`, does the plan
  actually get teams to that milestone? If M2 is due S14 and S13's plan still has teams
  inventorying, flag it. Milestone slippage is visible here and nowhere else.

### 2. `units/<NN-unit>/Unit Overview.md`

- **Sessions table** — is this session listed, with the right title and date?
- **Key Learning Objectives** — do the session's objectives roll up into at least one unit
  objective? If the session teaches something the unit never promised, either add the unit
  objective or reconsider the session.
- **Unit Outcome** — many Fall unit overviews are still `<!-- comment -->` stubs. If you now have
  enough from two or three planned sessions to draft the outcome and objectives, offer it. This
  is the highest-leverage byproduct of session planning.
- **How We Know This Unit Landed** — does the session's deliverable belong in that list?
- **Partner Touchpoints** — add this session's, if any.

### 3. Previous session's plan and student docs — what was promised

The previous plan's Outcome / "Along the way" table and its student session doc told teams what
comes next and when. Does today's plan deliver that, on those dates? If not, the student doc is now
wrong for thirty people. Update it (or flag that the published Google Doc needs updating).

Also update the previous plan's link to this session if the title changed.

### 4. Next session's plan — assumed inputs

Read the next session's Outcome, "Along the way" dates and Steering checkpoints. Whatever it expects
to look at — a tab filled in, a draft sent, a PM named — does today actually produce it?

This is where the pilot lost a whole session. The two failure shapes:

- **Gap** — next session assumes X; today doesn't produce X. Either add it to today's dated steps
  or tell the instructor the next plan needs to change.
- **Orphan** — today produces a deliverable nothing downstream consumes. Either it's genuinely
  terminal, or the arc has a hole.

Also update the next session's link back to this one if today's output changed shape.

### 5. `Syllabus.md`

Rare, and deliberately so — it's high level and explicitly does not restate the calendar. Only
touch it when a plan changes something the syllabus actually promises students:

- the milestone list or their due sessions
- pass requirements or the deliverable count
- the technology list (a new required tool or account, e.g. an API key students must fund)
- pre-class expectations, attendance, or late-work implications

If a session requires students to spend money or create an outside account, that is a syllabus
matter and an instructor decision. Raise it explicitly.

### 6. Slides — `$SLIDES_DIR` (e.g. `<slides-repo>/ssc-490/markdown/`)

Not part of the vault; a separate, separately published slides repo.
Slide building is its own step in the instructor's rhythm (**full arc → units → weekly slide build →
post-class retro**), so **flag, don't build** — unless he asks.

Check for `session-<NN>-<slug>.md`:

- **No deck** → `🔄 Slides — needs building: session-<NN>-<slug>.md`
- **Deck exists, matches** → `✅ Slides — deck exists and matches the plan`
- **Deck exists but is the pilot's** (`ssc-490/markdown/` currently holds copies of the Spring
  decks under pilot titles) → say so plainly: the deck at that number teaches a different session.
- **Deck exists and the plan changed** → name what's now stale: exercise count, model roster,
  tool names, the QR codes, the milestone slide.

Also note any asset the plan calls for that doesn't exist in `ssc-490/assets/`.

### 7. `course-facts.md` — open items

If planning resolved an ⚠️ item (the model roster, the submission mechanism, a team count), say so
and offer to update `course-facts.md`. If planning *created* a new open item — a tool that must be
verified, an account that must exist, a partner confirmation needed — offer to add it to the Open
Items list. That list is the course's actual to-do list.

## Reporting the pass

Report every line, including the clean ones. "No change needed" is information — it means the pass
ran.

```
Sync pass:
  ✅ course-calendar.md — S10 title "Data Source Inventory Workshop" + deliverable filled (applied)
  ⚠️  Unit 1 Overview — Unit Outcome is still a stub; I can draft it from S7–S10, want that?
  ⚠️  S9 preview promises "we'll connect the CRM" — S10 doesn't. Change the preview or the plan?
  ✅ S11 prerequisites — satisfied by today's post-class deliverable
  ✅ Syllabus — no change needed
  🔄 Slides — no deck; session-10-data-source-inventory.md needs building
  ⚠️  course-facts.md — S10 depends on the ⚠️ n8n multi-tenant scoping item, still unconfirmed
```

Then stop and let the instructor answer the ⚠️ lines before applying anything he hasn't approved.
