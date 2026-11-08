# Annotating the lesson plan

Optional, and only when the instructor says yes. The retro file is the primary record; this makes the
*plan* honest too, so that when someone reopens it next August it doesn't describe a class that
never happened.

**These conventions are the instructor's, documented in the course vault's `CLAUDE.md` (or README) under "Post-Session
Reflection Workflow." Preserve them precisely** — same four markers, same meanings. He reads these
markers fluently; inventing new ones costs him that fluency for no gain.

## The four markers

### `~~strikethrough~~` — planned but not done

Strike the activity, leave it visible. Deleting it loses the information that it was intended;
striking it records the intent *and* the outcome. Where the reason is short, append it.

```markdown
- ~~Generate 30 pillar topics via conversation (10 min)~~ — no team reached this; the MCP build took the full block
~~### 3. Temperature Parameter Exercise (8 min)~~
```

### `> [!note] What Actually Happened` — done differently

For pivots and substitutions. Say what was planned, what replaced it, and whether it was better —
the judgment is the part that's useful later.

```markdown
> [!note] What Actually Happened
> Did NOT start with parallel mode. Had students test models one at a time first to build the
> habit of observing individual differences, THEN showed parallel. This worked better — they
> appreciated the efficiency after experiencing the tedious version.
```

### `> [!warning] Timing Issue` — overruns and things that went wrong

Real numbers. "Ran long" is not reusable; "needed 20–25, had 15" rebuilds the plan.

```markdown
> [!warning] Timing Issue
> The 5 min for Baserow table creation and 15 min for the MCP build were too tight. Teams needed
> closer to 10 and 20–25 including troubleshooting. Allocate 35+ min for infrastructure and treat
> topic generation as homework.
```

Also correct for tech failures and access problems, which is where the pilot's worst surprises
lived.

### `> [!tip] For Next Time` — future-cohort insights

Explicitly aimed at whoever plans this session next year, including the instructor. Place it next to the
block it's about, not at the bottom — proximity is what gets it read at the moment it matters.

```markdown
> [!tip] For Next Time
> Reduce to 3–4 models (Frontier / Balanced / Fast), or extend hands-on to 50 min. Students
> reading outputs carefully is GOOD — don't rush them.
```

## Where annotations go

**Inline, next to the block they describe.** A callout attached to "Activity 2" is found by
someone reading Activity 2. The same text in a reflection section at the bottom is found by
nobody — which is the pilot's actual, documented failure: the long embedded reflection section
was filled in for 4 of 23 sessions and, when filled in, sat below everything anyone re-read.

Don't recreate a "Post-Session Reflection" section in the Fall plans. That structure was
deliberately removed — retros are separate files now. Annotations are inline markers only.

## Scope

Light touch. Annotate what actually diverged; leave accurate blocks untouched. A plan with three
strikethroughs and two callouts is more useful than one rewritten to match reality, because the
divergence is the information — a silently corrected plan looks like it went perfectly.

Never annotate something the instructor didn't tell you. Same ground rule as the retro: you weren't there.

## Frontmatter

If the plan carries `status: 🔄`, offer to flip it to ✅ — it's been taught. Ask; a session he
considers half-done shouldn't be marked complete on your initiative.
