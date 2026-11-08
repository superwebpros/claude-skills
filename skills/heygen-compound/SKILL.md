---
name: heygen-compound
description: >
  Use for any HeyGen video generation, avatar render, or reel voiceover task.
  The canonical guide is AGENTS.md in the private superwebpros/heygen-production
  repo and the one true command is heygen-render. Load this before rendering,
  choosing an avatar or voice, formatting a HOOK/BODY/CTA script, adding
  ElevenLabs audio tags, or debugging HeyGen auth, 402 insufficient_credit, or
  tags being spoken aloud.
compatibility: >
  Requires a local checkout of the private superwebpros/heygen-production repo
  (set HEYGEN_PRODUCTION_DIR to its path), its heygen-render command on PATH,
  and the heygen CLI authenticated via OAuth. Script-formatting rules in
  references/ are usable without the repo.
metadata:
  canonical-source: "superwebpros/heygen-production (private): AGENTS.md and docs/"
---

# HeyGen

**All HeyGen generation is governed by `$HEYGEN_PRODUCTION_DIR/AGENTS.md`**, the
`AGENTS.md` at the root of a checkout of the private `superwebpros/heygen-production`
repo. Read it before generating any video.

That repo is canonical for auth, script formatting, avatar selection, render
defaults, and where output goes. It supersedes every other HeyGen instruction,
including earlier versions of this skill, which pointed at an older Python script
that is now a stub that exits non-zero.

**Prerequisite.** If `HEYGEN_PRODUCTION_DIR` is unset or the checkout is missing,
stop and tell the human. Without the repo you can still author and check scripts
against [references/script-formatting.md](references/script-formatting.md), but do
not render with ad-hoc API calls or the MCP tools (see below).

## That repo is READ-ONLY unless you are working inside it

Unless your working directory **is** the heygen-production checkout, you may read
its docs and run `heygen-render`, nothing more. Do **not** edit its code, docs,
defaults, `.beads` memories, or this skill file, even to correct something you are
sure is wrong. Editing HeyGen settings from scattered workspaces is exactly what
produced the contradicting instructions that repo was built to replace; a fix
applied from outside adds an opinion instead of settling one.

If something is wrong, missing, or blocking you, file a request and stop:

```bash
bd -C "$HEYGEN_PRODUCTION_DIR" create "<one-line ask>" -t feature -p 2 -d \
"USE CASE: what you were doing, and from which workspace.
RATIONALE: why the current behaviour is wrong or insufficient.
TRIED: what you ran, verbatim, and what happened.
PROPOSED: the change you would make, as a suggestion, not a decision."
```

Then tell the human. That bead is the only write you may make there.

## Render

```bash
heygen-render /abs/path/to/script.md --out /abs/path/to/piece/footage/
```

Run `--dry-run` first: it prints the exact spoken text, the resolved recipe, and
the payload without spending credits. **Read the VO text it prints**; that is
the whole safeguard.

`--out` is required for a real render (or a `media_path` frontmatter naming a
`<YYYY-MM>_<slug>` piece folder). There is no cwd default, and writing into the
service repo itself is refused.

The renderer blocks on **contamination only**: an unknown `[bracketed]` tag, a
`#`/`**`/markdown link/list marker in spoken text, an empty VO, or a missing
`HOOK`/`BODY`/`CTA`. It reports the offending span with its line number and
exits `2`.

**A runtime-budget overrun warns and still renders.** A 70-second "reel" may be
the right call. There is no `--force`, because there is no hard block to escape;
`--strict` is the opt-in for treating an overrun as an error instead.

## The three things agents get wrong

1. **Auth is OAuth**, via the heygen CLI's stored credentials (subscription
   ledger, premium credits). Never pass a key. `HEYGEN_API_KEY` is a $0
   pay-as-you-go wallet and it *overrides* stored credentials in the CLI.
   `heygen-render` scrubs it from every subprocess; a bare `heygen` call does
   **not**, so drive the CLI by hand as `env -u HEYGEN_API_KEY heygen …`.
   Details: [references/auth.md](references/auth.md).
2. **Publication metadata must sit after `<!-- END VO -->`.** Otherwise headings
   and hashtags land in the voiceover and get read aloud. Audio tags must come
   from the vocabulary: `thoughtful`, `serious`, `reassuring`, `confident`,
   `curious`. Details: [references/script-formatting.md](references/script-formatting.md).
3. **Don't use the HeyGen MCP tools for final renders.** They cannot express
   `voice_settings.engine_settings`, so `eleven_v3` is never selected and
   ElevenLabs audio tags are spoken aloud. Read-only queries (list avatars,
   voices, videos, check status) are fine.

## Avatars and output

The house avatar/voice defaults, the avatar registry, and the filing rules for
rendered media live only in the private repo: `docs/avatars.md` and `AGENTS.md`
sections on avatars and output. Key rule worth repeating: 9:16 needs a
**portrait** avatar; a landscape one letterboxes and the take is wasted. Keep
rejected takes, and never rename original footage.

The references here are a snapshot for convenience. If they disagree with
`$HEYGEN_PRODUCTION_DIR/docs/`, the repo wins.
