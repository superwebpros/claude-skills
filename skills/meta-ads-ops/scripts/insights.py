"""Pull Meta ad insights and compute the funnel, video and cost maths.

  python3 insights.py --campaign <ID> [--preset yesterday|today|maximum|last_7d | --since D --until D]
                      [--level ad|campaign] [--by placement] [--json]

Rates are None (not 0) when the denominator is 0. Counts are always shown beside rates.
"""
import argparse
import json
import sys

FIELDS = ("ad_id,ad_name,spend,impressions,frequency,inline_link_clicks,actions,action_values,"
          "video_thruplay_watched_actions,video_p25_watched_actions,video_p50_watched_actions,"
          "video_p75_watched_actions,video_p100_watched_actions,video_avg_time_watched_actions")
ACTIONS = {
    "lpv": "landing_page_view",
    "view_content": "offsite_conversion.fb_pixel_view_content",
    "checkouts": "offsite_conversion.fb_pixel_initiate_checkout",
    "purchases": "offsite_conversion.fb_pixel_purchase",
    "video_3s": "video_view",
}
VIDEO = {"thruplay": "video_thruplay_watched_actions", "p25": "video_p25_watched_actions",
         "p50": "video_p50_watched_actions", "p75": "video_p75_watched_actions",
         "p100": "video_p100_watched_actions"}
COUNTS = ("spend", "impressions", "link_clicks", "value", *ACTIONS, *VIDEO)


def _action(row: dict, key: str, action_type: str | None = None) -> float:
    for a in row.get(key) or []:
        if action_type is None or a.get("action_type") == action_type:
            return float(a.get("value", 0))
    return 0.0


def counts(row: dict) -> dict:
    c = {"spend": float(row.get("spend", 0)), "impressions": int(row.get("impressions", 0)),
         "link_clicks": int(row.get("inline_link_clicks", 0) or 0),
         "value": _action(row, "action_values", ACTIONS["purchases"])}
    for k, t in ACTIONS.items():
        c[k] = _action(row, "actions", t)
    for k, f in VIDEO.items():
        c[k] = _action(row, f)
    return c


def _ratio(n, d, scale=1.0):
    return round(scale * n / d, 4) if d else None


def derive(c: dict) -> dict:
    """Add rates to a counts dict. None when the denominator is 0."""
    out = dict(c)
    out.update(
        ctr_pct=_ratio(c["link_clicks"], c["impressions"], 100),
        cpm=_ratio(c["spend"], c["impressions"], 1000),
        cost_per_click=_ratio(c["spend"], c["link_clicks"]),
        lpv_per_click_pct=_ratio(c["lpv"], c["link_clicks"], 100),
        hook_rate_pct=_ratio(c["video_3s"], c["impressions"], 100),
        thruplay_rate_pct=_ratio(c["thruplay"], c["impressions"], 100),
        p25_to_p100_pct=_ratio(c["p100"], c["p25"], 100),
        cost_per_checkout=_ratio(c["spend"], c["checkouts"]),
        cost_per_purchase=_ratio(c["spend"], c["purchases"]),
        roas=_ratio(c["value"], c["spend"]),
    )
    return out


def summarize(rows: list[dict]) -> dict:
    total = {k: 0.0 for k in COUNTS}
    for r in rows:
        for k, v in counts(r).items():
            total[k] += v
    total["impressions"] = int(total["impressions"])
    total["link_clicks"] = int(total["link_clicks"])
    return derive(total)


def label(row: dict, by_placement: bool) -> str:
    name = row.get("ad_name") or row.get("campaign_name") or "total"
    if by_placement:
        name += f" | {row.get('publisher_platform', '?')} {row.get('platform_position', '?')}"
    return name


def _fmt(v):
    return "—" if v is None else (f"{v:,.2f}" if isinstance(v, float) and not v.is_integer() else f"{v:,.0f}")


def table(items: list[tuple[str, dict]]) -> str:
    cols = ["spend", "impressions", "cpm", "link_clicks", "ctr_pct", "lpv", "hook_rate_pct",
            "thruplay_rate_pct", "checkouts", "purchases", "roas"]
    lines = ["\t".join(["row", *cols])]
    lines += ["\t".join([name[:60], *(_fmt(m.get(c)) for c in cols)]) for name, m in items]
    return "\n".join(lines)


def main(argv=None) -> int:
    import graph
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--campaign", required=True, help="campaign (or ad set / ad) id")
    ap.add_argument("--level", default="ad", choices=["ad", "adset", "campaign"])
    ap.add_argument("--preset", default="yesterday")
    ap.add_argument("--since"); ap.add_argument("--until")
    ap.add_argument("--by", choices=["placement"])
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    params = {"level": a.level, "fields": FIELDS, "limit": 200}
    if a.since and a.until:
        params["time_range"] = {"since": a.since, "until": a.until}
    else:
        params["date_preset"] = a.preset
    if a.by == "placement":
        params["breakdowns"] = "publisher_platform,platform_position"
    rows = graph.get_all(f"{a.campaign}/insights", **params)
    items = [(label(r, a.by == "placement"), summarize([r])) for r in rows]
    items.append(("TOTAL", summarize(rows)))
    print(json.dumps(dict(items), indent=1) if a.json else table(items))
    return 0


if __name__ == "__main__":
    sys.exit(main())
