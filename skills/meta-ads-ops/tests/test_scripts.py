import json
import pathlib
import sys
import unittest

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))
import clone_creative  # noqa: E402
import insights  # noqa: E402
import set_placements  # noqa: E402


def fixture(name):
    return json.loads((HERE / "fixtures" / name).read_text())


class Insights(unittest.TestCase):
    def setUp(self):
        self.rows = fixture("insights_ad.json")["data"]

    def test_counts_and_rates(self):
        m = insights.summarize([self.rows[0]])
        self.assertEqual(m["link_clicks"], 12)
        self.assertEqual(m["lpv"], 6)
        self.assertAlmostEqual(m["ctr_pct"], 0.7678, places=3)
        self.assertAlmostEqual(m["hook_rate_pct"], 22.0089, places=3)
        self.assertAlmostEqual(m["thruplay_rate_pct"], 5.6942, places=3)
        self.assertEqual(m["p25_to_p100_pct"], 25.0)

    def test_zero_denominators_are_none_not_zero(self):
        m = insights.summarize([self.rows[0]])           # no checkouts, no purchases
        self.assertIsNone(m["cost_per_checkout"])
        self.assertIsNone(m["cost_per_purchase"])
        self.assertEqual(m["roas"], 0.0)                 # spend > 0, value 0 -> a real 0
        empty = insights.summarize([])
        self.assertIsNone(empty["ctr_pct"]); self.assertIsNone(empty["roas"]); self.assertIsNone(empty["cpm"])

    def test_total_sums_counts_then_derives(self):
        t = insights.summarize(self.rows)
        self.assertEqual(t["impressions"], 1903)
        self.assertEqual(t["link_clicks"], 13)
        self.assertEqual(t["purchases"], 1)
        self.assertAlmostEqual(t["roas"], 497 / (117.14 + 18.93), places=3)
        self.assertAlmostEqual(t["cost_per_checkout"], 136.07, places=2)

    def test_placement_label(self):
        r = {"ad_name": "A", "publisher_platform": "facebook", "platform_position": "feed"}
        self.assertEqual(insights.label(r, True), "A | facebook feed")


class Clone(unittest.TestCase):
    def setUp(self):
        self.src = fixture("creative.json")
        self.p = clone_creative.build_clone(self.src, {"9x16": "v-new-916", "4x5": "v-new-45"},
                                            {"9x16": "https://t/916", "4x5": "https://t/45"},
                                            "v2-hook", "03-four-stages-v2-hook", None)

    def test_videos_swapped_per_placement_with_new_labels(self):
        vids = {v["adlabels"][0]["name"]: v["video_id"] for v in self.p["asset_feed_spec"]["videos"]}
        self.assertEqual(vids, {"03-four-stages-v2-hook-9x16": "v-new-916", "03-four-stages-v2-hook-4x5": "v-new-45"})

    def test_rules_follow_labels_and_keep_positions(self):
        rules = self.p["asset_feed_spec"]["asset_customization_rules"]
        r916 = next(r for r in rules if r["video_label"]["name"].endswith("9x16"))
        self.assertEqual(r916["video_label"], {"name": "03-four-stages-v2-hook-9x16"})
        self.assertEqual(r916["customization_spec"]["facebook_positions"], ["story", "facebook_reels"])
        self.assertNotIn("age_min", r916["customization_spec"])

    def test_read_only_fields_stripped_and_source_untouched(self):
        afs = self.p["asset_feed_spec"]
        self.assertNotIn("additional_data", afs)
        self.assertTrue(all("id" not in v["adlabels"][0] for v in afs["videos"]))
        self.assertIn("additional_data", self.src["asset_feed_spec"])   # deep copy

    def test_new_utm_content_only(self):
        self.assertEqual(self.p["url_tags"],
                         "utm_source={{site_source_name}}&utm_medium=paid_social&utm_campaign=c-01"
                         "&utm_content=03-four-stages-v2-hook&utm_term=t")
        self.assertEqual(clone_creative.retag("a=1", "x"), "a=1&utm_content=x")

    def test_copy_and_link_kept(self):
        afs = self.p["asset_feed_spec"]
        self.assertEqual(afs["link_urls"], self.src["asset_feed_spec"]["link_urls"])
        self.assertEqual(afs["bodies"], self.src["asset_feed_spec"]["bodies"])

    def test_missing_aspect_refused(self):
        with self.assertRaises(ValueError):
            clone_creative.build_clone(self.src, {"9x16": "v"}, {"9x16": "t"}, "x", None, None)


class Placements(unittest.TestCase):
    T = {"age_min": 30, "geo_locations": {"countries": ["US"]}, "publisher_platforms": ["facebook", "instagram"],
         "facebook_positions": ["feed", "story", "facebook_reels"], "instagram_positions": ["stream", "story", "reels"]}

    def test_drop_changes_only_that_list(self):
        new, diff = set_placements.change(self.T, drops=["facebook:feed"])
        self.assertEqual(new["facebook_positions"], ["story", "facebook_reels"])
        self.assertEqual(set(diff), {"facebook_positions"})
        self.assertEqual(self.T["facebook_positions"], ["feed", "story", "facebook_reels"])  # not mutated

    def test_set_replaces_list(self):
        new, diff = set_placements.change(self.T, sets=["instagram=reels"])
        self.assertEqual(new["instagram_positions"], ["reels"])

    def test_unknown_position_refused(self):
        with self.assertRaises(ValueError):
            set_placements.change(self.T, drops=["facebook:marketplace"])

    def test_emptying_a_platform_refused(self):
        with self.assertRaises(ValueError):
            set_placements.change(self.T, sets=["facebook="])


if __name__ == "__main__":
    unittest.main()
