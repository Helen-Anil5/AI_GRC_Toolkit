import pandas as pd
import numpy as np

def calculate_inherent_risk(data_sensitivity, autonomy, impact, fairness_risk, explainability):
    """
    Calculates an inherent AI risk score (0-100) based on 5 key dimensions.
    Scale: 1 (Low) to 5 (High)
    
    Weighting reflects modern GRC priorities (Impact and Fairness are heavily weighted).
    """
    # Weights sum to 1.0
    weights = {
        'data_sensitivity': 0.20,  # ISO 42001 A.8.3 (Data Protection)
        'autonomy': 0.15,          # NIST AI RMF (Human Oversight)
        'impact': 0.30,            # NIST AI RMF (Safety & Rights)
        'fairness_risk': 0.20,     # NIST AI RMF (Fairness & Bias)
        'explainability': 0.15     # ISO 42001 A.8.7 (Transparency)
    }
    
    score = (
        (data_sensitivity * weights['data_sensitivity']) +
        (autonomy * weights['autonomy']) +
        (impact * weights['impact']) +
        (fairness_risk * weights['fairness_risk']) +
        (explainability * weights['explainability'])
    )
    
    # Normalize to 0-100 scale (max possible raw score is 5)
    normalized_score = (score / 5.0) * 100
    
    # Determine Risk Level
    if normalized_score >= 80:
        level = "CRITICAL"
        color = "🔴"
    elif normalized_score >= 60:
        level = "HIGH"
        color = "🟠"
    elif normalized_score >= 40:
        level = "MEDIUM"
        color = "🟡"
    else:
        level = "LOW"
        color = "🟢"
        
    return round(normalized_score, 1), level, color

def get_nist_iso_mapping(risk_area):
    """Returns relevant framework mappings based on the primary risk area."""
    mappings = {
        "Data Privacy": "NIST: GOVERN 2.5 | ISO 42001: A.8.3",
        "Autonomy/Oversight": "NIST: MANAGE 3.3 | ISO 42001: A.8.2",
        "Business Impact": "NIST: MAP 2.2 | ISO 42001: A.8.2",
        "Fairness/Bias": "NIST: MEASURE 2.2 | ISO 42001: A.8.2",
        "Explainability": "NIST: MANAGE 3.3 | ISO 42001: A.8.7"
    }
    return mappings.get(risk_area, "General AI Governance")