import spacy

nlp = spacy.load("en_core_web_sm")

SYMPTOM_KEYWORDS = [
    "pain", "ache", "headache", "nausea", "vomiting", "dizzy",
    "fever", "cramp", "fatigue", "cough", "burning", "rash",
    "swelling", "throat", "bleeding"
]

class SymptomExtractor:

    def extract(self, text):
        doc = nlp(text)
        symptoms = []

        for token in doc:
            if token.lemma_ in SYMPTOM_KEYWORDS:
                symptoms.append(token.text)

        # fallback: include nouns
        if not symptoms:
            for token in doc:
                if token.pos_ == "NOUN":
                    symptoms.append(token.text)

        return list(set(symptoms))
