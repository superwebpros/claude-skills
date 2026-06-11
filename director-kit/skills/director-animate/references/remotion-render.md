# Remotion render (branded assembly on Lambda)

The final cut is assembled by a deployed **Remotion** composition rendered on **AWS Lambda** —
not ffmpeg. This gives branded title/CTA cards, animated word-by-word captions, crossfades,
and a programmatically **editable** cut (change a prop, re-render). ffmpeg `concat`/`drawtext`
is only a fallback for a quick raw stitch.

## Deployed infra (fixed)

| Thing | Value |
|---|---|
| Region | `us-east-1` |
| Remotion version | **4.0.475** (pin the CLI to this — it must match the deployed function) |
| Serve URL | `https://remotionlambda-useast1-4kqe8hy4n8.s3.us-east-1.amazonaws.com/sites/compound-video/index.html` |
| Composition id | `Reel` |

One site serves **every brand** — brand tokens come in as props, so don't redeploy per brand.
(Source project: `~/agents/compound-remotion/`, see its `INFRA.md`. Redeploy the site only when
the composition code changes.)

## Credentials

- On Jesse's machine: the `[remotion]` AWS profile (`~/.aws`). Set `AWS_PROFILE=remotion`.
- For teammates without `~/.aws`: put `REMOTION_AWS_ACCESS_KEY_ID` / `REMOTION_AWS_SECRET_ACCESS_KEY`
  in a project `.env`. Remotion reads those directly.

## Build the props from the shotlist

Map the approved shots/clips into the `Reel` props. Scenes play in order with 15-frame
crossfades; duration is derived from the scenes automatically.

```jsonc
{
  "brand": { "bg": "#0A0A0A", "text": "#F2EDE4", "accent": "#E5484D" },  // from 00-brand/brand-guide.md
  "scenes": [
    // optional branded hook card
    { "type": "title", "durationInFrames": 60, "title": "Hook line", "subtitle": "optional" },

    // one scene per animated clip — src is the REMOTE clip URL (Seedance/fal or HeyGen output)
    { "type": "video", "durationInFrames": 150, "src": "https://.../shot-01.mp4", "caption": "on-screen line for this shot" },
    { "type": "video", "durationInFrames": 120, "src": "https://.../shot-02.mp4" },

    // optional branded CTA card
    { "type": "title", "durationInFrames": 75, "title": "Book the clarity call.", "subtitle": "CTA" }
  ]
}
```

Rules for the mapping:
- **`durationInFrames` = shot seconds × 30** (fps is 30).
- **`src` must be a URL AWS can fetch.** Seedance/fal and HeyGen outputs are already remote URLs — pass them straight through, do **not** download them first. If a clip only exists locally, upload it to a public/S3 URL before rendering.
- **`caption`** = the shot's spoken line or on-screen text (optional per scene). Captions reveal word-by-word, active word in `brand.accent`.
- **`brand`** = the active brand's tokens from its `00-brand/brand-guide.md`. Omit to use the composition defaults (Compound).
- Lead with a `title` hook and end with a `title` CTA when the brief calls for it; otherwise all `video`.

Write the props to `creatives/<slug>/clips/reel.props.json`.

## Render — use the portable runner (default, works on any machine)

The render runs in the **cloud**, so you don't need the composition source. Use the bundled
**render-runner** (`./render-runner/`, see its README). It talks to the deployed Lambda via
`@remotion/lambda/client` only — no composition project, no native render binaries.

One-time per machine:

```bash
cd ${CLAUDE_PLUGIN_ROOT}/skills/director-animate/render-runner && npm install
```

Then, after writing the props to a file:

```bash
cd ${CLAUDE_PLUGIN_ROOT}/skills/director-animate/render-runner
# creds: AWS_PROFILE=remotion, or REMOTION_AWS_ACCESS_KEY_ID/SECRET in env (.env)
AWS_PROFILE=remotion node render.mjs /abs/creatives/<slug>/clips/reel.props.json /abs/creatives/<slug>/clips/final.mp4
```

It prints the S3 MP4 URL (and downloads `final.mp4` if the second arg + `aws` CLI are present).
The deployed function is auto-discovered, so a function redeploy needs no change here as long
as the runner's `@remotion/lambda` version matches the deployed function version.

> `${CLAUDE_PLUGIN_ROOT}` is the installed director-kit plugin path. If `npm install` into the
> plugin dir is awkward (e.g. a read-only install), copy `render-runner/` into the working
> project once and run it there.

### Dev alternative (the composition author's machine)

From the `~/agents/compound-remotion` project (which has the full Remotion install), you can
also render directly: `AWS_PROFILE=remotion npx remotion lambda render "<serve-url>" Reel --props=<abs path>`.
A standalone `npx @remotion/cli …` is NOT reliable (it can't resolve the native renderer
binaries) — use the runner or the project, not ad-hoc npx.

Cost is ~$0.002 for a ~10s reel; scales linearly with length/resolution.

## Editing (the payoff)

To revise the cut, edit `reel.props.json` (swap a clip `src`, change a caption, reorder
scenes, recolor via `brand.accent`, retime a scene) and re-run the render. No timeline editor,
no re-stitch. Composition/layout changes (new scene types, motion) live in the
`~/agents/compound-remotion` project and need a `npm run deploy:site` redeploy.

## Audio

Remotion composites video + captions + branding. Voiceover/music is layered separately
(`fal-ai/minimax/speech-02-hd` TTS, synced in post) — or add an audio track to the composition
later. The `video` clip's own audio (e.g. a HeyGen avatar's voice) plays as part of the clip.
