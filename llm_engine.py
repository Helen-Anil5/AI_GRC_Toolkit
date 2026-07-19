"""
LLM Engine for AI GRC Toolkit
Uses OpenAI API to generate framework-aligned controls based on AI system descriptions.
Includes a mock mode for demo purposes (no API key required).
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# System prompt that instructs the LLM on how to behave as a GRC expert
SYSTEM_PROMPT = """You are an expert AI Governance, Risk, and Compliance (GRC) consultant 
specialized in NIST AI RMF and ISO/IEC 42001 frameworks. 

When given a description of an AI system, you will:
1. Identify the top 3-5 critical risks
2. For each risk, provide:
   - Risk ID (format: R-XX)
   - Risk description (1 sentence)
   - NIST AI RMF mapping (specific function and subcategory)
   - ISO 42001 mapping (specific Annex A control)
   - Recommended control (actionable, specific mitigation)
   - Control type (Preventive, Detective, or Administrative)
   - Suggested owner (role responsible)

Format your response as a clean, structured markdown table.
Be specific, practical, and aligned with real-world GRC best practices.
"""


def generate_controls_with_llm(system_description: str, use_mock: bool = False) -> str:
    """
    Generates AI governance controls using an LLM.
    
    Args:
        system_description: User's description of their AI system
        use_mock: If True, returns a pre-written response (no API call, no cost)
    
    Returns:
        Formatted markdown string with risks and controls
    """
    
    # Mock mode - perfect for demos and portfolio without API costs
    if use_mock or not os.getenv("OPENAI_API_KEY"):
        return _get_mock_response(system_description)
    
    # Real LLM mode - only initialize client if we actually need it
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Cost-effective model
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Analyze this AI system and generate controls:\n\n{system_description}"}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        return response.choices[0].message.content
    
    except Exception as e:
        return f"Error calling LLM: {str(e)}\n\nFalling back to mock response.\n\n" + _get_mock_response(system_description)


def _get_mock_response(system_description: str) -> str:
    """Returns a realistic pre-written response for demo purposes."""
    
    # Detect keywords to provide a contextually relevant mock response
    desc_lower = system_description.lower()
    
    if any(word in desc_lower for word in ["hr", "resume", "hiring", "recruit"]):
        return """## AI System Analysis: HR Resume Screener

Based on your description, here are the critical risks and recommended controls:

| Risk ID | Risk Description | NIST AI RMF | ISO 42001 | Recommended Control | Type | Owner |
|---------|------------------|-------------|-----------|---------------------|------|-------|
| R-01 | Model may exhibit demographic bias from historical hiring data | MEASURE 2.2 | A.8.2 | Implement quarterly fairness audits using IBM AIF360; require balanced training datasets | Detective | Data Science Lead |
| R-02 | Applicant PII exposure during resume processing | GOVERN 2.5 | A.8.3 | Enforce data anonymization before model ingestion; enable DLP monitoring | Preventive | InfoSec Team |
| R-03 | Inability to explain candidate rejection decisions | MANAGE 3.3 | A.8.7 | Deploy SHAP values for explainability; mandate Human-in-the-Loop for all rejections | Administrative | HR Compliance |
| R-04 | Model drift degrading ranking accuracy over time | MEASURE 2.5 | A.8.5 | Monitor prediction distributions weekly; trigger retraining on accuracy drop >5% | Detective | ML Engineer |

### Implementation Priority
1. **Immediate (Week 1-2):** Deploy PII anonymization (R-02)
2. **Short-term (Month 1):** Implement fairness audits (R-01)
3. **Ongoing:** Quarterly explainability reviews (R-03)
"""
    
    elif any(word in desc_lower for word in ["chatbot", "customer", "support"]):
        return """## AI System Analysis: Customer Service Chatbot

Based on your description, here are the critical risks and recommended controls:

| Risk ID | Risk Description | NIST AI RMF | ISO 42001 | Recommended Control | Type | Owner |
|---------|------------------|-------------|-----------|---------------------|------|-------|
| R-01 | Chatbot may generate harmful or inappropriate responses | MANAGE 3.1 | A.8.4 | Implement input/output guardrails using content filtering; conduct red-teaming quarterly | Preventive | AI Safety Team |
| R-02 | Hallucination risk providing incorrect product/service info | MEASURE 2.3 | A.8.6 | Use RAG architecture with verified knowledge base; add confidence scoring | Preventive | ML Engineer |
| R-03 | Customer data leakage through prompt injection attacks | GOVERN 2.5 | A.8.3 | Sanitize all inputs; implement PII detection in outputs; rate-limit API calls | Preventive | InfoSec Team |
| R-04 | Escalation failures for complex/emotional customer issues | MAP 2.3 | A.8.2 | Define clear escalation triggers; monitor sentiment; require HITL for high-stakes cases | Administrative | CX Operations |

### Implementation Priority
1. **Immediate:** Deploy content guardrails (R-01)
2. **Week 1-2:** Implement RAG with knowledge base (R-02)
3. **Month 1:** Red-team testing and escalation workflows (R-03, R-04)
"""
    
    else:
        return """## AI System Analysis: General AI System

Based on your description, here are the critical risks and recommended controls:

| Risk ID | Risk Description | NIST AI RMF | ISO 42001 | Recommended Control | Type | Owner |
|---------|------------------|-------------|-----------|---------------------|------|-------|
| R-01 | Potential for biased or unfair outcomes affecting stakeholders | MEASURE 2.2 | A.8.2 | Conduct bias testing across protected classes; document fairness metrics | Detective | Data Science Lead |
| R-02 | Unauthorized access to training or inference data | GOVERN 2.5 | A.8.3 | Implement RBAC; encrypt data at rest and in transit; audit access logs | Preventive | InfoSec Team |
| R-03 | Lack of transparency in decision-making process | MANAGE 3.3 | A.8.7 | Deploy explainability tools (SHAP/LIME); create user-facing documentation | Administrative | AI Ethics Officer |
| R-04 | Model performance degradation over time | MEASURE 2.5 | A.8.5 | Monitor drift metrics weekly; establish retraining triggers | Detective | ML Engineer |

### Implementation Priority
1. **Immediate:** Data access controls (R-02)
2. **Short-term:** Bias testing and explainability (R-01, R-03)
3. **Ongoing:** Continuous monitoring (R-04)

**Tip:** For more tailored controls, connect a real OpenAI API key in the `.env` file.
"""