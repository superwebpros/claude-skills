---
name: paid-media-strategy
description: Use when reading paid-ad results (Meta, Google, any platform), recommending a campaign change, judging a creative or placement, comparing two runs, or writing daily/weekly ad commentary — especially early in a run, with small numbers, or when someone says "pause it", "it's not working", "scale it", or "which ad won".
metadata:
  author: superwebpros
  version: "1.0"
---

# Paid-media strategy

Platform-neutral judgment for paid campaigns. Platform mechanics (APIs, placements, quirks) live in the platform skill, e.g. `meta-ads-ops`.

**Core principle: every change is a test, and a test is only read at its read point.** Early numbers are noise until the sample says otherwise.

## Before you recommend anything

1. **Read the campaign decision log** (e.g. `decisions.jsonl`) for this run. List the active decisions and their read points.
2. **Anything a pending decision covers is under test.** Do not recommend pausing, cutting, switching or replacing it, and do not call it failing, before its read point. Say "pending until $X" instead.
3. **Check the registry/checkpoint criteria.** Checkpoints decide; commentary interprets. Below the first checkpoint, the default answer is "hold, and watch X".

## Every change is a test

A recommendation is complete only with all five parts, written before the change and logged in the decision log:

| Part | Example |
|---|---|
| Change | Remove Facebook feed from the ad set's placements |
| Why (evidence with counts) | Feed took 40% of impressions, 3s rate 15%, link CTR 0.17% (2 clicks) |
| Metric | Link CTR and 3s view rate, run-wide |
| Read point | At ~$350 cumulative spend |
| Decision rule | Keep if CTR rises and 3s rate ≥ 25%; otherwise revisit placements |

## Sample sense

- Report every rate **with its count**: "0.68% (13 clicks / 1,903 impressions)", never "0.68%".
- Give a rough interval for small counts. For k events, a 95% range is about k ± 2√k (13 clicks → ~6–20 → 0.35%–1.1%). If the range straddles the threshold, say "can't tell yet".
- **No winner** with fewer than ~15 events per arm or less than ~$150 spend per arm.
- An arm the platform barely delivers (e.g. a new ad beside an incumbent) is unread, not losing.

## Like-for-like comparisons

Compare at **matched spend** or **matched days since first delivery** (not launch date), on the **same optimisation event** and the **same placements**. Say when they aren't comparable:
- Traffic/LPV-optimised runs buy cheap clickers; their CTR is not a benchmark for conversion-optimised runs.
- A run that never used a placement can't be compared overall with one that did; compare placement by placement.

## Creative read order

Read by placement first, then overall. Stop at the first broken stage; that's the fix.

| Stage | Metric | Typical healthy (cold, vertical video) |
|---|---|---|
| Hook | 3-second views / impressions | 25–30%+ |
| Hold | ThruPlay (15s) / impressions; quartile drop-off | p25→p100 retention steady |
| Click | Link CTR | depends on offer: free ≫ paid |
| Intent | Landing page views / link clicks | ≥ 60%; low = accidental taps or slow page |

High CTR with low hook and low LPV/click (often Stories) usually means accidental taps, not interest.

## Not yours to decide

- Budget split **across platforms** (Meta vs Google): a human's call.
- Price, offer and funnel strategy: recommend with evidence; the owner decides.

## Red flags — stop and re-read this skill

| Thought | Reality |
|---|---|
| "Pause it immediately" before the first checkpoint | Hold; name what to watch and when you'll read it |
| "The new ad has 0 conversions, kill it" | It's unread until it has the sample, not losing |
| "CTR is 0.6% vs 0.9% target, it's failing" | Check the interval and the spend vs the checkpoint |
| "Last campaign got 3% CTR" | Was it the same optimisation event and placements? |
| Recommending a change already in the decision log | Read the log first |

Worked example (a full early-run read, with the decisions it produced): [references/worked-example.md](references/worked-example.md).
