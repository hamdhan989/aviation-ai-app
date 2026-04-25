import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import datetime

# --- 1. CONFIGURATION & STYLING ---
st.set_page_config(page_title="AeroMaster AI Academy", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0B0E14; color: #E0E0E0; }
    .stButton>button { background-color: #FF9500; color: black; font-weight: bold; width: 100%; border-radius: 5px; }
    .stSidebar { background-color: #161B22; border-right: 1px solid #30363D; }
    h1, h2, h3 { color: #FF9500 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. API SETUP ---
# PASTE YOUR KEY FROM GOOGLE AI STUDIO BELOW:
API_KEY = "AIzaSyCj5ajhi1NlUTlmTM5Vbugt8zklswZPz-Y" 

try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Setup Error: Please ensure your API Key is correctly pasted in the code.")

# --- 3. SESSION STATE ---
if 'is_premium' not in st.session_state:
    st.session_state.is_premium = False
if 'scores' not in st.session_state:
    st.session_state.scores = {"Aerodynamics": 85, "Meteorology": 70, "Regulations": 90}

# --- 4. SIDEBAR NAVIGATION ---
st.sidebar.title("✈️ AeroMaster Pro")
st.sidebar.markdown(f"**Pilot Status:** {'PREMIUM' if st.session_state.is_premium else 'CADET'}")
menu = st.sidebar.radio("Flight Deck Menu", ["Dashboard", "AI Ground School", "Exam Vault (Pay & Get)", "Readiness Analytics"])

# --- 5. APP MODULES ---

if menu == "Dashboard":
    st.title("Welcome to the Flight Deck, Captain")
    col1, col2, col3 = st.columns(3)
    col1.metric("Readiness Score", f"{sum(st.session_state.scores.values())//3}%")
    col2.metric("License Track", "PPL (VFR)")
    col3.metric("Status", "Premium" if st.session_state.is_premium else "Free")
    st.info("Your AI Flight Instructor is ready. Use the sidebar to navigate.")

elif menu == "AI Ground School":
    st.title("🎓 AI Flight Instructor")
    user_query = st.text_input("ATC Intercom (Ask a question):", placeholder="e.g., Explain the four forces of flight...")
    if user_query:
        with st.spinner("Instructor is analyzing..."):
            try:
                response = model.generate_content(f"You are a professional Flight Instructor. Answer this student's question clearly: {user_query}")
                st.chat_message("assistant").write(response.text)
            except Exception as e:
                st.error("API Error. Please check if your Google AI Studio key is active.")

elif menu == "Exam Vault (Pay & Get)":
    st.title("📝 Exam Vault")
    if not st.session_state.is_premium:
        st.warning("⚠️ ACCESS RESTRICTED: Professional Mock Papers are locked.")
        if st.button("BUY PREMIUM ACCESS - $29.99"):
            st.session_state.is_premium = True
            st.success("Transaction Complete! License Upgraded.")
            st.rerun()
    else:
        st.success("✅ PREMIUM ACCESS UNLOCKED")
        if st.button("Generate & Download Mock Paper"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, "OFFICIAL MOCK EXAM PAPER", ln=True, align='C')
            pdf.ln(10)
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, "Q1: What is the transponder code for a hijacked aircraft?\nA: 7500\nB: 7600\nC: 7700")
            pdf_output = "Aviation_Exam_Paper.pdf"
            pdf.output(pdf_output)
            with open(pdf_output, "rb") as file:
                st.download_button(label="📥 Download PDF Paper", data=file, file_name=pdf_output, mime="application/pdf")

elif menu == "Readiness Analytics":
    st.title("📊 Readiness Analytics")
    for subject, score in st.session_state.scores.items():
        st.write(f"**{subject}**")
        st.progress(score / 100)

