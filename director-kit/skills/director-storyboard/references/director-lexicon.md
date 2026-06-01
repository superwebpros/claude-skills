# Director's Lexicon — Filmmaking Vocabulary for AI-Video Prompts

> Purpose: translate the language of directing into drop-in phrasing for AI-video prompts (OpenArt, Higgsfield, fal.ai). Use the prompt phrases verbatim or as building blocks. Describe only what is literally visible (see "Uninflected Shot Rule").

---

## Shot Sizes

How much of the subject/world fills the frame. Smaller framing = more intimacy/intensity; wider = more context/world.

| Size | Definition | Drop-in prompt phrase |
|---|---|---|
| Extreme wide (EWS) | Subject tiny in a vast environment; establishes world/scale. | `extreme wide shot, lone figure dwarfed by a vast desert landscape` |
| Wide (WS) | Full subject head-to-toe with surrounding space. | `wide shot of a man standing alone in an empty bar` |
| Medium wide (MWS) | Roughly knees-up; subject and immediate space. | `medium wide shot, woman from the knees up walking toward camera` |
| Medium (MS) | Roughly waist-up; conversational, neutral. | `medium shot of a man seen in a window reflection, waist up` |
| Medium close-up (MCU) | Chest/shoulders up; emphasizes face while keeping some context. | `medium close-up on a face, chest and shoulders in frame` |
| Close-up (CU) | Face fills the frame; emotion. | `close-up of a nervous face, eyes darting` |
| Extreme close-up (ECU) | A single detail fills frame (eyes, hands, mouth). Use sparingly for max impact. | `extreme close-up on trembling hands` / `extreme close-up on a throat tightening as he swallows` |
| Over-the-shoulder (OTS) | Framed past one person's shoulder onto another; conversation/POV anchor. | `over-the-shoulder shot looking past a man toward a woman across the room` |
| "Dirty" shot | A shot with deliberate out-of-focus foreground blocking part of frame (not a clean shot of the subject). | `dirty shot, out-of-focus foreground object framing the subject` |
| POV | What a character literally sees; camera = their eyes. | `POV shot from the doorway looking into a classroom of students` |

Impact note: in the Casablanca breakdown, ECUs are rationed — only 3 in the whole scene — so a single ECU reads as a major emotional beat. Treat ECU as a deliberate punctuation mark in prompts, not a default.

---

## Camera Movements

| Move | Definition | Drop-in prompt phrase |
|---|---|---|
| Dolly | Camera body moves forward or backward. | `slow dolly in toward the subject` / `dolly out revealing the room` |
| Truck | Camera moves laterally side-to-side (whole body slides). | `trucking shot moving left to right alongside the subject` |
| Pedestal | Camera moves straight up or down (booms vertically) without tilting. | `pedestal up rising from waist level to eye level` |
| Pan | Camera pivots horizontally on a fixed point. | `slow pan from the piano across to a watching face` |
| Tilt | Camera pivots vertically on a fixed point. | `tilt up from the feet to the face` |
| Crane / jib | Camera lifts/sweeps through space on an arm; sweeping vertical+lateral move. | `sweeping crane shot rising above the crowd` |
| Push-in / pull-out | Move closer (push-in, builds intensity) or away (pull-out, releases/reveals). Often via dolly. | `slow push-in on the face` / `pull-out to reveal the empty hall` |
| Tracking | Camera follows a moving subject, keeping pace. | `tracking shot following a man as he walks down a hallway` |
| Whip / swish pan | Very fast pan that blurs between subjects; energetic transition. | `fast whip pan, motion blur transition to the next subject` |
| Handheld | Camera held by operator; organic shake, immediacy/realism. | `handheld shot, subtle natural shake` |
| Stabilizer / gimbal | Smooth glide while moving (the modern default look). | `smooth gimbal move gliding alongside the subject` |

Notes from source: "static" is the default and need not be stated (no movement = locked-off). A dolly just means moving forward/back; if shot from a stabilizer it's the smooth modern equivalent of handheld. Source gives no guidance on which moves AI tools render well vs. poorly, so none is asserted here.

---

## The "Uninflected Shot" Rule

Describe ONLY what is literally visible in the frame — never intent, emotion, backstory, or what a character "wants." Meaning is created later by juxtaposition (the cut), not loaded into the single shot. This is the single most important habit for prompting AI video, which renders literal visual content, not narrative intent.

Why it matters for prompting: AI tools can't draw "waiting anxiously" — they draw a man and a doorknob. Inflected language produces vague or wrong outputs; uninflected language produces exact, controllable frames. Stack uninflected shots in sequence to build the story.

| Inflected (bad) | Uninflected (good) |
|---|---|
| man waiting nervously for the professor | `man walks down a hallway` / `a hand on a doorknob` |
| she realizes he's in danger | `woman looks down at a table, then looks up` |
| he prepares his argument | `man takes a notebook out of a bag` / `a hand writing on a page` |
| nervous man approaches the girl | `man runs his fingers through his hair` / `a throat tightening as he swallows` / `man walks toward a woman holding a piece of paper` |

Rule of thumb: if the word implies a feeling or a goal ("waiting," "realizes," "wants," "nervously"), strip it. Keep nouns, visible actions, and physical detail.

---

## Takes vs. Shots vs. Setups

A planning hierarchy — knowing which is which is how you budget time and order a shot list.

- **Take** — one continuous recording (camera starts → stops). Many takes can capture the same shot. Cheap; you do lots of these.
- **Shot** — a distinct framing. It becomes a new shot when you change the lens or reframe/point the camera somewhere significantly different. Medium cost.
- **Setup** — a new physical camera position. Most expensive: moving the camera means moving lights and most of the rig. Minimize and batch these.

