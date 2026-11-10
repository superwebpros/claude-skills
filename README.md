# Super Web Pros — Skills

The canonical library of [Agent Skills](https://agentskills.io) for the Super Web Pros team. Every skill here is a folder with a `SKILL.md`, so it works in Claude Code, Codex, Cursor, Copilot, Gemini CLI and the other tools supported by the [`skills` CLI](https://skills.sh), and the repo doubles as a Claude Code plugin marketplace.

## Install

### Any agent: `npx skills` (recommended)

```bash
# See everything available
npx skills add superwebpros/claude-skills --list

# Install one skill into the current project for Claude Code
npx skills add superwebpros/claude-skills --skill excalidraw -a claude-code

# Install globally instead of per-project
npx skills add superwebpros/claude-skills --skill excalidraw -a claude-code -g
```

Project installs land in `.claude/skills/` (or `.agents/skills/` for other agents) and write a `skills-lock.json` — commit both so teammates get the same set. Keep up to date with `npx skills check` and `npx skills update`.

Set `DISABLE_TELEMETRY=1` if you don't want installs reported to skills.sh.

### Claude Code plugins (multi-skill bundles)

```bash
claude plugin marketplace add superwebpros/claude-skills
claude plugin install director-kit@superwebpros
```

To enable a plugin for everyone working in a repo, commit this to that repo's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "superwebpros": { "source": { "source": "github", "repo": "superwebpros/claude-skills" } }
  },
  "enabledPlugins": { "director-kit@superwebpros": true }
}
```

### Other importers (Mausbot, claude.ai uploads, etc.)

Point them at a skill folder URL:

```
https://github.com/superwebpros/claude-skills/tree/main/skills/<name>
https://github.com/superwebpros/claude-skills/tree/main/plugins/<plugin>/skills/<name>
```

## Team setup (SuperWebPros)

- **Nothing to configure to install.** The repo is public, so `npx skills`, the plugin marketplace and importers like Mausbot work without GitHub auth. You only need `gh auth login` to push branches and open PRs.
- **Per project, not global.** Install the skills a project needs into that project and commit `.claude/skills/` + `skills-lock.json`. Run `npx skills check` / `npx skills update` now and then to pick up improvements.
- **Skills that need private config** read it from `~/.credentials/<name>.env` (see each skill's Prerequisites below). Ask Jesse for the values privately — never paste them into Slack, issues, or this repo.
  - `beads-sync` → `~/.credentials/beads-remote.env` (`BEADS_REMOTE_HOST`, `BEADS_REMOTE_SSH_USER`, `BEADS_REMOTE_SSH_KEY`, `BEADS_REMOTE_PORT`)
- **Improving a skill:** edit it here (not a copy inside a project), open a PR, and re-run `npx skills update` in your projects after it merges.

## Skills

| Skill | What it does | Prerequisites |
|---|---|---|
| [ad-scriptwriter](./skills/ad-scriptwriter/) | Direct-response short-form video ad scripts (9:16) in the AI Process Pros voice | — |
| [beads-sync](./skills/beads-sync/) | Diagnose and sync Beads (`bd`) with the team's shared Dolt remote | `BEADS_REMOTE_*` vars (team: `~/.credentials/beads-remote.env`) |
| [news-minute](./skills/news-minute/) | Fact-checked, avatar-ready news-roundup video scripts (HOOK/BODY/CTA) from a brief of picks; voice and rules come from a show pack | A show pack (context); `heygen-render` to dry-run |
| [excalidraw](./skills/excalidraw/) | Generate Excalidraw diagrams, flowcharts and carousels from text | — |
| [heygen-compound](./skills/heygen-compound/) | HeyGen avatar renders and reel voiceovers via `heygen-render` | Private `superwebpros/heygen-production` checkout, `HEYGEN_PRODUCTION_DIR` |
| [okf](./skills/okf/) | Configure, audit and convert folders to Google's Open Knowledge Format | — |

## Plugins

| Plugin | What it does | Install |
|---|---|---|
| [director-kit](./plugins/director-kit/) | Direct AI video like a director: brief → assets → shot list → storyboard → animate, with optional fal.ai generation | `claude plugin install director-kit@superwebpros` |
| [edit-kit](./plugins/edit-kit/) | Post-production for talking-head video: remove clap-marked flubs, render on Lambda, transcribe. Requires the private `superwebpros/compound-remotion` repo | `claude plugin install edit-kit@superwebpros` |
| [incident-response](./plugins/incident-response/) | Run a fleet-wide security/ops incident with AI agents safely: audit, beads epic, canary changes, human gates, verifier, teardown | `claude plugin install incident-response@superwebpros` |
| [msu-course](./plugins/msu-course/) | MSU SSC 490 course ops: lesson planning, post-class retrospectives, student-facing docs | `claude plugin install msu-course@superwebpros` |

Plugin skills are also installable individually with `npx skills add superwebpros/claude-skills --skill <name>`.

## Third-party skills we use

We don't vendor third-party skills — install them from upstream so you always get the maintained version.

| Skill(s) | Install |
|---|---|
| graphify ([Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify), Apache-2.0) | `npx skills add Graphify-Labs/graphify` or `graphify install --platform claude` |
| paperclip ([paperclipai/paperclip](https://github.com/paperclipai/paperclip), MIT) | `npx skills add paperclipai/paperclip --skill paperclip` |
| Cloudflare: cloudflare, wrangler, workers-best-practices, durable-objects, agents-sdk, cloudflare-email-service, cloudflare-one, cloudflare-one-migrations, sandbox-stable, sandbox-next, sandbox-migrate-to-next, turnstile-spin, web-perf ([cloudflare/skills](https://github.com/cloudflare/skills), Apache-2.0) | `npx skills add cloudflare/skills --skill <name>` |

## Repo layout

```
.claude-plugin/marketplace.json   # Claude Code marketplace ("superwebpros")
skills/<name>/SKILL.md            # standalone skills
plugins/<name>/.claude-plugin/plugin.json
plugins/<name>/skills/<skill>/SKILL.md
scripts/validate-skills.py        # spec checks (also run in CI)
.agents/skills/beads/             # beads tooling for this repo (internal, hidden from installs)
```

## Adding a skill

1. Branch, then create `skills/<name>/SKILL.md` (or run `npx skills init <name>` inside `skills/`). For a bundle of related skills, create a plugin under `plugins/` and add it to `.claude-plugin/marketplace.json`.
2. Frontmatter, per the [Agent Skills spec](https://agentskills.io/specification):
   ```yaml
   ---
   name: my-skill            # must equal the folder name; a-z, 0-9, hyphens; ≤64 chars
   description: What it does and when to use it.   # ≤1024 chars
   # optional: license, compatibility, metadata, allowed-tools (space-separated)
   ---
   ```
3. Keep `SKILL.md` under ~500 lines; put detail in `references/` and link it with relative paths (`references/x.md`), never `~/.claude/skills/...`.
4. **This repo is public.** No home-directory paths, server IPs, SSH details, client data, account IDs or secret values. Reference secrets by env var name and state prerequisites instead.
5. Validate locally, then open a PR (CI runs the same checks):
   ```bash
   python3 scripts/validate-skills.py .
   claude plugin validate . --strict
   DISABLE_TELEMETRY=1 npx skills add . --list
   ```
6. Plugins: bump `version` in `plugin.json` when you change one, or users won't receive the update.
