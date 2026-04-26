import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import datetime

# --- 1. CORE ENGINE CONFIG ---
# PASTE YOUR NEW API KEY HERE:
API_KEY = "AIzaSyAdjvKf61KBtW3ktwGPkzLR_gajhdfWMLE"

def init_engine():
    if "AIza" not in API_KEY: return None
    try:
        genai.configure(api_key=API_KEY)
        return genai.GenerativeModel(
            model_name='gemini-pro',
            generation_config={"temperature": 0.7, "top_p": 0.95, "max_output_tokens": 2048}
        )
    except: return None

model = init_engine()

# --- 2. THE ULTRA UI (GEMINI DESIGN LANGUAGE) ---
st.set_page_config(page_title="AeroMaster Ultra", layout="wide", page_icon="💠")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #09090b; }
    
    .stApp { background: #09090b; color: #fafafa; }

    /* Custom Sidebar - Professional Depth */
    [data-testid="stSidebar"] {
        background-color: #111114 !important;
        border-right: 1px solid #27272a;
    }

    /* Professional Title Gradient */
    .ultra-title {
        background: linear-gradient(90deg, #60a5fa 0%, #a855f7 50%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
        letter-spacing: -2px;
        margin-bottom: 5px;
    }

    /* Premium Chat Bubbles */
    .user-bubble {
        background: #27272a;
        padding: 1.2rem;
        border-radius: 1.5rem 1.5rem 0.2rem 1.5rem;
        margin: 1rem 0;
        border: 1px solid #3f3f46;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .ai-bubble {
        background: rgba(30, 41, 59, 0.4);
        padding: 1.5rem;
        border-radius: 1.5rem 1.5rem 1.5rem 0.2rem;
        margin: 1rem 0;
        border: 1px solid rgba(59, 130, 246, 0.2);
        backdrop-filter: blur(10px);
        line-height: 1.7;
    }

    /* Subscription Badges */
    .tier-badge {
        padding: 6px 16px;
        border-radius: 50px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .badge-plus { background: linear-gradient(135deg, #8b5cf6, #ec4899); color: white; }
    
    /* Sleek Input Box */
    .stChatInputContainer { padding-bottom: 20px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. INTELLIGENT STATE MANAGEMENT ---
if "history" not in st.session_state: st.session_state.history = []
if "chat_obj" not in st.session_state: st.session_state.chat_obj = model.start_chat(history=[]) if model else None
if "tier" not in st.session_state: st.session_state.tier = "PREMIUM PLUS"

# --- 4. NAVIGATION & COMMAND CENTER ---
with st.sidebar:
    st.markdown('<h1 style="color: #60a5fa;">💠 AeroMaster</h1>', unsafe_allow_html=True)
    st.markdown(f'<span class="tier-badge badge-plus">{st.session_state.tier}</span>', unsafe_allow_html=True)
    
    st.markdown("---")
    app_mode = st.radio("Intelligence Hub", ["Chat Terminal", "Exam Architect", "Flight Visualizer"])
    
    st.markdown("---")
    st.markdown("### Flight Log Operations")
    if st.button("Archive & Clear Chat"):
        st.session_state.history = []
        st.session_state.chat_obj = model.start_chat(history=[]) if model else None
        st.rerun()
    
    st.caption(f"Engine: Gemini 1.5 Pro-Ready\nLast Sync: {datetime.datetime.now().strftime('%H:%M')}")

# --- 5. FUNCTIONAL MODES ---

if app_mode == "Chat Terminal":
    st.markdown('<h1 class="ultra-title">Intelligence Terminal</h1>', unsafe_allow_html=True)
    st.markdown("<p style='color: #a1a1aa;'>Professional aviation guidance with full context memory.</p>", unsafe_allow_html=True)

    # Display History with Premium Styling
    for msg in st.session_state.history:
        if msg["role"] == "user":
            st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="ai-bubble"><b>AeroMaster AI</b><br><br>{msg["content"]}</div>', unsafe_allow_html=True)

    # Smart Input Loop
    if prompt := st.chat_input("Command the AI..."):
        st.session_state.history.append({"role": "user", "content": prompt})
        st.markdown(f'<div class="user-bubble">{prompt}</div>', unsafe_allow_html=True)

        with st.chat_message("assistant", avatar="💠"):
            if not model:
                st.error("Engine Fault: Insert valid API key in Line 15.")
            else:
                try:
                    response = st.session_state.chat_obj.send_message(prompt)
                    st.markdown(f'<div class="ai-bubble"><b>AeroMaster AI</b><br><br>{response.text}</div>', unsafe_allow_html=True)
                    st.session_state.history.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"Signal Interference: {str(e)}")

elif app_mode == "Exam Architect":
    st.markdown('<h1 class="ultra-title">Exam Architect</h1>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        subj = st.selectbox("Specialization", ["PPL General", "Meteorology", "Navigation", "Human Factors", "Air Law"])
        difficulty = st.select_slider("Intensity", options=["Cadet", "Commercial", "Ace"])
    with col2:
        q_count = st.number_input("Questions", 5, 50, 10)
    
    if st.button("Generate Professional Paper"):
        with st.spinner("Generating high-fidelity assessment..."):
            paper_prompt = f"Generate a {difficulty} level pilot exam on {subj} with {q_count} questions. Include answers."
            res = model.generate_content(paper_prompt)
            st.markdown(f'<div class="ai-bubble">{res.text}</div>', unsafe_allow_html=True)
            
            # Auto-PDF Generation
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=11)
            pdf.multi_cell(0, 10, txt=f"AeroMaster Pro - {subj} Exam\n\n" + res.text.encode('latin-1', 'replace').decode('latin-1'))
            pdf_path = f"Exam_{subj}.pdf"
            pdf.output(pdf_path)
            with open(pdf_path, "rb") as f:
                st.download_button("📥 Export as PDF", f, file_name=pdf_path)

elif app_mode == "Flight Visualizer":
    st.markdown('<h1 class="ultra-title">Visual Lab</h1>', unsafe_allow_html=True)
    st.markdown("<div class='ai-bubble'><b>Feature Note:</b> Premium Plus utilizes Gemini's multimodal reasoning to generate high-detail situational briefings.</div>", unsafe_allow_html=True)
    scene = st.text_area("Describe the flight scenario for visualization:")
    if st.button("Generate Tactical Briefing"):
        vis_res = model.generate_content(f"Act as a tactical flight instructor. Provide a visual and safety briefing for: {scene}")
        st.markdown(f'<div class="ai-bubble">{vis_res.text}</div>', unsafe_allow_html=True)
