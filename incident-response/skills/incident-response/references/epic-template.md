# Incident epic template (beads)

Run these from the repo that tracks operations work. The template builds in the two beads teams forget: **verify** and **cleanup**.

```bash
E=$(bd create "<CVE/incident>: patch & contain fleet" -t epic -p 0 -l incident --silent \
  -d "Trigger: <advisory link>. Fixed versions: <list>. Exploited in wild: <yes/no>. Audit script: <path>.")

AUDIT=$(bd create "Read-only blast-radius audit (all hosts)" -t task -p 0 --parent $E -l incident --silent)

# One bead per system to change. Serialize risky ones with --deps.
CANARY=$(bd create "Patch <low-stakes system> (CANARY)" -t task -p 0 --parent $E --deps $AUDIT -l incident --silent)
NEXT=$(bd create "Patch <next system>" -t task -p 0 --parent $E --deps $CANARY -l incident --silent)
PROD=$(bd create "Patch <production system>" -t task -p 0 --parent $E --deps $NEXT -l incident --silent)

# Built in from the start: the epic isn't done without these.
CLEAN=$(bd create "Cleanup: work through the artifact ledger" -t task -p 1 --parent $E --deps $PROD -l incident,cleanup --silent \
  -d "Every bead lists the temp artifacts it created, each with a removal date. Delete now / defer with --defer <date> / owner actions.")
VERIFY=$(bd create "Independent read-only verification of all claims" -t task -p 1 --parent $E --deps $CLEAN -l incident,verify --silent \
  -d "Run by an agent that did none of the work. VERIFIED/DISCREPANCY/UNVERIFIABLE per claim. Leave open if any discrepancy.")
```

## Conventions
- **Owner labels** for handoffs, e.g. `--add-label owner-<name>`. The bead carries the context.
- **`needs-input`** means waiting on a human decision. Remove it once the decision is made.
- **Found along the way:** `bd create "<finding>" --parent $E -l <area>`, one bead per finding, with an owner.
- **Artifact ledger entry,** added as a comment on the bead that created the artifact:
  `bd comments add <ID> "ARTIFACT: <path/tag/key> | why: <reason> | remove after: <date or condition>"`
- **Deferred cleanup:** `bd create "<what> — DUE <date>" --parent $CLEAN --defer <date>`.
- **Closing a parent while deferred children are still open** needs `--force`, and that's intended.
