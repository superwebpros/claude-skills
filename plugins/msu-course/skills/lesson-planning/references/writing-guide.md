# Writing guide — the six-part plan

Calibrated against the instructor's review of the S11 inventory sprint plan (2026-10-05/06). Three drafts were
rejected; v4 (`units/01-inventory-and-map/11-inventory-sprint.md`) is the approved shape. Where a more
recent plan the instructor approved differs from this file, the plan wins.

---

## What a plan is for

A plan is a **steering document for a client project**, read by the instructor. It answers: what teams produce,
by when, how it's tracked, who on each team does what, and where the instructor looks to steer. It is not a
teaching script. The instructor decides how to teach; his in-class time appears as a block ("go through each
team's SOW with them"), never as lines to say.

Class time is mostly **work time**. The instructor circulates as meta-PM. The plan gives him guardrails that
direct teams' effort while he does that.

## The six parts, in order

### 1 · Outcome

- **The artifact(s)** each team hands over, and to whom (the instructor, the partner, D2L).
- **The standard**, as a table: part → what "done" means, checkable by looking at the artifact.
- **The due date**, plus any follow-on (e.g. a partner review call right after the milestone).
- **Along the way**: a dated table of steps from today to the milestone, including partner sends.

If several artifacts make up the deliverable, say they are all the deliverable ("they're both the
deliverable"). A machine-readable artifact needs a plain-language companion for the partner, who
otherwise won't know what they're looking at.

### 2 · Roadmap (deck outline)

- The process steps, numbered, one line each. This list is what goes on the deck.
- If the instructor presents, a **lecture outline**: topics only, plus a "Vocabulary to define on slides" line
  naming every technical term students will meet.
- **None of your prose goes on slides** — no framing lines, quotes or explanations. Outline only.

Organize the process around **real use cases** (requirements in the partner's terms → can the system
do it? Yes / No / Maybe), not entity-first modeling. Use cases are easier for students to research and
for partners to confirm. Proposed systems belong in the process too — teams often recommend tools the
partner doesn't have yet; label them Proposed rather than excluding them.

### 3 · Tracking

Table: **What | Where | Who updates.** Every tracked thing (research agenda, inventory rows, team
assignments, partner log, index of links, drafts) has exactly one home.

Disambiguate overloaded words here. The canonical case: **client owner** (the person at the partner
who uses or maintains a system — matters to the client) vs **assigned to** (the teammate researching
it — internal). Never write bare "owner."

Name tool constraints that shape the workflow, e.g. *Claude can't write to Google Sheets/Docs through
the Drive connector, so skills return paste-ready rows in the Sheet's exact columns.*

### 4 · Team operating model

- **Project manager**: what the PM drives (team working session, assigning work, keeping the Project
  Journal, sending everything partner-facing after the instructor's review).
- **Division of work**: what's done together vs split, and the unit of assignment (e.g. one system per
  teammate, end to end). Whatever must exist before work can split (e.g. the full systems list) is done
  as a team first.
- **Tasks and due dates**: where they live (e.g. `@`-assigned tasks in the team's Project Journal).
- **Team AI setup**: a team Claude Project with the guardrails in its instructions, and which skills
  to install.

### 5 · Steering checkpoints

Table: **When | I look at | I step in if.** One row per class day and per between-class check, through
the milestone and after it.

- "I look at" names an artifact (a tab, a Journal section, a draft before it's sent), not an impression.
- "I step in if" names observable triggers ("systems with no client owner," "requirements still
  Unknown with no task," "jargon in partner questions").
- At least one **between-class** check.
- Individual submissions (labs): due when, and what happens to missing ones.
- Per-team detail goes in a linked team guide that surfaces each team's underlying assumptions and
  what it must deliver — not questions for the instructor to ask.

### 6 · Student docs

Links to every student-facing doc: session doc (setup and every link), milestone/assignment doc (the
process), step examples, templates, student skills. Flag any that don't exist yet. These are written
with the **course-student-docs** skill.

### After the six parts

- **Frameworks** — one line, only what the session touches: IMPACT stage; AI Periodic Table elements
  introduced / deepened / applied. Never promise coverage.
- **Partner milestone** table — to partner, partner interaction, partner prep. Even "none."
- **Prep** — test the exact student path 24–48h out; publish student docs; deck outline; record.
- **Retrospective** — `[[NN-retro]]`, empty.

Open decisions for the instructor go in a `> [!question] Open — <topic> (instructor)` callout with a decision date
and bead ID. His own action items are beads assigned to him.

## Voice

Instructor-facing, direct, short declaratives, tables over paragraphs. The approved S11 plan covers a
two-week sprint in ~150 lines. Length comes from content, not narration.

- **Plain words over shorthand.** "Can a machine change an existing record?" not "can it PUT?"
- **No coined names.** Use the instructor's terms (research agenda, Inventory Sheet, design doc, Project
  Journal, client owner). Don't invent artifact names — "System Card" confused him.
- **No drama, hyperbole or cheek.** "Get this wrong and the build is wrong… in front of your partner"
  was rejected as dramatic; "That's on me" was struck.
- **Every sentence tells the reader something they act on.** If the instructor would write "what?" next to it,
  cut it. Rejected: *"You'll loop: research turns up new systems… That's expected,"* *"Every question
  says what changes depending on the answer,"* *"What did that table let you skip?"*

## Rejected patterns

| Pattern | Why |
|---|---|
| Quoted lines for the instructor to say | He decides how to teach |
| "Ask the room" / call-and-response | "Very few people respond, and it's usually the same people." For participation: a team demos where they are and where they're stuck |
| Circulating-question lists | "So prescriptive they miss the forest for the trees" — he needs how the project is steered |
| Minute-by-minute blocks with Purpose / Talking points / Watch for | Replaced by Outcome → Roadmap → Steering |
| Prose or framing lines for slides | "ABSOLUTELY NONE of your prose should make it into the deck" |
| "See Discord" / links scattered across posts | Every link lives in the student session doc |
| Team guides made of questions to ask | Surface assumptions and what each team must deliver |
| Bare "owner" | Client owner vs assigned to |

Scan before reporting — this must return nothing:

```bash
grep -nE '^> *"|[Aa]sk the room|[Cc]irculating|Talking points|Watch for|\([0-9]+ min\)' <plan>
```

## What still holds from the pilot

- `course-calendar.md` is authoritative; reference it rather than restating it.
- Test the student path, not the instructor path, 24–48h ahead.
- Never pre-fill the retrospective.
- Never invent partner names, tools, dates or rosters — `⚠️ TBD` and ask.
- Automation before process contradicts the course stance; flag it.
- Students hold their own Claude.ai Team seats; don't assume LibreChat/n8n because the pilot used them.
