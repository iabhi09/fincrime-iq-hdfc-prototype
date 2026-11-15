# Deployment Guide

This guide is for a later public portfolio demonstration. Deployment is optional and requires the repository owner to sign in to the hosting provider and approve the deployment.

## Current readiness

Do not deploy this as a real AML/KYC decision tool. It is an educational prototype. Before a public demo:
- Confirm the latest GitHub Actions run is green.
- Run the source ingestion locally and review the generated manifest and passages.
- Confirm that no raw documents, generated customer records, secrets, or personal data are committed.
- Review the app's limitations and HDFC non-affiliation notice.
- Test the interface using synthetic scenarios only.

## Streamlit Community Cloud (optional)

1. Sign in to Streamlit Community Cloud using the account that can access the GitHub repository.
2. Choose **Create app** and select `iabhi09/fincrime-iq-hdfc-prototype`.
3. Select branch `main`.
4. Set the main file path to `app.py`.
5. Deploy. The platform should install packages from `requirements.txt`.
6. Open the generated app URL and verify both tabs load.
7. Keep the app public only if you are comfortable with the repository and demo being public.

Hosting free tiers, limits, and availability are controlled by the provider and can change. This repository does not promise free hosting forever.

## Knowledge-base setup

The source ingestion command is:

```bash
python -m ingestion.ingest
```

It downloads configured public sources into `knowledge_base/raw/` and writes:
- `knowledge_base/extracted/chunks.jsonl`
- `knowledge_base/extracted/manifest.json`

These files are local generated data and should remain uncommitted. Review every source and extracted passage before relying on it. If the deployed app has no extracted chunks, Policy Intelligence will correctly return the abstention response rather than pretending the knowledge base is populated.

## Privacy and security

- Never enter live customer names, account numbers, identity documents, case notes, or confidential data.
- Never add internal HDFC Bank SOPs or AML RightSource / client documents to this public repository.
- Do not add API keys or passwords to source files, Git history, Streamlit config, or issue comments.
- A public demo is not suitable for institutional workflows or production case handling.
