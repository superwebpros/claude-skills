---
name: edit-deflub
description: Remove flubbed takes marked with a clap from raw talking-head footage. Keeps every deliberate pause, renders the clean cut on Lambda, and transcribes the result. Use whenever a speaker has raw footage with marked retakes.
---

# Edit Deflub

**raw footage with clap-marked flubs → clean cut + transcript.** Remove flubbed takes while preserving intentional pauses and timing. Renders on AWS Lambda via Remotion and transcribes the result.

## Prerequisites

The private `superwebpros/compound-remotion` repo must be cloned and set up (see the `README.md` in edit-kit for the exact commands). You also need AWS credentials with a deployed Remotion Lambda function and an S3 bucket for renders.

## The capture contract

This skill assumes one behavior at capture time:

> **Clap, then restart the line from its first word.**

The clap marks the flub. Deflub detects it from the waveform and removes that segment. No words are transcribed; the clap cannot collide with the script.

## Workflow

### 1. Check the prerequisites
- Is `~/services/compound-remotion` checked out and `npm install` + `pip install -r deflub/requirements.txt` complete?
- Do you have AWS credentials in the environment, and does the Lambda function exist?

If either is missing, fail fast with a clear message.

### 2. Locate the raw footage
Get the path to the master video file (typically `.mov` from Premiere/Final Cut). Confirm it's the right take.

### 3. Run deflub
```bash
cd ~/services/compound-remotion/deflub
python3 deflub.py <path-to-master-mov> [--probe] [<clip1> <clip2> ...]
```

The script:
- Extracts and analyzes audio to find claps (the flub marker)
- Finds speech islands (regions where speech occurs)
- Warns if any clap is outside a speech island (bias to under-cut)
- Builds a cut list removing each flubbed segment
- Renders the clean cut on Lambda
- Transcribes the result
- Writes output to `renders/<slug>/` (video + `.vtt` transcript)

### 4. Review the output
- Watch the rendered cut
- Check the transcript for accuracy (speech is rarely 100% accurate from ASR)
- If retraining the transcription model is needed, that's a separate step

### 5. Use the result
The clean cut and transcript are ready for downstream work (filing, editing, publishing).

## Bias to under-cut

When a clap boundary is uncertain or a clap is outside a speech island, deflub errs toward leaving a fragment rather than reaching further back. This preserves audio quality and avoids cutting mid-word. Review the warning list if any claps were skipped.

## Constraints (from the design)

- **ffmpeg is Remotion's bundled binary**, not Homebrew's — the script uses the binary at `~/services/compound-remotion/node_modules/@remotion/compositor-darwin-arm64/ffmpeg` with `DYLD_LIBRARY_PATH` set correctly.
- **All timestamps are original footage seconds.** Conversion to rendered time happens exactly once in code.
- **Renders always happen on Lambda.** No local renders.
- **Orientation is decided by looking at an extracted frame**, never inferred from metadata.
