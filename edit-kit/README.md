# Edit Kit

Post-production for talking-head video. Each skill is one non-destructive transformation
from raw footage toward a finished cut.

| Skill | Does |
|---|---|
| `edit-deflub` | Removes flubbed takes marked with a clap, keeping every deliberate pause. Renders on Lambda and transcribes the result. |

Ingest and filing are deliberately **not** in this kit — deciding which clips belong to
which campaign is a judgment call, done conversationally as setup.

## Prerequisite: compound-remotion

These skills render through Remotion on AWS Lambda, so they need the
**private** `superwebpros/compound-remotion` repo:

```bash
git clone git@github.com:superwebpros/compound-remotion.git ~/services/compound-remotion
cd ~/services/compound-remotion && npm install
pip install -r deflub/requirements.txt
```

Without it the skills fail with a clear message rather than a confusing error. You also
need AWS credentials with a deployed Remotion Lambda function and an S3 bucket.

## The capture contract

`edit-deflub` depends on one behaviour at capture time:

> **Clap, then restart the line from its first word.**

The clap marks the flub. A clap is used rather than a spoken marker because it is
detectable from the waveform, so it needs no speech recognition, cannot be
mis-transcribed, and cannot collide with words in the script.
