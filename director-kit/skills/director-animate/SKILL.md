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
- `references/remotion-render.md` — branded assembly on Lambda (the default Assemble path).

## Cost gate (state it, then proceed)
720p ≈ **$0.30/s**, 1080p ≈ **$0.68/s**. A 30-shot piece is real money. Confirm scope first: a tight key-beats cut, or the full arc. Only animate **approved** shots.

## Animate
For each approved panel, run `fal-ai/bytedance/seedance-2.0/image-to-video` with `image_url` = the panel, a **restrained motion** prompt (subtle, one action — i2v degrades on big moves), `aspect_ratio:"9:16"`, `duration` per the shot's planned length. Generate via the queue endpoint and poll. (Template: `animate_shot.py` / `make_twist_cut.py`.)

## Assemble (branded render on Lambda — default)
Assemble the cut with the deployed **Remotion** composition, not ffmpeg. It gives branded
title/CTA cards, animated word-by-word captions, crossfades, and an **editable** cut. Follow
`references/remotion-render.md`:

1. Map the approved clips into the `Reel` props — one `video` scene per clip (`src` = the clip's
   **remote** URL from Seedance/fal or HeyGen; `durationInFrames` = shot seconds × 30; `caption` =
   the shot's line). Lead with a `title` hook and end with a `title` CTA when the brief calls for it.
2. Pull `brand` tokens (bg/text/accent) from the active brand's `00-brand/brand-guide.md`. The one
   deployed site renders any brand — brand is passed as props, never redeployed.
3. Write `creatives/<slug>/clips/reel.props.json`, then render (pin `remotion@4.0.475` to the
   deployed function; creds via `AWS_PROFILE=remotion` or `REMOTION_AWS_*` in `.env`). Returns an
   S3 MP4 URL; optionally `aws s3 cp` it to `creatives/<slug>/clips/final.mp4`.

**Fallback (raw cut only):** if Lambda creds aren't available, stitch clips with `ffmpeg` (normalize
to 1080×1920, concat, re-encode) for an unbranded, uncaptioned cut. No `drawtext` captions — captions
are the composition's job now.

## Audio (optional layer)
- **Voiceover:** `fal-ai/minimax/speech-02-hd` (TTS) for narration; `fal-ai/minimax/voice-clone` to
  lock a character's voice (from their asset's `voice` profile). A `video` clip's own audio (e.g. a
  HeyGen avatar) plays as part of the clip; layer added VO/music in post, or as a future composition track.
- **Captions / title cards** are produced by the Remotion composition (see Assemble), not burned in here.

## Finish
1. Deliver the final MP4 (S3 URL + local `final.mp4`). Captions, title cards, and brand styling are baked by the render; note anything still to add (added VO, music).
2. The cut is editable: to revise, edit `reel.props.json` and re-render (no re-stitch).
3. Log which model/prompt nailed each shot back into `generation.md` / `tool-profiles.md` so the kit improves.
