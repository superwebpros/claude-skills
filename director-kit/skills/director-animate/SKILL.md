---
name: director-animate
description: Animate an approved storyboard into video clips and assemble the final cut — stage 5 (final) of the director-kit pipeline. Use only after the storyboard is approved, or when someone says "animate it", "make the video", "turn the board into a cut", "render the clips", "assemble the film", "add voiceover/captions". Animates approved panels via image-to-video, stitches them in order, and optionally adds AI voiceover and captions.
---

# Director Animate — Stage 5 (final)

**approved storyboard → moving clips → assembled cut.** This is the expensive stage, so it only runs on an **approved** board (gate from director-storyboard).

Pipeline: director-brief → director-assets → director-shotlist → director-storyboard → **director-animate**

## Load
- `creatives/<slug>/shotlist.md` + `storyboard.html` (the approved panels in `stills/`).
- `references/generation.md` — Seedance i2v params, the queue endpoint, costs, audio models.

## Cost gate (state it, then proceed)
720p ≈ **$0.30/s**, 1080p ≈ **$0.68/s**. A 30-shot piece is real money. Confirm scope first: a tight key-beats cut, or the full arc. Only animate **approved** shots.

## Animate
For each approved panel, run `fal-ai/bytedance/seedance-2.0/image-to-video` with `image_url` = the panel, a **restrained motion** prompt (subtle, one action — i2v degrades on big moves), `aspect_ratio:"9:16"`, `duration` per the shot's planned length. Generate via the queue endpoint and poll. (Template: `animate_shot.py` / `make_twist_cut.py`.)

## Assemble
Stitch clips in shot order with `ffmpeg` (normalize to 720×1280, concat, re-encode). Output `creatives/<slug>/clips/<name>.mp4`.

## Audio + captions (optional layer)
- **Voiceover:** `fal-ai/minimax/speech-02-hd` (TTS) for narration; `fal-ai/minimax/voice-clone` to lock a character's voice (from their asset's `voice` profile). Sync over the cut.
- **Captions / title cards:** burn in with a **freetype-enabled `ffmpeg`** (`drawtext`) — note a stock ffmpeg may lack it (`brew install ffmpeg`), or overlay pre-rendered PNG captions.

## Finish
1. Deliver the cut path; note what's baked vs. still to add (VO, captions, music).
2. Log which model/prompt nailed each shot back into `generation.md` / `tool-profiles.md` so the kit improves.
