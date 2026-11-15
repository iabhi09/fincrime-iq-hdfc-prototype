"""Invented, privacy-safe AML learning scenarios for the public demo.

These are not real customer cases, policy rules, thresholds, or evidence of crime.
"""

DEMO_SCENARIOS = {
    "Routine salary and household bills": (
        "The customer receives a monthly salary from their employer. "
        "They use the account to pay rent, electricity and grocery expenses."
    ),
    "Marketplace collection with a stated business purpose": (
        "A small online marketplace receives payments from many buyers and "
        "pays registered sellers every week. The customer says this is the "
        "declared purpose of the business account and provides settlement records."
    ),
    "Multiple unrelated senders and rapid onward movement": (
        "A salaried customer receives funds from several unrelated individuals. "
        "Most of the money is transferred to one beneficiary within a few hours. "
        "The customer has not yet explained the relationships or purpose."
    ),
    "Repeated smaller cash deposits": (
        "The account shows repeated cash deposits in similar smaller amounts "
        "across several days. The customer's occupation and source of cash "
        "have not yet been established."
    ),
    "Funds routed through several accounts": (
        "Funds move from the customer's account through several intermediary "
        "accounts before reaching a connected beneficiary. The reason for the "
        "routing and the role of each intermediary are unclear."
    ),
    "Possible circular movement": (
        "Similar amounts move between two connected accounts and later return "
        "to the originating account. The customer has not provided a clear "
        "commercial or personal reason for the repeated transfers."
    ),
}


def get_demo_scenario(name: str) -> str:
    return DEMO_SCENARIOS.get(name, "")
