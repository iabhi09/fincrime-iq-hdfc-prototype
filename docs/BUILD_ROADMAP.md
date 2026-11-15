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
- [ ] Run tests in GitHub Actions and resolve any failures
- [ ] Run the app locally and review the user experience

## Phase 2 — Evidence and source governance
- [ ] Verify each source URL and current version before ingestion
- [ ] Record retrieval date, publication/effective date, version and authority
- [ ] Improve PDF extraction checks for tables, footnotes and scanned pages
- [ ] Preserve source-to-passage traceability and stable page references
- [ ] Add source filters so HDFC public policy, Indian regulation and FATF are not conflated
- [ ] Add source freshness and superseded-document warnings

## Phase 3 — Investigation assistant
- [ ] Expand scenario vocabulary and add negation/context safeguards
- [ ] Explain each potential indicator in plain language
- [ ] Separate observed facts, possible interpretations and missing information
- [ ] Generate evidence-led next-check suggestions
- [ ] Add synthetic scenario test suite
- [ ] Keep all outputs explicitly non-determinative and human-reviewed

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
