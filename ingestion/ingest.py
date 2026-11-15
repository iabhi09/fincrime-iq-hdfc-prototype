"""Download and extract configured public sources into local JSONL chunks.

Run from repository root: python -m ingestion.ingest
Review source versions and extracted text before relying on the content.
"""
from __future__ import annotations

import json
import re
import time
from pathlib import Path
from urllib.parse import urlparse

import fitz
import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "config" / "source_registry.json"
RAW = ROOT / "knowledge_base" / "raw"
OUT = ROOT / "knowledge_base" / "extracted" / "chunks.jsonl"
HEADERS = {"User-Agent": "FinCrimeIQ-ResearchPrototype/0.1 (public-source document indexing)"}


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def split_chunks(text: str, size: int = 1100, overlap: int = 140) -> list[str]:
    text = clean(text)
    if not text:
        return []
    chunks, start = [], 0
    while start < len(text):
        end = min(len(text), start + size)
        if end < len(text):
            boundary = text.rfind(" ", start, end)
            if boundary > start + size // 2:
                end = boundary
        chunks.append(text[start:end].strip())
        if end >= len(text):
            break
        start = max(start + 1, end - overlap)
    return [c for c in chunks if c]


def extract_pdf(data: bytes) -> list[tuple[str, str]]:
    doc = fitz.open(stream=data, filetype="pdf")
    return [(str(page.number + 1), page.get_text("text")) for page in doc]


def extract_html(data: bytes) -> list[tuple[str, str]]:
    soup = BeautifulSoup(data, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header", "noscript"]):
        tag.decompose()
    title = soup.title.get_text(" ", strip=True) if soup.title else ""
    body = soup.get_text(" ", strip=True)
    return [(title or "Web page", body)]


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    all_chunks = []

    for source in registry["sources"]:
        if source.get("status") in {"directory"}:
            print(f"Skipping directory page pending curated document links: {source['title']}")
            continue
        url = source["url"]
        filename = f"{source['id']}.{'pdf' if source['format'] == 'pdf' else 'html'}"
        target = RAW / filename
        print(f"Fetching {source['title']} ...")
        try:
            response = requests.get(url, headers=HEADERS, timeout=35)
            response.raise_for_status()
            content_type = response.headers.get("Content-Type", "").lower()
            is_pdf = source["format"] == "pdf" or "application/pdf" in content_type or response.content[:4] == b"%PDF"
            target.write_bytes(response.content)
            pages = extract_pdf(response.content) if is_pdf else extract_html(response.content)
            for page_label, text in pages:
                for index, chunk in enumerate(split_chunks(text)):
                    all_chunks.append({
                        "source_id": source["id"],
                        "source_title": source["title"],
                        "authority": source["authority"],
                        "url": url,
                        "page": page_label if is_pdf else None,
                        "chunk_index": index,
                        "text": chunk
                    })
            print(f"  Extracted {len(pages)} page/section(s)")
        except Exception as exc:
            print(f"  WARNING: Could not ingest {url}: {exc}")
        time.sleep(1.0)

    with OUT.open("w", encoding="utf-8") as handle:
        for item in all_chunks:
            handle.write(json.dumps(item, ensure_ascii=False) + "\n")
    print(f"Wrote {len(all_chunks)} chunks to {OUT}")
    print("IMPORTANT: Review source currency, completeness, and extracted text before using any passage.")


if __name__ == "__main__":
    main()
