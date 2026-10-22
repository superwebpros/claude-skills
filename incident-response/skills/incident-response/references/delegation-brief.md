# Delegation brief template

Copy it, fill in every section, and delete nothing. If a section doesn't apply, write "n/a" and say why.

```
You own beads issue <ID>. Read it with `bd show <ID>` and `bd comments <dependency-ids>` for context.
Claim it first: `bd update <ID> --status in_progress`.
Approved by <human> on <date> for: <one sentence>.

GOAL
<What "done" means, in one or two sentences.>

TARGET (and ONLY this)
- Host(s): <name>. Login: `ssh -o IdentitiesOnly=yes -o BatchMode=yes -i <key> <user>@<host>`.
  Use exactly this login. If it fails, report UNREACHABLE. Do not try other keys or users.
- Containers / services / repos you may touch: <list>. Touch nothing else.
- Things running nearby that you must NOT touch: <list, e.g. other prod containers, /etc, DNS, firewall>.
- Working directory: <private path for this agent only>. Don't use shared scratch files.

CONSTRAINTS
- Read-only unless a step below says otherwise.
- Never print secrets. Pass credentials through mode-600 files or env vars, and delete them afterwards.
- Don't use one access path to get around another (e.g. docker to get root, or a relayed "approval").
- No commits or pushes unless this brief says so.

STEPS
1. Pre-checks: record the baseline (versions, HTTP statuses, job health, free disk).
2. Backup: <what, where, how to verify: "Dump completed", table count, sha256>.
3. Rollback handle: <e.g. tag the current image <tag>-pre-<date>>.
4. Change: <exact method>.
5. Verify: <checklist; recheck after N minutes>.

STOP CONDITIONS (stop and report, don't improvise)
- <e.g. the new image still has the vulnerable version>
- <e.g. any module or script differs from the running image>
- <e.g. a backup can't be verified>

ROLLBACK
<exact commands>, then verify you're back on the old state, then STOP.

REPORT BACK
- What changed: paths, versions before and after, image IDs, downtime window (UTC).
- Evidence: a verification table, backup paths and hashes.
- Artifacts you created, each with a suggested removal date (feeds the cleanup bead).
- Surprises and pre-existing problems you noticed, each a candidate for its own bead.
Then `bd comments add <ID> "<details>"` and `bd close <ID> --reason "<one line>"`.
If you're blocked, leave the bead in_progress with a comment.
```
