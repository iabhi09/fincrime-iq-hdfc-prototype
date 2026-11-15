from __future__ import annotations

import streamlit as st
from fincrime_core import ABSTENTION, analyse_scenario, load_chunks, retrieve, source_label

st.set_page_config(page_title="FinCrime IQ", page_icon="🛡️", layout="wide")

st.title("🛡️ FinCrime IQ")
st.subheader("Policy & Investigation Intelligence")
st.warning(
    "Independent public-source prototype. Not an official HDFC Bank product and not affiliated with or endorsed by HDFC Bank. "
    "Use anonymised examples only. Never enter real customer, personal, confidential, or account information."
)

st.markdown(
    "An evidence-led learning assistant for understanding publicly available AML/KYC material and exploring "
    "anonymised transaction scenarios. It does not make customer decisions or replace approved institutional procedures."
)

chunks = load_chunks()
st.caption(f"Knowledge base: {len(chunks)} extracted passages loaded · Retrieval: transparent lexical ranking")

policy_tab, investigation_tab, about_tab = st.tabs(
    ["📚 Policy Intelligence", "🔎 Investigation Intelligence", "ℹ️ About & limitations"]
)

with policy_tab:
    st.markdown("### Ask about indexed public-source material")
    authority_options = sorted({
        str(row.get("authority")).strip()
        for row in chunks
        if row.get("authority") and str(row.get("authority")).strip()
    })
    selected_authority = st.selectbox(
        "Source authority",
        options=["All source classes"] + authority_options,
        help="Keep HDFC public policy, Indian regulation and international standards distinct."
    )
    question = st.text_area(
        "Your policy or AML/KYC question",
        placeholder="Example: What customer due diligence concepts are described in the indexed public documents?",
        height=110,
        key="policy_question"
    )
    if st.button("Search knowledge base", type="primary", key="policy_search"):
        if not question.strip():
            st.info("Enter a question first.")
        else:
            authority_filter = None if selected_authority == "All source classes" else {selected_authority}
            hits = retrieve(question, chunks, authorities=authority_filter)
            if not hits:
                st.warning(ABSTENTION)
                st.caption("No sufficiently relevant passage was found in the currently indexed knowledge base.")
            else:
                st.markdown("#### Relevant source passages")
                for i, hit in enumerate(hits, 1):
                    with st.expander(f"{i}. {source_label(hit)} · score {hit['retrieval_score']}", expanded=(i == 1)):
                        if hit.get("authority"):
                            st.caption(f"Authority class: {hit['authority']}")
                        st.write(hit["text"])
                        if hit.get("url"):
                            st.markdown(f"[Open source document]({hit['url']})")
                        if hit.get("page"):
                            st.caption(f"Page: {hit['page']}")
                st.info("Review the cited source text directly before relying on it. Ranking scores are not confidence scores. This MVP retrieves evidence; it does not generate a verified legal interpretation.")

with investigation_tab:
    st.markdown("### Explore an anonymised transaction scenario")
    scenario = st.text_area(
        "Describe the activity without personal or identifying information",
        placeholder="Example: A salaried customer receives funds from several unrelated individuals and transfers most of the money to one beneficiary on the same day.",
        height=140,
        key="scenario"
    )
    if st.button("Analyse indicators", type="primary", key="scenario_analyse"):
        if not scenario.strip():
            st.info("Describe an anonymised scenario first.")
        else:
            findings = analyse_scenario(scenario)
            if findings:
                st.markdown("#### Potential indicators to consider")
                for finding in findings:
                    with st.expander(finding["name"], expanded=True):
                        st.write(finding["explanation"])
                        st.caption("Detection method: explicit phrase matching. A missing match does not mean the activity is safe.")
                        st.markdown("**Matched phrases in your description**")
                        st.write(", ".join(finding["matched_indicators"]))
                        st.markdown("**Suggested investigative checks**")
                        for check in finding["checks"]:
                            st.markdown(f"- {check}")
            else:
                st.info("No configured phrase-based indicator was matched. This does not mean the activity is low risk or cleared.")
            st.warning(
                "These are preliminary educational indicators, not findings of wrongdoing. "
                "A red flag is not proof of money laundering. Consider the full customer profile, context, evidence, and applicable approved procedures."
            )

with about_tab:
    st.markdown("### What this prototype can and cannot do")
    st.markdown("""
**Current capabilities**
- Search locally indexed text passages from configured public sources.
- Display retrieved passages and source links.
- Match a small set of phrase-based AML typology indicators in anonymised scenarios.
- Suggest general evidence-led investigation checks.

**Current limitations**
- Retrieval uses transparent lexical ranking (TF-IDF-like), not semantic search or BM25.
- Scenario analysis is phrase matching, not a trained AML model.
- The application does not establish facts, determine suspicion, generate SAR/STR decisions, or provide legal advice.
- Internal HDFC Bank SOPs, alert thresholds, workflows, and confidential procedures are not included unless separately approved and lawfully provided.
- Source versions and applicability must be checked before operational reliance.
- No live customer data should be entered.

**Required abstention**
> This information is not covered in the provided policy documents.

**Production prerequisites**
Approved source documents, access controls, secure hosting, audit logs, source versioning, formal validation, security testing, and compliance/legal approval.
""")
