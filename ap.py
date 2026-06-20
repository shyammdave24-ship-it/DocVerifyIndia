import streamlit as st
from supabase import create_client
import time 
import pytesseract
from PIL import Image

# --- 1. SUPABASE CONNECTION ---
SUPABASE_URL = "https://osbbdapzegmiqgavlezr.supabase.co"
SUPABASE_KEY = "sb_publishable_OC-t8R7IZ6oy1ohHWW2ZhA_lak9hSav"

@st.cache_resource
def init_connection():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

try:
    supabase = init_connection()
except Exception as e:
    st.error("Database Connection Failed. Check your internet.")

# --- 2. PAGE CONFIG & ENTERPRISE CSS ---
st.set_page_config(page_title="DocVerifyIndia", page_icon="🇮🇳", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .main-title { font-size: 55px; font-weight: 900; color: #002D62; padding-bottom: 0px; margin-bottom: 0px; line-height: 1.2;}
    .sub-title { font-size: 22px; color: #FF9933; font-weight: bold; margin-bottom: 40px; }
    .section-header { font-size: 35px; font-weight: 800; color: #002D62; margin-top: 60px; margin-bottom: 20px; border-bottom: 3px solid #ccc; padding-bottom: 10px;}
    .card { background-color: #ffffff; padding: 40px; border-radius: 12px; border-top: 6px solid #002D62; box-shadow: 0px 10px 30px rgba(0,0,0,0.08); margin-bottom: 40px; }
    .footer { text-align: center; padding: 80px 20px; color: #fff; background-color: #002D62; margin-top: 150px; font-size: 15px; }
    </style>
""", unsafe_allow_html=True)

# --- 3. MULTI-PAGE ROUTING SYSTEM ---
if "page" not in st.session_state:
    st.session_state.page = "home"
if "user_email" not in st.session_state:
    st.session_state.user_email = None

st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/5/55/Emblem_of_India.svg", width=90)
st.sidebar.markdown("## DocVerifyIndia\n*Digital Sovereignty*")

if st.session_state.user_email is None:
    st.sidebar.markdown("---")
    if st.sidebar.button("🔐 Login to Portal", use_container_width=True):
        st.session_state.page = "login"
        st.rerun()
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    if st.sidebar.button("New to DocVerify India? Create a new account", type="primary", use_container_width=True):
        st.session_state.page = "register"
        st.rerun()
    if st.session_state.page != "home":
        if st.sidebar.button("🏠 Back to Home"):
            st.session_state.page = "home"
            st.rerun()
else:
    st.sidebar.success(f"Verified User:\n**{st.session_state.user_email}**")
    if st.sidebar.button("🏠 Dashboard Home"):
        st.session_state.page = "home"
        st.rerun()
    if st.sidebar.button("🚪 Logout Session", type="primary"):
        supabase.auth.sign_out()
        st.session_state.user_email = None
        st.session_state.page = "home"
        st.rerun()

# ==========================================
# PAGE: REGISTRATION
# ==========================================
if st.session_state.page == "register":
    st.markdown("<div class='section-header'>Create Your Secure Identity Vault</div>", unsafe_allow_html=True)
    with st.form("reg_form"):
        reg_email = st.text_input("Enter Official Email")
        reg_pass = st.text_input("Create Secure Password", type="password")
        confirm = st.text_input("Confirm Secure Password", type="password")
        if st.form_submit_button("Initialize Registration", type="primary"):
            if reg_pass != confirm: st.error("Passwords must match.")
            else:
                try:
                    supabase.auth.sign_up({"email": reg_email, "password": reg_pass})
                    st.success("Account Created! You can now log in.")
                except: st.error("Registration failed.")

# ==========================================
# PAGE: LOGIN
# ==========================================
elif st.session_state.page == "login":
    st.markdown("<div class='section-header'>Secure Portal Access</div>", unsafe_allow_html=True)
    with st.form("log_form"):
        log_email = st.text_input("Registered Email")
        log_pass = st.text_input("Secure Password", type="password")
        if st.form_submit_button("Unlock Vault", type="primary"):
            try:
                supabase.auth.sign_in_with_password({"email": log_email, "password": log_pass})
                st.session_state.user_email = log_email
                st.session_state.page = "home"
                st.rerun()
            except: st.error("Invalid credentials.")

# ==========================================
# PAGE: HOME (MAIN DASHBOARD)
# ==========================================
elif st.session_state.page == "home":
    
    st.image("https://images.unsplash.com/photo-1618044733300-9472054094ee?auto=format&fit=crop&w=2000&q=80", use_container_width=True)
    st.markdown("<div class='main-title'>DocVerifyIndia Engine</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>The National AI Document Pre-Verification Protocol</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-header'>📄 Live AI Verification Console</div>", unsafe_allow_html=True)
    
    SERVICES = {
        "-- Select Your Official Service --": [],
        "Update Aadhaar Card (Name/Address)": ["Proof of Identity", "Proof of Address", "Marriage Certificate/Gazette"],
        "Savings Bank Account Opening": ["Officially Valid ID", "PAN Card", "Updated Address Proof"]
    }

    selected = st.selectbox("Select the application you are preparing for:", list(SERVICES.keys()))

    if selected != "-- Select Your Official Service --":
        reqs = SERVICES[selected]
        st.markdown(f"<div class='card'><h3>Required KYC Checklist</h3><p>Upload the following items to begin the Real AI mismatch scan.</p></div>", unsafe_allow_html=True)
        
        uploaded_files = {}
        # Notice we removed PDF so the free image reader doesn't crash
        for doc in reqs:
            uploaded_files[doc] = st.file_uploader(f"Upload {doc} (JPG/PNG only)", type=["jpg", "jpeg", "png"], key=doc)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🔍 Verify Documents Using OCR AI", type="primary", use_container_width=True):
            if all(uploaded_files.values()):
                
                # --- THE REAL AI OCR ENGINE IS HERE ---
                with st.spinner('👁️ OCR Engine activated. Extracting text from your first document...'):
                    try:
                        # Grab the first uploaded file
                        first_doc_name = list(uploaded_files.keys())[0]
                        first_file = uploaded_files[first_doc_name]
                        
                        # Open the image and let Tesseract read the text
                        img = Image.open(first_file)
                        extracted_text = pytesseract.image_to_string(img)
                        
                        # Display what the AI actually saw!
                        st.success(f"✅ AI successfully read your {first_doc_name}!")
                        st.markdown("**Here is the exact data the AI pulled from your image:**")
                        st.code(extracted_text if extracted_text.strip() else "No text could be found. Is the image blurry?")
                        
                        st.info("In a full production app, this text would be instantly compared to government databases to find spelling mistakes.")
                        st.balloons()
                    except Exception as e:
                        st.error(f"OCR Error: {e}")
            else:
                st.error("❌ Action Blocked: You must upload all required files.")
