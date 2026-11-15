import json
import tempfile
import unittest
from pathlib import Path

from fincrime_core import ABSTENTION, analyse_scenario, build_investigation_summary, load_chunks, retrieve


class CoreTests(unittest.TestCase):
    def test_retrieval_returns_matching_chunk(self):
        chunks = [
            {"source_title": "CDD policy", "text": "Customer due diligence and beneficial ownership checks."},
            {"source_title": "Cash deposits", "text": "Cash deposit monitoring and branch location records."},
        ]
        result = retrieve("beneficial ownership", chunks)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["source_title"], "CDD policy")
        self.assertIn("matched_terms", result[0])

    def test_retrieval_can_filter_by_authority_class(self):
        chunks = [
            {"authority": "HDFC Bank public policy", "text": "Customer due diligence requirements."},
            {"authority": "International standards", "text": "Customer due diligence recommendations."},
        ]
        result = retrieve(
            "customer due diligence",
            chunks,
            authorities={"International standards"},
        )
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["authority"], "International standards")

    def test_retrieval_handles_empty_inputs(self):
        self.assertEqual(retrieve("   ", []), [])
        self.assertEqual(retrieve("beneficial ownership", [], limit=0), [])

    def test_retrieval_ranks_more_relevant_passage_first(self):
        chunks = [
            {"source_title": "General", "text": "Customer records are maintained."},
            {"source_title": "Relevant", "text": "Beneficial ownership identification and verification is part of customer due diligence."},
        ]
        result = retrieve("beneficial ownership verification", chunks)
        self.assertEqual(result[0]["source_title"], "Relevant")

    def test_load_chunks_skips_malformed_lines(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "chunks.jsonl"
            path.write_text('{"text":"valid passage"}\nnot-json\n', encoding="utf-8")
            self.assertEqual(len(load_chunks(path)), 1)

    def test_pass_through_phrase_is_detected(self):
        result = analyse_scenario("Funds received and transferred on the same day.")
        self.assertTrue(any(x["name"] == "Potential pass-through activity" for x in result))

    def test_salary_alone_does_not_trigger_profile_mismatch(self):
        self.assertFalse(any(
            x["name"] == "Potential customer-profile mismatch"
            for x in analyse_scenario("The customer receives a monthly salary.")
        ))

    def test_explicit_profile_mismatch_is_detected(self):
        result = analyse_scenario("Transaction activity is much higher than salary and outside expected activity.")
        self.assertTrue(any(x["name"] == "Potential customer-profile mismatch" for x in result))


    def test_natural_language_multi_originator_same_day_scenario(self):
        scenario = (
            "A salaried customer received funds from 12 unrelated individuals "
            "and transferred nearly all to a single beneficiary on the same day."
        )
        result = analyse_scenario(scenario)
        names = {item["name"] for item in result}
        self.assertIn("Potential pass-through activity", names)
        self.assertIn("Potential money-mule indicators", names)

    def test_explicit_negation_suppresses_phrase_match(self):
        result = analyse_scenario(
            "There was no rapid movement of funds and no same-day transfer."
        )
        self.assertFalse(any(
            x["name"] == "Potential pass-through activity" for x in result
        ))

    def test_non_negated_same_day_pattern_still_matches(self):
        result = analyse_scenario("Funds moved on the same day.")
        self.assertTrue(any(
            x["name"] == "Potential pass-through activity" for x in result
        ))

    def test_one_beneficiary_phrase_detected(self):
        result = analyse_scenario("Funds from multiple people were sent to one beneficiary.")
        self.assertTrue(any(x["name"] == "Potential pass-through activity" for x in result))

    def test_no_match_is_not_a_clearance(self):
        self.assertEqual(analyse_scenario("A customer updated their email address."), [])
        self.assertEqual(ABSTENTION, "This information is not covered in the provided policy documents.")


    def test_investigation_summary_separates_user_statements_and_interpretations(self):
        scenario = "The customer receives funds from several unrelated individuals. Most funds move out on the same day."
        summary = build_investigation_summary(scenario)
        self.assertEqual(
            summary["observed_facts"],
            [
                "The customer receives funds from several unrelated individuals.",
                "Most funds move out on the same day.",
            ],
        )
        self.assertTrue(summary["potential_indicators"])
        self.assertTrue(summary["alternative_explanations"])
        self.assertTrue(summary["missing_information"])
        self.assertTrue(summary["suggested_checks"])
        self.assertIn("not independently verified", summary["disclaimer"])

    def test_investigation_summary_does_not_invent_customer_details(self):
        scenario = "The customer receives a monthly salary."
        summary = build_investigation_summary(scenario)
        self.assertEqual(summary["observed_facts"], [scenario])
        self.assertEqual(summary["potential_indicators"], [])
        self.assertIn("not a clearance", summary["no_indicator_message"])
        self.assertNotIn("customer is a mule", " ".join(summary["observed_facts"]).lower())

    def test_investigation_summary_alternatives_are_explicitly_hypothetical(self):
        summary = build_investigation_summary("Funds were transferred to a beneficiary.")
        self.assertTrue(any(
            "possibilities to test" in item.lower()
            for item in summary["alternative_explanations"]
        ))


if __name__ == "__main__":
    unittest.main()
