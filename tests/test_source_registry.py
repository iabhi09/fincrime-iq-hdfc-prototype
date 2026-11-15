import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "config" / "source_registry.json"


class SourceRegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))

    def test_registry_has_review_date_and_independence_notice(self):
        self.assertTrue(self.registry.get("registry_reviewed_on"))
        self.assertIn("not affiliated", self.registry.get("disclaimer", "").lower())

    def test_source_ids_are_unique(self):
        ids = [item["id"] for item in self.registry["sources"]]
        self.assertEqual(len(ids), len(set(ids)))

    def test_every_source_has_minimum_governance_metadata(self):
        for source in self.registry["sources"]:
            with self.subTest(source=source.get("id")):
                self.assertTrue(source.get("title"))
                self.assertTrue(source.get("publisher"))
                self.assertTrue(source.get("authority"))
                self.assertTrue(source.get("url", "").startswith("https://"))
                self.assertTrue(source.get("checked_on"))
                self.assertTrue(source.get("status"))

    def test_directory_entry_is_explicitly_not_policy_text(self):
        directory = next(
            item for item in self.registry["sources"]
            if item["id"] == "hdfc_codes_policies"
        )
        self.assertEqual(directory["status"], "directory_only_not_policy_text")

    def test_historical_hdfc_process_note_is_not_current_sop(self):
        note = next(
            item for item in self.registry["sources"]
            if item["id"] == "hdfc_note_kyc_aml_cft_process"
        )
        self.assertEqual(note["status"], "historical_overview_review_before_use")
        self.assertIn("do not use as current", note["notes"].lower())


if __name__ == "__main__":
    unittest.main()
