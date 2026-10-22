# The change ritual

Do these steps for every production change, in this order. Rollout order: **canary → next → production**, with a 2–3 minute soak between each.

## 1. Baseline
Record the current state, so you can prove the "after" matches it:
- runtime version in **every** container of the service (app, workers, daemons, websocket)
- local HTTP status, unauthenticated API status (often 401), authenticated API status
- public URL status, checked from outside
- job/cron health: last run time, stuck jobs, stale processes
- free disk space

## 2. Verified backup
- Database: dump with `--single-transaction --routines --triggers --no-tablespaces` (MySQL) or the equivalent for your database.
- Check the dump: it should end with "Dump completed" (or the equivalent marker) and its table count should match the live database. Record its sha256.
- Copy the config you can read (compose file, env files, ini). Use folder mode 700 and file mode 600.
- **If the backup can't be verified, don't change anything.**

## 3. Rollback handle: the retag pattern (containers)
Swap the image without editing compose files:
```bash
docker tag <current-image:tag> <current-image:tag>-pre-<date>   # keep the old image
docker tag <patched-image:tag> <current-image:tag>             # point the name compose uses at the patch
docker compose up -d --no-build                                  # recreate from the local image
```
- Rollback: `docker tag <current-image:tag>-pre-<date> <current-image:tag> && docker compose up -d --no-build`.
- First confirm no other compose project uses the same tag: `docker ps -a --format '{{.Names}} {{.Image}}'` and grep the compose files.
- ⚠️ After retagging an *upstream* name, `docker compose pull` would put the vulnerable image back. Write that down, and pin the compose file to your own tag when you can.

## 4. Building a patched image when the vendor hasn't shipped one
1. Use the vendor's **own** Dockerfile for the **exact app version you run**, changing only the `FROM` line to the patched base image.
2. Before swapping, compare the new image against the running one: runtime modules (`php -m`, etc.), web server modules, entrypoint/cmd, env var names, volumes and startup scripts (byte-diff them).
3. Treat any unexplained difference as a stop condition.

## 5. Verify, then soak
- Repeat the baseline checks; everything should match except the version.
- Check logs for fatal errors right after the change and again after 2–3 minutes.
- Confirm background jobs are advancing. Logs alone can mislead, so check last-run times.

## 6. Can't patch yet? Contain it, and say so
- Put auth in front (e.g. Cloudflare Access with a service token for machine clients), turn on the proxy, and **lock the origin to the proxy's IP ranges**. Otherwise attackers just go straight to the origin.
- Second-order effects to check:
  - **Certificate renewal:** HTTP-01 breaks behind auth, so use an origin certificate.
  - **API clients:** they need the service-token headers.
  - **Other vhosts on the same web server:** recheck them after a reload.
- Record the system as **contained**, with a bead that waits for the upstream fix.
