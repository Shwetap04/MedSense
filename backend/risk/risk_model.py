# backend/risk/risk_model.py
from typing import List, Dict

class RiskModel:
    """
    Rule-based risk scoring module.
    Accepts symptom_info: list of {'symptom':str,'severity':int}
    Returns: {'risk_score': int, 'risk_level': str}
    """
    def __init__(self):
        pass

    def compute(self, symptom_info: List[Dict]) -> Dict:
        if not symptom_info:
            return {"risk_score": 0, "risk_level": "Low"}

        total = sum(item.get("severity", 1) for item in symptom_info)
        max_sev = max(item.get("severity", 1) for item in symptom_info)

        # Tunable formula: weight total + max
        score = int(min(100, total * 10 + max_sev * 5))
        if score < 25:
            level = "Low"
        elif score < 50:
            level = "Medium"
        elif score < 75:
            level = "Elevated"
        else:
            level = "High"
        return {"risk_score": score, "risk_level": level}
