# Script formatting: the authoring contract

Snapshot of `docs/script-formatting.md` from the private `superwebpros/heygen-production`
repo. That file (and the code it mirrors, `heygen_production/script.py`) is authoritative;
if this copy disagrees, the repo wins.

A file that satisfies this contract renders correctly. A file that violates it is
**rejected by `heygen-render` before any credit is spent.**

## 1. Canonical document shape

```markdown
---
format: reel | ad | lesson | vsl
...other frontmatter
---

# <Title>

**[VISUAL NOTES: … ]**          ← optional; MUST sit outside the VO sections

**HOOK:**
<voiceover>

**BODY:**
<voiceover, MAY contain [audio tags]>

**CTA:**
<voiceover>

<!-- END VO -->                 ← explicit VO terminator; REQUIRED for new authoring

---
# Mixpost Data                  ← publication metadata; never spoken
**Platform:** [instagram, linkedin]
**Caption:** …
#Hashtags
```

## 2. Rules R1–R7

**R1. The voiceover is HOOK + BODY + CTA, in that order, joined by a single space.**
Nothing else is spoken. An empty voiceover, or a missing section, is a blocking error.

**R2. A section begins at a line-initial `**LABEL:**`, optionally qualified.**
`**HOOK (0:00 - 0:05):**` and `**BODY / MECHANISM:**` are accepted; the qualifier may not
contain `*` or a newline. New authoring SHOULD use the bare form.

```markdown
✅  **HOOK:**
✅  **HOOK (0:00 - 0:05):**
❌      **HOOK:**                (indented, not line-initial)
❌  **HOOK**                     (no colon inside the emphasis)
❌  **HOOK *beat*:**             (asterisk inside the qualifier)
```

**R3. A section ends at the first of five stops:** the next `**HOOK|BODY|CTA:**` label,
`<!-- END VO -->`, an ATX heading (`^#{1,6}\s`), a thematic break (`^---\s*$`), or EOF.
(An older parser ended CTA at end-of-file, so everything after it was read aloud.)

**R4. Bracketed spans inside VO text MUST be audio tags** from the vocabulary below.
`eleven_v3` treats any bracketed span as a performance directive; an unknown one lands as
noise. `[instagram, linkedin]` or `[excited]` inside a VO section is a blocking error.

**R5. VO text MUST NOT contain `#`, `**`, `---`, markdown links, or list markers.** They
are read aloud (`#SomeBrand` becomes "hashtag some brand"). Carry emphasis with audio tags
and sentence construction.

**R6. Visual notes, on-screen text, and publication metadata sit outside the VO sections**:
before `**HOOK:**` or after `<!-- END VO -->`.

**R7. New authoring SHOULD emit `<!-- END VO -->`** on its own line after the CTA, so the
boundary does not depend on how the metadata block happens to be formatted.

## 3. Audio-tag vocabulary

Lowercase, one word, in square brackets, at the start of the sentence or clause they govern.

| Tag | Use it when |
|---|---|
| `[thoughtful]` | Opening an explanation or reframing a common assumption. |
| `[serious]` | Naming the stakes, the risk, or the hard lesson. |
| `[reassuring]` | Right after the stakes: "this is solvable". |
| `[confident]` | Delivering the fix, recommendation, or prescription. |
| `[curious]` | Posing the question the piece answers, or inviting the viewer to check their own situation. |

Anything else in brackets is a blocking error.

Tags are **not spoken** on the OAuth CLI path: `heygen-render` sends
`voice_settings.engine_settings` with `engine_type: elevenlabs` and `model: eleven_v3`.
The HeyGen MCP tools cannot express `engine_settings`, so on that path tags *are* spoken,
which is why MCP is not used for final renders.

House default is `stability: 1.0` (established by A/B testing; low stability reads as
hesitant). Under `eleven_v3` stability must be `0`, `0.5`, or `1.0`; the renderer snaps to
the nearest. Earlier guidance that `stability: 0` is most tag-responsive is retracted.

## 4. Runtime budget

Estimated at **145 wpm**.

| `format` | Budget | ≈ words |
|---|---|---|
| `reel` | 30–60s | 73–145 |
| `ad` | 15–60s | 36–145 |
| `lesson` | 60–900s | 145–2175 |
| `vsl` | 180–1800s | 435–4350 |

Over budget warns by default and blocks only under `--strict`. An undeclared or
unrecognised `format` skips the budget check entirely, so declare one.

## 5. Checklist for script-authoring skills

1. Emit bare labels `**HOOK:**`, `**BODY:**`, `**CTA:**`, line-initial, all three, in order.
2. Emit `<!-- END VO -->` after the CTA and before any publication metadata.
3. Keep `[VISUAL NOTES: …]`, on-screen text, and the metadata block outside VO sections.
4. Keep markdown out of spoken text: no `#`, no `**`, no `---`, no links, no list markers.
5. Only use tags from the vocabulary; never put platform names, timestamps, or metadata in
   brackets inside a VO section.
6. Declare `format:` in the frontmatter and write to its budget.
7. Verify with `heygen-render <script.md> --dry-run` and read the VO text it prints.
