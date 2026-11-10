---
name: news-minute
description: Turn a short list of news picks into a spoken, avatar-ready "news minute" script (HOOK / BODY / CTA, heygen-render authoring contract), checked against the sources. Use whenever a bot or person is writing a daily or weekly news-roundup video script from a brief of picks (title, source, URL, summary). Voice, audience, length and banned words come from the show's context pack, never from this skill. Not for ads (ad-scriptwriter) or long-form lessons.
metadata:
  owner: "SuperWebPros"
---

# News Minute

A **news minute** is one short spoken segment that tells a specific audience what in the news matters to *them*, and why, in under a minute. This skill is the method. The **show pack** (a folder of `voice.md`, `audience.md`, `rules.md`, `learnings.md`, `README.md`) is the context: who's talking, to whom, how long, which words are banned, what the CTA is. Read the whole pack before writing. When the pack and this skill disagree, **the pack wins**.

## Inputs

- **The brief**: a JSON list of picks. Each has at least `title`, `source_name`, `url`, and usually `summary`, `excerpt`, `theme`, `published_at`, scores. There may also be `runners_up`.
- **The show pack**: path given by whoever runs you (e.g. `context.show = impact-minute` → that show's folder).

## Method

### 1. Check facts before writing a word

For every pick you might use:

1. Open the `url` and read enough to confirm the claim you'd make. If you can't open it (paywall, block, error), you may rely on `summary`/`excerpt` only, and you must attribute ("Reuters reports…").
2. Write down, for each story, **one sentence of what happened**, with the number, name or date exactly as the source states it. That sentence is the only factual claim you may make about the story.
3. **Drop** a story when: the source doesn't support the headline; the item is a forum or social post whose claim you can't trace to a primary source (you may still use it, framed as "people are arguing about…", only if the pack allows); it's older than the pack's freshness window.

**Hooks, transitions and generalizations are claims too.** "Almost everyone uses AI", "everyone is buying", "very few are making money" are factual statements; make them only if a source supports them, and in the source's terms ("nine in ten companies surveyed…"). Stay inside the source's scope ("surveyed respondents" is not "everyone"; "limited evidence" is not "no effect"); faithful spoken paraphrase ("nine in ten" for nearly 90%) is fine unless the pack is stricter. Never add a fact from memory. Never round, inflate or "simplify" a number into a different claim (42% is not "nearly half of all companies" unless the source says so). If two sources conflict, say less.

### 2. Choose and order

- Use **fewer stories, said well**, rather than all of them. The pack sets the maximum; one to three is typical for under a minute.
- Order: the story with the clearest "so what" for the audience goes first (it's the hook). End on the most actionable one.
- A runner-up may replace a pick that fails the fact check. Say which you swapped and why in your notes (never in the voiceover).

### 3. Write each story as: what happened → why it matters to the audience

- **What happened**: one or two plain sentences. Attribute: "Gartner surveyed CMOs and found…".
- **Why it matters**: one or two sentences in the audience's terms (the pack's `audience.md`): what they should notice, decide, or do. This is the show's value; a headline alone is not a segment.
- No hype words, no breathless framing, no prediction stated as fact. If the pack has a framework to apply (e.g. a method name), apply it here, lightly, at most once per script.

### 4. Shape it for the ear

- **HOOK** = the **lede** (1–2 sentences): the day's most consequential fact, stated sharply and specifically, newsroom style. Prefer a declarative fact over a question. No greetings, no "welcome to", no show name first (the pack may put the show name in the CTA).
- **BODY**: the stories, with spoken transitions ("Second…", "Meanwhile…", "And one more…").
- **CTA** (1–2 sentences): exactly the pack's CTA pattern.
- Short sentences. One idea per sentence. Write numbers as they should be said when it matters ("forty-two percent" is fine as `42%`; the voice reads it; avoid symbols like `~`, `>`, `/`).
- Read it aloud in your head at the pack's pace. Cut until it fits the word budget **with room to breathe**.

### 5. Format: the heygen-render authoring contract

The output must render without edits. Follow `heygen-production/docs/script-formatting.md` (rules R1–R7). The short version:

```markdown
---
format: reel
show: <show slug>
date: <YYYY-MM-DD>
writer: <model or person>
stories: [<url>, <url>]
---

# <Show name>: <YYYY-MM-DD>

**[VISUAL NOTES: optional direction for the editor, e.g. lower-third per story with the source name]**

**HOOK:**
<voiceover>

**BODY:**
<voiceover; may use the audio tags below>

**CTA:**
<voiceover>

<!-- END VO -->

## Sources
- <source name>: <url>
```

- Labels exactly `**HOOK:**`, `**BODY:**`, `**CTA:**`, line-initial, in that order.
- `<!-- END VO -->` on its own line after the CTA, before anything else.
- Inside the voiceover: **no** `#`, `**`, `---`, links, URLs, list markers, or square brackets other than these audio tags: `[thoughtful]`, `[serious]`, `[reassuring]`, `[confident]`, `[curious]`. Lowercase, at the start of the sentence they govern. Use two or three per script, not one per sentence.
- Sources, notes and metadata go **after** `<!-- END VO -->` only.

### 6. Self-check before handing it over

- [ ] Every factual sentence traces to step 1's notes; every number matches its source exactly.
- [ ] Word count of HOOK+BODY+CTA is inside the pack's budget (count it; don't estimate).
- [ ] No banned words from the pack; no markdown or URLs in the voiceover; only allowed audio tags.
- [ ] The hook is about the audience's problem, not about the show.
- [ ] Read it aloud once. Anything you stumble on, rewrite.

Then, if `heygen-render` is available, run `heygen-render --dry-run <file>` and read the voiceover it prints. That printed text is what will be spoken.

## Output

The script file only, plus (separately, if asked) a short note: stories used, stories dropped and why, any runner-up swapped in, word count.
