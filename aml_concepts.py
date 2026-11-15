"""Curated, deterministic AML concept explanations for the public prototype.

These are educational concepts, not HDFC Bank policy or legal advice.
Lookup is keyword/alias matching, not an LLM or semantic model.
"""
from __future__ import annotations

import re
from typing import Any

CONCEPTS: list[dict[str, Any]] = [
    {
        "name": "Funnel account",
        "aliases": ["funnel account", "funnel accounts"],
        "definition": "An account that receives funds from multiple people or locations, which are then consolidated or moved onward. The pattern can make the true source or controller of funds harder to understand.",
        "example": "Several people deposit money into one account, and the balance is then transferred to a single person or another account.",
        "indicators": ["Deposits from multiple unrelated people or locations", "Funds consolidated and moved onward", "Activity inconsistent with the account holder's stated purpose"],
        "alternatives": ["A collection account for a legitimate business", "Shared household or community collections", "A merchant or agent collecting payments for a disclosed service"],
        "checks": ["Identify depositors, locations, dates, channels and amounts.", "Establish the relationship between depositors and the account holder.", "Compare the activity with the customer's business model and expected cash use.", "Trace where the consolidated funds go and assess the stated economic purpose."],
        "source_class": "General AML typology education",
        "source_note": "Curated explanatory material; not an HDFC Bank policy definition."
    },
    {
        "name": "Pass-through activity",
        "aliases": ["pass through", "pass-through", "pass through account", "rapid movement of funds"],
        "definition": "Money enters an account and is moved out soon afterwards, sometimes with little balance retained or no clear economic reason for the account to act as an intermediary.",
        "example": "An account receives several credits and transfers most of the money to another beneficiary within hours.",
        "indicators": ["Rapid movement after receipt", "Most funds quickly transferred onward", "Repeated inflow/outflow pattern", "No clear relationship or purpose for the intermediary account"],
        "alternatives": ["A disclosed payment-collection or settlement service", "A business paying suppliers after receiving customer funds", "A planned transfer between a customer's own accounts"],
        "checks": ["Compare timestamps and amounts of incoming and outgoing transactions.", "Identify originators and beneficiaries and their relationships.", "Review account purpose, historical pattern and expected activity.", "Seek evidence for the economic reason and the customer's role in the flow."],
        "source_class": "General AML typology education",
        "source_note": "Curated explanatory material; not an HDFC Bank policy definition."
    },
    {
        "name": "Money mule",
        "aliases": ["money mule", "mule account", "mule activity", "money mules"],
        "definition": "A person or account used to receive, hold or transfer money on behalf of someone else. The account holder may know what is happening, be deceived, or be exploited.",
        "example": "A person receives money from strangers and forwards it to another account, sometimes keeping a fee.",
        "indicators": ["Receiving funds for unrelated parties", "Forwarding funds soon after receipt", "Commission or payment for moving money", "Customer cannot explain counterparties or purpose"],
        "alternatives": ["Legitimate agency or payment-service activity", "Family support or reimbursements", "A disclosed job involving collections or disbursements"],
        "checks": ["Clarify who controls the account and who instructed the transfers.", "Establish relationships with senders and recipients.", "Review customer explanation and supporting evidence.", "Consider whether the customer may be a victim of coercion, deception or account takeover."],
        "source_class": "General AML typology education",
        "source_note": "Curated explanatory material; indicators do not establish criminal involvement."
    },
    {
        "name": "Layering",
        "aliases": ["layering", "layers", "multiple layers of transfers"],
        "definition": "A money-laundering stage in which transactions, accounts or entities are used to make the origin, ownership or movement of funds more difficult to follow.",
        "example": "Funds move through several accounts or entities before reaching the final destination, with no clear commercial reason for the routing.",
        "indicators": ["Unnecessarily complex transaction chains", "Multiple intermediaries without clear purpose", "Funds routed through connected or opaque entities", "Rapid movement across accounts or jurisdictions"],
        "alternatives": ["Ordinary correspondent banking or payment routing", "Legitimate group-company treasury transfers", "Complex but documented trade or investment settlements"],
        "checks": ["Reconstruct the flow of funds from origin to destination.", "Identify beneficial owners and control relationships where relevant.", "Understand the purpose of each intermediary and transfer.", "Compare the routing with contracts, invoices and other supporting records."],
        "source_class": "General AML concept education",
        "source_note": "General concept explanation; legal definitions and application depend on applicable law."
    },
    {
        "name": "Placement",
        "aliases": ["placement", "placement stage"],
        "definition": "The stage commonly described as introducing proceeds of crime into the financial system, for example by depositing cash or converting it into financial instruments or assets.",
        "example": "Cash proceeds are deposited into an account or used to purchase a financial instrument.",
        "indicators": ["Cash activity inconsistent with the customer's profile", "Unexplained third-party cash deposits", "Repeated deposits without a plausible business explanation"],
        "alternatives": ["A cash-intensive legitimate business", "Documented sale of an asset", "A genuine cash deposit by the account holder"],
        "checks": ["Understand the source of cash and the customer's business or occupation.", "Review deposit pattern, locations, channels and supporting records.", "Compare activity with the customer's expected profile."],
        "source_class": "General AML concept education",
        "source_note": "Traditional AML teaching model; not a standalone legal test."
    },
    {
        "name": "Integration",
        "aliases": ["integration", "integration stage"],
        "definition": "The stage in the traditional money-laundering model where funds are reintroduced into the economy and made to appear connected to apparently legitimate activity.",
        "example": "Funds are used to purchase property, a business or other assets while being presented as legitimate wealth.",
        "indicators": ["Asset purchases inconsistent with known wealth", "Unclear funding source for investments or business assets", "Complex ownership or financing without a clear rationale"],
        "alternatives": ["A legitimate loan or investment", "Inheritance or documented asset sale", "A genuine business expansion"],
        "checks": ["Establish source of funds and, where relevant, source of wealth.", "Review ownership, financing and transaction documentation.", "Compare the purchase with the customer's known financial profile."],
        "source_class": "General AML concept education",
        "source_note": "Traditional AML teaching model; not a standalone legal test."
    },
    {
        "name": "Structuring",
        "aliases": ["structuring", "smurfing", "smurfing deposits"],
        "definition": "Breaking a larger amount into multiple smaller transactions, potentially to avoid scrutiny or a reporting or record-keeping requirement. The relevant legal requirements and thresholds depend on jurisdiction and current rules.",
        "example": "A person repeatedly makes smaller deposits instead of one larger deposit, with signs the pattern is intended to avoid a requirement.",
        "indicators": ["Repeated similar deposits or transfers", "Transactions clustered around a relevant threshold", "Multiple people or accounts used to divide activity"],
        "alternatives": ["Ordinary instalments or staged business receipts", "Daily sales in a cash-intensive business", "Operational or channel limits"],
        "checks": ["Aggregate activity across relevant accounts, channels and time periods where permitted.", "Check timing, amounts, locations and links between parties.", "Verify the current applicable rule; never assume or invent a threshold.", "Assess the customer's explanation and supporting records."],
        "source_class": "General AML typology education",
        "source_note": "Curated explanatory material; no threshold is specified or implied."
    },
    {
        "name": "Round-tripping",
        "aliases": ["round tripping", "round-tripping", "circular transactions", "circular transfers"],
        "definition": "Funds move through one or more parties or accounts and eventually return to the original party or a connected party, potentially creating a misleading appearance of genuine activity.",
        "example": "Money leaves an account, passes through several related entities and returns to the starting point with no clear economic reason.",
        "indicators": ["Funds return to the originator or connected party", "Similar amounts circulate between related accounts", "Repeated circular movement without clear business purpose"],
        "alternatives": ["Refunds or reversals", "Treasury cash management", "Documented settlement or internal group transfers"],
        "checks": ["Map the complete transaction loop and identify connected parties.", "Compare amounts, dates, fees and stated reasons.", "Check contracts, invoices, refunds or settlement records."],
        "source_class": "General AML typology education",
        "source_note": "Curated explanatory material; a circular flow alone is not proof of wrongdoing."
    },
    {
        "name": "Customer-profile mismatch",
        "aliases": ["profile mismatch", "activity inconsistent with profile", "expected activity mismatch"],
        "definition": "A difference between a customer's known profile or expected account use and the actual value, frequency, counterparties, geography or nature of transactions.",
        "example": "A personal account with a modest declared income begins receiving frequent high-value business-like credits from unrelated parties.",
        "indicators": ["Transaction values materially differ from known income or turnover", "Activity does not fit the stated occupation or account purpose", "New counterparties, locations or channels without an apparent explanation"],
        "alternatives": ["A new job or business", "Sale of an asset or inheritance", "A temporary, documented family or business event"],
        "checks": ["Confirm customer information is current.", "Compare actual activity with a reasonable expected profile and historical baseline.", "Ask what changed and review evidence supporting the explanation."],
        "source_class": "General AML investigation concept",
        "source_note": "An investigative comparison, not a legal conclusion or automatic suspicion trigger."
    },
    {
        "name": "Source of funds vs source of wealth",
        "aliases": ["source of funds", "sof", "source of wealth", "sow"],
        "definition": "Source of funds concerns where the money for a particular transaction or relationship came from. Source of wealth concerns how the customer accumulated their overall wealth.",
        "example": "For a property purchase, source of funds may be the bank account or loan used to pay; source of wealth may be salary, business ownership, investments or inheritance accumulated over time.",
        "indicators": ["Explanation does not match transaction trail", "Evidence is missing or inconsistent", "Stated wealth appears unsupported by known background"],
        "alternatives": ["A legitimate loan, inheritance, asset sale or investment return", "A recent change in employment or business circumstances"],
        "checks": ["Identify the immediate origin of funds for the transaction.", "Where risk and applicable procedures require, understand how the customer's wealth was accumulated.", "Match explanations to reliable, relevant supporting evidence."],
        "source_class": "General AML/KYC concept education",
        "source_note": "General distinction; specific collection requirements depend on applicable law and approved institutional policy."
    }
]


def _normalise(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def retrieve_concepts(query: str, limit: int = 3) -> list[dict[str, Any]]:
    """Return concept cards using transparent alias and keyword overlap."""
    normalised = _normalise(query)
    if not normalised or limit <= 0:
        return []
    query_tokens = set(normalised.split())
    ranked: list[tuple[int, int, dict[str, Any]]] = []
    for item in CONCEPTS:
        aliases = [_normalise(alias) for alias in item["aliases"]]
        name = _normalise(item["name"])
        exact = int(any(alias and alias in normalised for alias in aliases) or name in normalised)
        searchable = " ".join([
            item["name"], " ".join(item["aliases"]), item["definition"],
            item["example"], " ".join(item["indicators"]), " ".join(item["checks"])
        ])
        overlap = len(query_tokens.intersection(set(_normalise(searchable).split())))
        if exact or overlap >= 2:
            ranked.append((exact, overlap, item))
    ranked.sort(key=lambda row: (row[0], row[1]), reverse=True)
    return [dict(item, lookup_method="alias_and_keyword_match") for _, _, item in ranked[:limit]]
