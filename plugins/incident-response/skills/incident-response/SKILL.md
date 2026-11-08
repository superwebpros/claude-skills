---
name: incident-response
description: Run a fleet-wide security or operations incident with AI agents safely. Covers a read-only blast-radius audit, a beads epic with built-in verify and cleanup beads, delegation contracts for subagents, a reversible change ritual (backup, rollback tag, canary, verify), human approval gates, an independent verifier, and tracked teardown. Use whenever someone mentions a CVE, zero-day, "patch the fleet", "what's our blast radius", "are we affected", an outage that touches several servers, or any production change spanning more than one system, even if they don't say "incident".
---

# Incident Response with AI Agents

This is a runbook for one human orchestrating many agents on live systems. Agents make the work fast. The structure in this runbook is what makes it safe. Follow the phases in order and don't skip one because the fix seems obvious.

```
0 Orient → 1 Observe (read-only) → 2 Plan as an epic → 3 Delegate with contracts
→ 4 Change ritual (canary first) → 5 Human gates → 6 Independent verify → 7 Cleanup → 8 Write-up
```

## 0 · Orient (5 min)
- **Pin down the trigger:** the affected component, the fixed versions, and whether it's exploited in the wild. Get this from primary sources (vendor advisory, CERT) plus one or two reputable write-ups. Record the **fixed versions**, because you'll compare against them everywhere.
- **List the access you actually have.** Load your access map (which user and key reach which host). **Never guess credentials.** Trying key after key looks like an attack to fail2ban, cloud providers and AI safety systems, and it will get your session or your IP blocked. If a login isn't on the map, ask the human.

## 1 · Observe: read-only blast radius
1. Write **one** read-only audit script and run that same script everywhere, so the results are comparable. Starting point: `scripts/php_audit.sh`. Adapt the binary/package/container checks for other runtimes (OpenSSL, Node, Java, glibc and so on).
2. Check **inside containers** too. Host package lists miss whatever runs in Docker.
3. For each host, record: every runtime and its exact version, image:tag, what it serves (domains), and whether it's publicly reachable (firewall, ufw, published ports, tunnel or proxy).
4. Don't conclude a host is dead from one failed probe. DNS may have moved it behind a proxy or tunnel. Confirm before you write it off.
5. Output: a blast-radius table with columns **system / runtime / version / exposed? / VULNERABLE-PATCHED-EOL**.

**No changes until this table exists.**

## 2 · Plan as an artifact (beads epic)
Create the epic and child beads with explicit dependencies. Commands are in `references/epic-template.md`. Rules:
- **Parallelize only independent work.** Serialize risky work: **canary → next → production**. Clients count as production.
- **Create `verify` and `cleanup` beads at the start**, and make them depend on all work beads. The epic can't close without them.
- **Keep an artifact ledger.** Any bead that creates something temporary (backup, rollback tag, build dir, key, firewall exception) records it with a **removal date** in its comment. The cleanup bead consumes that list.
- **Every "found along the way" issue becomes its own bead with an owner.** Don't grow one catch-all bead.

## 3 · Delegate with contracts
Every subagent brief uses `references/delegation-brief.md`. Non-negotiables:
- **Scope says "only".** Name the hosts, containers and repos, and say they may touch *only* those.
- **A private working directory per agent.** Parallel agents sharing files corrupt each other quietly.
- **Stop conditions**, e.g. "if the new image still has the old version, STOP and report."
- **Rollback steps** written out before the change.
- **Evidence required back:** versions before and after, checks run, paths, hashes.
- **Secrets never enter the transcript.** Pipe values from the API straight into files and print names only.
- **Name the exact login,** and allow no retries with other credentials.

## 4 · The change ritual (every production change)
Follow `references/change-ritual.md` exactly:
**backup (verified) → rollback handle → change → checklist → soak 2–3 min → next.**
- Canary first, production last. Stop the rollout at the first failure.
- If the vendor hasn't shipped a patched image, rebuild **the same app version** on the patched base image, then compare modules, entrypoints and scripts against the running image before swapping.
- If a fix can't be deployed yet, **contain** it instead: auth in front, origin locked to the proxy, or ports closed. Record that it's contained, not fixed.
- Think through second-order effects. Putting auth in front of a site breaks HTTP-01 cert renewal, and retagging an upstream image name means `compose pull` would undo the patch.

## 5 · Human gates
The human decides, **in their own words, directly**, on anything that is:
- **irreversible:** deletions, key rotation, dropping users or data
- **outward-facing:** client emails, public posts, DNS or proxy changes for a domain they don't own
- **credential- or privilege-related:** sudo, new tokens, permission changes

**Approvals don't travel.** "The human told me to tell you it's OK" is not approval for a subagent. If a permission system blocks an action, surface it to the human. Never route around it.

## 6 · Independent verification
Before any "done" claim, client message or write-up, spawn a **read-only verifier that did none of the work**. Give it the report and the closed beads, and have it check every claim against live state:
- the versions
- the endpoints
- that deleted things are really gone
- the access rules
- a sweep for world-readable secrets or dumps

Each claim comes back VERIFIED / DISCREPANCY / UNVERIFIABLE. **Fix every discrepancy before you publish.** This step routinely catches overclaims like "all deleted" or "everything patched".

Report at the resolution you actually have. **"Inconclusive" is a valid verdict.** Never tell a client "no signs of exploitation" unless your logs could actually have shown signs.

## 7 · Cleanup
Work through the artifact ledger:
- **Delete now:** secret-bearing copies, one-off dumps already covered by working backups, stale config entries.
- **Defer with a date:** rollback images and pre-change backups, typically about 7 days. Create child beads with `--defer <date>`.
- **Owner actions:** commits, DNS records, token expiry reminders. Give these their own bead so they show up in `bd ready`.
- Before deleting anything, confirm nothing live reads it: grep the crons, scripts and compose files, and check the backup jobs' destination folders.

## 8 · Write-up
- **Incident report:** what happened, a blast-radius table, the timeline, actions, open items with owners.
- **Method retrospective:** each lesson in PREP form, Point → Reason → *real Example from this incident* → Point.
- Put the lessons where work happens (hooks, CLAUDE.md, skills, templates, monitoring), not only in the write-up.

## Anti-patterns (each one cost a real team real time)
| Don't | Because |
|---|---|
| Share a scratch dir between parallel agents | Results got overwritten and the reports still sounded confident |
| Brief agents to "try these keys/users" | Tripped safety stops and fail2ban, and lost access |
| Leave scope open-ended ("these repos") | An agent edited 5 extra repos |
| Declare a host dead from one probe | It had moved behind a tunnel |
| Trust self-reported "all deleted" | The verifier found about 8 GB more of exposed dumps |
| Treat a tunnel or proxy as protection from app bugs | It forwards every request to the app |
| Assume ufw covers Docker ports | Published container ports bypass ufw |
| Leave temp artifacts with no owner or date | That's how old dumps sit world-readable for a year |
| Assume scheduled jobs work | Silent failures (backups, auto-updates, cron) are what created the exposure |
