---
name: beads-sync
description: Diagnose, initialize, repair, and sync Beads (bd) issue databases against a shared remote Dolt server reached through an SSH tunnel. Use when `bd ready`, `bd dolt pull`, or `bd dolt push` fails with errors like "no beads database found", "connection refused", "cannot reach remote", "address already in use", "column could not be found", or "no common ancestor", or when setting up a fresh git clone of a beads-tracked repo on a new machine.
compatibility: Needs the bd (beads) CLI >= 1.0.0, dolt, and ssh. The persistent-tunnel option is macOS-only (launchd).
metadata:
  author: superwebpros
  version: "1.1"
---

# Beads Sync & Remote Setup

This skill diagnoses and configures beads issue databases that sync with a shared Dolt remote. The remote Dolt server is not exposed publicly. Each machine opens an SSH tunnel that forwards a local port to the server's Dolt remotesapi port, and beads talks to `http://localhost:<port>/<database>`.

## Configuration

The procedures below use these environment variables. None of the values belong in a repo.

| Variable | Meaning | Default |
|---|---|---|
| `BEADS_REMOTE_HOST` | Hostname or IP of the server running the Dolt remotesapi | none, required |
| `BEADS_REMOTE_SSH_USER` | SSH user on that server | none, required |
| `BEADS_REMOTE_SSH_KEY` | Path to the private key used for the tunnel | none, required |
| `BEADS_REMOTE_PORT` | Dolt remotesapi port, used on both ends of the tunnel | `50051` (the port Dolt's docs use for remotesapi) |

**SuperWebPros team members:** get the values from the team credentials store. Find the beads remote / agent-team section of `~/.credentials/README.md`, then load the project file it names with `set -a; source ~/.credentials/load.sh <project>; set +a` (or `loadenv <project>`). Don't paste the values into repos, issues, or chat logs.

Before running anything, check that the variables are set. This prints names only, never values, and works in bash and zsh:

```bash
for v in BEADS_REMOTE_HOST BEADS_REMOTE_SSH_USER BEADS_REMOTE_SSH_KEY; do
  printenv "$v" >/dev/null && echo "$v set" || echo "$v MISSING"
done
export BEADS_REMOTE_PORT="${BEADS_REMOTE_PORT:-50051}"
```

If any are missing, stop and ask the user where the beads remote credentials live. Don't guess a host.

---

## 1. Quick Diagnosis & Decision Tree

When you hit a beads error or are configuring a new clone:

```
Run: bd ready (or bd dolt pull)
 ├── Error: "no beads database found"
 │    └── Case 1: Fresh clone or missing embedded Dolt folder (see Section 3)
 ├── Error: "connection refused" or "cannot reach remote"
 │    └── Case 2: SSH tunnel on $BEADS_REMOTE_PORT is not running (see Section 2)
 ├── Error: "address already in use"
 │    └── Something else (often a stale tunnel) holds $BEADS_REMOTE_PORT (see Section 2)
 ├── Error: "column could not be found" / schema drift
 │    └── Case 3: bd CLI version mismatch. Upgrade to >= 1.0.0 (`brew upgrade beads`)
 └── Error: "no common ancestor"
      └── Case 4: Remote and local diverged (see Section 4)
```

---

## 2. Ensure the SSH Tunnel Is Running

Check whether the tunnel is already up:

```bash
lsof -i :"$BEADS_REMOTE_PORT" | grep LISTEN
```

If a process is listening but beads still can't reach the remote, it may be a stale tunnel or an unrelated process. Inspect it with `lsof -i :"$BEADS_REMOTE_PORT"` and confirm with the user before killing anything, since it may be the persistent launchd tunnel.

### If not running

#### Quick/ad-hoc start

```bash
ssh -fNL "$BEADS_REMOTE_PORT:127.0.0.1:$BEADS_REMOTE_PORT" \
  -i "$BEADS_REMOTE_SSH_KEY" \
  -o ServerAliveInterval=60 -o ServerAliveCountMax=3 -o ExitOnForwardFailure=yes \
  "$BEADS_REMOTE_SSH_USER@$BEADS_REMOTE_HOST"
```

#### Persistent auto-start on macOS (launchd)

To keep the tunnel up across reboots and network drops, install a LaunchAgent. See [references/launchd-tunnel.md](references/launchd-tunnel.md) for the plist template and the load/unload commands.

---

## 3. Fresh Clone Setup ("no beads database found")

In modern beads (v1.2+ with embedded Dolt), the local database directory is gitignored under `.beads/embeddeddolt/<database_name>`, so a fresh git clone has no database.

### Step 3.1: Identify the database name

Check `.beads/metadata.json` or `.beads/config.yaml` in the repo:

- Look for `"dolt_database"` in `.beads/metadata.json`.
- Or look for `sync.remote` in `.beads/config.yaml` (for example `http://localhost:50051/<database>`).
- If neither exists, try the project name, or list the databases on the remote (Section 5).

### Step 3.2: Clone the remote database into `embeddeddolt`

From the project root, with the tunnel running:

```bash
# 1. Stop any running beads processes for safety
bd dolt stop 2>/dev/null || true

# 2. Ensure the embeddeddolt directory exists
mkdir -p .beads/embeddeddolt

# 3. Clone the remote database
cd .beads/embeddeddolt
dolt clone "http://localhost:$BEADS_REMOTE_PORT/<PROJECT_DATABASE_NAME>"

# 4. Return to root and verify
cd ../..
bd ready
```

---

## 4. Normal Session Workflow & Edge Cases

### Start of work

```bash
bd dolt pull
bd ready
```

### End of work (session completion gate)

```bash
git pull --rebase
bd dolt commit
bd dolt push
git push
```

### Edge case: diverged histories ("no common ancestor")

This happens when the local database was initialized independently instead of cloned. Both fixes discard history on one side, so confirm with the user which side is authoritative first.

- **If the remote is authoritative** (discard accidental local scratch):
  ```bash
  bd dolt stop 2>/dev/null || true
  rm -rf .beads/embeddeddolt/<PROJECT_DATABASE_NAME>
  cd .beads/embeddeddolt && dolt clone "http://localhost:$BEADS_REMOTE_PORT/<PROJECT_DATABASE_NAME>"
  cd ../.. && bd ready
  ```
- **If local is authoritative**:
  ```bash
  bd dolt push --force
  ```

---

## 5. Finding Project Databases on the Remote

Each beads-tracked project has its own database on the remote, usually named after the repo. Its remote URL takes this form:

```
http://localhost:$BEADS_REMOTE_PORT/<project-database-name>
```

To see which databases exist, list the Dolt sql-server's data directory on the server. Replace `<dolt-data-dir>` with the directory the server's `dolt sql-server` runs from:

```bash
ssh -i "$BEADS_REMOTE_SSH_KEY" "$BEADS_REMOTE_SSH_USER@$BEADS_REMOTE_HOST" 'ls <dolt-data-dir>'
```

SuperWebPros team members can find the team's project database names next to the connection details in `~/.credentials/README.md`.
