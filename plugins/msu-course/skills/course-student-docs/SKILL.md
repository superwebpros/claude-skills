---
name: course-student-docs
description: "Write or revise student-facing documents for MSU SSC 490-005: session docs (setup and every link for a class day or sprint), milestone/assignment docs (the process teams follow to an M# deliverable), step examples ('what done looks like' at each step, from real class projects), team templates, and student-facing Claude skills - and publish them to Google Drive once stable. Use when asked for a session doc, class doc, student doc, assignment, milestone doc (M1, M2...), handout, examples, glossary, cheat sheet, team template, or a skill students will install; when revising one from instructor review notes (jf-note blocks); or when publishing course docs to Drive. The instructor-facing session plan is the lesson-planning skill; this skill writes the docs that plan links to."
---

# Course Student Docs — SSC 490-005

> **Setup.** Part of the `msu-course` plugin with its siblings `lesson-planning` and
> `lesson-retrospective` (invoked as `/msu-course:<skill>` when installed as a plugin). Paths below are
> relative to the course repo root: set `COURSE_ROOT` to it or run from it.

Students are running a client project for a real partner. Their docs give them **the process, the
links, the vocabulary, and examples of "done"** — then get out of the way. Everything here comes from
the instructor's review of the M2 inventory docs (2026-10-05/06).

**Read the approved references first** (`<course-root>/units/01-inventory-and-map/`):
`11-session-doc-inventory.md` (session doc) · `M2-assignment-inventory-design-doc.md` (milestone doc)
· `M2-step-examples.md` (step examples). Shapes: `templates/assignment-template.md`,
`templates/inventory/*`. Read the instructor plan that links the doc — its Outcome table is the
standard the doc must teach to.

## The three doc types

**Session doc** — `units/<unit>/<NN>-session-doc-<slug>.md`. Setup and links for a class day or sprint.
- Dates table (every due date and partner send through the milestone).
- Step 0: confirm setup that should already be done ("you can see your team's connector"), with
  what to do if it isn't.
- Numbered steps with who does each (team / PM / everyone) and rough time.
- Per-team table with that team's links (connector, upload folder, project folder).
- **Every link inline.** Never "see Discord." Placeholders like `M2_URL` until publishing fills them.
- Points to the milestone doc for the *how*; doesn't repeat it.

**Milestone / assignment doc** — `units/<unit>/M#-assignment-<slug>.md`, from the assignment template.
- What this is: what the deliverable lets us do next, in a short numbered list. Uncertainty is
  expected; say where unsure items go.
- **Guardrails on the thinking students skip** — especially *sources* (systems of record vs systems
  of knowledge; say where you learned it) and *data types*. Defined in small tables, not warnings.
- Working with AI: find the docs yourself → give Claude the relevant pages → make it cite → open
  every citation and check. Tool limits stated plainly.
