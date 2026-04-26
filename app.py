import streamlit as st
from groq import Groq
import datetime

# --- 1. CORE ENGINE CONFIG (GROQ) ---
# Paste your Groq Key here (starts with gsk_...)
# If you need a key, get it at https://console.groq.com/keys
GROQ_API_KEY = st.secrets["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"]


def get_ai_response(messages):
    try:
        client = Groq(api_key=GROQ_API_KEY)
        # Using Llama 3.3 70B - The newest, fastest, smartest model
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7,
            max_tokens=2048
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Engine Fault: {str(e)}"

# --- 2. AVIATION AI UI (LIGHT SIDEBAR, CHATGPT STYLE) ---
st.set_page_config(
    page_title="Aviation AI", 
    layout="wide", 
    page_icon="✈️",
    initial_sidebar_state="expanded"
)

# Custom Styling (Light Sidebar, ChatGPT-style colors)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@300;400;600&display=swap');
    html, body, [class*="css"] { font-family: 'Segoe UI', Tahoma, sans-serif; background-color: #f7f7f8; }
    
    /* Main Content Area (Light Grey) */
    .stApp { background-color: #f7f7f8; color: #333; }

    /* The ChatGPT-style Light Sidebar */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e5e5e5;
    }

    /* Professional Title (Non-gradient for light mode) */
    .pro-title {
        color: #1a1a1a;
        font-size: 2.8rem;
        font-weight: 700;
        letter-spacing: -1.5px;
        margin-bottom: 5px;
    }

    /* Chat Bubbles */
    .user-msg {
        background: #ffffff; color: #333; padding: 1.2rem;
        border-radius: 15px 15px 5px 15px; margin: 1rem 0;
        border: 1px solid #e5e5e5;
        max-width: 80%; float: right; clear: both;
    }
    
    .ai-msg {
        background: #f7f7f8; color: #333; padding: 1.2rem;
        border-radius: 15px 15px 15px 5px; margin: 1rem 0;
        border: 1px solid #e5e5e5;
        max-width: 80%; float: left; clear: both;
    }

    /* Subscription Badges */
    .tier-badge {
        padding: 5px 12px; border-radius: 20px; font-size: 10px; font-weight: 700;
        text-transform: uppercase; color: white;
    }
    .badge-plus { background: #3b82f6; } /* Professional Blue for light mode */
    
    /* Clean Input Box */
    .stChatInputContainer { border-top: 1px solid #e5e5e5 !important; background-color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. PERSISTENT MEMORY ---
if "history" not in st.session_state:
    st.session_state.history = [
        {"role": "system", "content": "You are Aviation AI, a senior aerodynamic engineer and global flight examiner. Provide highly accurate, professional guidance."}
    ]

# --- 4. SIDEBAR (THE LIGHT PANEL) ---
with st.sidebar:
    # --- PRO LOGO IN THE CODE ---
    # We use Markdown to generate a professional graphic directly in the sidebar
    st.markdown("""
        <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 25px;">
            <div style="background-color: #1a1a1a; padding: 12px; border-radius: 10px;">
                <span style="font-size: 30px; color: white;">✈️</span>
            </div>
            <span style="margin-left: 10px; font-size: 20px; font-weight: 600; color: #1a1a1a;">Aviation AI</span>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown('<div style="text-align: center;"><span class="tier-badge badge-plus">PROFESSIONAL</span></div>', unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("### Intelligence Hub")
    app_mode = st.radio("", ["Chat Terminal", "Exam Architect", "Visual Lab"], label_visibility="collapsed")
    
    st.markdown("---")
    if st.button("Clear Conversation"):
        st.session_state.history = [st.session_state.history[0]]
        st.rerun()
    
    st.caption(f"Engine: Llama 3.3 Pro | Speed: >300 t/s")

# --- 5. FUNCTIONAL MODES ---

if app_mode == "Chat Terminal":
    st.markdown('<h1 class="pro-title">Intelligence Terminal</h1>', unsafe_allow_html=True)
    st.markdown("<p style='color: #666;'>Continuous context memory active.</p>", unsafe_allow_html=True)

    # Display History (excluding system prompt)
    for msg in st.session_state.history[1:]:
        if msg["role"] == "user":
            st.markdown(f'<div class="user-msg">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="ai-msg"><b>Aviation AI</b><br>{msg["content"]}</div>', unsafe_allow_html=True)

    # ChatGPT-style input bar
    if prompt := st.chat_input("Command the AI..."):
        st.session_state.history.append({"role": "user", "content": prompt})
        # Instant UI update (Rerun logic can be complex; this simplified approach works better for Streamlit)
        st.markdown(f'<div class="user-msg">{prompt}</div>', unsafe_allow_html=True)

        with st.spinner("Processing..."):
            response = get_ai_response(st.session_state.history)
            st.session_state.history.append({"role": "assistant", "content": response})
            st.rerun()

elif app_mode == "Exam Architect":
    st.markdown('<h1 class="pro-title">Exam Architect</h1>', unsafe_allow_html=True)
    st.write("Specialized assessment tools are unlocked.")
    st.info("Switch back to 'Chat Terminal' to generate.")

elif app_mode == "Visual Lab":
    st.markdown('<h1 class="pro-title">Visual Lab</h1>', unsafe_allow_html=True)
    st.write("Flight visualization tools are active.")
    st.info("Request a description briefing in the Chat Terminal.")

