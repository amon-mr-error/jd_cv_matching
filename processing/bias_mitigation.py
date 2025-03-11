import re
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def anonymize_text(text):
    """
    Removes personally identifiable information (PII) to reduce bias.
    """
    text = re.sub(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', 'CANDIDATE', text)  # Remove full names
    text = re.sub(r'\b(?:Male|Female|Other)\b', 'GENDER_NEUTRAL', text, flags=re.IGNORECASE)  # Remove gender info
    text = re.sub(r'\b(?:[0-9]{2}/[0-9]{2}/[0-9]{4}|[0-9]{2}-[0-9]{2}-[0-9]{4})\b', 'DOB_REDACTED', text)  # Remove DOB
    return text

def normalize_scores(scores, demographic_data):
    """
    Adjusts candidate scores based on demographic distribution to mitigate bias.
    """
    scaler = MinMaxScaler()
    normalized_scores = scaler.fit_transform(np.array(scores).reshape(-1, 1)).flatten()
    
    # Example: Adjust based on underrepresented groups
    for i, demo in enumerate(demographic_data):
        if demo in ['Female', 'Minority', 'Other']:  # Underrepresented groups
            normalized_scores[i] += 0.05  # Small boost for fairness
    
    return np.clip(normalized_scores, 0, 1)  # Ensure scores stay within [0,1] range

def adjust_for_fairness(ranked_candidates, demographic_data):
    """
    Re-ranks candidates to ensure a fair distribution across demographics.
    """
    adjusted_ranking = sorted(ranked_candidates, key=lambda x: (x['score'], demographic_data.get(x['id'], '')), reverse=True)
    return adjusted_ranking
