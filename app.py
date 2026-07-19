import streamlit as st
import pandas as pd
import os
from risk_engine import calculate_inherent_risk, get_nist_iso_mapping
from llm_engine import generate_controls_with_llm

# Page Configuration
st.set_page_config(page_title="AI GRC Toolkit 2026", page_icon="⚖️", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .main-header {font-size: 2.5rem; font-weight: bold; color: #1f77b4;}
    .sub-header {font-size: 1.2rem; color: #555;}
    .metric-card {background-color: #f0f2f6; padding: 1rem; border-radius: 0.5rem;}
    </style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("⚖️ AI GRC Toolkit")
page = st.sidebar.radio("Navigate", [
    "Home", 
    "Risk Assessment", 
    "Risk Register", 
    "Controls Catalog",
    "🤖 AI Control Generator"  # 🆕 NEW PAGE
])

# --- HOME PAGE ---
if page == "Home":
    st.markdown('<p class="main-header">AI Governance & Risk Management Toolkit</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Aligned with NIST AI RMF & ISO/IEC 42001:2023</p>', unsafe_allow_html=True)
    
    st.divider()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Framework", "NIST AI RMF")
    with col2:
        st.metric("Standard", "ISO/IEC 42001")
    with col3:
        st.metric("AI Engine", "LLM-Powered ✨")
        
    st.markdown("""
    ### 🎯 Project Objective
    This toolkit translates abstract AI ethics and regulatory concepts into actionable, auditable business controls. 
    It provides a standardized method to assess AI systems, map risks to global frameworks, and track mitigating controls.
    
    ### 🚀 How to Use
    1. Go to **Risk Assessment** to evaluate a new AI use case.
    2. Review the **Risk Register** for pre-mapped HR AI risks.
    3. Consult the **Controls Catalog** for actionable mitigation strategies.
    4. **🤖 NEW:** Use the AI Control Generator to auto-generate controls from any AI system description!
    """)

# --- RISK ASSESSMENT PAGE ---
elif page == "Risk Assessment":
    st.header("📊 AI System Risk Assessment")
    st.markdown("Rate the following dimensions from 1 (Low) to 5 (High) to calculate the inherent risk score.")
    
    col1, col2 = st.columns(2)
    with col1:
        data_sens = st.slider("1. Data Sensitivity (PII/Sensitive Data)", 1, 5, 4, help="ISO 42001 A.8.3")
        autonomy = st.slider("2. Level of Autonomy (Human-in-the-loop?)", 1, 5, 3, help="NIST MANAGE 3.3")
        impact = st.slider("3. Business/Societal Impact Severity", 1, 5, 5, help="NIST MAP 2.2")
    
    with col2:
        fairness = st.slider("4. Fairness & Bias Risk", 1, 5, 4, help="NIST MEASURE 2.2")
        explain = st.slider("5. Explainability / 'Black Box' Risk", 1, 5, 4, help="ISO 42001 A.8.7")

    if st.button("Calculate Risk", type="primary"):
        score, level, color = calculate_inherent_risk(data_sens, autonomy, impact, fairness, explain)
        
        st.divider()
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Inherent Risk Score", f"{score}/100")
        with c2:
            st.metric("Risk Level", f"{color} {level}")
        with c3:
            st.metric("Recommended Action", "Immediate Mitigation" if score >= 60 else "Standard Monitoring")
            
        st.info("**Next Steps:** Document this assessment in the Risk Register and assign controls from the Controls Catalog.")

# --- RISK REGISTER PAGE ---
elif page == "Risk Register":
    st.header("📑 Mapped Risk Register (HR AI Use Case)")
    
    data = {
        "Risk ID": ["R-01", "R-02", "R-03"],
        "Risk Description": [
            "Model exhibits gender/racial bias due to historical training data.",
            "Unauthorized access to applicant PII (Resumes, contact info).",
            "'Black box' decisions lead to inability to explain candidate rejection."
        ],
        "Inherent Risk": ["High", "Critical", "High"],
        "NIST AI RMF Mapping": [
            "MEASURE 2.2 (Assess for harmful bias)",
            "GOVERN 2.5 (Integrate with privacy frameworks)",
            "MANAGE 3.3 (Ensure transparency & handle anomalies)"
        ],
        "ISO 42001 Mapping": [
            "A.8.2 (AI System Impact Assessment)",
            "A.8.3 (Data for AI Systems)",
            "A.8.7 (Transparency and Explainability)"
        ]
    }
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.download_button(
        label="📥 Download Risk Register (CSV)",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name='ai_risk_register.csv',
        mime='text/csv'
    )

# --- CONTROLS CATALOG PAGE ---
elif page == "Controls Catalog":
    st.header("🛡️ Mitigating Controls Catalog")
    
    controls_data = {
        "Control ID": ["C-01", "C-02", "C-03"],
        "Linked Risk": ["R-01 (Bias)", "R-02 (PII)", "R-03 (Explainability)"],
        "Control Type": ["Detective", "Preventive", "Administrative"],
        "Control Description": [
            "Mandate quarterly fairness audits using open-source tools (e.g., IBM AIF360).",
            "Enforce data anonymization/pseudonymization prior to model ingestion.",
            "Require 'Human-in-the-Loop' (HITL) review for all automated rejection decisions."
        ],
        "Owner": ["Data Science Lead", "InfoSec Team", "HR Compliance Officer"]
    }
    df_controls = pd.DataFrame(controls_data)
    st.dataframe(df_controls, use_container_width=True, hide_index=True)

# --- 🆕 AI CONTROL GENERATOR PAGE ---
elif page == "🤖 AI Control Generator":
    st.header("🤖 AI-Powered Control Generator")
    st.markdown("""
    Describe your AI system below, and our LLM will automatically generate **framework-aligned risks and controls** 
    based on NIST AI RMF and ISO/IEC 42001.
    """)
    
    # Mode selector
    use_mock = st.toggle(
        "🎭 Use Demo Mode (no API key required)", 
        value=True,
        help="Demo mode uses pre-written responses. Turn off to use real OpenAI API (requires API key in .env file)."
    )
    
    # System description input
    system_description = st.text_area(
        "📝 Describe your AI system:",
        height=150,
        placeholder="Example: An AI-powered HR chatbot that screens resumes, ranks candidates, and sends automated rejection emails. It processes personal data including names, emails, and work history.",
        help="Be specific about what the AI does, what data it uses, and who it affects."
    )
    
    # Example buttons
    st.markdown("**💡 Try an example:**")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("HR Resume Screener", use_container_width=True):
            system_description = "An AI system that screens job resumes, extracts skills, and ranks candidates for software engineering roles. It processes PII and makes automated decisions affecting employment."
    with col2:
        if st.button("Customer Service Chatbot", use_container_width=True):
            system_description = "A customer-facing chatbot that handles support tickets, answers product questions, and escalates complex issues to human agents. It accesses customer account data."
    with col3:
        if st.button("Financial Fraud Detector", use_container_width=True):
            system_description = "An ML model that analyzes transaction patterns in real-time to detect potential fraud. It can freeze accounts and flags transactions for manual review."
    
    # Generate button
    if st.button("🚀 Generate Controls", type="primary", disabled=not system_description):
        with st.spinner("🧠 Analyzing AI system and generating controls..."):
            controls_output = generate_controls_with_llm(system_description, use_mock=use_mock)
        
        st.divider()
        st.markdown(controls_output)
        
        # Download buttons
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="📥 Download as Markdown",
                data=controls_output,
                file_name="ai_controls_report.md",
                mime="text/markdown"
            )
        with col2:
            st.download_button(
                label="📋 Copy to Clipboard",
                data=controls_output,
                mime="text/plain"
            )
        
        st.success("✅ Controls generated successfully! Review and customize for your organization.")
    
    # Info box
    st.info("""
    **💡 How it works:** This feature uses a Large Language Model (LLM) trained on GRC best practices to analyze your AI system description and generate tailored risks and controls. 
    In demo mode, it uses pre-written responses. Connect your OpenAI API key in the `.env` file for fully customized, real-time generation.
    """)