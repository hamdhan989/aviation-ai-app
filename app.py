import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import datetime

# --- 1. GEMINI DESIGN LANGUAGE ---
st.set_page_config(page_title="AeroMaster AI", layout="wide", page_icon="✈️")

st.markdown("""
    <style>
    /* Dark Deep-Space Background */
    .stApp {
        background: radial-gradient(circle at 20% 10%, #1e293b, #020617);
        color: #f1f5f9;
    }
    
    /* Sleek Sidebar */
    [data-testid="stSidebar"] {
        background-color: #030712;
        border-right: 1px solid #1e293b;
    }
    
    /* Gemini-Style Blue/Purple Gradient Text */
    .gemini-title {
        background: linear-gradient(90deg, #60a5fa, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 45px;
        font-weight: 800;
        margin-bottom: 10px;
    }
    
    /* Modern Glassmorphism Cards */
    .card {
        background: rgba(30, 41, 59, 0.4);
        padding: 25px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* High-Tech Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6, #2563eb);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 24px;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.5);
        transform: scale(1.02);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE ENGINE (API SETUP) ---
# PASTE YOUR KEY BETWEEN THE QUOTES BELOW:
API_KEY = "AIzaSyCj5ajhi1NlUTlmTM5Vbugt8zklswZPz-Y" 

def load_instructor():
    if "AIza" not in API_KEY:
        return None
    try:
        genai.configure(api_key=API_KEY)
        return genai.GenerativeModel('gemini-1.5-flash-latest')
    except:
        return None

instructor = load_instructor()

# --- 3. SESSION LOGIC ---
if 'premium' not in st.session_state:
    st.session_state.premium = False

# --- 4. NAVIGATION ---
with st.sidebar:
    st.markdown("<h2 style='color: #60a5fa; margin-bottom: 0;'>✈️ AeroMaster</h2>", unsafe_allow_html=True)
    st.caption("Professional Aviation Intelligence")
    st.markdown("---")
    choice = st.radio("Pilot Console", ["Mission Control", "AI Ground School", "Mock Exams", "Flight Stats"])
    st.markdown("---")
    status = "💎 PREMIUM PILOT" if st.session_state.premium else "🛩️ CADET"
    st.markdown(f"<p style='color: #94a3b8;'>{status}</p>", unsafe_allow_html=True)

# --- 5. APP PAGES ---

if choice == "Mission Control":
    st.markdown('<h1 class="gemini-title">Ready for Takeoff, Captain</h1>', unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3>Current Briefing</h3>
            <p style='color: #94a3b8;'>Your personalized AI-driven syllabus is synced. 
            Focus on <b>Meteorology</b> today to hit your readiness target.</p>
        </div>
        """, unsafe_allow_html=True)
        st.metric("Exam Readiness", "81%", "+2%")

    with col2:
        st.image("https://images.unsplash.com/photo-1540962351504-03099e0a754b?q=80&w=500&auto=format&fit=crop", 
                 caption="Skybound Precision")

elif choice == "AI Ground School":
    st.markdown('<h1 class="gemini-title">AI Flight Instructor</h1>', unsafe_allow_html=True)
    
    if instructor is None:
        st.warning("⚠️ SYSTEM OFFLINE: API Key is missing or invalid in GitHub Line 46.")
    else:
        q = st.text_input("Enter your technical query:", placeholder="e.g. Explain P-Factor in a climb...")
        if q:
            with st.spinner("Analyzing aeronautical data..."):
                try:
                    res = instructor.generate_content(f"You are a professional Flight Instructor. Answer this technical question clearly and professionally: {q}")
                    st.markdown(f"<div class='card'>{res.text}</div>", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Engine Stall: {str(e)}")

elif choice == "Mock Exams":
    st.markdown('<h1 class="gemini-title">Exam Vault</h1>', unsafe_allow_html=True)
    if not st.session_state.premium:
        st.error("Access Restricted to Premium Members")
        if st.button("Unlock Pilot License ($29.99)"):
            st.session_state.premium = True
            st.balloons()
            st.rerun()
    else:
        st.success("Authorized: Professional Exam Papers Ready")
        if st.button("Generate PPL Mock Paper"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, "AEROMASTER PROFESSIONAL MOCK EXAM", ln=True, align='C')
            pdf.output("Aviation_Mock.pdf")
            with open("Aviation_Mock.pdf", "rb") as f:
                st.download_button("📥 Download PDF", f, "Aviation_Mock.pdf")

elif choice == "Flight Stats":
    st.markdown('<h1 class="gemini-title">Readiness Metrics</h1>', unsafe_allow_html=True)
    st.write("Aerodynamics")
    st.progress(0.92)
    st.write("Meteorology")
    st.progress(0.68)
    st.write("Air Law")
    st.progress(0.85)
