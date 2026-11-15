"""Core logic for the FinCrime IQ educational prototype.

This is a lightweight keyword-retrieval MVP, not a complete RAG system.
It must not be used to make real customer decisions.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
CHUNKS_FILE = ROOT / "knowledge_base" / "extracted" / "chunks.jsonl"
ABSTENTION = "This information is not covered in the provided policy documents."


def load_chunks(path: Path = CHUNKS_FILE) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            item = json.loads(line)
            if item.get("text"):
                rows.append(item)
        except json.JSONDecodeError:
            continue
    return rows


def terms(text: str) -> set[str]:
    return {t for t in re.findall(r"[a-zA-Z0-9]{3,}", text.lower())}


def retrieve(query: str, chunks: list[dict[str, Any]] | None = None, limit: int = 5) -> list[dict[str, Any]]:
    corpus = chunks if chunks is not None else load_chunks()
    q = terms(query)
    if not q:
        return []
    scored = []
    for chunk in corpus:
        body = str(chunk.get("text", ""))
        tokens = terms(body)
        overlap = len(q & tokens)
        if overlap:
            # Simple transparent score; replace with BM25/hybrid retrieval in a later iteration.
            score = overlap / max(1, len(q)) + min(overlap, 10) / max(100, len(tokens))
            scored.append((score, chunk))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [dict(item, retrieval_score=round(score, 4)) for score, item in scored[:limit]]


TYPOLOGIES = [
    {
        "name": "Potential pass-through activity",
        "signals": ["pass through", "rapid movement", "immediately transferred", "same day", "received and transferred", "inflow and outflow"],
        "explanation": "Funds enter an account and are moved onward quickly, with little apparent economic purpose or retention.",
        "checks": ["Establish the customer's expected activity and account purpose.", "Identify originators and beneficiaries and their relationship to the customer.", "Compare timestamps, amounts, channels, and historical behaviour.", "Seek a clear, evidence-supported explanation for the flow of funds."]
    },
    {
        "name": "Potential funnel-account indicators",
        "signals": ["many locations", "multiple locations", "cash deposits", "different branches", "deposits followed by"],
        "explanation": "An account may receive deposits from multiple people or locations, followed by movement or consolidation of funds.",
        "checks": ["Map deposit locations, channels, dates, and depositors where available.", "Check whether depositors are connected to the customer or stated business.", "Compare activity with geography, occupation, and expected cash usage."]
    },
    {
        "name": "Potential money-mule indicators",
        "signals": ["unrelated counterparties", "third party", "commission", "account used by others", "forwarding funds"],
        "explanation": "An account may be used to receive and move funds for other people, sometimes in exchange for a fee. These indicators alone do not establish mule activity.",
        "checks": ["Clarify who controls the account and who initiated the transactions.", "Review device, access, and beneficiary patterns if lawfully available to the institution.", "Check customer explanation and supporting evidence."]
    },
    {
        "name": "Potential structuring indicators",
        "signals": ["just below threshold", "split deposits", "multiple small deposits", "avoid reporting", "repeated cash deposits"],
        "explanation": "Transactions may be divided into smaller amounts in an attempt to avoid attention or reporting requirements. Do not infer a threshold unless a verified source provides it.",
        "checks": ["Aggregate activity across relevant time periods and channels.", "Check repeated amounts, timing, locations, and common counterparties.", "Use only verified applicable reporting rules; do not invent thresholds."]
    },
    {
        "name": "Potential layering indicators",
        "signals": ["multiple accounts", "complex transfers", "several transfers", "intermediary accounts", "conceal origin"],
        "explanation": "A series of transactions or accounts may make the origin or ownership of funds harder to understand.",
        "checks": ["Reconstruct the flow of funds end to end.", "Identify intermediaries, common ownership, and control relationships.", "Assess whether the routing has a plausible economic purpose."]
    },
    {
        "name": "Potential profile mismatch",
        "signals": ["salary", "occupation", "expected activity", "profile mismatch", "income", "business turnover"],
        "explanation": "Observed transaction values, frequency, counterparties, or geography may not align with the customer's known profile.",
        "checks": ["Compare activity with occupation, income, business model, and declared purpose.", "Review historical baseline and whether a legitimate change explains the variance.", "Identify missing or stale customer information."]
    },
    {
        "name": "Potential circular or round-tripping activity",
        "signals": ["same funds returned", "circular transfers", "round trip", "money returned", "back to origin"],
        "explanation": "Funds may move through one or more parties and return to the originator or a connected party, potentially obscuring the underlying purpose.",
        "checks": ["Trace whether funds return to the original customer or connected parties.", "Compare amounts, timing, fees, and stated economic rationale.", "Check for common ownership or relationships among parties."]
    }
]


def analyse_scenario(scenario: str) -> list[dict[str, Any]]:
    text = scenario.lower()
    results = []
    for item in TYPOLOGIES:
        hits = [signal for signal in item["signals"] if signal in text]
        if hits:
            results.append({
                "name": item["name"],
                "matched_indicators": hits,
                "explanation": item["explanation"],
                "checks": item["checks"]
            })
    return results


def source_label(chunk: dict[str, Any]) -> str:
    title = chunk.get("source_title") or chunk.get("source_id") or "Unspecified source"
    section = chunk.get("section")
    return f"{title}" + (f" — {section}" if section else "")
