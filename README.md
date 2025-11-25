# MedSense
## AI-Powered Symptom Analyzer and Conversational Medical Assistant

MedSense is an intelligent, LLM-driven medical triage assistant that analyzes symptoms, remembers conversation history, asks clarifying questions, estimates clinical risk, and provides personalized recommendations.

Built using **FastAPI (backend)** and **Streamlit (frontend)**, it demonstrates practical prompt engineering, structured reasoning, and conversational memory.

---

## Features

### Symptom Analysis
- Extracts symptoms from free-text input  
- Identifies possible medical causes  
- Highlights red flags and urgent signs  
- Produces structured, interpretable output  

### Conversational Memory
- Maintains session history using session IDs  
- Supports follow-up questions  
- Functions like a continuous medical chatbot  

### Risk Assessment
- Generates a risk score  
- Categorizes risk level (Low, Moderate, High)  
- Provides emergency guidance when required  

### Personalized Advice
- Offers diet recommendations based on condition  
- Suggests self-care steps  
- Flags situations needing immediate medical attention  

### Explanation Layer
- Provides reasoning behind assessments  
- Asks clarification questions similar to clinical triage  

---

## Tech Stack

| Component     | Technology                          |
|---------------|-------------------------------------|
| Backend       | FastAPI, Python                     |
| Frontend      | Streamlit                           |
| Memory        | In-memory session store             |
| Reasoning     | GPT-based LLM prompt engineering    |
| Communication | JSON-based API                      |

---

## Project Structure

MedSense/
│── backend/
│ └── app.py
│── frontend/
│ └── app.py
│── README.md
│── requirements.txt


---

## Installation and Setup

1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/MedSense.git
cd MedSense
 ```
2. Install Dependencies
 ```bash
pip install -r requirements.txt
 ```
3. Run Backend (FastAPI)
 ```bash
cd backend
uvicorn app:app --reload --port 8000
 ```
4. Run Frontend (Streamlit)
 ```bash
cd ../frontend
streamlit run app.py
 ```
## Sample Inputs for Demonstration

Use symptom descriptions such as:

-"Chest tightness radiating to left arm, sweating, nausea."

-"Severe headache with blurred vision and neck stiffness."

-"Breathlessness while lying down, ankle swelling, fatigue."

-"Loose motion, vomiting, and headache since morning."

These showcase:

Multi-symptom understanding, Clarification questioning, Red-flag detection, Personalized diet and care, Risk scoring

## Future Improvements

Integration with vector-based medical retrieval (RAG)

Persistent database-backed user sessions

Voice input support

Multilingual capability

## Contributing

Contributions are welcome.
For significant changes, please open an issue to discuss proposed updates.
