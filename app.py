from __future__ import annotations

import streamlit as st
from demo_scenarios import DEMO_SCENARIOS, get_demo_scenario
from aml_concepts import retrieve_concepts
from fincrime_core import ABSTENTION, build_investigation_summary, load_chunks, retrieve, source_label

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

policy_tab, investigation_tab, concepts_tab, about_tab = st.tabs(
    ["📚 Policy Intelligence", "🔎 Investigation Intelligence", "💡 AML Concepts", "ℹ️ About & limitations"]
)

with policy_tab:
    st.markdown("### Ask about indexed public-source material")
    if not chunks:
        st.warning(
            "No policy passages are indexed in this checkout yet. The policy tab will not invent answers. "
            "Run the local source-ingestion command and review its manifest and extracted passages before using this tab."
        )
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
    st.caption("You can use one of the invented examples or write your own fully anonymised scenario.")
    def _load_demo_scenario() -> None:
        st.session_state["scenario"] = get_demo_scenario(
            st.session_state.get("demo_scenario", "")
        )

    demo_names = ["Write my own scenario"] + list(DEMO_SCENARIOS.keys())
    selected_demo = st.selectbox(
        "Optional synthetic example",
        demo_names,
        key="demo_scenario",
        on_change=_load_demo_scenario,
    )
    default_scenario = get_demo_scenario(selected_demo)
    scenario = st.text_area(
        "Describe the activity without personal or identifying information",
        value=default_scenario,
        placeholder="Example: A salaried customer receives funds from several unrelated individuals and transfers most of the money to one beneficiary on the same day.",
        height=140,
        key="scenario"
    )
    if st.button("Analyse indicators", type="primary", key="scenario_analyse"):
        if not scenario.strip():
            st.info("Describe an anonymised scenario first.")
        else:
            summary = build_investigation_summary(scenario)
            st.markdown("#### 1. Observed facts — as described")
            st.caption("These are statements from the scenario you entered; the assistant has not independently verified them.")
            for fact in summary["observed_facts"]:
                st.markdown(f"- {fact}")
            st.markdown("#### 2. Potential indicators")
            if summary["potential_indicators"]:
                for finding in summary["potential_indicators"]:
                    with st.expander(finding["name"], expanded=True):
                        st.write(finding["explanation"])
                        st.caption("Detection method: explicit phrase matching, not a probability or risk score.")
                        st.markdown("**Matched phrases**")
                        st.write(", ".join(finding["matched_indicators"]))
            else:
                st.info(summary["no_indicator_message"])
            st.markdown("#### 3. Alternative explanations to test")
            for explanation in summary["alternative_explanations"]:
                st.markdown(f"- {explanation}")
            st.markdown("#### 4. Missing information")
            for item in summary["missing_information"]:
                st.markdown(f"- {item}")
            st.markdown("#### 5. Suggested investigation checks")
            for check in summary["suggested_checks"]:
                st.markdown(f"- {check}")
            st.warning(summary["disclaimer"])

with concepts_tab:
    st.markdown("### Ask an AML concept in plain language")
    st.caption("Curated educational explanations with transparent alias/keyword lookup. These are not HDFC Bank policy, legal advice, or a substitute for current approved procedures.")
    concept_question = st.text_input(
        "What would you like to understand?",
        placeholder="Example: What is a funnel account and what should I check?"
    )
    if st.button("Explain concept", type="primary", key="concept_search"):
        if not concept_question.strip():
            st.info("Enter a concept or question first.")
        else:
            concept_hits = retrieve_concepts(concept_question, limit=3)
            if not concept_hits:
                st.info("This concept is not yet in the curated AML Concepts library. Try a specific term such as funnel account, layering, structuring, money mule, placement, integration, round-tripping, pass-through activity, or source of funds.")
            else:
                for concept in concept_hits:
                    with st.expander(concept["name"], expanded=True):
                        st.markdown("**In simple words**")
                        st.write(concept["definition"])
                        st.markdown("**Simple example**")
                        st.write(concept["example"])
                        st.markdown("**Possible indicators to understand**")
                        for indicator in concept["indicators"]:
                            st.markdown(f"- {indicator}")
                        st.markdown("**Other explanations to test**")
                        for alternative in concept["alternatives"]:
                            st.markdown(f"- {alternative}")
                        st.markdown("**What an investigator can check**")
                        for check in concept["checks"]:
                            st.markdown(f"- {check}")
                        st.caption(f"Knowledge classification: {concept['source_class']} · {concept['source_note']}")
                st.warning("A concept match is educational only. It does not establish suspicious activity, customer risk, or a reporting decision.")

with about_tab:
    st.markdown("### What this prototype can and cannot do")
    st.markdown("""
**Current capabilities**
- Search locally indexed text passages from configured public sources.
- Display retrieved passages and source links.
- Match a small set of phrase-based AML typology indicators in anonymised scenarios.
- Explain a curated set of AML concepts using transparent keyword/alias lookup.
- Suggest general evidence-led investigation checks.

**Current limitations**
- Policy retrieval uses transparent lexical ranking (TF-IDF-like), not semantic search or BM25.
- Concept lookup is curated alias/keyword matching, not an LLM or semantic model.
- Scenario analysis is phrase matching, not a trained AML model.
- The application does not establish facts, determine suspicion, generate SAR/STR decisions, or provide legal advice.
- Internal HDFC Bank SOPs, alert thresholds, workflows, and confidential procedures are not included unless separately approved and lawfully provided.
- Source versions and applicability must be checked before operational reliance.
- No live customer data should be entered.

**Required policy abstention**
> This information is not covered in the provided policy documents.

**Production prerequisites**
Approved source documents, access controls, secure hosting, audit logs, source versioning, formal validation, security testing, and compliance/legal approval.
""")
