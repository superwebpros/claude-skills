// Portable Remotion-on-Lambda render runner.
//
// Renders the already-deployed `Reel` composition in the cloud. Imports only from
// `@remotion/lambda/client`, so it needs no composition source and no native render
// binaries — it just triggers the Lambda and polls. Works on any machine after a
// one-time `npm install` in this folder.
//
// Usage:   node render.mjs <props.json> [out.mp4]
// Creds:   REMOTION_AWS_ACCESS_KEY_ID / REMOTION_AWS_SECRET_ACCESS_KEY in env (or a .env
//          you've sourced), or an AWS profile via AWS_PROFILE=remotion.
// Config:  override REMOTION_REGION / REMOTION_SERVE_URL if the infra moves.

import {getFunctions, getRenderProgress, renderMediaOnLambda} from '@remotion/lambda/client';
import {readFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';

const REGION = process.env.REMOTION_REGION || 'us-east-1';
const SERVE_URL =
  process.env.REMOTION_SERVE_URL ||
  'https://remotionlambda-useast1-4kqe8hy4n8.s3.us-east-1.amazonaws.com/sites/compound-video/index.html';
const COMPOSITION = 'Reel';

const propsPath = process.argv[2];
const outPath = process.argv[3]; // optional local download path
if (!propsPath) {
  console.error('usage: node render.mjs <props.json> [out.mp4]');
  process.exit(1);
}

const inputProps = JSON.parse(readFileSync(propsPath, 'utf8'));

// Auto-discover the deployed function (version-agnostic — survives a function redeploy).
const fns = await getFunctions({region: REGION, compatibleOnly: true});
if (!fns.length) {
  console.error(
    `No compatible Remotion Lambda function in ${REGION}. ` +
      `Check creds (REMOTION_AWS_* or AWS_PROFILE) and that the function is deployed.`,
  );
  process.exit(1);
}
const functionName = fns[0].functionName;

const {renderId, bucketName} = await renderMediaOnLambda({
  region: REGION,
  functionName,
  serveUrl: SERVE_URL,
  composition: COMPOSITION,
  inputProps,
  codec: 'h264',
});
console.error(`render ${renderId} started on ${functionName}…`);

for (;;) {
  const p = await getRenderProgress({renderId, bucketName, functionName, region: REGION});
  if (p.fatalErrorEncountered) {
    console.error('\nrender failed:', JSON.stringify(p.errors, null, 2));
    process.exit(1);
  }
  if (p.done) {
    process.stderr.write('\r100%\n');
    // print the S3 URL on stdout (the one machine-readable line)
    console.log(p.outputFile);
    if (outPath && p.outputFile) {
      // best-effort local copy via the AWS CLI if present
      try {
        const s3 = p.outputFile.replace(
          /^https:\/\/s3\.[^/]+\.amazonaws\.com\/([^/]+)\//,
          's3://$1/',
        );
        execFileSync('aws', ['s3', 'cp', s3, outPath], {stdio: 'inherit'});
        console.error(`saved ${outPath}`);
      } catch {
        console.error(`(could not auto-download; fetch ${p.outputFile} manually)`);
      }
    }
    break;
  }
  process.stderr.write(`\r${Math.round((p.overallProgress || 0) * 100)}%`);
  await new Promise((r) => setTimeout(r, 2000));
}
