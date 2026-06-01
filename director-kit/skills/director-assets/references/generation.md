# Generation — the fal execution adapter

> How to actually generate, learned + proven in production. Tool-agnostic intent; concrete via fal.ai. When this kit ships as a plugin, swap the REST calls for the **fal MCP connector** tools (same models) — the director logic below is unchanged.

## Auth + transport (gotchas that cost us hours)
- Key in project `.env` as `FAL_KEY` (gitignored). Header: `Authorization: Key <FAL_KEY>`.
- **Images (sync):** `POST https://fal.run/{model}` → returns `{images:[{url}]}` directly. No polling needed for small batches.
- **⚠️ Send a browser `User-Agent` header** or fal's WAF returns `405`. (Default `Python-urllib` UA is blocked.)
- **Video (queue):** `POST https://queue.fal.run/{model}` → returns `status_url`/`response_url`; poll `status_url` until `COMPLETED`, then GET `response_url` → `{video:{url}}`. Use the URLs fal returns verbatim.

## Models (what each is for)
| Model | Use | Notes |
|---|---|---|
| `fal-ai/flux/dev` | Clean **reference** images (characters, props, locations); establishing shots | Respects `image_size:"portrait_16_9"` → true 9:16. Cheap (~pennies). |
| `fal-ai/nano-banana/edit` | **THE workhorse** — character/prop/location-consistent shots | Input `{prompt, image_urls:[...]}`. **Multi-ref:** pass `[character, prop, location]` and say "reference image 1/2/3 is …". Ignores `image_size` (inherits ref aspect — make refs 9:16). |
| `fal-ai/bytedance/seedance-2.0/image-to-video` | **Animate** a still → clip | `{prompt, image_url, resolution:"720p", duration:"4".."15", aspect_ratio:"9:16", generate_audio}`. Queue endpoint. **720p ≈ $0.30/s, 1080p ≈ $0.68/s.** |
| `fal-ai/minimax/speech-2.8-hd` | **TTS** narration / dialogue / VO | `{prompt, voice_setting:{voice_id, speed, vol, pitch}, output_format:"url"}` → `audio.url` (mp3) + `duration_ms`. Preset voices e.g. `Wise_Woman`, `Calm_Woman`, `Friendly_Person`. |
| `fal-ai/minimax/voice-clone` | **Lock a character's voice** from a sample | Voice = part of the character asset (see continuity.md). |

## The asset-ref workflow (continuity in one move)
1. Lock each character/prop/location once as a reference image (flux), stored in the asset registry (`assets/registry.json`) with its `fal_url`.
2. Generate every shot with `nano-banana/edit`, feeding the relevant asset `fal_url`s as `image_urls`. Same refs → same look, shot after shot.
3. This is why continuity holds: you're not re-rolling the character/set each shot, you're compositing locked assets.

## Iron rules
- **9:16 vertical** for social; state it in the prompt.
- **Uninflected prompts** (see director-lexicon.md) — literal visible content, one action per shot.
- **No baked-in text** — AI text is unreliable; keep generations clean. Add captions/titles/end-cards in post with an **external caption tool (e.g. Submagic)**, or burn in with a freetype-enabled `ffmpeg` (`drawtext`).
- **Cost discipline:** stills are pennies → iterate + review here. Video is dollars → only animate **approved** shots.
- **Generate 2–3 takes** of hero shots and pick; these models are a slot machine.

## Reusable scripts (templates / patterns)
Proven patterns to adapt per project (write small per-creative scripts, or call the fal MCP tools directly):
lock cast/props/locations (flux refs → registry); multi-ref panel generation + render the board; regenerate flagged panels; Seedance i2v + ffmpeg assemble; editable markdown shot list.

## Production techniques (proven in real runs)
- **Put a REAL person in scenes** — feed their actual photo (e.g. a HeyGen talking-photo seed) as the `nano-banana/edit` reference, and explicitly lock styling + proportions ("her blazer, natural feminine build"). A from-scratch generation drifts off-likeness ("man arms", wrong build); a from-seed edit holds.
- **Multi-ref balance** — feeding a busy/crowded LOCATION ref alongside a person can SWAMP the subject (you get a crowd, no person). For a foreground person in a setting, use the CHARACTER as the **single primary ref** and describe the setting in words.
- **Screen direction is NOT reliably promptable** — "face left/right" is obeyed inconsistently. Set it **deterministically with `ffmpeg -vf hflip`** in post. (Mirrors text/asymmetry, fine for candid shots.)
- **Animate a LOCAL still** with Seedance by passing it as a **base64 data URI** in `image_url` (`data:image/png;base64,…`) — no hosting/upload step needed.
- **Split-screen / two-shot** — stack two real stills with `ffmpeg` `vstack` (scale+crop each to half-height) rather than generating; guarantees both subjects look like themselves.
- **Cutaway questioner** (interview format) — a profile/at-the-mic framing **hides lip-sync**, so the questioner needs only TTS voice + subtle Seedance motion, not a true talking-head. Far cheaper than a second avatar.
- **External talking-head** (e.g. HeyGen) is the right tool for a character delivering long on-camera dialogue with lip-sync; the kit handles everything around it (questioner, B-roll, assembly). It plugs in at the animate stage.

## Generation modes (dual)
Same pipeline (brief → shot list → storyboard plan), two ways to make pixels — only the final step differs:
- **Connector (auto):** a fal connector is present (Claude Code / Cowork, or claude.ai once fal supports OAuth) → generate directly via the fal MCP tools below.
- **Manual (prompts):** no connector (e.g. **claude.ai today** — fal's MCP requires OAuth it doesn't support yet) → **emit copy-paste prompts**; the user generates in their own tools (OpenArt / Higgsfield / HeyGen / Submagic). **Never block on a missing connector** — the direction is the value.

## Via the fal MCP connector (tools)
The fal MCP exposes: `search_models`, `get_model_schema`, `get_pricing`, `run_model` (submit + wait), `submit_job` + `check_job` (long jobs), `upload_file`, `recommend_model`. Invoke any model with **`run_model`** (or `submit_job`/`check_job` for video) passing `endpoint_id` (e.g. `fal-ai/nano-banana/edit`, `fal-ai/flux/dev`, `bytedance/seedance-2.0/image-to-video`, `fal-ai/minimax/speech-2.8-hd`) + an `input` object (same params as the REST bodies above). The REST/Bash calls above are the raw-scripting equivalent. Auth = your fal API key (Bearer). ⚠️ claude.ai browser connectors require OAuth (fal: not yet) → in claude.ai use Manual mode.
