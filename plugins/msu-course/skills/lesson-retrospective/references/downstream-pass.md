# The downstream pass

A retro that changes nothing was not worth writing. This is where a retro becomes an edit.

## The failure this exists to prevent

Spring 2026, Session 15 retro, written honestly and well:

> **Carry Forward to Next Session**
> - No pillars in Baserow yet — Session 16 needs to account for this (can't assume pillars are done)

Session 16 did not account for it. The retro correctly identified the problem, named the affected
session, and stated the required change — and the change never reached the file. The insight sat
in a document nobody reopened at planning time.

Notice the shape of the failure: it isn't that the instructor lacked the insight. He *wrote it down*. The
gap is purely between "recorded in a retro" and "edited into the plan." That gap is a mechanical
one, and closing it is mechanical work — which is exactly the work you should be doing for him.

So: **the deliverable of this step is proposed edits to specific files, not observations.**
"Session 9's prerequisites may need review" is a restatement. "Session 9's Prerequisite
Deliverables says 'working GET request in n8n' — four teams don't have one; propose changing it to
X and adding a 10-min recovery block" is an edit.

## Work through these

Not all will apply. Most retros produce two or three real edits. Say so plainly when a retro
implies nothing downstream — a clean session that needs no changes is a legitimate and common
outcome, and manufacturing edits to look thorough trains him to ignore the list.

### 1. The next session's plan

The highest-yield check, because it's the one that breaks soonest.

Open the next session's plan and read its **Prerequisite Deliverables** and **Pre-Class Work**
sections against what the retro says students actually finished. The template says to name
prerequisites concretely ("pillars in Baserow") *because the pilot lost a session assuming work
that wasn't done* — so the mismatch is usually visible in one read.

Ask:
- Does every prerequisite still hold? If students didn't finish something, **the next plan is now
  factually wrong**, not merely optimistic.
- Does today's overrun mean content has to move into the next session? What gets cut to make room?
- If a block got skipped today, does the next session reference it as known?
- If today pivoted to a different tool or path, does the next plan still name the old one?

Propose the concrete edit: which section, what text changes, what gets cut to pay for added time.

### 2. `course-calendar.md`

Authoritative for dates and session numbering. It's referenced everywhere and restated nowhere, so
it's the highest-leverage single file to keep true.

- Did a deliverable slip? The calendar's Session Grid and Milestones table both carry due points.
- Is a session title now wrong because the session became something else? (Many Fall session titles
  are still blank — filling one in from what actually got taught is a real improvement.)
- Did a partner day move? S7 is already flagged as possibly shifting.

**Dates and session numbers are confirmed and do not move.** What moves is *content and
deliverables between fixed slots*. Never propose changing a date; propose changing what's in it.

### 3. The `Unit Overview.md`

Slower-moving, so check it but expect fewer hits.

- Do the unit's stated deliverables still match what teams will actually produce?
- Did a Key Learning Objective not land, or land somewhere other than planned?
- Does "How We Know This Unit Landed" still describe something observable?

### 4. Later sessions — the cascade

A slipped prerequisite rarely stops at the next session. If teams didn't finish the inventory in
S13, then S14's assessment, S15's process maps, and the M2 defense are all built on it.

Trace the chain forward until you hit a session that doesn't depend on the slipped thing, and name
every session you'd touch. It's fine — often better — to conclude "this only costs S9 ten minutes
and recovers." But say that explicitly, so the cascade was *checked* rather than *assumed absent*.

### 5. Milestones — say it plainly

M1–M5 in `course-calendar.md` are the summative spine and go to partners.

If today's session puts one at risk, say so in one direct sentence with the mechanism:

> **M2 (S14, Oct 15) is at risk.** Two of nine teams have no data-source connections after S8; the
> inventory assessment assumes connections exist by S11.

Don't hedge this into invisibility. An at-risk milestone is the single most valuable output the
downstream pass can produce, and the pilot's lesson is that delivery slack disappears silently —
it delivered Apr 21 with classes ending Apr 22, and Sessions 24–28 evaporated.

Also flag the inverse when it's true: a session that ran ahead buys slack somewhere, and knowing
where is useful.

### 6. Off-track students — the clock item

The retro records who and by when. The downstream question is what changes because of it:

- Does the next session need a recovery block, or a pairing plan for the teams that are behind?
- Is `carried-over/get-back-on-track.md` (the Archie companion doc) the right referral, and does it
  cover what these particular students are missing?
- Do the Steering checkpoints in the *next* plan need to change, because today proved the
  current artifact doesn't surface the problem? The pilot's finding was that real-time spot checks
  weren't sufficient — the audit was.

### 7. Future-cohort insights — don't strand them

Some insights apply to next semester, not this one: "six models was too many," "always test the
student upload path 48h ahead," "LibreChat-first is pedagogically better than Custom GPTs."

These are the most durable thing a retro produces and the easiest to lose, because nobody rereads
session 2's retro while planning next August. The pilot's rework banners in the Fall lesson plans
exist precisely because someone had to go mine them back out by hand.

Leave them in the retro *and* propose a durable home. Ask the instructor where he wants them rather than
inventing a file — `whiteboard.md` holds unresolved ideas, and the affected lesson plan can carry
a `> [!tip] For Next Time` callout that will be read at the moment it's relevant. Adding a note to
the *plan* is usually better than a note in the retro, because the plan is what gets reopened.

## How to present it

A short list. File path, what's wrong, proposed change. Group by file, order by urgency (anything
with a date first). Then one question.

```
Downstream from the S8 retro:

1. units/01-inventory-and-map/09-*.md — Prerequisite Deliverables says "working GET
   request in n8n." Four teams don't have one. Propose: soften to "n8n account access"
   and open with a 10-min recovery block, cutting the warm-up demo to pay for it.

2. course-calendar.md — S8 notes column is empty; add "API block ran 25 min over,
   POST/PUT moved to S9."

3. M2 (S14, Oct 15) — not at risk yet, but if the same four teams are still stuck
   after S9 it will be. Worth a check Thursday.

4. Future cohort — "test the student n8n path, not the instructor path, 48h ahead."
   Want that as a [!tip] on the S8 plan, or in whiteboard.md?

Want me to make 1 and 2?
```

Then wait. **Do not make these edits silently.** Several are the instructor's judgment calls about scope,
pacing, and what he's promised a partner — items 1 and 3 above especially. Presenting them as a
list he approves is not a formality; it's the step where his knowledge of the room corrects your
inference from the files.

When he approves, make the edits, and keep them minimal and surgical — change the sentence that's
wrong, don't rewrite the section around it. Then note what you changed in the retro's
**Downstream edits needed** line at the bottom of the template, so the record shows the loop
actually closed.
