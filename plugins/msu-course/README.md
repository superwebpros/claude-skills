# MSU Course

Three linked skills for running MSU SSC 490-005 (*AI Workflows & Organizational Intelligence*) from a
markdown course vault. The course runs like a client project: teams deliver real artifacts to real
partners, and the instructor is the meta-PM.

| Skill | Does |
|-------|------|
| `lesson-planning` | Plans one session or a milestone sprint as a six-part outcome/steering plan, then runs a sync pass over the calendar, unit overview, adjacent plans, slides and course facts. |
| `lesson-retrospective` | Short post-class interview -> `units/<unit>/<NN>-retro.md`, then a downstream pass proposing concrete edits to the next plan, calendar and at-risk milestones. |
| `course-student-docs` | Writes the student-facing docs a plan links to: session docs, milestone/assignment docs, step examples, team templates, student skills; publishes to Google Drive when stable. |

The loop: **lesson-planning** writes the plan and links the docs **course-student-docs** writes;
after class **lesson-retrospective** records what happened, and its carry-forward items become
requirements for the next **lesson-planning** run.

## Setup

- `COURSE_ROOT` — path to the course vault (the folder with `course-calendar.md`, `units/`,
  `templates/`). Or run Claude from that folder.
- `SLIDES_DIR` (optional) — slide-deck markdown folder, checked during the sync pass.
- `PILOT_ROOT` (optional) — a previous offering's frozen record; read, never written.

The skills expect the vault layout described in
`skills/lesson-retrospective/references/course-layout.md`.

## Install

```bash
claude plugin marketplace add superwebpros/claude-skills
claude plugin install msu-course@superwebpros
```

Local dev: `claude --plugin-dir /path/to/msu-course`.
