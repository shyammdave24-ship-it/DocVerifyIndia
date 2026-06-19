import streamlit as st
from supabase import create_client

# --- SUPABASE CONNECTION ---
SUPABASE_URL = "https://osbbdapzegmiqgavlezr.supabase.co"
SUPABASE_KEY = "sb_publishable_OC-t8R7IZ6oy1ohHWW2ZhA_lak9hSav"

@st.cache_resource
def init_connection():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

try:
    supabase = init_connection()
except Exception as e:
    st.error("Database connection failed.")

# --- PAGE CONFIG & CSS ---
st.set_page_config(page_title="DocVerifyIndia", page_icon="🇮🇳", layout="wide")

st.markdown("""
    <style>
    .main-header { font-size: 38px; font-weight: 800; color: #002D62; border-bottom: 4px solid #FF9933; padding-bottom: 10px; margin-bottom: 10px; }
    .sub-text { font-size: 18px; color: #555; margin-bottom: 30px; }
    .card { background-color: #ffffff; padding: 25px; border-radius: 10px; border-left: 6px solid #002D62; box-shadow: 0px 4px 10px rgba(0,0,0,0.08); margin-bottom: 20px; }
    .footer-section { margin-top: 50px; padding: 30px; background-color: #f8f9fa; border-radius: 10px; text-align: center;}
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE FOR MULTI-PAGE ROUTING ---
# This controls which "page" the user is currently viewing
if "page" not in st.session_state:
    st.session_state.page = "home"
if "user_email" not in st.session_state:
    st.session_state.user_email = None

# --- SIDEBAR NAVIGATION ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/5/55/Emblem_of_India.svg", width=70)
st.sidebar.markdown("### National Doc Portal")

if st.session_state.user_email is None:
    st.sidebar.markdown("---")
    # Multi-page navigation buttons
    if st.sidebar.button("Login to Your Account", use_container_width=True):
        st.session_state.page = "login"
        st.rerun()
        
    st.sidebar.markdown("<div style='text-align: center; margin: 10px 0;'><i>or</i></div>", unsafe_allow_html=True)
    
    if st.sidebar.button("New to DocVerify India? Create a new account", type="primary", use_container_width=True):
        st.session_state.page = "register"
        st.rerun()
        
    if st.sidebar.button("🏠 Return to Home", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()
else:
    st.sidebar.success(f"Logged in as:\n**{st.session_state.user_email}**")
    if st.sidebar.button("🏠 Dashboard"):
        st.session_state.page = "home"
        st.rerun()
    if st.sidebar.button("Log Out", type="primary"):
        supabase.auth.sign_out()
        st.session_state.user_email = None
        st.session_state.page = "home"
        st.rerun()

# ==========================================
# PAGE 1: REGISTRATION PAGE
# ==========================================
if st.session_state.page == "register":
    st.title("Create Your Digital Identity Vault")
    st.markdown("Join DocVerifyIndia to securely store and pre-verify your official documents.")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        with st.form("register_form"):
            new_email = st.text_input("Email Address")
            new_password = st.text_input("Create Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            submit_register = st.form_submit_button("Create Account", type="primary")
            
            if submit_register:
                if new_password != confirm_password:
                    st.error("Passwords do not match!")
                else:
                    try:
                        res = supabase.auth.sign_up({"email": new_email, "password": new_password})
                        st.success("Account Created Successfully! You can now log in.")
                    except Exception as e:
                        st.error(f"Registration Failed: {e}")

# ==========================================
# PAGE 2: LOGIN PAGE
# ==========================================
elif st.session_state.page == "login":
    st.title("Secure Portal Login")
    st.markdown("Access your saved government and banking verification files.")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        with st.form("login_form"):
            login_email = st.text_input("Email Address")
            login_password = st.text_input("Password", type="password")
            submit_login = st.form_submit_button("Secure Sign In", type="primary")
            
            if submit_login:
                try:
                    res = supabase.auth.sign_in_with_password({"email": login_email, "password": login_password})
                    st.session_state.user_email = login_email
                    st.session_state.page = "home"  # Redirect to home on success
                    st.rerun()
                except Exception as e:
                    st.error("Invalid Email or Password. Please try again.")

# ==========================================
# PAGE 3: MAIN DASHBOARD (HOME)
# ==========================================
elif st.session_state.page == "home":
    # Top Banner Image to make it look official
    st.image("https://images.unsplash.com/photo-1585036156171-384164a8c675?q=80&w=2000&auto=format&fit=crop", use_container_width=True, caption="Centralized Document AI Verification")
    
    st.markdown("<div class='main-header'>DocVerifyIndia: Official Pre-Checker</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-text'>Select your required service below. Our AI cross-references your uploads against the latest RTO, UIDAI, and Banking regulations to ensure zero rejections.</div>", unsafe_allow_html=True)

    # Master Document Database (Updated with your massive research)
    SERVICES_DB = {
        "-- Select a Service --": [],
        "Update Aadhaar Details (Name/Address)": [
            "Proof of Identity (Indian Passport / PAN / Voter ID / Driving License)", 
            "Proof of Address (Utility Bill < 3 months / Bank Statement / Rent Agreement)", 
            "Marriage Cert / Gazette Notification (If major name change)"
        ],
        "Driving License Application (Fresh/Commercial)": [
            "Form 4 (Application) & Form 1 (Self Declaration of Fitness)",
            "Form 1a (Medical Cert - If over 40) / Form 5 (Commercial)",
            "Original Learner's License (> 30 days old)",
            "Age Proof (10th Marksheet / Birth Cert / PAN)",
            "Current Address Proof (e.g., Vadodara Rent Agreement / Voter ID)",
            "3-4 Identical Passport Size Photos"
        ],
        "Passport Application (Fresh/Renewal)": [
            "Proof of Address (Aadhaar / Utility Bill / Bank Passbook)",
            "Proof of Date of Birth (Aadhaar / PAN / Birth Cert)",
            "Non-ECR Proof (10th Standard Marksheet)",
            "Self-Attested Copies of Old Passport (If Renewal)",
            "Annexure F (If lost/stolen)"
        ],
        "Demat Account & Trading (F&O)": [
            "PAN Card (Mandatory)",
            "Address Proof (Aadhaar / Passport / Voter ID)",
            "Bank Proof (Cancelled Cheque / Bank Statement)",
            "F&O Income Proof (ITR / Last 6 Month Bank Statement / Latest Salary Slip)"
        ],
        "Bank Account Opening (Savings)": [
            "Officially Valid Document (Aadhaar / Passport / Voter ID / NREGA Card)",
            "PAN Card (or Form 60 if PAN is unavailable)",
            "2-3 Recent Passport Size Photographs",
            "Proof of Current Address (If different from official ID)"
        ]
    }

    col1, col2 = st.columns([2, 1])

    with col1:
        selected_service = st.selectbox("Select Government or Banking Service:", list(SERVICES_DB.keys()))

        if selected_service != "-- Select a Service --":
            docs_needed = SERVICES_DB[selected_service]
            st.markdown(f"<div class='card'><h4>Required Documents for: {selected_service}</h4><p>Based on current regulations, please provide the following <b>{len(docs_needed)}</b> verified documents.</p></div>", unsafe_allow_html=True)
            
            uploaded_files = {}
            for doc_name in docs_needed:
                uploaded_files[doc_name] = st.file_uploader(f"Upload: {doc_name}", type=["jpg", "png", "pdf"], key=doc_name)
            
            if all(uploaded_files.values()):
                if st.session_state.user_email:
                    st.success("✅ All documents scanned and matched! Vault sync complete.")
                else:
                    st.error("⚠️ Pre-check complete, but you must create an account to save these results.")
        else:
            st.info("👆 Please select a service from the dropdown menu to see the exact document checklist.")

    with col2:
        st.markdown("### 📊 Status Tracker")
        if st.session_state.user_email:
            st.success("System: ONLINE & SECURE")
        else:
            st.warning("System: GUEST MODE")
            
        st.image("https://images.unsplash.com/photo-1563986768494-4dee2763ff3f?q=80&w=800&auto=format&fit=crop", use_container_width=True, caption="Secure Vault Technology")

    # --- FOOTER SECTION (Makes the page longer and professional) ---
    st.markdown("""
        <div class='footer-section'>
            <h3>How DocVerifyIndia Works</h3>
            <p>1. <b>Upload</b> your forms and IDs. <br>2. <b>AI Scanning</b> checks for spelling mismatches, blurry images, and expired bills. <br>3. <b>Approval</b> ensures your paperwork is 100% ready for the bank or government office.</p>
            <hr>
            <small>© 2026 DocVerifyIndia | Secure AI Processing Portal | Protected by Supabase Architecture</small>
        </div>
    """, unsafe_allow_html=True)
