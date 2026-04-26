import streamlit as st
from groq import Groq
from fpdf import FPDF
import datetime

# --- 1. CORE ENGINE CONFIG (GROQ) ---
# Get your key at https://console.groq.com/keys
GROQ_API_KEY = "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"

def get_ai_response(messages):
    try:
        client = Groq(api_key=GROQ_API_KEY)
        # Using Llama 3.1 70B - One of the smartest models available
        completion = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=messages,
            temperature=0.7,
            max_tokens=2048
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Engine Fault: {str(e)}"

# --- 2. ULTRA UI (GEMINI-STYLE AESTHETICS) ---
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
        font-size: 3rem; font-weight: 800; letter-spacing: -2px;
    }
    
    .user-bubble {
        background: #27272a; padding: 1.2rem; border-radius: 1.5rem 1.5rem 0.2rem 1.5rem;
        margin: 1rem 0; border: 1px solid #3f3f46; box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .ai-bubble {
        background: rgba(30, 41, 59, 0.4); padding: 1.5rem; border-radius: 1.5rem 1.5rem 1.5rem 0.2rem;
        margin: 1rem 0; border: 1px solid rgba(59, 130, 246, 0.2); backdrop-filter: blur(10px);
    }

    .tier-badge { padding: 6px 16px; border-radius: 50px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; }
    .badge-plus { background: linear-gradient(135deg, #8b5cf6, #ec4899); color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. PERSISTENT MEMORY ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": "You are AeroMaster AI, a world-class Senior Flight Instructor and Aeronautical Engineer. Speak professionally and with technical depth."}
    ]

# --- 4. SIDEBAR COMMAND CENTER ---
with st.sidebar:
    st.markdown('<h1 style="color: #60a5fa;">💠 AeroMaster</h1>', unsafe_allow_html=True)
    st.markdown('<span class="tier-badge badge-plus">PREMIUM PLUS (GROQ)</span>', unsafe_allow_html=True)
    st.markdown("---")
    app_mode = st.radio("Intelligence Hub", ["Chat Terminal", "Exam Architect", "Visual Lab"])
    
    if st.button("Archive & Clear Chat"):
        st.session_state.chat_history = [st.session_state.chat_history[0]]
        st.rerun()

# --- 5. FUNCTIONAL MODES ---
if app_mode == "Chat Terminal":
    st.markdown('<h1 class="ultra-title">Intelligence Terminal</h1>', unsafe_allow_html=True)
    
    # Display History
    for msg in st.session_state.chat_history[1:]:
        bubble_class = "user-bubble" if msg["role"] == "user" else "ai-bubble"
        label = "YOU" if msg["role"] == "user" else "AEROMASTER"
        st.markdown(f'<div class="{bubble_class}"><b>{label}</b><br>{msg["content"]}</div>', unsafe_allow_html=True)

    # Input Loop
    if prompt := st.chat_input("Command the AI..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        with st.spinner("LPU Processing..."):
            response = get_ai_response(st.session_state.chat_history)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.rerun()

elif app_mode == "Exam Architect":
    st.markdown('<h1 class="ultra-title">Exam Architect</h1>', unsafe_allow_html=True)
    topic = st.text_input("Exam Topic (e.g., Aerodynamics, Navigation)")
    if st.button("Build Professional Paper"):
        q_prompt = [{"role": "user", "content": f"Create a 10-question multiple choice exam about {topic} with answers at the end."}]
        res = get_ai_response(q_prompt)
        st.markdown(f'<div class="ai-bubble">{res}</div>', unsafe_allow_html=True)
