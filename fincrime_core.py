"""Core logic for the FinCrime IQ educational prototype.

Transparent lexical retrieval and rule-based indicators. This is not a legal
reasoning engine, a trained AML model, or a production decision system.
"""
from __future__ import annotations

import json
import math
import re
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
CHUNKS_FILE = ROOT / "knowledge_base" / "extracted" / "chunks.jsonl"
ABSTENTION = "This information is not covered in the provided policy documents."

STOP_WORDS = {
    "the", "and", "for", "with", "from", "that", "this", "what", "when",
    "where", "which", "who", "how", "does", "about", "into", "under",
    "are", "was", "were", "has", "have", "had", "can", "could", "should",
    "would", "will", "shall", "may", "might", "not", "you", "your",
    "customer", "bank", "please", "explain", "tell", "give", "describe",
}


def load_chunks(path: Path = CHUNKS_FILE) -> list[dict[str, Any]]:
    """Load valid JSONL passages; malformed rows are skipped safely."""
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            item = json.loads(line)
            if isinstance(item, dict) and str(item.get("text", "")).strip():
                rows.append(item)
        except (json.JSONDecodeError, TypeError):
            continue
    return rows


def terms(text: str) -> list[str]:
    return [
        token for token in re.findall(r"[a-zA-Z0-9]{2,}", text.lower())
        if token not in STOP_WORDS
    ]


def retrieve(
    query: str,
    chunks: list[dict[str, Any]] | None = None,
    limit: int = 5,
    authorities: set[str] | None = None,
) -> list[dict[str, Any]]:
    """Rank passages with a small transparent TF-IDF-like lexical score.

    This is not BM25 or semantic search. Scores are relative ranking signals,
    not calibrated confidence values.
    """
    corpus = chunks if chunks is not None else load_chunks()
    if authorities:
        corpus = [row for row in corpus if row.get("authority") in authorities]
    query_terms = set(terms(query))
    if not query_terms or not corpus or limit <= 0:
        return []

    document_terms = [Counter(terms(str(row.get("text", "")))) for row in corpus]
    doc_frequency = Counter()
    for counts in document_terms:
        doc_frequency.update(set(counts))

    scored: list[tuple[float, int, dict[str, Any]]] = []
    total_docs = len(corpus)
    for index, (chunk, counts) in enumerate(zip(corpus, document_terms)):
        matched = query_terms.intersection(counts)
        if not matched:
            continue
        length_norm = math.sqrt(max(1, sum(counts.values())))
        score = sum(
            (1.0 + math.log(1 + counts[token]))
            * (math.log(1 + total_docs / (1 + doc_frequency[token])))
            for token in matched
        ) / length_norm
        scored.append((score, len(matched), chunk))

    scored.sort(key=lambda item: (item[0], item[1]), reverse=True)
    return [
        dict(chunk, retrieval_score=round(score, 4), matched_terms=matched)
        for score, matched, chunk in scored[:limit]
    ]


