# FinCrime IQ — Policy & Investigation Intelligence

An independent, public-source-based AML/KYC learning and analyst-support prototype focused on Indian banking regulations and publicly available HDFC Bank materials.

> **Important:** This is an independent portfolio prototype. It is not an official HDFC Bank product, is not affiliated with or endorsed by HDFC Bank, and must not be used to make real customer decisions. Do not enter personal, confidential, or live customer information.

## Purpose

FinCrime IQ is designed to help AML/KYC analysts understand public policy material and reason through anonymised transaction scenarios. It aims to:

- Retrieve relevant passages from a curated public-source knowledge base.
- Explain AML concepts and potential red flags in plain language.
- Suggest evidence-led investigation questions and next checks.
- Distinguish public HDFC material, Indian regulation, international standards, and general typology guidance.
- Cite source passages and abstain when the knowledge base does not support an answer.

## Safety boundaries

- A typology or red flag is an indicator, not proof of financial crime.
- The prototype does not approve, reject, close, or file on any case.
- It does not represent internal HDFC procedures, thresholds, or systems.
- Where information is not supported by indexed sources, it should say: **“This information is not covered in the provided policy documents.”**
- Use anonymised examples only. Production use would require approved internal documentation, security controls, auditability, and compliance/legal approval.

## Planned stack

Python, Streamlit, local document extraction, source-aware retrieval, and a local metadata/index store. No paid external LLM API is required for the initial deterministic prototype.

## Status

Project foundation is being assembled. Source verification, ingestion quality, tests, and deployment are still required before the prototype can be considered ready for demonstration.
