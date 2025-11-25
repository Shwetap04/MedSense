# backend/nlp/symptom_mapper.py
from pathlib import Path
import json
import re
import spacy
from typing import List, Dict, Any

nlp = spacy.load("en_core_web_sm")

class SymptomMapper:
    """
    Maps user text to normalized symptoms from data/symptoms_db.json,
    returns structured symptom info for downstream modules.
    """
    def __init__(self, db_path: str = "../../data/symptoms_db.json"):
        self.db_path = Path(db_path).resolve()
        with open(self.db_path, "r") as f:
            self.db = json.load(f)
        self.known_symptoms = set(self.db.get("symptoms", {}).keys())

    def _normalize(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r"[^a-z0-9\s]", " ", text)
        return re.sub(r"\s+", " ", text).strip()

    def map(self, user_text: str) -> List[Dict[str, Any]]:
        """
        Return a list of dicts: { symptom, severity, related_conditions }
        """
        text = self._normalize(user_text)
        doc = nlp(text)
        tokens = [t.lemma_ for t in doc if not t.is_stop]

        matched = set()
        # direct substring matches
        for s in self.known_symptoms:
            if s in text:
                matched.add(s)

        # token-level fuzzy
        for tok in tokens:
            for s in self.known_symptoms:
                if tok == s or tok in s or s in tok:
                    matched.add(s)

        results = []
        for s in matched:
            info = self.db["symptoms"].get(s, {})
            results.append({
                "symptom": s,
                "severity": info.get("severity_score", 1),
                "related_conditions": info.get("related_conditions", [])
            })
        return results
