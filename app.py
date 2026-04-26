import streamlit as st
from groq import Groq

# --- 1. ENGINE CONFIG (DIRECT KEY) ---
# We are skipping secrets for now—paste your real key here
# Example: GROQ_API_KEY = "gsk_XyZ..."
GROQ_API_KEY = "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"

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

# --- 2. AVIATION AI UI (LIGHT MODE) ---
st.set_page_config(
    page_title="Aviation AI", 
    layout="wide", 
    page_icon="✈️"
)

# ChatGPT-style styling
st.markdown("""
    <style>
    html, body, [class*="css"] { font-family: 'Segoe UI', sans-serif; background-color: #f7f7f8; }
    .stApp { background-color: #f7f7f8; color: #333; }
    [data-testid="stSidebar"] { background-color: #ffffff !important; border-right: 1px solid #e5e5e5; }
    .pro-title { color: #1a1a1a; font-size: 2.8rem; font-weight: 700; letter-spacing: -1.5px; }
    
    /* Message Bubbles */
    .user-box { background: #ffffff; color: #333; padding: 1rem; border-radius: 12px; margin: 1rem 0; border: 1px solid #e5e5e5; width: fit-content; max-width: 80%; margin-left: auto; }
    .ai-box { background: #f7f7f8; color: #333; padding: 1rem; border-radius: 12px; margin: 1rem 0; border: 1px solid #e5e5e5; width: fit-content; max-width: 80%; }
    
    /* Clean Input */
    .stChatInputContainer { background-color: white !important; }
    </style>
    """, unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = [{"role": "system", "content": "You are Aviation AI, a senior flight instructor and technical expert. Be professional, helpful, and concise."}]

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("""
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <div style="background-color: #1a1a1a; padding: 10px; border-radius: 8px;">
                <span style="font-size: 24px; color: white;">✈️</span>
            </div>
            <span style="margin-left: 10px; font-size: 18px; font-weight: 600; color: #1a1a1a;">Aviation AI</span>
        </div>
        """, unsafe_allow_html=True)
    
    if st.button("Clear History"):
        st.session_state.history = [st.session_state.history[0]]
        st.rerun()

# --- 4. THE TERMINAL ---
st.markdown('<h1 class="pro-title">Aviation AI Terminal</h1>', unsafe_allow_html=True)

# Display Chat History
for msg in st.session_state.history[1:]:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-box">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai-box"><b>AI:</b> {msg["content"]}</div>', unsafe_allow_html=True)

# User Input
if prompt := st.chat_input("Command the AI..."):
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.spinner("Calculating Flight Path..."):
        response = get_ai_response(st.session_state.history)
        st.session_state.history.append({"role": "assistant", "content": response})
        st.rerun()
