import unittest

from demo_scenarios import DEMO_SCENARIOS, get_demo_scenario
from fincrime_core import analyse_scenario


class DemoScenarioTests(unittest.TestCase):
    def test_scenarios_are_nonempty_and_labelled_as_synthetic(self):
        self.assertGreaterEqual(len(DEMO_SCENARIOS), 5)
        self.assertTrue(all(name and text.strip() for name, text in DEMO_SCENARIOS.items()))

    def test_unknown_demo_returns_empty(self):
        self.assertEqual(get_demo_scenario("not a demo"), "")

    def test_routine_scenario_does_not_trigger_typology(self):
        result = analyse_scenario(get_demo_scenario("Routine salary and household bills"))
        self.assertEqual(result, [])

    def test_multi_sender_scenario_has_expected_educational_indicators(self):
        result = analyse_scenario(
            get_demo_scenario("Multiple unrelated senders and rapid onward movement")
        )
        names = {item["name"] for item in result}
        self.assertIn("Potential pass-through activity", names)
        self.assertIn("Potential money-mule indicators", names)

    def test_repeated_cash_deposits_scenario_detects_structuring_phrase(self):
        result = analyse_scenario(get_demo_scenario("Repeated smaller cash deposits"))
        self.assertIn("Potential structuring indicators", {x["name"] for x in result})


if __name__ == "__main__":
    unittest.main()
