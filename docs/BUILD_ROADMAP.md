# Build Roadmap

This roadmap describes the public portfolio prototype. It is not an HDFC Bank implementation plan.

## Phase 1 — Safe working foundation
- [x] Repository structure and public-source disclaimer
- [x] Basic Streamlit interface with Policy and Investigation tabs
- [x] Local document ingestion skeleton
- [x] Transparent lexical retrieval
- [x] Phrase-based educational indicator rules
- [x] Unit tests for core logic
- [x] GitHub Actions test workflow
- [x] Core and ingestion tests run in GitHub Actions
- [ ] Run the app locally and review the user experience

## Phase 2 — Evidence and source governance
- [x] Review official publisher URLs and visible version metadata; record caveats in `docs/PUBLIC_SOURCE_CATALOGUE.md`
- [ ] Independently archive and manually validate each downloaded source before relying on it
- [x] Add source review dates, known publication/update metadata and authority labels to the registry
- [x] Add retrieval timestamps, HTTP metadata and SHA-256 hashes to the local ingestion manifest
- [ ] Improve PDF extraction checks for tables, footnotes and scanned pages
- [ ] Preserve source-to-passage traceability and stable page references
- [x] Add source filters so HDFC public policy, Indian regulation and FATF are not conflated
- [ ] Add source freshness and superseded-document warnings

## Phase 3 — Investigation assistant
- [x] Add a basic explicit-negation safeguard to phrase matching (limited; not full NLP)
- [x] Add a synthetic scenario regression suite
- [ ] Expand scenario vocabulary and add broader context safeguards
- [x] Explain each potential indicator in plain language
- [x] Separate user-provided observations, potential interpretations, alternative explanations and missing information
- [x] Generate general evidence-led next-check suggestions
- [x] Keep outputs explicitly non-determinative and human-reviewed
- [x] Add a curated AML concept library with definitions, examples, alternative explanations and investigation checks
- [x] Add deterministic concept lookup and unit tests

## Phase 4 — Demonstration readiness
- [ ] Add privacy-safe sample questions and synthetic scenarios
- [ ] Add clear source coverage and known-limitations pages
- [ ] Add deployment configuration and deployment guide
- [ ] Perform end-to-end testing
- [ ] Review branding and disclaimers before public sharing

## Non-negotiable boundaries
- No real customer or employee data.
- No confidential HDFC Bank or employer/client documents.
- No invented internal thresholds, workflows, escalation rules or reporting timelines.
- A typology match is an investigative prompt, not proof of wrongdoing.
- No automated case decision, SAR/STR filing decision, approval or closure.
- The project must never imply HDFC Bank sponsorship, ownership or endorsement.
