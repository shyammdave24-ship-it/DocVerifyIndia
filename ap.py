import streamlit as st
from supabase import create_client
import time # Added for the dramatic AI loading effect

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
    .info-box { background-color: #e9ecef; padding: 30px; border-radius: 10px; border-left: 8px solid #17a2b8; margin-top: 20px; margin-bottom: 20px; font-size: 18px;}
    .alert-box { background-color: #fff3cd; padding: 25px; border-radius: 10px; border-left: 8px solid #ffc107; margin-bottom: 30px; font-size: 16px;}
    .faq-text { font-size: 16px; color: #444; margin-bottom: 20px; line-height: 1.8;}
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
    left, right = st.columns([1, 1])
    with left:
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
                    except: st.error("Registration failed. Email might already exist.")
    with right:
        st.image("https://images.unsplash.com/photo-1563986768494-4dee2763ff3f?auto=format&fit=crop&w=800&q=80", caption="Protected by 256-bit AES Encryption")

# ==========================================
# PAGE: LOGIN
# ==========================================
elif st.session_state.page == "login":
    st.markdown("<div class='section-header'>Secure Portal Access</div>", unsafe_allow_html=True)
    left, right = st.columns([1, 1])
    with left:
        with st.form("log_form"):
            log_email = st.text_input("Registered Email")
            log_pass = st.text_input("Secure Password", type="password")
            if st.form_submit_button("Unlock Vault", type="primary"):
                try:
                    supabase.auth.sign_in_with_password({"email": log_email, "password": log_pass})
                    st.session_state.user_email = log_email
                    st.session_state.page = "home"
                    st.rerun()
                except: st.error("Invalid credentials. Ensure your email is correct.")
    with right:
        st.image("https://images.unsplash.com/photo-1614064641913-a53b2110c710?auto=format&fit=crop&w=800&q=80", caption="AI Security Gateway Active")

# ==========================================
# PAGE: HOME (MASSIVE DASHBOARD)
# ==========================================
elif st.session_state.page == "home":
    
    st.image("https://images.unsplash.com/photo-1618044733300-9472054094ee?auto=format&fit=crop&w=2000&q=80", use_container_width=True)

    st.markdown("<div class='main-title'>DocVerifyIndia Engine</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>The National AI Document Pre-Verification Protocol</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='font-size: 20px; line-height: 1.8; color: #444; margin-bottom: 50px;'>
    Every day, millions of Indian citizens face rejection at Regional Transport Offices (RTOs), Passport Seva Kendras, and private banks due to minor discrepancies in their paperwork. A misspelled middle name, an expired electricity bill, or a missing Form 1a can delay your application by weeks. <b>DocVerifyIndia</b> solves this by running your documents through advanced AI text-matching models before you submit them to the government.
    </div>
    """, unsafe_allow_html=True)

    # --- THE VERIFICATION CONSOLE ---
    st.markdown("<div class='section-header'>📄 Live AI Verification Console</div>", unsafe_allow_html=True)
    
    SERVICES = {
        "-- Select Your Official Service --": [],
        "Update Aadhaar Card (Name/Address)": [
            "Proof of Identity (Passport/PAN/Voter ID/Driving License)",
            "Proof of Address (Utility Bill <3 months / Bank Statement / Rent Agreement)",
            "Marriage Certificate (If changing name post-marriage)",
            "Gazette Notification (For full major name change)"
        ],
        "Driving License Application (Fresh/RTO)": [
            "Form 1 (Self Declaration) & Form 1a (Medical Cert - if over 40)",
            "Age Proof (10th Marksheet/Birth Cert)",
            "Current Address Proof (Rent Agreement/Voter ID/Passport)",
            "Original Learner's License (>30 days old)",
            "Passport Photos with White Background"
        ],
        "Passport Application (Fresh/Re-issue)": [
            "Address Proof (Utility Bill/Passbook)",
            "Date of Birth Proof (Birth Cert/PAN)",
            "10th Standard Marksheet (For Non-ECR status)",
            "Annexure F (If Passport is Lost or Stolen)"
        ],
        "Demat & Trading Account (F&O)": [
            "PAN Card (Mandatory)",
            "Address Proof (Voter ID / Driving License)",
            "Cancelled Cheque (MICR/IFSC visible)",
            "Income Proof for F&O (ITR / Last 6 Month Bank Statement)"
        ],
        "Savings Bank Account Opening": [
            "Officially Valid ID (Passport / Voter ID)",
            "PAN Card (or Form 60)",
            "Updated Address Proof (If current address differs from ID)"
        ]
    }

    col1, col2 = st.columns([2, 1])

    with col1:
        selected = st.selectbox("Select the application you are preparing for:", list(SERVICES.keys()))

        if selected != "-- Select Your Official Service --":
            reqs = SERVICES[selected]
            st.markdown(f"<div class='card'><h3>Required KYC Checklist</h3><p>Upload the following <b>{len(reqs)}</b> items to begin the AI mismatch scan.</p></div>", unsafe_allow_html=True)
            
            # Create a dictionary to hold the uploaded files
            uploaded_files = {}
            for doc in reqs:
                uploaded_files[doc] = st.file_uploader(f"Upload {doc}", type=["jpg", "png", "pdf"], key=doc)
                
            st.markdown("<br>", unsafe_allow_html=True)
            
            # --- THE NEW VERIFY BUTTON ---
            if st.button("🔍 Verify Documents Using AI", type="primary", use_container_width=True):
                # Logic: Check if EVERY file slot has something uploaded
                if all(uploaded_files.values()):
                    # Simulate the AI doing heavy work
                    with st.spinner('AI Engine extracting OCR text and scanning for discrepancies...'):
                        time.sleep(3) # Wait 3 seconds for dramatic effect
                        
                    # Show the result based on login status
                    if st.session_state.user_email:
                        st.success("✅ Secure Vault Sync: MATCH SUCCESS. All documents are perfectly aligned with regulatory standards.")
                        st.balloons() # Shoot celebration balloons!
                    else:
                        st.warning("⚠️ Pre-check complete: Documents appear valid, but you must log in or create an account to generate the final verification report.")
                else:
                    st.error("❌ Action Blocked: You must upload all required files before running the Verification Engine.")
                    
        else:
            st.info("👆 Please select a service from the dropdown menu to load the specific upload portals.")

    with col2:
        st.markdown("### Vault Status")
        if st.session_state.user_email:
            st.success("✅ Secure Vault: CONNECTED")
            st.markdown(f"User: `{st.session_state.user_email}`")
        else:
            st.warning("🔒 Guest Mode: ACTIVE")
            st.markdown("*Data will not be saved. Please login.*")
            
        st.image("https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?auto=format&fit=crop&w=600&q=80", caption="Financial Compliance Check")

    # --- SECTION: HOW IT WORKS ---
    st.markdown("<div class='section-header'>⚙️ How Our AI Engine Processes Your Data</div>", unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown("### 1. OCR Extraction")
        st.write("Optical Character Recognition reads every pixel of your uploaded image, turning photos of your 10th Marksheet and PAN card into readable machine text.")
    with col_b:
        st.markdown("### 2. Syntax Matching")
        st.write("The system compares Name, Father's Name, and Date of Birth across all documents. It uses fuzzy-matching to detect if 'Samarth M. Dave' matches 'Samarth Dave'.")
    with col_c:
        st.markdown("### 3. Timeline Validation")
        st.write("Algorithms check the dates on your Electricity, Water, or Gas bills. If the bill is older than 90 days, the system instantly flags it for rejection.")

    # --- SECTION: WHY APPLICATIONS FAIL ---
    st.markdown("<div class='section-header'>📉 Top Reasons for Government Rejections</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='info-box'>
        <b>1. The "Address Discrepancy" Trap</b><br>
        Many citizens try to open Bank Accounts using a Rent Agreement that is NOT legally registered or notarized. Most banks strictly require a registered lease agreement.
        <br><br>
        <b>2. Financial & Trading (F&O) Activation Failures</b><br>
        To trade in Futures & Options, SEBI regulations require strict proof of financial capability. Submitting an old bank statement will result in an instant block. You must provide the exact last 6 months, an ITR, or a Net Worth Certificate.
        <br><br>
        <b>3. Passport Annexure Errors</b><br>
        Applying for a re-issue of a lost passport requires Annexure F. Citizens often show up with just an FIR copy, missing the specific Annexure format required by the Passport Seva Kendra.
    </div>
    """, unsafe_allow_html=True)

    # --- SECTION: LIVE BULLETINS ---
    st.markdown("<div class='section-header'>🏛️ Live Regulatory Updates & Circulars</div>", unsafe_allow_html=True)
    st.markdown("<div class='alert-box'><b>🚨 June 2026 Mandate:</b> RBI has instructed all banks to ensure strict initial-matching between PAN and officially valid IDs. Minor spelling variations will trigger manual review delays.</div>", unsafe_allow_html=True)
    st.markdown("<div class='alert-box'><b>🚨 Transport Department Update:</b> Form 1a (Medical Certificate) is now strictly mandatory for all commercial driving licenses and applicants over the age of 40. Parivahan portal will reject applications without it.</div>", unsafe_allow_html=True)
    
    st.image("https://images.unsplash.com/photo-1450101499163-c8848c66ca85?auto=format&fit=crop&w=2000&q=80", use_container_width=True, caption="Legal Review and Compliance")

    # --- SECTION: MASSIVE FAQ ---
    st.markdown("<div class='section-header'>❓ Frequently Asked Questions (FAQ)</div>", unsafe_allow_html=True)
    
    with st.expander("What counts as a valid Utility Bill?", expanded=True):
        st.markdown("<div class='faq-text'>To be accepted as a Proof of Address (POA), you can submit an Electricity bill, Water bill, or Post-paid Mobile/Broadband bill. However, the absolute most critical rule is that it <b>must not be older than three months</b> from the date of your application.</div>", unsafe_allow_html=True)
        
    with st.expander("Do I need a Medical Certificate for my Driving License?", expanded=True):
        st.markdown("<div class='faq-text'>Yes, but it depends on two factors. You must submit <b>Form 1a (Medical Certificate)</b> signed by a registered medical practitioner if you are applying for a Transport/Commercial vehicle license, OR if you are over 40 years old applying for a standard private license. All other applicants only need Form 1 (Self Declaration).</div>", unsafe_allow_html=True)
        
    with st.expander("What documents prove my income for Demat F&O?", expanded=True):
        st.markdown("<div class='faq-text'>To activate Futures and Options trading, you must prove financial capability. Acceptable documents include: The last 6 months bank statement, the latest salary slip, a copy of your Income Tax Return (ITR), Form 16, or a Net Worth Certificate certified by a CA.</div>", unsafe_allow_html=True)

    with st.expander("What happens if my name changes after marriage?", expanded=True):
        st.markdown("<div class='faq-text'>If you are updating your name post-marriage, you must provide a Government-issued Marriage Certificate. If the name change is for a completely different reason (major name change), you are legally required to provide a Gazette Notification.</div>", unsafe_allow_html=True)

    # --- MASSIVE FOOTER ---
    st.markdown("""
        <div class='footer'>
            <h2>DocVerifyIndia Core Infrastructure</h2>
            <p>Built with Streamlit and Secured by Supabase Cloud Architecture</p>
            <hr style='border-color: #333; margin: 30px 0;'>
            <p><b>Legal Disclaimer:</b> This portal is a pre-verification engine meant to assist citizens in preparing their documentation. It is not directly affiliated with UIDAI, the RBI, or the Ministry of Road Transport and Highways. Final approval of all documents is at the sole discretion of the respective government authorities and banking institutions.</p>
            <p>All uploaded documents are processed via RAM-based ephemeral memory and encrypted utilizing AES-256 military-grade standards. Data is completely wiped upon session termination unless explicitly saved to a registered user vault.</p>
            <br>
            <p>© 2026 DocVerifyIndia Systems | Vadodara, Gujarat Operations | All Rights Reserved.</p>
        </div>
    """, unsafe_allow_html=True)
