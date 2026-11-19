"""Change only an ad set's placement position lists; everything else in targeting is kept.

  python3 set_placements.py --adset <ID> --drop facebook:feed [--drop instagram:story] [--apply]
  python3 set_placements.py --adset <ID> --set facebook=story,facebook_reels [--apply]

Dry-run (default) prints the before/after. This is a significant edit: Meta restarts learning.
"""
import argparse
import copy
import json
import sys

KEYS = {"facebook": "facebook_positions", "instagram": "instagram_positions",
        "audience_network": "audience_network_positions", "messenger": "messenger_positions"}


def change(targeting: dict, drops=(), sets=()) -> tuple[dict, dict]:
    """Pure: returns (new_targeting, diff). diff maps key -> (before, after) for changed keys only."""
    new = copy.deepcopy(targeting)
    for spec in drops:
        platform, pos = spec.split(":", 1)
        key = KEYS[platform]
        if pos not in new.get(key, []):
            raise ValueError(f"{pos} is not in {key} {new.get(key)}")
        new[key] = [p for p in new[key] if p != pos]
    for spec in sets:
        platform, positions = spec.split("=", 1)
        new[KEYS[platform]] = [p for p in positions.split(",") if p]
    for platform, key in KEYS.items():
        if key in new and not new[key]:
            raise ValueError(f"{key} would be empty: remove {platform!r} from publisher_platforms instead")
    diff = {k: (targeting.get(k), new.get(k)) for k in set(targeting) | set(new) if targeting.get(k) != new.get(k)}
    return new, diff


def main(argv=None) -> int:
    import graph
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--adset", required=True)
    ap.add_argument("--drop", action="append", default=[], help="platform:position, e.g. facebook:feed")
    ap.add_argument("--set", action="append", default=[], help="platform=pos1,pos2")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args(argv)
    targeting = graph.get(a.adset, fields="targeting")["targeting"]
    new, diff = change(targeting, a.drop, a.set)
    for k, (before, after) in sorted(diff.items()):
        print(f"{k}: {before} -> {after}")
    if not diff:
        print("no change"); return 0
    if not a.apply:
        print("(dry run: add --apply to write)", file=sys.stderr); return 0
    print(json.dumps(graph.post(a.adset, targeting=new)))
    after = graph.get(a.adset, fields="targeting")["targeting"]
    still = {k for k in set(targeting) | set(after) if k not in diff and targeting.get(k) != after.get(k)}
    if still:
        print(f"WARNING: keys outside the change also differ now: {sorted(still)}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
