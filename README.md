# FinCrime IQ — Policy & Investigation Intelligence

An independent, public-source-based AML/KYC learning and analyst-support prototype focused on Indian banking regulations and publicly available HDFC Bank materials.

> **Important:** This is an independent portfolio prototype. It is not an official HDFC Bank product, is not affiliated with or endorsed by HDFC Bank, and must not be used to make real customer decisions. Do not enter personal, confidential, or live customer information.

## Purpose

FinCrime IQ is designed to help AML/KYC analysts understand public policy material and explore anonymised transaction scenarios. It aims to:
- Retrieve relevant passages from a curated public-source knowledge base.
- Explain selected AML concepts in plain language.
- Highlight possible indicators and suggest evidence-led investigation checks.
- Distinguish public HDFC material, Indian regulation, international standards, and general typology education.
- Abstain when indexed policy material does not support an answer.

## Current capabilities
- Streamlit interface with Policy Intelligence, Investigation Intelligence and AML Concepts areas.
- Transparent lexical policy retrieval (not semantic search or a complete RAG system).
- Phrase-based educational indicators for a limited set of typologies.
- Structured investigation summaries separating user-described facts, possible indicators, alternative explanations, missing information and checks.
- Curated AML concept cards with definitions, simple examples, possible indicators, alternative explanations and investigation checks.
- GitHub Actions compiles Python files and runs unit tests.

## Safety boundaries
- A typology or red flag is an indicator, not proof of financial crime.
- Concept explanations are general educational content, not HDFC Bank policy or legal advice.
- The prototype does not approve, reject, close, or file on any case.
- It does not represent internal HDFC procedures, thresholds, or systems.
- Where indexed policy information is not found, it should say: **“This information is not covered in the provided policy documents.”**
- Use anonymised examples only. Production use would require approved internal documentation, security controls, auditability, and compliance/legal approval.

## Technical approach
Python, Streamlit, local document extraction, transparent lexical/alias lookup, and local files. No paid external LLM API is required for the current deterministic prototype.

## Known limitations and next work
The prototype is not a validated or deployment-ready AML assistant. Policy extraction, source currency, broader language coverage, end-to-end behaviour, security and user experience still require review. The concept library is curated and finite; it does not understand arbitrary questions like a general-purpose language model.
