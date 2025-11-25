# backend/app.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, List
import os
import uuid
import time

import google.generativeai as genai
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Configure Gemini
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("Missing GEMINI_API_KEY")

genai.configure(api_key=API_KEY)

# Import internal modules
from backend.nlp.symptom_mapper import SymptomMapper
from backend.rag.rag_engine import RagEngine
from backend.risk.risk_model import RiskModel

# Initialize app
app = FastAPI(title="MedSense API")

# CORS for Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load components
symptom_mapper = SymptomMapper("data/symptoms_db.json")
rag = RagEngine("data/medical_docs")
risk_model = RiskModel()

# ----------------------------
# Session Memory (in RAM)
# ----------------------------
sessions: Dict[str, Dict] = {}
SESSION_EXPIRY = 6 * 60 * 60  # 6 hours


def create_session(age, lifestyle):
    sid = str(uuid.uuid4())
    sessions[sid] = {
        "messages": [],
        "profile": {"age": age, "lifestyle": lifestyle},
        "last_active": time.time(),
    }
    return sid


def touch_session(sid):
    if sid in sessions:
        sessions[sid]["last_active"] = time.time()


def expire_sessions():
    now = time.time()
    expired = [sid for sid, s in sessions.items() if now - s["last_active"] > SESSION_EXPIRY]
    for sid in expired:
        del sessions[sid]


# ----------------------------
# Request Models
# ----------------------------

class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    user_message: str
    age: Optional[int] = None
    lifestyle: Optional[str] = None


# ----------------------------
# Utility Functions
# ----------------------------

def call_gemini(prompt):
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    return response.text


def clean_llm_json(text):
    import json, re
    try:
        raw = re.search(r"\{[\s\S]*\}", text)
        if raw:
            return json.loads(raw.group())
    except:
        pass
    return {"raw_text": text}


def personalize(mapped, risk):
    urgent = risk["risk_level"] == "High"

    if urgent:
        diet = ["Hydrate lightly", "Avoid heavy meals", "Stay seated", "Seek emergency help immediately"]
    else:
        diet = ["Balanced diet", "Low sodium", "More fruits & vegetables", "Maintain hydration"]

    return {
        "urgent": urgent,
        "recommended_diet": diet,
    }


# ----------------------------
# CHAT ENDPOINT
# ----------------------------

@app.post("/chat")
def chat(req: ChatRequest):

    expire_sessions()

    sid = req.session_id
    if not sid or sid not in sessions:
        sid = create_session(req.age, req.lifestyle)

    # Save user message
    sessions[sid]["messages"].append({
        "role": "user",
        "text": req.user_message,
        "ts": time.time()
    })
    touch_session(sid)

    # NLP + RAG + Risk
    mapped = symptom_mapper.map(req.user_message)
    risk = risk_model.compute(mapped)
    context_docs = rag.query(", ".join([m["symptom"] for m in mapped]), top_k=3)
    context_block = "\n\n---\n".join(context_docs)

    # Include conversation memory
    past_dialogue = "\n".join([f"{m['role'].upper()}: {m['text']}" for m in sessions[sid]["messages"][-8:]])

    # LLM prompt
    prompt = f"""
You are MedSense, a medically-safe AI assistant. You analyze symptoms but DO NOT diagnose.

Here is the past conversation:
{past_dialogue}

Here is the new user message:
{req.user_message}

MAPPED SYMPTOMS:
{mapped}

RISK ASSESSMENT:
{risk}

RELEVANT MEDICAL CONTEXT:
{context_block}

Return a CLEAN JSON with keys:
- possible_causes (short list)
- lifestyle_factors
- red_flags
- explanation (very clear, 2-3 sentences)
- suggested_actions
- risk_score
- risk_level
- llm_insights (new, explain reasoning)
- clarification_needed (what follow-up questions should be asked)
- personalized_diet (diet advice based on problem)
- urgent_advice (if high risk)

Keep text SHORT and medically safe.
"""

    llm_text = call_gemini(prompt)
    structured = clean_llm_json(llm_text)

    # Personalization Layer
    personalization = {
        "urgent": risk["risk_level"] == "High",
        "recommended_diet": [
            "Hydrate lightly",
            "Avoid spicy/heavy meals",
            "Eat soft, stomach-friendly foods",
            "Avoid caffeine/alcohol"
        ] if risk["risk_level"] == "High" else [
            "Balanced meal",
            "High fiber",
            "Low sodium",
            "Plenty of fruits"
        ]
    }

    # Save assistant response into memory
    sessions[sid]["messages"].append({
        "role": "assistant",
        "text": structured,
        "ts": time.time()
    })
    touch_session(sid)

    return {
        "session_id": sid,
        "mapped_symptoms": mapped,
        "risk": risk,
        "rag_docs_found": len(context_docs),
        "assistant_structured": structured,
        "personalization": personalization
    }

@app.get("/history/{sid}")
def history(sid: str):
    if sid not in sessions:
        raise HTTPException(status_code=404, detail="No such session")
    return sessions[sid]


@app.delete("/clear/{sid}")
def clear_session(sid: str):
    if sid in sessions:
        del sessions[sid]
    return {"cleared": True}
