# SSC 490-005 — course context

Orientation, not truth. Every fact here can move; `course-facts.md` and `course-calendar.md`
in the vault are authoritative and you read them at runtime. What this file gives you is the
*shape* of the course and the reasoning behind it, so you can tell a good plan from a plausible one.

---

## The course in one paragraph

SSC 490-005, *AI Workflows & Organizational Intelligence*, Michigan State, Fall 2026. A practitioner
instructor teaches; a co-instructor (instructor of record) is in the room. 3 credits, Pass/No Pass, Tue/Thu
80 minutes, 28 sessions, ~30 students in 8–10 teams. Students spend the first three weeks building
consumer-AI capability on a client they already understand completely — themselves — then spend
twelve weeks applying a method to a real business partner's internal process, ending in a working
prototype, training, and an honest ledger of what's unfinished.

Prior offering: SSC 493, Spring 2026. That's "the pilot," frozen in a sibling pilot folder (`$PILOT_ROOT`). Read it,
never edit it — its value is that it's the honest record of what broke.

## The five units

| Weeks | Unit | Question it answers | Milestone |
|-------|------|---------------------|-----------|
| 1–3 | Foundations & Career Project | Can I make consumer AI do real work? | M1 · S6 — Claude env + career-coaching Project (individual) |
| 4–7 | **I·M** Inventory & Map | What does this org know, and where does AI actually pay? | M2 · S14 — Inventory & Mapping assessment, one problem scoped and defended |
| 8–10 | **P·A** Process & Anchor | Can we do this by hand, twice, the same way? | M3 · S19 — Process maps |
| 11–13 | **C** Compose | Does it work? | M4 · S24 — Working automation in partner's hands |
| 14–15 | **T** Track & Handoff | Can someone else run it? | M5 · S27 — Training, handoff, debt ledger |

Milestones are summative. The load-bearing assessment is the **interstitial layer**: near-daily,
small, individual, scored on *completion not quality*. That layer exists solely so stuck students
surface in days rather than weeks.

## The two frameworks — and how to use them honestly

**AI Periodic Table** — what the technology *is*. Primitives (prompts, embeddings, language
models), compositions (retrieval, vector search, multi-modal, function calling, guardrails),
deployment (agents, skills, frameworks, small models), emerging (multi-agent, thinking models).

**IMPACT** — how you apply it to a real organization: **I**nventory · **M**ap · **P**rocess ·
**A**nchor · **C**ompose · **T**rack.

The syllabus is explicit: *"The periodic table is a map, not a checklist. You will not touch every
element on it, and you shouldn't try."* Naming all 13 elements as a coverage promise is the
specific thing that broke the Spring course. In a session plan, name only the elements that
session genuinely exercises, and say whether each is **introduced**, **deepened**, or **applied**.

## The stance

> **AI belongs inside a process, not independent of one. Build a process, get AI. The inverse
> isn't true.**

This is why Process & Anchor comes before Compose. Grounding is subordinate to the process it
serves. If a session plan has students automating before the process is written down and run by
hand twice, that's a real design problem — flag it rather than writing around it.

## The learning pattern

`Interactive → Agent → Automated`, applied per content type:

1. **Interactive** — students do the task by hand and feel where it's hard
2. **Agent** — students build an agent that does it, encoding expertise they may not have
3. **Automated** — the agent runs at production scale

The pattern repeats deliberately; recognizing it is part of the point. Every session plan should
be able to say where it sits. Diagram asset: `three-phase-arc.svg` in the pilot slide deck's `assets/`.

## The course runs like a client project

Teams work toward partner milestones (M1, M2, …) in sprints; the instructor is the meta-PM. Class time is
mostly team work time while he circulates; a short lecture block appears only when new concepts
arrive (e.g. APIs before the inventory sprint). *"Students learn when they work, not when I
yammer."* When he wants participation, a team demos where it is and where it's stuck —
call-and-response doesn't work in his room. Plans are steering documents, never teaching scripts
(see `writing-guide.md`). The concept-to-studio ratio tapers across the semester. Sessions pair across
the week — Tuesday introduces, Thursday builds — except weeks 9 and 13, which have a single
session and are used for consolidation, not new material.

## Scale, and why detection has to be systematic

19 students / 5 teams in the pilot → **30 students / 8–10 teams** in Fall. Roughly 1.6×. Past
about six teams you cannot see who isn't working by looking around the room. The pilot's worst
failure was exactly this: an n8n audit *after the fact* found students with zero execution
records. That's why every plan has steering checkpoints: an artifact, a time, and a trigger —
including checks between classes.

