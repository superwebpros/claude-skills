---
name: edit-deflub
description: Remove flubbed takes from already-filed raw footage, keeping every deliberate pause, then render the cut on Lambda and transcribe it. Flubs are marked at capture time by a clap. Trigger when the user wants to de-flub, clean up raw takes, remove bad takes or false starts, or run step 1 of the video edit pipeline.
---

# edit-deflub

Turn already-filed raw footage into a review cut with the flubbed takes removed and
**every deliberate pause intact**, plus a transcript of the result.

This is transformation step 1. It does not tighten pauses, add captions, zoom, crop, or
cut the ad — those are later steps.

Design: `aiprocesspros/docs/superpowers/specs/2026-09-04-video-deflub-design.md`.

## Precondition

Footage is already filed at `<piece>/footage/`. Ingest and filing are a live judgment
call about campaign membership and are done conversationally, not by this skill.

## The capture contract

> **Clap, then restart the line from its first word.**

Everything from the start of the botched attempt through the clap is removed; the retry
that follows is the keeper. If a clip contains no claps this skill reports that and
stops — it does not guess.

## Run it

```bash
cd ~/services/compound-remotion/deflub

# 1. ALWAYS probe first. Orientation cannot be inferred.
python3 deflub.py <piece-folder> --probe

# 2. LOOK at the frames it wrote, then run with the confirmed orientation
python3 deflub.py <piece-folder> --transpose=transpose=2
python3 deflub.py <piece-folder> --no-transpose
```

## Orientation is a hard gate — look at a frame

**Never infer orientation from metadata or pixel dimensions.** Both traps appeared in a
single shoot on 2026-09-04:

- iPhone `.MOV` — 3840×2160 carrying a −90 display matrix that ffmpeg applies itself.
  Decodes portrait. Needs no filter.
- DSLR `.MP4` — 1920×1080 shot on a physically rotated camera that wrote **no rotation
  metadata at all**: no side data, no `rotate` tag, DAR reports 16:9. Decodes sideways,
  needs `transpose=2`. Nothing in the container reveals this.

Generalising from the first produced three sideways renders that had to be redone. The
tool refuses to run until you pass `--transpose` or `--no-transpose`.

## What it does

1. **Orientation** — probe, extract a frame, wait for your confirmation.
2. **Proxy + stage** — rotate, scale to 1080×1920, native frame rate, hardware encode,
   upload to S3, hand the render a presigned URL.
3. **Detect** — clap transients on the high-passed waveform; speech islands from a
   loudnorm-adaptive gate. No ASR.
4. **Cut list** — each cut runs from the start of the speech run before the clap through
   the clap. Guards reject any edge landing inside speech, any overlap, any cut past the
   end.
5. **Render** — Lambda, `SpeechEdit` composition. The ripple happens in the composition,
   so a cut change is a props change.
6. **Transcribe** — ASR the *rendered* file, write the transcript and an `edits.md` stub
   beside the video.

## Output

```
<piece>/footage/_selects/<stem>/
├── <stem>_deflubbed-v1.mp4
├── <stem>_transcript.md
└── edits.md
```

## Things that will bite you

- **ffmpeg** is Remotion's bundled binary, not Homebrew's. Homebrew's has been broken
  since the x265 4.3 upgrade (2026-08-30). It needs `DYLD_LIBRARY_PATH` set to its own
  directory; `deflub/ffmpeg.py` handles this.
- **Never parse Remotion's console output to find a render.** It prints an
  `https://s3...` url, not `s3://`. List the bucket by prefix and take the newest key —
  a wrapper that grepped for `s3://` aborted three runs, each after a paid render.
- **All timestamps are original footage seconds.** The rendered timebase is derived, never
  hand-converted.
- **Bias to under-cut.** An uncertain boundary leaves a fragment rather than reaching
  further back. Fragments show up in the transcript and are recoverable; deleted good
  takes are not.
- **Clap thresholds are measured, not proven at scale.** A clap more than ~12 dB down, or
  one landing on speech instead of in a pause, may be missed. Every run logs detected
  features to `_build/claps-<stem>.json` so a miss comes with the data to retune.

## Verify

The transcript is the check. It is produced from the rendered file by a pass that knows
nothing about what was supposed to be removed, so a surviving flub or an eaten line shows
up plainly. Skim it before moving to the next pipeline step.
