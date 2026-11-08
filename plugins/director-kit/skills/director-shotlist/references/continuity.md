# Continuity — the director layer that separates "cool images" from a film

> AI generates each shot in isolation, so it has no memory of story-state. Continuity is what you impose on top. Four dimensions — lock all four.

## The 4 dimensions
1. **Identity** — characters/props look the same shot-to-shot. *Locked by:* the asset layer (reference images reused via nano-banana/edit).
2. **Prop** — the same object recurs and tracks (the can opener in shot 1 IS the one revealed in shot 23). *Locked by:* prop assets, fed as refs.
3. **Location** — sets don't drift (the bedroom is one bedroom). *Locked by:* location assets, fed as refs.
4. **Period / world** — lighting tech, props, wardrobe cohere to one era. *Locked by:* the World/Period bible (`assets/world.md`). (e.g. a rotary phone ⇒ mid-20th-C ⇒ electric lamplight, not candles.)

The asset layer (`assets/`) is the system-of-record for dimensions 1–3; the world bible for 4.

## Dramatic-object extraction (do this at the brief stage)
A competent director reads the source/brief and **names the object(s) of value** — the MacGuffin, the thing wanted/feared-for — and its **arc**. Without this, a heist has no stakes and a twist has nothing to misdirect from.
- Identify: what is coveted / at risk / the target? (e.g. *Frances the cat* = the cat-napping target.)
- Give it an arc: typically **established → escalated/endangered → resolved** (coveted → endangered → saved).
- Every object of value must be **planted** early and **tracked** through to payoff.

## The continuity ledger (carry story-state shot-to-shot)
Maintain a per-shot table (keep a `CONTINUITY_LEDGER.md` in your creative folder). Columns:
`# | shot | present (chars/props/location) | blocking/position | dramatic-object status | hidden/withheld items`
- **Feed the prior shot's state into each generation prompt** (e.g. "David STILL crouched at the bag" prevents a teleport).
- Mark presence/absence **deliberately** — a tight face CU legitimately omits the cat; a wide shot that drops it is an error.

## The continuity critic pass (run before animating)
Review the drafted shotlist/storyboard and flag:
- [ ] **Blocking jumps** — a character/object teleports or changes pose with no motivated cut.
- [ ] **Unmotivated presence/absence** — an element appears/vanishes without reason.
- [ ] **Objects of value** — is each one planted early and escalating, or just set-dressing?
- [ ] **Period anachronisms** — lighting tech, props, wardrobe off-era (the candle-in-an-electrified-house trap).
- [ ] **Repetitive framing** — several near-identical shots in a row (vary size/angle; also kills mid-piece sag).
- [ ] **Off-model** — a character/prop/location drifted from its locked asset.
- [ ] **Screen direction (eyeline)** — in an intercut conversation the two speakers must face OPPOSITE screen directions (one screen-left, one screen-right) or the cut won't read as an exchange. Decide it from the fixed footage first (e.g. the avatar faces left ⇒ the other faces right). nano-banana can't reliably set left/right — fix deterministically with `ffmpeg -vf hflip`.
Output a flagged list for the human; regenerate the offenders (cheap, stills). Human approves intent; the skill tracks + flags.
