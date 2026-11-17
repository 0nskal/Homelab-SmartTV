"""Offline unit tests for tv.py (no network, no adb). Run: python -m unittest discover -s tests"""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import tv  # noqa: E402


class ProfileTests(unittest.TestCase):
    def test_direct_key(self):
        self.assertEqual(tv.profile_for("sony")[0], "sony")

    def test_alias(self):
        key, prof = tv.profile_for("  Bravia ")
        self.assertEqual(key, "sony")
        self.assertTrue(prof["adb"])

    def test_unknown_brand_falls_back(self):
        key, prof = tv.profile_for("no-such-brand")
        self.assertEqual(key, "android-tv")
        self.assertIn("bloat", prof)

    def test_known_brand(self):
        self.assertTrue(tv.known_brand("tizen"))
        self.assertFalse(tv.known_brand("zzz"))


class ScrubTests(unittest.TestCase):
    def test_mac_masked(self):
        out = tv.scrub_text("name=tv\nsome=aa:bb:CC:11:22:33 end")
        self.assertIn("XX:XX:XX:XX:XX:XX", out)
        self.assertNotIn("aa:bb", out)

    def test_serial_lines_removed(self):
        text = "[ro.serialno]: [ABC123]\n[ro.product.model]: [X1]\n[ro.boot.wifimacaddr]: [1]\nandroid_id=deadbeef"
        out = tv.scrub_text(text)
        self.assertNotIn("ABC123", out)
        self.assertNotIn("deadbeef", out)
        self.assertIn("ro.product.model", out)

    def test_scrub_macs_keeps_lines(self):
        self.assertEqual(tv.scrub_macs("x 00:11:22:33:44:55"), "x XX:XX:XX:XX:XX:XX")


class CandidateTests(unittest.TestCase):
    OUT = (
        "package:/system/app/A/A.apk=com.vendor.retaildemo\n"
        "package:/system/app/B/B.apk=com.google.android.tv\n"
        "package:/data/app/C/base.apk=com.partner.app\n"
        "package:/system/app/A/A.apk=com.vendor.retaildemo\n"
    )

    def test_matches_sorted_unique(self):
        self.assertEqual(tv.find_candidates(self.OUT, "retaildemo|partner"),
                         ["com.partner.app", "com.vendor.retaildemo"])

    def test_no_match(self):
        self.assertEqual(tv.find_candidates(self.OUT, "nothing-here"), [])


class SlugTests(unittest.TestCase):
    def test_slugify(self):
        self.assertEqual(tv.slugify("My Living Room/TV!"), "My-Living-Room-TV")

    def test_empty(self):
        self.assertEqual(tv.slugify("***"), "device")


class I18nTests(unittest.TestCase):
    def test_languages_differ(self):
        self.assertEqual(tv.t("adb_yes", lang="en"), "yes")
        self.assertEqual(tv.t("adb_yes", lang="pl"), "tak")

    def test_format_args(self):
        self.assertIn("1.2.3.4", tv.t("connecting", lang="pl", ip="1.2.3.4"))
        self.assertIn("1.2.3.4", tv.t("connecting", lang="en", ip="1.2.3.4"))

    def test_same_keys(self):
        self.assertEqual(set(tv.T["en"]), set(tv.T["pl"]))

    def test_unknown_lang_and_key(self):
        self.assertEqual(tv.t("adb_no", lang="xx"), "no")
        self.assertEqual(tv.t("missing_key"), "missing_key")


class BrandsJsonTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / "data" / "brands.json").read_text(encoding="utf-8"))

    def test_profiles(self):
        self.assertIn("android-tv", self.data["profiles"])
        for key, p in self.data["profiles"].items():
            self.assertIn("os", p, key)
            self.assertIn("adb", p, key)
            if p["adb"] is False:
                self.assertTrue(p.get("note_en"), key)
                self.assertTrue(p.get("note_pl"), key)
            else:
                self.assertIn("bloat", p, key)

    def test_notes(self):
        self.assertIn("_note_en", self.data)
        self.assertIn("_note_pl", self.data)


if __name__ == "__main__":
    unittest.main()
