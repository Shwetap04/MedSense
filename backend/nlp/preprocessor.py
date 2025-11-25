# backend/nlp/preprocessor.py
import re
import spacy
from typing import List, Dict

nlp = spacy.load("en_core_web_sm")

def clean_text(text: str) -> str:
    """
    Basic normalization:
    - lowercase
    - remove symbols except alphanumeric + space
    - collapse whitespace
    """
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize(text: str) -> List[str]:
    """Tokenize text using spaCy."""
    doc = nlp(text)
    return [token.text for token in doc if not token.is_space]


def extract_noun_phrases(text: str) -> List[str]:
    """
    Extract medically relevant text chunks (symptoms often appear as noun phrases):
    e.g. "severe headache", "lower back pain"
    """
    doc = nlp(text)
    return [chunk.text for chunk in doc.noun_chunks]


def extract_symptom_candidates(text: str) -> List[str]:
    """
    Medical symptom candidates — filtered noun phrases + tokens:
    """
    text = clean_text(text)
    tokens = tokenize(text)
    chunks = extract_noun_phrases(text)

    candidates = set(tokens + chunks)
    return list(candidates)