Why it matters: setups eat the most time. Group your shot list by setup (shoot everything from one camera position before moving) to optimize the schedule. Lens change = new shot but maybe same setup; camera relocation = new setup.

---

## Photographic / Optical Concepts (Day 6)

Plain-English effect + the prompt phrase that achieves the look.

### Lenses — focal length
Changes perspective and the felt distance between subject and background.
- **Wide / short lens (e.g., 25mm):** wider field of view; backgrounds feel farther away and smaller; up close it distorts faces (looks unnatural). Use for environment, energy, distortion.
  - `shot on a 25mm wide lens, expansive background, faces close to camera`
- **Standard/telephoto (e.g., 85–100mm):** compresses space; flattering, natural faces; background feels closer and larger. The portrait sweet spot.
  - `shot on an 85mm lens, flattering compressed portrait, background pulled in close`
- **Long telephoto (e.g., 240mm):** extreme compression; background looms huge behind subject; over-flattens faces (ears push forward) if too long.
  - `shot on a 240mm telephoto lens, heavily compressed perspective, massive background looming behind the subject`

### Aperture / Depth of Field
F-stop sets how much is in focus. Low f-number = wide opening = shallow focus; high f-number = small opening = deep focus.
- **Shallow DoF (low f-stop, e.g., f/1.4–f/2.8):** subject sharp, background a soft blur (bokeh). Isolates subject; hides ugly backgrounds. Needs fast/prime lens.
  - `shallow depth of field, creamy bokeh, subject isolated against blurred background, shot at f/1.4`
- **Deep DoF (high f-stop, e.g., f/16–f/40):** everything sharp foreground to background (the Citizen Kane look).
  - `deep depth of field, everything in sharp focus from foreground to background, shot at f/16`
- Bokeh = the quality of the out-of-focus blur. `soft creamy bokeh`, `blurred background highlights`.

### Shutter Speed — motion blur & the 180° rule
Controls motion blur. Standard cinema = shutter at 1/48s for 24fps (the "180-degree rule"): shutter open half the time = natural motion blur.
- **Standard / 180° (1/48s):** natural cinematic blur; default, romantic/drama feel.
  - `natural cinematic motion blur, 180-degree shutter look`
- **Slower (e.g., 1/24s):** heavy blur, frames smear together; dreamy/creamy or messy.
  - `heavy motion blur, smeared dreamy movement, slow shutter`
- **Faster (e.g., 1/500s):** zero blur; crisp, choppy, hyper-alert. Action/fight scenes (Gladiator), heightened/jittery reality.
  - `high shutter speed, crisp sharp motion, choppy staccato action, no motion blur`

### Film Speed / ISO — grain & low-light
Sensor sensitivity. Keep low for clean images; raise only when forced — it adds noise/grain.
- **Low ISO (100):** cleanest image, needs lots of light.
  - `low ISO, clean image, minimal grain`
- **High ISO (800–2000+):** brighter in low light but noisy/grainy; vintage disposable-camera or gritty low-light feel.
  - `high ISO, heavy grain, noisy low-light footage` / `grainy disposable-camera look`

### Aspect Ratio & Resolution
Frame shape, chosen by genre and delivery. Decide before shooting.
- **16:9** — universal screen standard; safe default. `16:9 widescreen`
- **1.85:1** — comedy/drama/rom-com; frames faces and intimacy well. `1.85:1 aspect ratio, intimate framing`
- **2.35:1** — epic/action/space; ultra-wide, packs world into frame even on close-ups. `2.35:1 cinematic widescreen, epic anamorphic framing`
- **4:3** — near-square; IMAX native, comic-book/heroic stacking (Snyder's Justice League). `4:3 aspect ratio, boxy IMAX framing`
- **9:16 vertical** — social/mobile delivery. `9:16 vertical format for social media`
- Resolution: max it out (4K). `4K resolution`

### Gamma / Post / Color Grade
Capture format vs. final look.
- **Standard/baked-in:** camera processes the image; looks fine immediately, little flexibility.
- **RAW / Log:** footage comes out flat & washed-out but holds far more data in highlights/shadows (data kept in the middle, 0–1023), enabling heavy color grading later — change color temperature, recover highlights/shadows, craft a custom look.
  - Flat capture: `flat log color profile, low contrast, washed-out for grading`
  - Final graded looks (what you actually prompt for the end image): `cinematic color grade, teal and orange`, `cool desaturated Antarctica color grade`, `warm filmic LUT`, `high dynamic range, rich highlights and shadow detail`

---

## Shot List Fields Cheat

Columns of a proper shot list. Type all uninflected descriptions first, then pass back through adding size/movement/lens/notes.

| Field | What goes in it |
|---|---|
| Scene # | Groups shots by scene (e.g., 1). |
| Shot # | Sequential within scene (1, 2, 3…). Prefix `V` if VFX (affects slating). |
| Description (uninflected) | Only what's visible: `man walks down hall`, `hand on doorknob`. |
| Shot size | EWS / WS / MWS / MS / MCU / CU / ECU / OTS / dirty / POV. |
| Movement | dolly / truck / pedestal / pan / tilt / crane / tracking / whip pan / handheld / gimbal (omit if static). |
| Lens | focal length, e.g., 25mm / 85mm / 240mm. |
| Notes | equipment, est. time, start time (sun position), prep time, lighting, sound, VFX, setup grouping. |
