# Tool Profiles — OpenArt vs Higgsfield vs fal.ai

Purpose: pick the right tool for a given shot and write to its grain. We are in **HYBRID mode**: skills output copy-paste prompts for the web UIs now; fal.ai API automation comes later.

## At a glance

| | OpenArt | Higgsfield | fal.ai |
|---|---|---|---|
| **Layer** | Consumer creative app | Consumer creative app | Developer API / infra |
| **Best for** | Character + narrative consistency across scenes | Fast viral/VFX looks, presets, volume | Programmatic generation, batching, automation |
| **Standout** | Character consistency, multi-scene "Story", voiceover (30+ langs), lip-sync | 40+ viral presets, Cinema Studio, Adobe plugins, face swap | 1000+ models, one API, scale-to-zero GPUs |
| **Models** | Seedance, Sora 2, Kling 3.0 | Sora 2, Kling 3.0, Veo 3.1, Nano Banana Pro, Soul | hosts most of the above as endpoints |
| **Interface now** | Web UI (paste prompt) | Web UI (pick preset + prompt) | API/SDK (deferred to phase 2) |
| **Coding** | None | None | Yes |

## When to reach for which

**OpenArt** → when the ad needs **a recurring character or a multi-shot story** (e.g. the same "blocked writer" across 4 beats), consistent face/wardrobe, or **AI voiceover + lip-sync** narration. Best default for narrative ad creatives that aren't just a montage.

**Higgsfield** → when you want a **look fast** — a viral preset, a dramatic camera move, a transformation/VFX beat, or high-volume variant spinning. Best for **hook shots** and **pattern-interrupt** moments, and for cranking many angle variants quickly. Has Adobe Premiere/After Effects plugins for finishing.

**fal.ai** → **phase 2.** When prompts are proven and we want to batch-generate dozens of variants programmatically, render the same shot list across multiple models to compare, or wire generation into a pipeline. Needs API key + spend caps before use.

## Prompt-writing grain (applies to all)

These tools render **literally** — this is exactly why the course's *uninflected shot* rule matters (see `director-lexicon.md`). Structure prompts as:

```
[shot size] + [subject, uninflected action] + [setting/lighting] +
[lens/DoF look] + [camera move] + [mood/grade] + [aspect ratio]
```

Example (a hook shot for the fiction course):
> "Extreme close-up of a writer's hands frozen over a laptop keyboard, blank document glowing, dim warm desk lamp, shallow depth of field on an 85mm lens, slow push-in, melancholic cinematic color grade, 9:16 vertical."

### Rules of thumb
- **One clear action per clip.** AI video degrades with compound actions. Generate simple beats; build meaning in the cut (`montage-kuleshov.md`).
- **9:16 vertical** for Meta placements — state it explicitly.
- **Keep clips short** (these tools top out at a few seconds to ~15s). Plan the ad as a *sequence of generated clips*, not one long generation.
- **Bake captions in post**, not in the generation (AI text rendering is unreliable).
- **Generate 2–3 takes per shot** and pick — cheaper than perfecting a prompt.
- **Match the model to the beat:** photoreal emotional close-ups vs. stylized/aspirational vs. kinetic hook — note which model nailed which in a running log so prompts improve over time.

## Phase-2 hook (fal.ai automation — not yet)
When we automate: store the shot list as structured data → map each shot to a fal endpoint + params → batch-render N variants → pull results for review. Requires `FAL_KEY`, per-run spend cap, and a results/review folder. Flagged here so the shot-list format stays API-friendly now.
