---
name: meta-ads-ops
description: Use when reading or changing Meta (Facebook/Instagram) ads through the Marketing/Graph API — pulling insights by ad, placement or video retention, cloning a video creative with new videos or UTMs, adding or pausing ads, editing ad set placements, or when a Meta change "didn't take", an ad won't deliver, or a new ad gets no spend.
compatibility: Python 3.11+, standard library only (runs with python3 or uv run). Needs network access to the Graph API or a relay.
metadata:
  author: superwebpros
  version: "1.0"
---

# Meta ads operations

Mechanics only. For *whether* to make a change (test design, sample size, read points), use `paid-media-strategy` first.

## Setup

| Variable | Meaning |
|---|---|
| `META_GRAPH_BASE` | Default `https://graph.facebook.com/v21.0`. Point it at a relay in a sandbox. |
| `META_TOKEN` | Optional. Unset = no token is sent (the relay injects it). Never print it. |

From a shell with plain curl, always use `curl -g` (Graph URLs contain `{}` and `[]`).

## Scripts

```bash
S=<this-skill-dir>/scripts
python3 $S/insights.py --campaign <ID> --preset maximum                 # per ad + TOTAL
python3 $S/insights.py --campaign <ID> --preset yesterday --by placement # per ad x placement
python3 $S/insights.py --campaign <ID> --since 2026-01-01 --until 2026-01-03 --json
python3 $S/clone_creative.py --account act_<ID> --creative <SRC> --video-9x16 <V1> --video-4x5 <V2> --suffix v2-hook   # dry run
python3 $S/set_placements.py --adset <ID> --drop facebook:feed          # dry run; add --apply to write
```

`insights.py` gives spend, CPM, link clicks + CTR, landing page views, hook rate (3s views / impressions), ThruPlay rate, p25→p100 retention, checkouts, purchases, cost per checkout and ROAS. A rate whose denominator is 0 is `None`/`—`, never 0. Writes default to dry run.

## Quirks that bite

| Quirk | What to do |
|---|---|
| **Activation doesn't cascade.** Campaign, ad set and ad each have their own status. | Set `status=ACTIVE` on each level you need; check `effective_status` on all three. |
| **Creatives are immutable.** | New video, opening or UTM = a new creative, then a new ad (or `POST /<ad_id>` with `creative={"creative_id": …}`). |
| **Give each creative its own `utm_content`.** A clone keeps the source's `url_tags`. | Change `utm_content` when cloning, or the site and checkout can't tell versions apart. |
| **Placement asset customisation**: one creative, 9:16 video for Stories/Reels, 4:5 for Feed/Explore, via `asset_customization_rules` keyed to video labels. | Clone with `clone_creative.py`; it maps videos by labels ending `9x16` / `4x5`. Strip `additional_data`, label ids and echoed `age_min`/`age_max` before re-posting. |
| **Uploaded videos get re-hosted** under new ids inside the creative. | Verify by the video `title` / `length`, not by id. Wait for `status.video_status == ready` before using thumbnails. |
| **New ads beside an incumbent get starved** (often 3–4× less spend on day 1). | A new ad with little delivery is unread, not losing. To force a read, pause the incumbent or split ad sets. |
| **Significant edits reset learning** (targeting, placements, optimisation event, big budget moves, new ads). | Expect a few uneven days; batch edits. |
| **Dropping a placement** = edit `targeting.facebook_positions` / `instagram_positions`. | `set_placements.py` reads targeting, changes only the lists, writes the full object, and checks nothing else moved. |
| `ad_review_feedback` is not a field on ads. | Use `effective_status` and `issues_info`. |
| New ads show `IN_PROCESS` / `PENDING_REVIEW` after activation. | Normal; delivery starts after review (minutes to ~2 h). |
| Insights lag a few hours and change for ~3 days. | Judge yesterday's numbers the next morning, not same-day. |
| Purchase optimisation with ~1 purchase/week never exits learning (needs ~50/week). | Consider optimising for a higher-volume event, or accept a noisy auction. |

## Action types used

`landing_page_view`, `offsite_conversion.fb_pixel_view_content`, `offsite_conversion.fb_pixel_initiate_checkout`, `offsite_conversion.fb_pixel_purchase` (value in `action_values`), `video_view` (= 3-second views). Video fields: `video_thruplay_watched_actions`, `video_p25…p100_watched_actions`, `video_avg_time_watched_actions`.

## Before any write

1. Know the test it belongs to and its read point (`paid-media-strategy`).
2. Dry run, read the diff, then `--apply`.
3. Create ads **PAUSED**; activate only after a human's go-ahead if money is involved.
4. Log the change in the campaign decision log with its reason and read point.
