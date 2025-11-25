# MedSense
MedSense is an AI-powered medical assistant that analyzes user-reported symptoms, asks clarifying questions, provides structured insights, estimates risk levels, and delivers personalized diet and care recommendations.
Built using FastAPI (backend) and Streamlit (frontend), it demonstrates practical prompt engineering, structured reasoning, and conversational memory.

Features
Symptom Analysis

Extracts symptoms from free-text input

Identifies possible medical causes

Highlights red flags and urgent signs

Produces structured, interpretable output

Conversational Memory

Maintains session history using session IDs

Supports follow-up questions

Functions like a continuous medical chatbot

Risk Assessment

Generates a risk score

Categorizes risk level (Low, Moderate, High)

Provides emergency guidance when required

Personalized Advice

Offers diet recommendations based on condition

Suggests self-care steps

Flags situations needing immediate medical attention

Explanation Layer

Provides reasoning behind assessments

Asks clarification questions similar to clinical triage

Tech Stack
Component	Technology
Backend	FastAPI, Python
Frontend	Streamlit
Memory	In-memory session store
Reasoning Engine	GPT-based LLM prompt engineering
Communication	JSON-based API
Project Structure
MedSense/
│── backend/
│   └── app.py
│── frontend/
│   └── app.py
│── README.md
│── requirements.txt

Installation and Setup
1. Clone the Repository
git clone https://github.com/YOUR_USERNAME/MedSense.git
cd MedSense

2. Install Dependencies
pip install -r requirements.txt

3. Run Backend (FastAPI)
cd backend
uvicorn app:app --reload --port 8000


Backend will start at:

http://127.0.0.1:8000

4. Run Frontend (Streamlit)
cd ../frontend
streamlit run app.py


Frontend will open at:

http://localhost:8501

Sample Inputs for Demonstration

You can test the system with inputs such as:

"Chest tightness radiating to left arm, sweating, nausea."

"Severe headache with blurred vision and neck stiffness."

"Breathlessness while lying down, ankle swelling, fatigue."

"Loose motion, vomiting, and headache since morning."

These examples highlight:

Multi-symptom understanding

Clarification questioning

Red-flag detection

Personalized diet and care

Risk scoring

Academic Relevance

This project demonstrates:

Prompt Engineering

Direct, indirect, instruction-based, and role-based prompts

Structured output prompting

Iterative refinement and testing

Testing and Optimization

Multiple prompt variations

Evaluation of output quality

Hallucination control strategies

Safety-focused reasoning

Learning Outcome

Real-world application of LLMs in medical triage

Conversational AI with memory

Structured reasoning and explanation generation

Ethical Disclaimer

MedSense is not a medical device and does not replace professional medical diagnosis or treatment.
It is intended for informational and educational purposes only.
Users should consult qualified healthcare professionals for serious or urgent conditions.

Future Improvements

Integration with vector-based medical retrieval (RAG)

Persistent database-backed user sessions

Voice input support

Multilingual capability

Contributing

Contributions are welcome.
For significant changes, please open an issue to discuss the proposed update.
