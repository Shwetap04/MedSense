# frontend/app.py
import streamlit as st
import requests
import json

st.set_page_config(page_title="MedSense", layout="wide")

API_URL = "http://127.0.0.1:8000/chat"

st.title("🩺 MedSense – Intelligent Symptom Assistant")

# ------------------- SESSION STATE -------------------
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "history" not in st.session_state:
    st.session_state.history = []
if "last_response" not in st.session_state:
    st.session_state.last_response = None


# ------------------- INPUT BOX (now supports follow-ups) -------------------
user_input = st.text_area(
    "Message to MedSense (Describe symptoms or answer its questions):",
    height=120,
    placeholder="Example: chest pressure radiating to left arm OR 'been going on 2 days', etc."
)

col1, col2 = st.columns(2)
with col1:
    age = st.number_input("Age:", min_value=1, max_value=120, value=25)
with col2:
    lifestyle = st.text_input(
        "Lifestyle (optional):",
        placeholder="smoker / athlete / sedentary ..."
    )

send = st.button("Send", use_container_width=True)


# ------------------- CHAT AREA -------------------
st.markdown("## 💬 Conversation")
chat_box = st.container()

sidebar = st.sidebar
sidebar.title("🔍 Personal Insights")


# ------------------- ON SEND -------------------
if send and user_input.strip():

    # FIRST message → send age/lifestyle
    if st.session_state.session_id is None:
        payload = {
            "user_message": user_input,
            "session_id": None,
            "age": age,
            "lifestyle": lifestyle,
        }
    else:
        # FOLLOW-UP messages → do NOT resend demographics
        payload = {
            "user_message": user_input,
            "session_id": st.session_state.session_id,
        }

    with st.spinner("Analyzing..."):
        res = requests.post(API_URL, json=payload)
        data = res.json()

    # Store latest result
    st.session_state.session_id = data["session_id"]
    st.session_state.last_response = data

    # Fetch full updated history
    history = requests.get(
        f"http://127.0.0.1:8000/history/{st.session_state.session_id}"
    ).json()

    st.session_state.history = history["messages"]


# ------------------- ALWAYS SHOW CHAT HISTORY -------------------
if st.session_state.history:
    with chat_box:
        for msg in st.session_state.history:
            if msg["role"] == "user":
                st.markdown(f"💬 **You:** {msg['text']}")
            else:
                st.markdown("🤖 **MedSense:**")
                st.json(msg["text"])


# ------------------- SIDEBAR (Safe Access) -------------------
if st.session_state.last_response:

    data = st.session_state.last_response
    personal = data["personalization"]

    # RISK
    sidebar.subheader("Risk Level")
    sidebar.info(
        f"**{data['risk']['risk_level']} ({data['risk']['risk_score']}%)**"
    )

    # DIET
    sidebar.subheader("Recommended Diet")
    for item in personal["recommended_diet"]:
        sidebar.write(f"- {item}")

    # URGENT FLAG
    if personal["urgent"]:
        sidebar.error("⚠️ URGENT: Seek medical help immediately.")


# ------------------- RESET BUTTON -------------------
if sidebar.button("Reset Session"):
    st.session_state.session_id = None
    st.session_state.history = []
    st.session_state.last_response = None
    st.experimental_rerun()
