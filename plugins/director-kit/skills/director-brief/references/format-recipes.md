# Format Recipes — Short / Reel / Ad / Trailer

Purpose: the structural skeleton per format, fusing cinematic craft (the course) with short-form marketing mechanics (hook/retention/CTA). Every recipe is engineered against the known failure mode: **the hook lands but the middle sags (~50% drop, 25%→50% mark).** See `project-context.md`.

## Universal short-form spine (applies to all below)
1. **HOOK (0–3s)** — stop the thumb. Visual pattern-interrupt + a verbal/text promise. No logos, no slow build, no "hi guys."
2. **ESCALATE (every 3–5s)** — each beat raises a question or stake the previous one opened. This is the anti-sag rule: **never let a beat coast.** If a beat doesn't escalate, cut it.
3. **TURN (the pivot)** — the moment of insight/transformation/product reveal. In a 30s ad this lands around 50–60%, NOT the end.
4. **PAYOFF + CTA** — show the after-state, then ONE clear instruction.

> Anti-sag tactics (use at least one): start *in media res* (mid-action), front-load your best mid-video beat, hard-cut don't dissolve, kill any beat that only "sets up," use a Kuleshov pain→relief juxtaposition so the middle *implies* transformation instead of explaining it (`montage-kuleshov.md`).

---

## 1. Meta Sales Ad — 15–30s (PRIMARY format for FictionOS)
Goal: cheap thumb-stop → emotional resonance → click to GHL offer.

| Beat | Time | Job | Example (Writing Pain as Fiction) |
|---|---|---|---|
| Hook | 0–3s | Interrupt + name the tension | ECU hands frozen over blank doc; text: "You have a story. You just can't get it out." |
| Relate | 3–8s | Mirror their identity/pain | Writer at night, crumpled drafts; "It's not talent you're missing." |
| Turn | 8–16s | The reframe = the offer's promise | Pain→page juxtaposition; "Your pain *is* the material." |
| Proof/After | 16–24s | Show transformation/credibility | Finished manuscript, confident writer, aspirational |
| CTA | 24–30s | One action | "Learn the method. Link below." → GHL |

- **Variants are the point.** Produce 3–5 *angle-distinct* cuts (see angles in `project-context.md`), not re-skins.
- **Two lengths per angle:** a 30s and a tight **15–18s** (the analysis says tighter likely wins).
- Captions baked in; designed sound-off.

## 2. Reel / Short (organic, 15–45s)
Looser, more native, value-or-story-first. Same spine but the "CTA" is softer (follow / "full method in bio").
- Lead with a **story or contrarian claim** ("Stop trying to *invent* a story. Use the one that happened to you.").
- Retention trick: open a loop in the hook, close it only at the end.
- Can be talking-head + B-roll (AI-generated) or full AI narrative.

## 3. Book Trailer (30–60s)
For Allison's actual fiction titles (not the course). More cinematic, mood-driven.
- Built on `story-frameworks.md` logline + a montage (`montage-kuleshov.md`).
- Structure: **Atmosphere → Character in tension → Escalating glimpses → Title/▼ stakes question → cover + release/buy.**
- Tone over information. Withhold; don't summarize the plot.
- Still obeys hook-in-3s and no-sag — a trailer that drags is a trailer no one finishes.

## 4. Micro-ad / Spark variant (6–10s)
Single-idea, single-juxtaposition. One Kuleshov cut (pain shot → relief shot) + one line + CTA. Cheapest to produce, best for rapid A/B angle testing and re-engagement.

## 5. Interview / Stage-Q&A — 45–90s (talking-head, intercut)
Hormozi-style: an expert answers a question from an audience member. Great for authority + objection-handling.
- **Expert (the answerer)** = a talking-head with real lip-sync — render in an external avatar tool (e.g. **HeyGen**) from the answer lines.
- **Questioner (the asker)** = a **cutaway** — a locked character at a mic in the audience, **VO only** (TTS), with subtle Seedance motion. Profile/mic framing hides lip-sync, so no second avatar needed.
- **Structure:** Hook = the question (red caption) → the rule/reframe (answer) → stakes (questioner reacts) → promise → CTA. Intercut Q ↔ A.
- **Eyeline (critical):** asker and answerer face OPPOSITE screen directions so they read as facing each other (set with `ffmpeg hflip`; see `continuity.md`). Add a **split-screen two-shot** (both stacked) to establish the conversation.
- Captions/title card in post (Submagic).

---

## Choosing a format
- Testing a new **angle** cheaply → Micro-ad (#4) then scale winners to full Ad (#1).
- Core paid acquisition → Meta Sales Ad (#1).
- Organic / warming the audience → Reel (#2).
- Selling a **novel** (not the course) → Book Trailer (#3).

## Output discipline for every piece
- 9:16 vertical, captions baked, sound-off-safe.
- Shot list must map to *short generatable clips* (`tool-profiles.md`).
- Run the brief/shot list through the **Director's Intent Checklist** (`directors-eye.md`) before generating.
