---
name: director-assets
description: Lock the reusable cast, props, locations, and world/period for a video creative — stage 2 of the director-kit pipeline. Use after a brief exists, or when someone says "lock the characters", "build the cast", "create the characters/props/sets", "make a character reference", "keep the same person across shots", or wants visual consistency across a video. Builds reference images + profiles into the asset registry so every later shot stays on-model.
---

# Director Assets — Stage 2

**brief → locked, reusable assets.** AI generates each shot in isolation, so consistency comes from feeding the *same locked reference* into every shot. This stage builds that library. (Why it matters: `references/continuity.md`. How to generate: `references/generation.md`.)

Pipeline: director-brief → **director-assets** → director-shotlist → director-storyboard → director-animate

## Three asset classes + the world bible
From the brief, enumerate what recurs:
- **Characters** — people/animals (Liza, David, a cat). Each gets a reference image **+ a profile** (the course schema: name, description, `voice`{tone/cadence/emotion/accent}, personality, appearance, camera). The `voice` block is itself a lockable asset (fal `voice-clone` later).
- **Props** — objects that recur or carry meaning (the can opener, the phone).
- **Locations / sets** — every distinct place (bedroom, hallway). Lock these or sets drift.
- **World / period bible** (`assets/world.md`) — the era + its rules (e.g. "1950s ⇒ electric tungsten light, no candles as primary; rotary phones; no anachronisms"). Everything else is generated to obey it.

## Build it
1. **Reuse first:** read `assets/registry.json` — if a needed asset exists, reuse it (don't re-lock).
2. **Generate references** with `fal-ai/flux/dev` at `portrait_16_9`, in the world/period style, clean and well-lit (clear identity), per `generation.md`. Plain background for characters/props; empty establishing shot for locations.
3. **Write profiles** (characters) using the course JSON schema; write/update `assets/world.md`.
4. **Register** each in `assets/registry.json`: `{id, type, ref_image, fal_url, profile?}`. The `fal_url` is what later shots feed as `image_urls`.

(Mechanism + the exact fal calls: `references/generation.md`. Locations are built the same way — a flux reference per set, in the world/period style.)

## Finish
1. Show the user the locked references; regenerate any that are off (cheap).
2. Confirm the world/period bible reads right (the anachronism trap).
3. Offer next: "Break the brief into a shot list with these assets? → **director-shotlist**."
