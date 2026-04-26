import streamlit as st
from groq import Groq

# --- 1. CORE ENGINE CONFIG (SECURE) ---
# This line looks for the "GROQ_API_KEY" inside your Streamlit Secrets vault
try:
    GROQ_API_KEY = st.secrets["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"]
except KeyError:
    st.error("Secret Key Missing: Add 'GROQ_API_KEY' to your Streamlit Secrets.")
    st.stop()

def get_ai_response(messages):
    try:
        client = Groq(api_key=GROQ_API_KEY)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7,
            max_tokens=2048
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Engine Fault: {str(e)}"

# --- 2. AVIATION AI UI (CHATGPT STYLE) ---
st.set_page_config(
    page_title="Aviation AI", 
    layout="wide", 
    page_icon="✈️"
)

st.markdown("""
    <style>
    html, body, [class*="css"] { font-family: 'Segoe UI', sans-serif; background-color: #f7f7f8; }
    .stApp { background-color: #f7f7f8; color: #333; }
    [data-testid="stSidebar"] { background-color: #ffffff !important; border-right: 1px solid #e5e5e5; }
    .pro-title { color: #1a1a1a; font-size: 2.8rem; font-weight: 700; letter-spacing: -1.5px; }
    .user-msg { background: #ffffff; color: #333; padding: 1rem; border-radius: 12px; margin: 1rem 0; border: 1px solid #e5e5e5; float: right; width: 85%; }
    .ai-msg { background: #f7f7f8; color: #333; padding: 1rem; border-radius: 12px; margin: 1rem 0; border: 1px solid #e5e5e5; float: left; width: 85%; }
    </style>
    """, unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = [{"role": "system", "content": "You are Aviation AI, a senior flight instructor. Help with aviation, commerce, and coding."}]

# --- 3. SIDEBAR LOGO ---
with st.sidebar:
    st.markdown("""
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <div style="background-color: #1a1a1a; padding: 10px; border-radius: 8px;">
                <span style="font-size: 24px; color: white;">✈️</span>
            </div>
            <span style="margin-left: 10px; font-size: 18px; font-weight: 600;">Aviation AI</span>
        </div>
        """, unsafe_allow_html=True)
    if st.button("Clear Conversation"):
        st.session_state.history = [st.session_state.history[0]]
        st.rerun()

# --- 4. TERMINAL ---
st.markdown('<h1 class="pro-title">Intelligence Terminal</h1>', unsafe_allow_html=True)

for msg in st.session_state.history[1:]:
    msg_class = "user-msg" if msg["role"] == "user" else "ai-msg"
    st.markdown(f'<div class="{msg_class}">{msg["content"]}</div>', unsafe_allow_html=True)

if prompt := st.chat_input("Command the AI..."):
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.spinner("Processing..."):
        response = get_ai_response(st.session_state.history)
        st.session_state.history.append({"role": "assistant", "content": response})
        st.rerun()
