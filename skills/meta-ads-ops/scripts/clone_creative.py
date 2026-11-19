"""Clone a placement-customised (asset_feed_spec) video creative with new videos and a new utm_content.

Creatives are immutable: a new opening, video or UTM means a new creative. This keeps copy, links,
CTA and the placement rules, and swaps the video per placement label (labels ending 9x16 / 4x5).

  python3 clone_creative.py --account act_<ID> --creative <SRC_ID> --video-9x16 <VIDEO_ID> --video-4x5 <VIDEO_ID>
                            --suffix v2-hook [--utm-content <value>] [--name "..."] [--apply]

Dry-run (default) prints the request. --apply creates the creative and prints its id; attach it to a
new PAUSED ad (POST act_<ID>/ads with creative={"creative_id": ...}, status=PAUSED) and review before activating.
"""
import argparse
import copy
import json
import re
import sys

ASPECTS = ("9x16", "4x5")


def _aspect(label_name: str) -> str:
    for a in ASPECTS:
        if label_name.endswith(a):
            return a
    raise ValueError(f"placement label {label_name!r} doesn't end in one of {ASPECTS}")


def retag(url_tags: str, utm_content: str) -> str:
    if re.search(r"(^|&)utm_content=", url_tags or ""):
        return re.sub(r"((?:^|&)utm_content=)[^&]*", lambda m: m.group(1) + utm_content, url_tags)
    return f"{url_tags}&utm_content={utm_content}" if url_tags else f"utm_content={utm_content}"


def build_clone(src: dict, videos: dict, thumbs: dict, suffix: str, utm_content: str | None,
                name: str | None) -> dict:
    """Pure: source creative (GET fields name,object_story_spec,asset_feed_spec,degrees_of_freedom_spec,url_tags)
    -> POST params for act_<ID>/adcreatives. `videos`/`thumbs` are keyed by aspect ('9x16', '4x5')."""
    afs = copy.deepcopy(src["asset_feed_spec"])
    afs.pop("additional_data", None)                   # read-only
    old = {}
    for v in afs.get("videos", []):
        lbl = v["adlabels"][0]["name"]
        old[_aspect(lbl)] = lbl
    if set(old) != set(videos):
        raise ValueError(f"source has placements {sorted(old)}, got videos for {sorted(videos)}")
    new_label = {a: re.sub(rf"-?{a}$", "", old[a]) + f"-{suffix}-{a}" for a in old}
    afs["videos"] = [{"video_id": videos[a], "thumbnail_url": thumbs[a], "adlabels": [{"name": new_label[a]}]}
                     for a in ASPECTS if a in videos]
    for rule in afs.get("asset_customization_rules", []):
        rule["video_label"] = {"name": new_label[_aspect(rule["video_label"]["name"])]}
        for k in ("age_min", "age_max"):                # echoed defaults the API rejects on create
            rule.get("customization_spec", {}).pop(k, None)
    params = {"name": name or f"{src.get('name', 'creative')} | {suffix}",
              "object_story_spec": src["object_story_spec"], "asset_feed_spec": afs}
    if src.get("degrees_of_freedom_spec"):
        params["degrees_of_freedom_spec"] = src["degrees_of_freedom_spec"]
    tags = src.get("url_tags") or ""
    if utm_content:
        tags = retag(tags, utm_content)
    if tags:
        params["url_tags"] = tags
    return params


def preferred_thumbnail(video_id: str) -> str:
    import graph
    for _ in range(60):
        status = graph.get(video_id, fields="status").get("status", {}).get("video_status")
        if status == "ready":
            break
        __import__("time").sleep(10)
    else:
        raise RuntimeError(f"video {video_id} not ready (status {status})")
    th = graph.get(f"{video_id}/thumbnails").get("data", [])
    pick = [t for t in th if t.get("is_preferred")] or th
    if not pick:
        raise RuntimeError(f"video {video_id} has no thumbnails yet")
    return pick[0]["uri"]


def main(argv=None) -> int:
    import graph
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--account", required=True, help="act_<ID>")
    ap.add_argument("--creative", required=True)
    ap.add_argument("--video-9x16"); ap.add_argument("--video-4x5")
    ap.add_argument("--suffix", required=True, help="label suffix, e.g. v2-hook")
    ap.add_argument("--utm-content", help="new utm_content (default: <old>-<suffix>)")
    ap.add_argument("--name")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args(argv)
    videos = {k: v for k, v in (("9x16", a.video_9x16), ("4x5", a.video_4x5)) if v}
    src = graph.get(a.creative, fields="name,object_story_spec,asset_feed_spec,degrees_of_freedom_spec,url_tags")
    utm = a.utm_content
    if not utm:
        m = re.search(r"utm_content=([^&]*)", src.get("url_tags") or "")
        utm = f"{m.group(1)}-{a.suffix}" if m else a.suffix
    thumbs = {k: preferred_thumbnail(v) for k, v in videos.items()}
    params = build_clone(src, videos, thumbs, a.suffix, utm, a.name)
    if not a.apply:
        print(json.dumps(params, indent=1)); print("\n(dry run: add --apply to create)", file=sys.stderr)
        return 0
    print(json.dumps(graph.post(f"{a.account}/adcreatives", **params)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