- What you hand in · Who does what · The process (each step: Who / Do / Record / Done when /
  Example link) · Glossary · Cheat sheet · Guardrails block for the team Claude Project · How it's
  evaluated (matches the plan's Outcome table).

**Step examples** — `units/<unit>/M#-step-examples.md`. One short example per step, 2–4 rows.
- **A different real class project for each step**, so no team gets its own work done for it.
- Real citations (recording + chunk, docs page), honest ❓ and ⚠️ marks — a finished step still has blanks.
- A one-line italic caption saying what the example demonstrates, and a **Not this:** counter-example
  where a common mistake exists.
- Draw facts from the vault (`partners/`, transcripts, team work); never invent partner facts.

## Writing rules

1. **Abstract enough for every project.** "NOT A HANDHELD SCRIPT; EVERY PROJECT IS DIFFERENT." Steps
   say what to find out and record, not which buttons to click for one team.
2. **Organize around real use cases.** Requirements in the partner's terms ("Staff can update a
   donor's mailing address") → can the system do it? Yes / No / Maybe, with a docs link or reason.
   Scope research to the capability the project needs, not "what can the API do."
3. **Glossary for every technical term** (API, API key, OAuth, endpoint, MCP, connector, entity, data
   type…). Explain on first use too. Assume students don't know them.
4. **Use the instructor's terms; coin none.** No "System Card," no "can it PUT?" If a name is needed and he
   hasn't chosen one, use a plain description and ask him.
5. **Disambiguate overloaded words.** *Client owner* (person at the partner who uses or maintains a
   system) vs *assigned to* (teammate doing the research). Never bare "owner."
6. **No hyperbole, drama or cheek.** Struck examples: "they matter more than anything else here,"
   "Get this wrong… in front of your partner," "Claude said so are not sources" (cheeky).
7. **Every sentence communicates something the student acts on.** the instructor's "what? I don't get what
   this means" notes hit: "You'll loop: research turns up new systems…," "Every question says what
   changes depending on the answer," "Not graded on polish; graded on whether it's real." Cut lines
   like these.
8. **Proposed systems count.** Teams often recommend tools the partner doesn't have; the process
   records them, labeled Proposed — don't tell students to exclude them.
9. **Partner-facing correspondence is de-risked.** The PM sends everything; the instructor reviews first;
   drafted with a partner-correspondence skill if you have one; every teammate must be able to explain every
   sentence. Partner deliverables get a plain-language explanation, and a review call (Zoom, real
   back-and-forth) beats a recorded walkthrough.
10. **AI guardrails live in the team Claude Project's instructions**, not pasted per chat.
11. **Writes go through Claude** (the instructor, 2026-10-29). With the Google Sheets / Docs connectors and Excalidraw, Claude writes to the team's systems of record (Inventory Sheet), systems of knowledge (Journal, design doc) and artifacts (canvases). Docs tell students to make changes through Claude and have it keep everything in sync; the team decides first and checks what Claude wrote (Claude-drafted → team-confirmed). Paste-ready rows are only the fallback when a connector isn't on.
12. **Scaffold the formatting, not the thinking.** Give teams pre-made templates (journal with an
    Index, Sheet with tabs) so their time goes to the research. Tasks via Google Docs `@`-assign
    (only works for people the doc is shared with — say so).

## Student-facing Claude skills

Skills students install (zips) must **coach**: define each term as it comes up, say what it's doing
and why, and stop at a few key points to ask the student ("why do you think X?") before continuing —
not so often it derails the work or invites mistakes. They enforce the guardrails (sources cited,
unknowns marked) and return paste-ready rows rather than writing to Drive.

## Workflow and publishing

- **Vault markdown is the source of truth.** Draft in the vault; the instructor comments inline with
  ` ```jf-note ``` ` blocks. Before revising, copy the annotated file to the scratchpad as
  `<name>.vN-with-jf-notes.md`; address every note; leave none in the live file; bump `status:` in
  frontmatter.
- **Publish to Google Drive once, when the instructor says it's stable** — not after every draft. Use the
  `google-workspace` skill (or the Google Drive/Docs connectors). Folder IDs: `partners/drive-folder-map.md`.
  - **Team templates** (Project Journal, Inventory Sheet, design doc…) → a copy in each team's client
    folder `MSU/SSC490/Clients/<slug>/`, named `<project> — <Doc name>`. Folder-level sharing; an
    auditable trail per client. Students work in those copies, never their own.
  - **Masters and skill zips** → `MSU/SSC490/Resources/`.
  - **Reference material** (glossary, cheat sheets) → append to the instructor's class journal Google Doc
    (the multi-tab doc linked in `partners/README.md`) rather than creating new docs.
- After publishing, replace placeholders (`M2_URL`, `EXAMPLES_URL`) in the vault with real links,
  and set sharing to what the instructor specifies.

## Checklist before handing to the instructor

- [ ] Matches the plan's Outcome table and dates
- [ ] Process steps fit every team's project; each step has Who / Do / Done when / example
- [ ] Sources and data types guarded; glossary covers every technical term; cheat sheet present
- [ ] Examples: one per step, a different real project each, real citations, honest ❓/⚠️
- [ ] Every link inline (or a named placeholder); nothing says "see Discord"
- [ ] Client owner vs assigned to kept separate; no coined names; no jargon shorthand
- [ ] No hyperbole, drama, cheek, or sentences that don't tell the student something
- [ ] Partner-facing steps: PM sends, the instructor reviews first
- [ ] Not published to Drive unless the instructor said it's final
