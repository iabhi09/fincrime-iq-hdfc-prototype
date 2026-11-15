# Local Test and Demonstration Plan

This checklist is for the repository owner when opening the project locally. Use only invented scenarios.

## 1. Environment and automated tests

From the repository root:

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Then:
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python -m compileall -q app.py fincrime_core.py aml_concepts.py demo_scenarios.py ingestion tests
```

Expected: all unit tests pass and compilation completes without errors.

## 2. Launch the app

```bash
streamlit run app.py
```

Check that all four areas load:
- Policy Intelligence
- Investigation Intelligence
- AML Concepts
- About & limitations

## 3. AML Concepts smoke tests

Try:
- "What is a funnel account?"
- "Explain layering"
- "What is a money mule?"
- "What is the difference between source of funds and source of wealth?"
- "Explain structuring"

Check that explanations show a simple definition, example, possible indicators, alternative explanations and investigation checks. Confirm the app says these are general educational concepts, not HDFC policy.

## 4. Investigation smoke tests

Select each synthetic scenario from the dropdown. Check that:
- Routine salary and household bills do not produce a typology indicator.
- Multiple unrelated senders and rapid onward movement can surface pass-through and possible mule indicators.
- Repeated smaller cash deposits can surface a possible structuring indicator.
- Several intermediary accounts can surface a possible layering indicator.
- User-described facts remain separate from interpretations.
- Alternative explanations and missing information are visible.
- No result claims that crime occurred or assigns a final customer risk rating.

## 5. Policy Intelligence

Before ingestion, the app should explicitly report that no public-source passages are indexed and should not fabricate a policy answer.

When ready to index:
1. Run `python -m ingestion.ingest`.
2. Inspect `knowledge_base/extracted/manifest.json` for failed downloads, zero-text sources, page counts and warnings.
3. Open sample raw documents and compare extracted text with the original pages.
4. Review publisher dates, amendments, authority class and legal applicability.
5. Only then test retrieval with questions whose answers can be located in the source documents.

Generated raw documents, chunks and manifests are local-only. Do not commit them to this public repository unless their licensing, size and governance have been reviewed.

## 6. Privacy and safety

- Never use a live customer, case, account, identity or employee record.
- Never upload internal HDFC Bank, AML RightSource or client documents.
- Never add passwords, tokens, API keys or secrets.
- Treat every phrase match as a prompt to investigate, not as proof.
