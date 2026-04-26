import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import datetime

# --- 1. CORE ENGINE CONFIG ---
# Tomorrow or now, paste your API key here:
API_KEY = "AIzaSyA2GSuhO_XCd3LdYldDJlmhFRXDxzo3s8U"

def init_engine():
    if "AIza" not in API_KEY: return None
    try:
        # transport='rest' fixes the 404/v1beta error
        genai.configure(api_key=API_KEY, transport='rest') 
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        return None

model = init_engine()

# --- 2. THE ULTRA UI (GEMINI DESIGN LANGUAGE) ---
st.set_page_config(page_title="AeroMaster Ultra", layout="wide", page_icon="💠")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #09090b; }
    .stApp { background: #09090b; color: #fafafa; }
    [data-testid="stSidebar"] { background-color: #111114 !important; border-right: 1px solid #27272a; }
    .ultra-title {
        background: linear-gradient(90deg, #60a5fa 0%, #a855f7 50%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem; font-weight: 800; letter-spacing: -2px; margin-bottom: 5px;
    }
    .user-bubble { background: #27272a; padding: 1.2rem; border-radius: 1.5rem 1.5rem 0.2rem 1.5rem; margin: 1rem 0; border: 1px solid #3f3f46; }
    .ai-bubble { background: rgba(30, 41, 59, 0.4); padding: 1.5rem; border-radius: 1.5rem 1.5rem 1.5rem 0.2rem; margin: 1rem 0; border: 1px solid rgba(59, 130, 246, 0.2); backdrop-filter: blur(10px); }
    .tier-badge { padding: 6px 16px; border-radius: 50px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; }
    .badge-plus { background: linear-gradient(135deg, #8b5cf6, #ec4899); color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. STATE MANAGEMENT ---
if "history" not in st.session_state: st.session_state.history = []
if "chat_obj" not in st.session_state: st.session_state.chat_obj = model.start_chat(history=[]) if model else None

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown('<h1 style="color: #60a5fa;">💠 AeroMaster</h1>', unsafe_allow_html=True)
    st.markdown('<span class="tier-badge badge-plus">PREMIUM PLUS</span>', unsafe_allow_html=True)
    st.markdown("---")
    app_mode = st.radio("Intelligence Hub", ["Chat Terminal", "Exam Architect", "Flight Visualizer"])
    if st.button("Archive & Clear Chat"):
        st.session_state.history = []
        st.session_state.chat_obj = model.start_chat(history=[]) if model else None
        st.rerun()

# --- 5. CHAT TERMINAL ---
if app_mode == "Chat Terminal":
    st.markdown('<h1 class="ultra-title">Intelligence Terminal</h1>', unsafe_allow_html=True)
    for msg in st.session_state.history:
        div_class = "user-bubble" if msg["role"] == "user" else "ai-bubble"
        st.markdown(f'<div class="{div_class}">{msg["content"]}</div>', unsafe_allow_html=True)

    if prompt := st.chat_input("Command the AI..."):
        st.session_state.history.append({"role": "user", "content": prompt})
        st.rerun()

# Logical processing after rerun to update UI
if st.session_state.history and st.session_state.history[-1]["role"] == "user":
    last_prompt = st.session_state.history[-1]["content"]
    if not model:
        st.error("Engine Fault: Insert valid API key in Line 11.")
    else:
        try:
            response = st.session_state.chat_obj.send_message(last_prompt)
            st.session_state.history.append({"role": "assistant", "content": response.text})
            st.rerun()
        except Exception as e:
            st.error(f"Signal Interference: {str(e)}")

# (Other modes "Exam Architect" and "Visualizer" logic can be added here)
