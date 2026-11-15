"""Synthetic, non-customer examples for regression testing.

These scenarios are invented for software testing. They are not case studies,
risk rules, regulatory thresholds, or evidence of criminal conduct.
"""
import unittest

from fincrime_core import analyse_scenario


CASES = [
    {
        "name": "routine salary credit",
        "text": "The customer receives a monthly salary from their employer.",
        "expected": set(),
    },
    {
        "name": "ordinary household bill payments",
        "text": "The customer pays monthly rent and utility bills from their salary.",
        "expected": set(),
    },
    {
        "name": "multiple originators and rapid onward movement",
        "text": (
            "A salaried customer received funds from 12 unrelated individuals "
            "and transferred nearly all to a single beneficiary on the same day."
        ),
        "expected": {
            "Potential pass-through activity",
            "Potential money-mule indicators",
        },
    },
    {
        "name": "explicitly negated rapid movement",
        "text": "There was no rapid movement of funds and no same-day transfer.",
        "expected": set(),
    },
    {
        "name": "possible split-deposit pattern",
        "text": "The account shows repeated cash deposits split into smaller amounts.",
        "expected": {"Potential structuring indicators"},
    },
    {
        "name": "complex chain of transfers",
        "text": "Funds were moved through several accounts using a chain of transfers.",
        "expected": {"Potential layering indicators"},
    },
    {
        "name": "activity inconsistent with declared income",
        "text": "Credits far exceed declared income and are outside expected activity.",
        "expected": {"Potential customer-profile mismatch"},
    },
]


class SyntheticScenarioTests(unittest.TestCase):
    def test_synthetic_scenario_expectations(self):
        for case in CASES:
            with self.subTest(case=case["name"]):
                actual = {item["name"] for item in analyse_scenario(case["text"])}
                self.assertEqual(actual, case["expected"])


if __name__ == "__main__":
    unittest.main()
