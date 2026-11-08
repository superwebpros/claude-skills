---
name: director-storyboard
description: Generate the visual storyboard (still images) for a shot list and review it scene-by-scene before any video — stage 4 of the director-kit pipeline. Use after a shot list exists, or when someone says "generate the storyboard", "make the panels", "show me the shots", "let's see it", "render the boards". Produces continuity-locked stills from the asset references, walks the user through them scene-by-scene for feedback, runs the continuity critic, and gates whether to animate.
---

# Director Storyboard — Stage 4

**shot list → visual storyboard (stills), reviewed scene-by-scene.** This is the **review & approval stage**, done in cheap stills before any dollar is spent on video. Generate via `references/generation.md`; judge via `references/continuity.md`.

Pipeline: director-brief → director-assets → director-shotlist → **director-storyboard** → director-animate

## Why stills first
Stills are pennies; video is dollars. Lock the look, continuity, and pacing here — then animation just executes an approved plan. Never animate an unreviewed board.

## Generate the panels (dual-mode)
For each shot in `shotlist.md`, build the panel from its **Assets used** + uninflected description + world/period style, 9:16 (see `references/generation.md` → Generation modes):
- **Generation available** (fal connector) → generate the still with `fal-ai/nano-banana/edit` (multi-ref: character + prop + location).
- **Not available** (e.g. claude.ai today) → don't block: the panel carries the **prompt + camera + continuity**, and the user generates it in their own tool and supplies the image.

**Render the board as an HTML Artifact** — in **claude.ai** produce an **Artifact**; in Claude Code write `storyboard.html`. One panel per shot: the image when available, otherwise the prompt/camera/continuity, plus shot #, dialogue, and the continuity note. Always keep the markdown **`shotlist.md`** as the editable source of truth (best for refining).

## The scene-by-scene review gate (the core of this stage)
Do **not** dump 30 panels and ask "good?" Walk it in scenes/acts:
1. Generate a scene's panels → **present them to the user with the shot intent** → ask for feedback on *that scene*.
2. Apply edits and **regenerate flagged shots** (cheap) until the scene is approved.
3. Only then move to the next scene.
This matches how a director reviews dailies and keeps feedback specific. Update the ledger + `shotlist.md` as you go.

## Run the continuity critic
Across the assembled board, flag (per `continuity.md`): blocking jumps, unmotivated presence/absence, objects of value not planted/escalating, **period anachronisms** (lighting tech, props), repetitive framing, off-model drift. Propose targeted regenerations; the human approves.

## Finish
1. Confirm the full board is approved scene-by-scene and continuity-clean.
2. Note: manual route — if the user has no fal access, export the per-shot prompts for OpenArt/Higgsfield instead of generating (see `references/tool-profiles.md`).
3. Offer next, only once approved: "Animate the approved board into a cut? → **director-animate**."
