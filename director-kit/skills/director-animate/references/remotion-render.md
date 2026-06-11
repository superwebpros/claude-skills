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

## Render

Run the render **from the `~/agents/compound-remotion` project** — it has the Remotion deps
(including the platform-native render binaries) installed. A standalone `npx @remotion/cli …`
is **not** reliable: it fails to resolve the native `@remotion/renderer` binaries. The site is
already deployed, so this only uses the local install for the CLI, not for the composition.

Write the props to an **absolute** path first (e.g. `/abs/creatives/<slug>/clips/reel.props.json`),
then:

```bash
cd ~/agents/compound-remotion
# creds: AWS_PROFILE=remotion (Jesse), or REMOTION_AWS_ACCESS_KEY_ID/SECRET in env
AWS_PROFILE=remotion AWS_REGION=us-east-1 \
npx remotion lambda render \
  "https://remotionlambda-useast1-4kqe8hy4n8.s3.us-east-1.amazonaws.com/sites/compound-video/index.html" \
  Reel \
  --props="/abs/creatives/<slug>/clips/reel.props.json"
```

(The project's `@remotion/cli` is pinned to the deployed function's version, so no version
flag is needed.) Prints an S3 URL to the finished MP4. Optionally pull it local:

```bash
aws s3 cp "s3://remotionlambda-useast1-4kqe8hy4n8/renders/<id>/out.mp4" /abs/creatives/<slug>/clips/final.mp4 --profile remotion
```

**Teammate portability:** running this requires the `compound-remotion` project on the machine.
For teammates who only have the plugin (not the project), the render step is run centrally for
now (on Jesse's machine / infra). A self-contained render-runner (its own `package.json` +
`npm install`, or a tiny hosted render endpoint) is the future unlock — see roadmap.

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
