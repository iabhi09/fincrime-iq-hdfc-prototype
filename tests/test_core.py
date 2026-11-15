import unittest

from fincrime_core import analyse_scenario, retrieve


class CoreTests(unittest.TestCase):
    def test_retrieval_returns_matching_chunk(self):
        chunks = [{"source_title": "Test policy", "text": "Customer due diligence and beneficial ownership checks."}]
        result = retrieve("beneficial ownership", chunks)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["source_title"], "Test policy")

    def test_pass_through_phrase_is_detected(self):
        result = analyse_scenario("Funds received and transferred on the same day.")
        self.assertTrue(any(x["name"] == "Potential pass-through activity" for x in result))

    def test_no_match_is_not_a_clearance(self):
        self.assertEqual(analyse_scenario("A customer updated their email address."), [])


if __name__ == "__main__":
    unittest.main()
