"""Download and extract configured public sources into local JSONL chunks.

Run from repository root: python -m ingestion.ingest

The raw files, chunks and manifest are generated locally and are intentionally
not committed to the public repository. Review publisher versions and extraction
quality before using any passage.
"""
from __future__ import annotations

import hashlib
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path

import pymupdf as fitz
import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "config" / "source_registry.json"
RAW = ROOT / "knowledge_base" / "raw"
OUT = ROOT / "knowledge_base" / "extracted" / "chunks.jsonl"
MANIFEST = ROOT / "knowledge_base" / "extracted" / "manifest.json"
HEADERS = {"User-Agent": "FinCrimeIQ-ResearchPrototype/0.2 (public-source document indexing)"}
MAX_DOWNLOAD_BYTES = 35 * 1024 * 1024


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def split_chunks(text: str, size: int = 1100, overlap: int = 140) -> list[str]:
    if size <= 0 or overlap < 0 or overlap >= size:
        raise ValueError("Require size > overlap >= 0.")
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
    return [chunk for chunk in chunks if chunk]


def extract_pdf(data: bytes) -> list[tuple[str, str]]:
    with fitz.open(stream=data, filetype="pdf") as doc:
        return [(str(page.number + 1), page.get_text("text")) for page in doc]


def extract_html(data: bytes) -> list[tuple[str, str]]:
    soup = BeautifulSoup(data, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header", "noscript"]):
        tag.decompose()
    title = soup.title.get_text(" ", strip=True) if soup.title else ""
    body = soup.get_text(" ", strip=True)
    return [(title or "Web page", body)]


def safe_filename(source_id: str, extension: str) -> str:
    safe_id = re.sub(r"[^a-zA-Z0-9_-]", "_", source_id)
    return f"{safe_id}.{extension}"


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    all_chunks: list[dict] = []
    manifest_sources: list[dict] = []

    for source in registry["sources"]:
        source_id = source["id"]
        if source.get("status") in {"directory", "directory_only_not_policy_text"}:
            print(f"Skipping directory page: {source['title']}")
            manifest_sources.append({
                "source_id": source_id, "title": source["title"],
                "status": "skipped_directory", "indexed_at": utc_now(), "chunk_count": 0
            })
            continue

        url = source["url"]
        expected_format = source.get("format", "html")
        print(f"Fetching {source['title']} ...")
        response = None
        record = {
            "source_id": source_id,
            "title": source["title"],
            "url": url,
            "authority": source.get("authority"),
            "registry_status": source.get("status"),
            "indexed_at": utc_now(),
            "chunk_count": 0,
        }
        try:
            response = requests.get(url, headers=HEADERS, timeout=(10, 45), stream=True)
            response.raise_for_status()
            content_length = response.headers.get("Content-Length")
            if content_length and int(content_length) > MAX_DOWNLOAD_BYTES:
                raise ValueError(f"Download exceeds {MAX_DOWNLOAD_BYTES} byte safety limit.")

            body = bytearray()
            for block in response.iter_content(chunk_size=64 * 1024):
                if not block:
                    continue
                body.extend(block)
                if len(body) > MAX_DOWNLOAD_BYTES:
                    raise ValueError(f"Download exceeds {MAX_DOWNLOAD_BYTES} byte safety limit.")
            data = bytes(body)
            content_type = response.headers.get("Content-Type", "").lower()
            is_pdf = expected_format == "pdf" or "application/pdf" in content_type or data[:4] == b"%PDF"
            if is_pdf and data[:4] != b"%PDF":
                raise ValueError("Expected a PDF response but the downloaded content is not a PDF.")
            if not is_pdf and not data:
                raise ValueError("Downloaded response is empty.")

            extension = "pdf" if is_pdf else "html"
            raw_path = RAW / safe_filename(source_id, extension)
            raw_path.write_bytes(data)
            pages = extract_pdf(data) if is_pdf else extract_html(data)
            digest = hashlib.sha256(data).hexdigest()
            extracted_chars = 0
            source_chunks = []

            for page_label, page_text in pages:
                extracted_chars += len(page_text)
                for index, chunk in enumerate(split_chunks(page_text)):
                    source_chunks.append({
                        "source_id": source_id,
                        "source_title": source["title"],
                        "authority": source.get("authority"),
                        "publisher": source.get("publisher"),
                        "url": url,
                        "page": page_label if is_pdf else None,
                        "section": None,
                        "chunk_index": index,
                        "retrieved_at": record["indexed_at"],
                        "publisher_updated_as_of": source.get("publisher_updated_as_of"),
                        "publisher_last_updated": source.get("publisher_last_updated"),
                        "text": chunk,
                    })

            all_chunks.extend(source_chunks)
            record.update({
                "status": "downloaded_extraction_needs_review",
                "content_type": content_type,
                "http_last_modified": response.headers.get("Last-Modified"),
                "etag": response.headers.get("ETag"),
                "sha256": digest,
                "raw_file": str(raw_path.relative_to(ROOT)),
                "page_or_section_count": len(pages),
                "extracted_character_count": extracted_chars,
                "chunk_count": len(source_chunks),
                "warning": "Extraction success does not establish source currency, legal applicability, or completeness.",
            })
            print(f"  Extracted {len(source_chunks)} chunks from {len(pages)} page/section(s)")
            if extracted_chars == 0:
                record["status"] = "downloaded_but_no_extractable_text"
                record["warning"] = "Likely scanned or image-only content; OCR/manual review required."
        except Exception as exc:
            record.update({"status": "failed", "error": str(exc)})
            print(f"  WARNING: Could not ingest {url}: {exc}")
        finally:
            if response is not None:
                response.close()
            manifest_sources.append(record)
            time.sleep(1.0)

    with OUT.open("w", encoding="utf-8") as handle:
        for item in all_chunks:
            handle.write(json.dumps(item, ensure_ascii=False) + "\n")

    manifest = {
        "generated_at": utc_now(),
        "registry_reviewed_on": registry.get("registry_reviewed_on"),
        "total_chunks": len(all_chunks),
        "sources": manifest_sources,
        "notice": "A successful download/extraction is not legal validation. Check current publisher versions, amendments, effective dates, completeness and extraction quality.",
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(all_chunks)} chunks to {OUT}")
    print(f"Wrote source manifest to {MANIFEST}")
    print("Review every source and extracted passage before relying on it.")


if __name__ == "__main__":
    main()
