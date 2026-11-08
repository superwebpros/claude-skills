# Render runner (portable)

Renders the deployed Remotion `Reel` composition on AWS Lambda. The composition lives in the
cloud, so this runner needs **no composition source and no GPU/native render setup** — just
Node and AWS credentials. Use it on any machine (e.g. a teammate's).

## One-time setup

```bash
cd render-runner
npm install            # needs Node 18+; pulls @remotion/lambda 4.0.475
```

Credentials — either:
- an AWS profile: `export AWS_PROFILE=remotion` (the scoped Remotion user), or
- env vars (good for a teammate `.env`):
  ```
  REMOTION_AWS_ACCESS_KEY_ID=...
  REMOTION_AWS_SECRET_ACCESS_KEY=...
  ```

## Render

```bash
node render.mjs /path/to/reel.props.json            # prints the S3 MP4 URL
node render.mjs /path/to/reel.props.json final.mp4  # also downloads it (needs aws CLI)
```

`reel.props.json` is the `Reel` props (brand tokens + scenes) built by `director-animate`
from the approved shotlist — see `../references/remotion-render.md` for the schema.

## Config (override only if the infra moves)

- `REMOTION_REGION` (default `us-east-1`)
- `REMOTION_SERVE_URL` (default = the deployed `compound-video` site)

The deployed Lambda function is auto-discovered (`compatibleOnly`), so a function redeploy
doesn't require changing anything here as long as the runner's `@remotion/lambda` version
matches the deployed function version.
