# Public Source Catalogue and Review Notes

**Review date:** 15 November 2026  
**Purpose:** Research catalogue for an independent educational prototype. This is not legal advice, and it does not establish HDFC Bank's internal requirements.

## Source classes

- HDFC Bank public policy: describes publicly disclosed bank policy only.
- Indian law and regulation: controlling legal/regulatory sources, subject to applicability, amendments and commencement.
- Indian regulatory guidance: official explanatory material; read alongside binding instruments.
- International standards: FATF standards are not automatically Indian law or HDFC Bank policy.

## Sources checked

| Source | Publisher / class | Version information observed | Handling |
|---|---|---|---|
| [HDFC Bank Policy on KYC norms, AML and CFT measures](https://www.hdfc.bank.in/content/dam/hdfcbankpws/in/en/personal-banking/discover-products/about-us/corporate-governance/codes-and-policies/Policy-on-KYC-norms-AML-and-CFT-measures.pdf) | HDFC Bank public policy | HDFC page metadata identifies last update as January 2026 | Preserve downloaded copy; inspect PDF, pages, tables and footnotes. |
| [HDFC Bank Codes and Policies](https://www.hdfc.bank.in/about-us/corporate-governance/codes-and-policies) | HDFC Bank public directory | Directory lists KYC/AML/CFT Policy and Note on KYC/AML/CFT process | Directory is not itself the underlying policy. Follow and verify linked documents before indexing. |
| [HDFC Bank Note on KYC/AML/CFT Process](https://www.hdfc.bank.in/content/dam/hdfcbankpws/in/en/personal-banking/discover-products/about-us/corporate-governance/codes-and-policies/note-on-kyc-aml-cft-process.pdf) | HDFC Bank public overview — historical / explanatory | Search metadata suggests an older document; current publication/effective date not established | Use only as a historical public overview. It explicitly distinguishes high-level policy from product/operations SOPs; do not present it as a current SOP. |
| [RBI Commercial Banks – KYC Directions, 2025](https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=13141) | RBI regulation | Page states updated as on 1 October 2026; issued 28 November 2025 | Use the consolidated direction with relevant amendment notices. Confirm entity scope and effective dates. |
| [RBI Commercial Banks – KYC Amendment Directions, 2026](https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=13699) | RBI regulation | Notice dated 18 September 2026 | Preserve as a change record; compare its amendments with the consolidated direction. |
| [Prevention of Money-laundering Act, 2002](https://www.indiacode.nic.in/indiacode/handle/123456789/2036?view_type=browse) | India Code / legislation | Current consolidated text and amendment history require further verification | Do not rely on an older standalone Act PDF as a current consolidated text. |
| [FIU-IND AML legislation and notifications](https://fiuindia.gov.in/files/AML_Legislation/notification.html) | FIU-IND / regulatory material | Page lists Rules and amendments; not treated as a consolidated compilation | Review all applicable amendments and Gazette notifications. |
| [FIU-IND FAQs](https://fiuindia.gov.in/files/FAQs/faqs.html) | FIU-IND / guidance | Current version date not clearly established in this review | Explanatory guidance only; verify requirements against binding law and regulation. |
| [FATF Recommendations](https://www.fatf-gafi.org/en/publications/Fatfrecommendations/Fatf-recommendations.html) | FATF / international standards | FATF page states last updated June 2026 | Label as international standards, not domestic law or HDFC policy. |

## Important source interpretation controls

1. Do not describe a public HDFC policy as a complete internal SOP.
2. Do not treat FATF standards as automatically binding domestic requirements.
3. Do not use a search-result snippet as a substitute for the source document.
4. A successful download or text extraction does not prove that a document is current, complete, legally applicable or authoritative.
5. Where sources conflict, preserve both sources and explain their dates and authority. Do not silently choose one.
6. Do not publish confidential internal procedures, customer data, case examples or employer/client material.
7. No reporting thresholds, timelines, escalation routes or acceptance criteria should be stated unless supported by a current, applicable primary source.

## Engineering status

The source registry is machine-readable at `config/source_registry.json`. The ingestion process writes local-only raw files, JSONL passages and a manifest under `knowledge_base/`. These generated source files are not committed to the public repository by design.

Before any demo, review the source manifest and the original source documents manually. The manifest records retrieval metadata and hashes; it is not a legal validation certificate.
