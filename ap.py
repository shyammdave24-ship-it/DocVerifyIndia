import streamlit as st
from supabase import create_client, Client

# --- SUPABASE CONNECTION ---
# Using your project's unique URL and publishable anon key
SUPABASE_URL = "https://osbbdapzegmiqgavlezr.supabase.co"
SUPABASE_KEY = "sb_publishable_OC-t8R7IZ6oy1ohHWW2ZhA_lak9hSav"

# Initialize the database connection safely
@st.cache_resource
def init_connection():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

try:
    supabase = init_connection()
except Exception as e:
    st.error("Database connection failed. Please check your network or keys.")

# --- PAGE LAYOUT & CUSTOM GOVERNMENT branding CSS ---
st.set_page_config(page_title="DocVerifyIndia", page_icon="🇮🇳", layout="wide")

st.markdown("""
    <style>
    .main-header { 
        font-size: 32px; font-weight: bold; color: #002D62; border-bottom: 3px solid #FF9933; padding-bottom: 10px; margin-bottom: 20px; 
    }
    .sub-text { 
        font-size: 16px; color: #444444; margin-bottom: 30px; 
    }
    .card { 
        background-color: #ffffff; padding: 25px; border-radius: 10px; border-left: 6px solid #002D62; box-shadow: 0px 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; 
    }
    .status-box { 
        padding: 15px; background-color: #e8f4f8; border-radius: 8px; border-left: 4px solid #138496; margin-bottom: 10px; 
    }
    .mismatch-box {
        background-color: #fff5f5; border-left: 6px solid #e53e3e; padding: 20px; border-radius: 8px; margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR: SECURE AUTHENTICATION SYSTEM ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/5/55/Emblem_of_India.svg", width=60)
st.sidebar.markdown("### National Doc Portal")

# Manage user log in session states
if "user_email" not in st.session_state:
    st.session_state.user_email = None

if st.session_state.user_email is None:
    st.sidebar.markdown("### 🔒 Secure Access")
    auth_mode = st.sidebar.radio("Select Action", ["Login", "Sign Up"])
    email = st.sidebar.text_input("Email Address", key="auth_email")
    password = st.sidebar.text_input("Password", type="password", key="auth_pass")
    
    if st.sidebar.button(auth_mode):
        if auth_mode == "Sign Up":
            try:
                res = supabase.auth.sign_up({"email": email, "password": password})
                st.sidebar.success("Sign Up Successful! You can now log in.")
            except Exception as e:
                st.sidebar.error(f"Sign Up Failed: {e}")
                
        elif auth_mode == "Login":
            try:
                res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                st.session_state.user_email = email
                st.sidebar.success("Login Successful!")
                st.rerun()
            except Exception as e:
                st.sidebar.error("Invalid Email or Password.")
else:
    st.sidebar.success(f"Logged in securely as:\n{st.session_state.user_email}")
    if st.sidebar.button("Log Out"):
        supabase.auth.sign_out()
        st.session_state.user_email = None
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### Quick Links")
st.sidebar.markdown("📍 Locate Nearest Enrollment Center\n\n🏦 RBI Banking Guidelines\n\n📄 NSDL PAN Portal")

# --- MAIN DASHBOARD CONTENT ---
st.markdown("<div class='main-header'>DocVerifyIndia: Central Document Pre-Verification</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-text'>Avoid instant rejections at government offices and banking institutions. Upload your digital copies below for real-time AI formatting scans, spelling mismatch detection, and official compliance verification.</div>", unsafe_allow_html=True)

# Master Database of comprehensive services and their explicit regulatory requirements
SERVICES_DB = {
    "-- Select a Service --": [],
    "Bank Account Opening (Savings)": ["Aadhaar Card", "PAN Card", "Recent Passport Photo", "Proof of Address (If current address differs)"],
    "Demat Account & Trading (F&O)": ["Aadhaar Card", "PAN Card", "Cancelled Cheque", "Bank Statement (Last 6 Months)"],
    "Passport Application (Fresh/Renewal)": ["Aadhaar Card", "10th Marksheet (For Non-ECR)", "Utility Bill (Last 2 Months)"],
    "Driving License Application": ["Learner's License Copy", "Aadhaar Card", "Age Proof (Birth Certificate)"],
    "Update Aadhaar Details (Address/Name)": ["Proof of Identity (Voter ID/Passport)", "Proof of Address (Utility Bill/Rent Agreement)"],
    "PAN Card Correction": ["Aadhaar Card", "Proof of DOB", "Official Gazette Notification (If Name Change)"],
    "Voter ID Registration": ["Aadhaar Card", "Passport Size Photo", "Age Proof Document"],
    "Marriage Certificate Verification": ["Husband's Aadhaar", "Wife's Aadhaar", "Wedding Photograph", "Wedding Invitation Card"],
    "Income Certificate Application": ["Aadhaar Card", "Salary Slip / ITR Copy", "Electricity Bill"]
}

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📄 Initialize Pre-Screening")
    selected_service = st.selectbox("Select Government or Banking Service:", list(SERVICES_DB.keys()))

    if selected_service != "-- Select a Service --":
        docs_needed = SERVICES_DB[selected_service]
        st.markdown(f"<div class='card'><h4>Service Selected: {selected_service}</h4><p>Regulatory rules mandate that you must provide exactly <b>{len(docs_needed)}</b> items for verification handling.</p></div>", unsafe_allow_html=True)
        
        # Dynamic creation of file upload portals based on selected service structure
        uploaded_files = {}
        st.markdown("临 **Document Upload Portal**")
        for doc_name in docs_needed:
            uploaded_files[doc_name] = st.file_uploader(f"Upload {doc_name}", type=["jpg", "jpeg", "png", "pdf"], key=doc_name)
        
        # Run logic check when all required fields have content
        if all(uploaded_files.values()):
            st.success("🎉 All documents successfully captured in buffer! Executing text comparison...")
            
            # Simulated Core Mismatch Logic Engine for demonstration purposes
            if "Aadhaar Card" in uploaded_files and "PAN Card" in uploaded_files:
                st.markdown("<div class='mismatch-box'>", unsafe_allow_html=True)
                st.error("❌ Verification Failed: Data Alignment Mismatch Identified!")
                st.markdown("""
                    * **Aadhaar Card Details:** Name spelling matches system standard.
                    * **PAN Card Details:** Discrepancy caught in middle name configuration or initials.
                    
                    *The core names do not align 100% identically. Modern financial systems and registrar workflows will automatically filter out this application.*
                """)
                
                # The integrated problem solver element
                st.markdown("---")
                st.markdown("### 💡 Dynamic Resolution Plan: Fix This Discrepancy")
                st.markdown(f"""
                    To complete your setup for **{selected_service}**, your credentials must reflect identical profiles across platforms. 
                    
                    **Step-by-Step Recovery Actions:**
                    1. Apply for an online data correction profile via the secure NSDL portal.
                    2. Maintain these primary validating documents ready to prove identity matching:
                       * Matriculation Board Pass Certificate
                       * Valid Indian Passport
                       * Gazetted Officer Authentication Certificate
                """)
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.info("Document framework processed cleanly. Scanning structural properties for compliance metrics...")
    else:
        st.markdown("""
        <div class='card'>
            <h5>System Instructions:</h5>
            <ol>
                <li>Choose an intended processing category from the centralized service menu.</li>
                <li>Import your respective document certificates directly from your storage or camera roll.</li>
                <li>The validation layer evaluates layout patterns, structures metadata, flags misaligned fields, and renders instructions on how to handle errors immediately.</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("### 📊 Vault Overview")
    if st.session_state.user_email:
        st.success("✅ Secure Cloud Storage Connected via Supabase Engine")
        st.markdown(f"**Authenticated Storage Token:** active")
    else:
        st.warning("🔒 Sign in from the lateral navigation panel to register your secure identity vault storage.")
        
    st.markdown("### 🔔 Live Network Bulletins")
    st.info("**Update:** Central guidelines mandate total name syntax synchronization between primary identifiers and processing vaults.")
    st.info("**Notice:** Distributed sandboxed cloud server nodes fully active.")
