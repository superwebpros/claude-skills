# Connectors

## fal.ai — generation (optional, graceful)
Director Kit can **auto-generate** images/video via the **fal.ai MCP connector** (`.mcp.json` → `https://mcp.fal.ai/mcp`). It runs fal models (flux references, nano-banana character/prop/location edits, Seedance image-to-video, MiniMax speech) via the connector's `run_model` / `submit_job` tools.

| Surface | fal connector | Mode |
|---|---|---|
| **Claude Code** | ✅ API-key (Bearer) — set `FAL_KEY` | **Full power** — locks characters, generates the image storyboard, animates |
| **Cowork** (desktop) | ✅ if API-key connectors are accepted | Full power |
| **claude.ai** (browser) | ⛔ not yet — claude.ai connectors require **OAuth**, which fal doesn't support yet | **Planner** — the kit emits copy-paste prompts; you generate in your own tools |

**You don't need the connector to get value.** Without it you still get the full director output — brief, shot list, continuity ledger, and ready-to-paste **storyboard prompts** — and generate in OpenArt / Higgsfield / **HeyGen** / Submagic. The signature feature (visual character/continuity locking) needs image-gen, so it's fullest in **Claude Code**. When fal ships OAuth, claude.ai upgrades to full auto with no change to this plugin.

### Setup (Claude Code)
Get a key at the fal dashboard, then `export FAL_KEY=…` before launching. The connector passes it as a Bearer token.

### Talking heads
For a character delivering on-camera dialogue (e.g. an avatar answering questions), render in **HeyGen**; the kit handles everything around it (questioner cutaways, B-roll, assembly). Captions/title cards: **Submagic**.
