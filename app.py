import streamlit as st
import google.generativeai as genai
from fpdf import FPDF

# --- 1. INTERFACE & STYLE (GEMINI AESTHETIC) ---
st.set_page_config(page_title="AeroMaster Pro", layout="wide", page_icon="✈️")

st.markdown("""
    <style>
    /* Gemini Dark Mode Gradient */
    .stApp {
        background: radial-gradient(circle at 10% 20%, #1e293b 0%, #020617 90%);
        color: #f8fafc;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #030712;
        border-right: 1px solid #1e293b;
    }

    /* Gradient Title */
    .gemini-title {
        background: linear-gradient(90deg, #60a5fa, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 40px;
        font-weight: 800;
        letter-spacing: -1px;
    }

    /* Content Cards */
    .card {
        background: rgba(30, 41, 59, 0.45);
        padding: 24px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(12px);
        margin-bottom: 20px;
    }

    /* Professional Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6, #2563eb);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 28px;
        font-weight: 600;
        transition: 0.3s;
    }
    .stButton>button:hover {
        box-shadow: 0 0 25px rgba(59, 130, 246, 0.4);
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE ENGINE (API SETUP WITH AUTO-DETECT) ---
# CRITICAL: PASTE YOUR KEY BETWEEN THE QUOTES BELOW
API_KEY = "AIzaSyCj5ajhi1NlUTlmTM5Vbugt8zklswZPz-Y" 

def start_engine():
    if "AIza" not in API_KEY:
        return None
    try:
        genai.configure(api_key=API_KEY)
        # Try different model names until one works
        for name in ['gemini-1.5-flash', 'gemini-1.5-flash-latest', 'gemini-pro']:
            try:
                model = genai.GenerativeModel(name)
                # Test run
                model.generate_content("test", generation_config={"max_output_tokens": 1})
                return model
            except:
                continue
        return None
    except:
        return None

instructor = start_engine()

# --- 3. NAVIGATION LOGIC ---
with st.sidebar:
    st.markdown("<h1 style='color: #60a5fa;'>✈️ AeroMaster</h1>", unsafe_allow_html=True)
    st.markdown("Professional Flight Training AI")
    st.markdown("---")
    page = st.radio("Pilot Console", ["Mission Control", "AI Ground School", "Exam Vault", "Pilot Stats"])
    
    if 'premium' not in st.session_state:
        st.session_state.premium = False
    
    st.markdown("---")
    st.caption("Status: " + ("💎 PREMIUM" if st.session_state.premium else "🛩️ CADET"))

# --- 4. APP PAGES ---

if page == "Mission Control":
    st.markdown('<h1 class="gemini-title">Welcome to the Flight Deck</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        <div class="card">
            <h3>Active Briefing</h3>
            <p style='color: #94a3b8;'>Your training readiness is currently at <b>81%</b>. 
            We recommend reviewing <b>Aft Center of Gravity</b> maneuvers today.</p>
        </div>
        """, unsafe_allow_html=True)
        st.metric("Exam Readiness", "81%", "+2.4%")
    
    with col2:
        st.image("https://images.unsplash.com/photo-1540962351504-03099e0a754b?auto=format&fit=crop&w=400", caption="Standard Departure")

elif page == "AI Ground School":
    st.markdown('<h1 class="gemini-title">AI Flight Instructor</h1>', unsafe_allow_html=True)
    
    if not instructor:
        st.error("🔑 Engine Error: Please check if your API Key is correctly pasted in GitHub Line 56.")
    else:
        query = st.text_input("Ask your instructor (e.g., Explain Bernoulli's Principle):", placeholder="Type your aviation question here...")
        if query:
            with st.spinner("Analyzing aeronautical data..."):
                try:
                    response = instructor.generate_content(f"You are a Senior Flight Instructor. Explain this professionally: {query}")
                    st.markdown(f"<div class='card'>{response.text}</div>", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Engine Stall: The model name or key is failing. Error: {str(e)}")

elif page == "Exam Vault":
    st.markdown('<h1 class="gemini-title">Training Vault</h1>', unsafe_allow_html=True)
    if not st.session_state.premium:
        st.warning("Locked: Mock Exams require a Professional License.")
        if st.button("Upgrade to Premium"):
            st.session_state.premium = True
            st.balloons()
            st.rerun()
    else:
        st.success("Authorized: Training documents unlocked.")
        if st.button("Generate PPL Mock Paper"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, "AEROMASTER MOCK EXAM", ln=True, align='C')
            pdf.output("Aviation_Mock.pdf")
            with open("Aviation_Mock.pdf", "rb") as f:
                st.download_button("📥 Download PDF", f, "Aviation_Mock.pdf")

elif page == "Pilot Stats":
    st.markdown('<h1 class="gemini-title">Readiness Metrics</h1>', unsafe_allow_html=True)
    skills = {"Navigation": 85, "Meteorology": 62, "Aerodynamics": 94, "Air Law": 78}
    for s, v in skills.items():
        st.write(f"{s}: {v}%")
        st.progress(v/100)