No TA, no grader. The co-instructor in the room is the only extra capacity.

## Infrastructure — the big Fall change

**New:** students hold their own **Claude.ai Team seats, Anthropic API keys, and OpenAI API
keys**. Direct Claude.ai + Skills + Connectors + MCP can absorb a lot of what the shared stack
carried in the pilot.

**Carried and still running:** LibreChat, n8n, Qdrant (per-team collections), Baserow.

⚠️ Genuinely open: which parts of the old stack are still load-bearing. Don't quietly assume a
session runs on LibreChat/n8n just because the pilot version did — check `course-facts.md`, and
if it's still open, say so in the plan rather than picking for the instructor.

## Business partners

Partners are listed in `course-facts.md` (typically three or four organizations). Multiple teams per partner —
delivery is a **prototype showcase** where a partner sees several attacks on their problem, not a
single handoff. Each team prototypes an automation for one of the partner's **internal
processes**. **These are prototypes, not production applications**, communicated up front.

**Scoping is instructor-led.** The instructor works with each team and partner to produce the SOW. Students
aren't expected to negotiate engagement boundaries in week 4. Never write a session that asks them to.

## Student-facing AI agents (carried, live, load-bearing)

- **Archie** — learning-recovery tutor with web search and context on past work. Companion to
  `carried-over/get-back-on-track.md`. The standard "if you get stuck" path in assignments.
- **Reggie** — individual reflection / pre-retrospective interview. Read Reggie transcripts before
  running a live retro.
- **Eve** — peer evaluation.

Delivered to students by QR code in slides.

## Assessment vocabulary

- **GWC** (EOS/Traction): **Get it** (understands, adds value) · **Want it** (engaged, on time,
  owns it) · **Capacity** (executes to standard, applies feedback). Ratings `+` / `+/-` / `-`.
- **Starfish** retrospectives: Keep Doing · More Of · Less Of · Start Doing · Stop Doing.
- Pass/No Pass. Peer eval via Eve, individual reflection via Reggie, partner evaluation at delivery.

## The pilot's failure modes — the checklist behind the required fields

| What broke | What it forces in every plan |
|---|---|
| Three contradicting plans ran at once; the syllabus described a course that stopped existing in Week 5 | The sync pass; `course-calendar.md` is authoritative |
| Students with zero workflow executions found only by a post-hoc audit | Steering checkpoints: artifact + time + trigger, including between classes |
| Most of Session 3 lost to an upload path that worked for the instructor and not for students | Instructor prep tests the **student** path, 24–48h ahead |
| A session lost assuming prior work that hadn't been done | Prerequisite Deliverables named concretely and checkably |
| "Post-Session Reflection" filled in for 4 of 23 sessions | Retros are separate small files, written after teaching, never pre-populated |
| Unit folders renamed mid-semester; files orphaned across two schemes | Session files carry the **global** number 01–28; units are folders |
| 13-element periodic-table completionism | Name only what a session touches |
| Partner delivery Apr 21 with classes ending Apr 22 — zero slack, sessions 24–28 evaporated | Fall parks M4 before Thanksgiving so partners test over the break |
| Six models compared in one lab was too many | Fewer, deeper reps beat coverage |

## Where things live

```
<course-root>/
  README.md            conventions and the three rules
  course-calendar.md   AUTHORITATIVE — dates, session numbers, units, milestones
  course-facts.md      enrollment, staffing, infra, partners, funding, open ⚠️ items
  course-arc.md        arc rationale and blocking questions
  Syllabus.md          student-facing; deliberately high level
  whiteboard.md        unresolved ideas, not decisions
  units/NN-unit/       Unit Overview.md · NN-slug.md (plan) · NN-session-doc-slug.md ·
                       M#-assignment-slug.md · M#-step-examples.md · NN-retro.md · evals/
  templates/           session-plan · assignment · retrospective · unit-overview · inventory/
  (Google Drive)       SSC490/Clients/<slug>/ team copies · SSC490/Resources/ masters + skill zips
  carried-over/        curated pilot assets + MANIFEST.md
  partners/  admin/  assets/
```

Slides live **outside** the vault, in a separate slides repo: source markdown at `$SLIDES_DIR`
(e.g. `<slides-repo>/ssc-490/markdown/`). Frozen pilot decks sit alongside it (`<slides-repo>/ssc-493/`).
The pilot's *slides* are a more accurate record of what was actually taught than its lesson plans —
sessions 21–23 exist only as decks.

Working rhythm, retained from the pilot: **full arc → units → weekly slide build → post-class retro.**
This skill owns the per-session step in the middle.
