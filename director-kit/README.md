# Director Kit

Direct AI video the way a real director would. Turn a plain-English idea — or a finished piece of writing — into a **continuity-locked, character-consistent short**: a story adaptation, an ad, a reel, or a book trailer. It packages filmmaking craft (story structure, shot grammar, montage, continuity) plus an AI-generation pipeline so someone who isn't a director gets professional, on-model results.

## Pipeline

```
director-brief      idea / story  → creative brief (picks profile, extracts the dramatic object, sets world/period)
director-assets     brief         → locked cast + props + locations + world bible (reusable references)
director-shotlist   brief+assets  → shot list + continuity ledger (identity · prop · location · period)
director-storyboard shot list     → storyboard stills, reviewed scene-by-scene (renders as an Artifact / HTML)
director-animate    approved board → animated clips + assembled cut (+ optional voiceover / captions)
```

## The mental model
- **The *direction* is the engine; the content type is a variable.** Story, ad, reel, trailer all run the same pipeline — a thin "content profile" changes only the framing (goal, structure, CTA).
- **Continuity has four dimensions** — *identity, prop, location, period* — locked by an **asset layer**: each character/prop/location is generated once as a reference image, then composited into every shot so the look holds shot-to-shot. A **world/period bible** locks the era (lighting tech, props, wardrobe).
- **Review in cheap stills, scene-by-scene, before spending on video.** Stills are pennies; video is dollars.

## Generation — dual-mode
Same pipeline, two ways to make pixels (see [`CONNECTORS.md`](./CONNECTORS.md)):
- **Connector (auto):** with the **fal.ai MCP connector** (`.mcp.json`) present — Claude Code / Cowork — it generates end-to-end: `flux` references → `nano-banana/edit` (character/prop/location-consistent shots) → `seedance` image-to-video → `minimax` voice.
- **Manual (prompts):** no connector (e.g. **claude.ai today** — fal's MCP needs OAuth, which it doesn't support yet) → it emits **copy-paste prompts**; you generate in OpenArt / Higgsfield / HeyGen / Submagic. The direction is the value, so nothing blocks.

## Install
- **Claude Code / Cowork (full power):**
  ```bash
  claude plugin marketplace add superwebpros/claude-skills
  claude plugin install director-kit@director-kit
  export FAL_KEY=…     # enables auto-generation via the fal connector
  ```
- **claude.ai:** add the marketplace; runs as the **planner** (prompts) until fal ships OAuth, then upgrades to full auto with no change.
- **Local dev:** `claude --plugin-dir /path/to/director-kit`.

## The five skills
| Skill | Stage | Does |
|-------|-------|------|
| `director-brief` | 1 | idea/story → creative brief (content profile, dramatic object, world/period, anti-sag beat sheet) |
| `director-assets` | 2 | lock the reusable cast / props / locations + world bible |
| `director-shotlist` | 3 | shot list + continuity ledger (uninflected, sized, camera-moved shots) |
| `director-storyboard` | 4 | generate the storyboard stills, reviewed scene-by-scene; continuity critic |
| `director-animate` | 5 | animate approved panels + assemble (+ VO / captions) |
| `swipe-research` | cross-cut | ground briefs/shots/visuals in **proven examples** via the Swipe File connector (works in claude.ai too) |

Each skill is self-contained (its own `references/`), so it also works as a standalone Claude skill.

This plugin ships two connectors (see [`CONNECTORS.md`](./CONNECTORS.md)): **fal.ai** (generation; full power in Claude Code) and **swipe-file** (proven-example research; no OAuth, so it also works in claude.ai).

## What we learned building this
Hard-won notes from real productions — *why* the kit is shaped the way it is:

- **Lock continuity as assets, or it drifts.** AI generates each shot in isolation; consistency comes from feeding the *same locked reference image* into every shot — for characters, props, **and locations** — plus a period bible. We learned this the hard way: sets drifted between shots and a key prop changed identity until we locked them.
- **Name the dramatic object up front.** A good director reads the source and names the object of value / MacGuffin and its arc (coveted → endangered → saved). Without it, a heist has no stakes and a twist has nothing to misdirect from.
- **Put a real person in scenes by editing *from their photo*.** Feed their actual photo (e.g. a HeyGen seed) as the reference and explicitly lock styling + proportions. A from-scratch generation drifts off-likeness ("man arms", wrong build); a from-seed edit holds.
- **Multi-ref balance.** A busy/crowded *location* reference can swamp the *person* (you get a crowd, no subject). Use the character as the single primary reference and describe the setting in words.
- **Screen direction is NOT reliably promptable.** "Face left/right" is obeyed inconsistently — set it **deterministically with `ffmpeg -vf hflip`**. For an intercut conversation the two speakers must face *opposite* screen directions, or the cut won't read as an exchange.
- **Cutaways hide lip-sync.** A questioner shot in profile at a mic needs only a TTS voice + subtle motion — far cheaper than a second talking-head avatar. Use an external avatar tool (HeyGen) for a character delivering long on-camera dialogue; caption in Submagic.
- **Stills are pennies; video is dollars.** Lock the look, continuity, and pacing in stills (reviewed scene-by-scene), then animate only the **approved** shots.
- **Technical gotchas:** the fal sync endpoint `https://fal.run/{model}` needs a browser `User-Agent` (else `405`); animate a *local* still by passing it as a base64 **data URI**; build a **split-screen** two-shot by stacking real stills with `ffmpeg vstack`.

## Layout
```
director-kit/
├── .claude-plugin/plugin.json
├── .mcp.json            # fal.ai connector (auto-gen where it can authenticate)
├── CONNECTORS.md        # the dual-mode / connector explainer
└── skills/<stage>/      # SKILL.md + bundled references/ (self-contained)
```
