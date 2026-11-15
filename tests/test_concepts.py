import unittest

from aml_concepts import CONCEPTS, retrieve_concepts


class AMLConceptTests(unittest.TestCase):
    def test_library_has_expected_core_concepts(self):
        names = {item["name"] for item in CONCEPTS}
        self.assertTrue({
            "Funnel account", "Pass-through activity", "Money mule", "Layering",
            "Placement", "Integration", "Structuring", "Round-tripping",
            "Customer-profile mismatch", "Source of funds vs source of wealth"
        }.issubset(names))

    def test_funnel_account_question_returns_explanation(self):
        result = retrieve_concepts("What is a funnel account and what should I check?")
        self.assertTrue(result)
        self.assertEqual(result[0]["name"], "Funnel account")
        self.assertTrue(result[0]["checks"])
        self.assertIn("keyword", result[0]["lookup_method"])

    def test_plain_english_question_finds_pass_through(self):
        result = retrieve_concepts("money comes in and quickly moves out")
        self.assertTrue(any(x["name"] == "Pass-through activity" for x in result))

    def test_structuring_does_not_invent_threshold(self):
        result = retrieve_concepts("Explain structuring")
        self.assertEqual(result[0]["name"], "Structuring")
        self.assertTrue(any("never assume" in x.lower() for x in result[0]["checks"]))

    def test_no_match_returns_empty(self):
        self.assertEqual(retrieve_concepts("quantum gardening spaceship"), [])

    def test_empty_query_and_limit(self):
        self.assertEqual(retrieve_concepts(" "), [])
        self.assertEqual(retrieve_concepts("layering", limit=0), [])


if __name__ == "__main__":
    unittest.main()
