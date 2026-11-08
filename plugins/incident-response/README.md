# incident-response

A Claude Code plugin for running a fleet-wide security or ops incident with AI agents, **safely**.

It packages one skill (`incident-response`) that walks the orchestrating session through:

0. **Orient.** Advisory, fixed versions, and your access map. Never guess credentials.
1. **Observe.** One read-only audit script, run everywhere, including inside containers.
2. **Plan as an artifact.** A beads epic with **verify** and **cleanup** beads built in, plus an artifact ledger.
3. **Delegate with contracts.** Scope says "only", a private work dir per agent, stop conditions, rollback, evidence.
4. **The change ritual.** Verified backup → rollback tag → change → checklist → soak, canary first.
5. **Human gates.** Anything irreversible, outward-facing or credential-related. Approvals don't travel.
6. **Independent verification.** An agent that did none of the work checks every claim.
7. **Cleanup.** Work through the ledger: delete now, defer with dates, owner actions.
8. **Write-up.** An incident report, plus lessons in PREP form (point, reason, real example, point).

## Contents
| Path | What |
|---|---|
| `skills/incident-response/SKILL.md` | The runbook |
| `skills/incident-response/references/delegation-brief.md` | Fill-in template for every subagent brief |
| `skills/incident-response/references/change-ritual.md` | Baseline, backup, retag pattern, rebuilding on a patched base, containment |
| `skills/incident-response/references/epic-template.md` | beads commands for an epic with verify and cleanup built in |
| `skills/incident-response/scripts/php_audit.sh` | Example read-only audit: PHP on the host and in Docker containers. Adapt it for other runtimes |

## Install
```bash
claude plugin marketplace add superwebpros/claude-skills
claude plugin install incident-response@superwebpros
```

To prompt everyone who opens a shared repo to install it automatically, add this to that repo's `.claude/settings.json`:
```json
{
  "extraKnownMarketplaces": {
    "superwebpros": { "source": { "source": "github", "repo": "superwebpros/claude-skills" } }
  },
  "enabledPlugins": { "incident-response@superwebpros": true }
}
```

## Origin
This plugin distils a real same-day response to a critical, actively exploited PHP RCE (PHP2Shell, CVE-2026-109618/109619, October 2026). One human and about 25 subagents patched or contained every exposed system they could reach. The anti-patterns table in the skill lists the mistakes we made along the way.