TYPOLOGIES = [
    {
        "name": "Potential pass-through activity",
        "signals": [
            "pass through", "pass-through", "rapid movement", "immediately transferred",
            "same day", "received and transferred", "inflow and outflow",
            "funds came in and went out", "quickly moved onward", "transferred out shortly",
            "transferred almost all", "transferred nearly all", "single beneficiary",
            "one beneficiary", "received funds from multiple people", "many unrelated people",
        ],
        "explanation": "Funds enter an account and are moved onward quickly, with little apparent economic purpose or retention. A legitimate explanation may exist.",
        "checks": [
            "Establish the customer's expected activity and account purpose.",
            "Identify originators and beneficiaries and their relationship to the customer.",
            "Compare timestamps, amounts, channels, and historical behaviour.",
            "Seek a clear, evidence-supported explanation for the flow of funds.",
        ],
    },
    {
        "name": "Potential funnel-account indicators",
        "signals": [
            "funnel account", "many locations", "multiple locations",
            "different branches", "deposits followed by", "deposits from different cities",
            "cash collected from multiple people",
        ],
        "explanation": "An account may receive deposits from multiple people or locations, followed by movement or consolidation of funds. This pattern requires context and verification.",
        "checks": [
            "Map deposit locations, channels, dates, and depositors where available.",
            "Check whether depositors are connected to the customer or stated business.",
            "Compare activity with geography, occupation, and expected cash usage.",
        ],
    },
    {
        "name": "Potential money-mule indicators",
        "signals": [
            "money mule", "unrelated counterparties", "third party", "commission",
            "account used by others", "forwarding funds", "receiving money for others",
            "keeping a commission", "transferring on behalf of others",
            "unrelated individuals", "several unrelated individuals", "multiple unrelated people",
        ],
        "explanation": "An account may be used to receive and move funds for other people, sometimes in exchange for a fee. These indicators alone do not establish mule activity.",
        "checks": [
            "Clarify who controls the account and who initiated the transactions.",
            "Review device, access, and beneficiary patterns if lawfully available to the institution.",
            "Check the customer explanation and supporting evidence.",
        ],
    },
    {
        "name": "Potential structuring indicators",
        "signals": [
            "just below threshold", "split deposits", "multiple small deposits",
            "avoid reporting", "repeated cash deposits", "split into smaller amounts",
            "many small transactions",
        ],
        "explanation": "Transactions may be divided into smaller amounts in an attempt to avoid attention or reporting requirements. Do not infer a legal or internal threshold unless a current authoritative source provides it.",
        "checks": [
            "Aggregate activity across relevant time periods and channels.",
            "Check repeated amounts, timing, locations, and common counterparties.",
            "Use only verified applicable reporting rules; do not invent thresholds.",
        ],
    },
    {
        "name": "Potential layering indicators",
        "signals": [
            "multiple accounts", "complex transfers", "several transfers",
            "intermediary accounts", "conceal origin", "multiple layers",
            "moved through several accounts", "chain of transfers",
        ],
        "explanation": "A series of transactions or accounts may make the origin or ownership of funds harder to understand. Complexity alone is not proof of layering.",
        "checks": [
            "Reconstruct the flow of funds end to end.",
            "Identify intermediaries, common ownership, and control relationships.",
            "Assess whether the routing has a plausible economic purpose.",
        ],
    },
    {
        "name": "Potential customer-profile mismatch",
        "signals": [
            "profile mismatch", "far exceeds salary", "much higher than salary",
            "income does not support", "inconsistent with occupation",
            "turnover mismatch", "unexpected high value", "outside expected activity",
            "activity inconsistent with profile", "salaried customer receives large",
            "large credits compared with salary", "credits far exceed declared income",
        ],
        "explanation": "Observed transaction values, frequency, counterparties, or geography may not align with the customer's known profile. A salary or occupation mention alone is not a red flag.",
        "checks": [
            "Compare activity with occupation, income, business model, and declared purpose.",
            "Review the historical baseline and whether a legitimate change explains the variance.",
            "Identify missing or stale customer information.",
        ],
    },
    {
        "name": "Potential circular or round-tripping activity",
        "signals": [
            "same funds returned", "circular transfers", "round trip", "round-tripping",
            "money returned", "back to origin", "funds came back to sender",
            "returned to original account",
        ],
        "explanation": "Funds may move through one or more parties and return to the originator or a connected party, potentially obscuring the underlying purpose.",
        "checks": [
            "Trace whether funds return to the original customer or connected parties.",
            "Compare amounts, timing, fees, and stated economic rationale.",
            "Check for common ownership or relationships among parties.",
        ],
    },
]


def _is_negated(text: str, signal: str) -> bool:
    """Detect a small set of explicit negations immediately before a phrase.

    This is a conservative safeguard, not full natural-language understanding.
    """
    start = 0
    while True:
        position = text.find(signal, start)
        if position < 0:
            return False
        prefix = text[max(0, position - 60):position]
        if re.search(
            r"\b(?:no|not|never|without|did not|does not|is not|was not|were not)\b"
            r"(?:\W+\w+){0,3}\W*$",
            prefix,
        ):
            return True
        start = position + len(signal)


def analyse_scenario(scenario: str) -> list[dict[str, Any]]:
    """Return possible educational indicators based on explicit phrase matches."""
    text = re.sub(r"\s+", " ", scenario.lower())
    results = []
    for item in TYPOLOGIES:
        hits = [
            signal for signal in item["signals"]
            if signal in text and not _is_negated(text, signal)
        ]
        if hits:
            results.append({
                "name": item["name"],
                "matched_indicators": hits,
                "explanation": item["explanation"],
                "checks": item["checks"],
                "method": "phrase_match",
            })
    return results


def source_label(chunk: dict[str, Any]) -> str:
    title = chunk.get("source_title") or chunk.get("source_id") or "Unspecified source"
    section = chunk.get("section")
    return f"{title}" + (f" — {section}" if section else "")
