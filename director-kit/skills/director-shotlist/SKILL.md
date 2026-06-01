---
name: director-shotlist
description: Turn a brief (and its locked assets) into a professional shot list plus a continuity ledger — stage 3 of the director-kit pipeline. Use after a brief/assets exist, or when someone says "make a shot list", "break this into shots", "plan the visuals", "storyboard this". Produces uninflected, sized, camera-moved shots that each map to one short clip, assigns the asset references per shot, and tracks 4-dimension continuity.
---

# Director Shot List — Stage 3

**brief + assets → shot list + continuity ledger.** Each shot is one short, generatable clip; each shot names the locked assets it uses; the ledger keeps story-state consistent.

Pipeline: director-brief → director-assets → **director-shotlist** → director-storyboard → director-animate

## Load
- `creatives/<slug>/brief.md` and `assets/registry.json` (the locked assets).
- `references/director-lexicon.md` — shot sizes, camera moves, lens/DoF, the **uninflected shot rule**.
- `references/montage-kuleshov.md` — order shots so the **cut** carries meaning.
- `references/continuity.md` — the ledger format + dramatic-object tracking.

## Two rules above all
1. **Uninflected** — describe only what's literally in frame ("hands frozen over keys", not "feeling stuck"). AI renders the literal words.
2. **One action per shot, short** — split compound actions; plan a *sequence of clips*, not one long generation.

## Build the shot list (editable source of truth)
Write `creatives/<slug>/shotlist.md` — one block per shot:
`SHOT # · Location/Time · Camera (size + move) · Action (uninflected) · Dialogue/VO · Assets used (registry ids) · Continuity note · Prompt`
- **Assets used** = which locked refs feed this shot (e.g. `liza, can-opener, bedroom`). This is what makes it stay on-model.
- **Vary size/angle** shot-to-shot (avoid a run of identical CUs — it sags and reads repetitive).
- Sanity: ~1.5–4s/clip; a 30s piece ≈ 8–15 shots.

## Maintain the continuity ledger
Alongside the shotlist, keep the per-shot state table (`continuity.md`): present elements, blocking/position, each **dramatic object's status** (planted→endangered→resolved), withheld items. Carry prior-shot state into the next shot's prompt (e.g. "STILL crouched at the bag" stops a teleport). Track all 4 dimensions: identity, prop, location, **period**.

## Finish
1. Run the **continuity critic** (`continuity.md`): flag blocking jumps, unmotivated presence/absence, unestablished objects of value, period anachronisms, repetitive framing. Fix on paper before generating.
2. Offer next: "Generate the storyboard and review it scene-by-scene? → **director-storyboard**."
