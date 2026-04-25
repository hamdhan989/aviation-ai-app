import streamlit as st
import google.generativeai as genai
from fpdf import FPDF

# --- 1. SET YOUR KEY HERE ---
# Tomorrow, paste your brand new API key between these quotes:
API_KEY = "AIzaSyCj5ajhi1NlUTlmTM5Vbugt8zklswZPz-Y"

# --- 2. THE ENGINE ---
def get_instructor():
    if "AIza" not in API_KEY:
        return None
    try:
        genai.configure(api_key=API_KEY)
        return genai.GenerativeModel('gemini-1.5-flash')
    except:
        return None

instructor = get_instructor()

# --- 3. STYLING (GEMINI LOOK) ---
st.set_page_config(page_title="AeroMaster Pro", layout="wide", page_icon="✈️")

st.markdown("""
    <style>
    /* Dark Theme & Gradient Background */
    .stApp {
        background: radial-gradient(circle at 10% 20%, #1e293b 0%, #020617 90%);
        color: #f8fafc;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #030712;
        border-right: 1px solid #1e293b;
    }

    /* Gemini-Style Blue/Purple Gradient */
    .gemini-title {
        background: linear-gradient(90deg, #60a5fa, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 40px;
        font-weight: 800;
        letter-spacing: -1px;
    }

    /* Glassmorphism Cards */
    .card {
        background: rgba(30, 41, 59, 0.5);
        padding: 24px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        margin-bottom: 20px;
    }

    /* High-Tech Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6, #2563eb);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 25px;
        font-weight: 600;
        transition: 0.3s ease;
    }
    .stButton>button:hover {
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.4);
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. NAVIGATION ---
with st.sidebar:
    st.markdown("<h1 style='color: #60a5fa;'>✈️ AeroMaster</h1>", unsafe_allow_html=True)
    st.markdown("Professional Flight Training AI")
    st.markdown("---")
    page = st.radio("Pilot Console", ["AI Ground School", "Mission Control", "Exam Vault"])
    st.markdown("---")
    st.caption("Status: CADET")

# --- 5. PAGES ---
if page == "AI Ground School":
    st.markdown('<h1 class="gemini-title">AI Flight Instructor</h1>', unsafe_allow_html=True)
    
    if not instructor:
        st.error(f"❌ Key missing or invalid. Check Line 7 in GitHub. (Key begins with: {API_KEY[:4]})")
    else:
        st.markdown("<div class='card'>Hello Captain. Ask me any aeronautical question.</div>", unsafe_allow_html=True)
        query = st.text_input("Enter query:", placeholder="e.g., Explain the four forces of flight.")
        
        if query:
            with st.spinner("Analyzing data..."):
                try:
                    response = instructor.generate_content(f"You are a professional Flight Instructor. Be concise: {query}")
                    st.markdown(f"<div class='card'><b>Instructor:</b><br><br>{response.text}</div>", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Engine Stall: {str(e)}")

elif page == "Mission Control":
    st.markdown('<h1 class="gemini-title">Mission Briefing</h1>', unsafe_allow_html=True)
    col1, col2 = st.columns([2,1])
    with col1:
        st.markdown("<div class='card'><h3>Flight Summary</h3>Your readiness for the upcoming PPL exam is at <b>84%</b>. Focus on Cross-Wind landings and Metrology next.</div>", unsafe_allow_html=True)
    with col2:
        st.metric("Flight Hours", "45h", "+2h")

elif page == "Exam Vault":
    st.markdown('<h1 class="gemini-title">Exam Documents</h1>', unsafe_allow_html=True)
    st.write("Professional training documents will appear here once the license is active.")
