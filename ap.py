import streamlit as st

# Set up the page layout to look clean and official like mAadhaar/mParivahan
st.set_page_config(page_title="DocVerifyIndia", page_icon="🇮🇳", layout="centered")

# Custom CSS to inject official government-style branding (trustworthy blues and high contrast)
st.markdown("""
    <style>
    .main-header {
        font-size: 28px; font-weight: bold; color: #003366; text-align: center; margin-bottom: 2px;
    }
    .sub-header {
        font-size: 14px; color: #666666; text-align: center; margin-bottom: 25px;
    }
    .feature-card {
        background-color: #f8f9fa; padding: 20px; border-radius: 10px; 
        border-left: 5px solid #003366; margin-bottom: 15px; box-shadow: 0px 2px 4px rgba(0,0,0,0.05);
    }
    .stButton>button {
        width: 100%; background-color: #003366; color: white; border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# App Header Layout
st.markdown("<div class='main-header'>DocVerifyIndia</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Official Pre-Verification & Document Correction Portal</div>", unsafe_allow_html=True)

# 1. User Authentication Section
st.sidebar.image("https://img.icons8.com/fluent/100/000000/user-male-circle.png", width=80)
st.sidebar.markdown("### Secure Sign In")
choice = st.sidebar.selectbox("Account Actions", ["Login", "Sign Up"])
email = st.sidebar.text_input("Email Address")
password = st.sidebar.text_input("Password", type="password")

if st.sidebar.button(choice):
    st.sidebar.success(f"Successfully authenticated as {email}!")

# 2. Main Service Dashboard Grid
st.markdown("### Select Your Verification Service")
service = st.selectbox(
    "What are you applying for / updating today?",
    [
        "-- Choose a Service --",
        "Bank Account Opening Check",
        "Demat Account Opening Check",
        "Update Aadhaar Card Details",
        "PAN Card Correction Verification",
        "Marriage Certificate Verification"
    ]
)

if service != "-- Choose a Service --":
    st.markdown(f"<div class='feature-card'><h4>Selected: {service}</h4><p>Please upload the required documents below from your phone gallery or take a live photo to initiate AI cross-matching.</p></div>", unsafe_allow_html=True)
    
    # Dynamic Document Requirements Based on Selection
    if service == "Demat Account Opening Check" or service == "Bank Account Opening Check":
        st.info("Required Documents: 1. PAN Card | 2. Aadhaar Card")
        doc1 = st.file_uploader("Upload PAN Card", type=["jpg", "jpeg", "png", "pdf"])
        doc2 = st.file_uploader("Upload Aadhaar Card", type=["jpg", "jpeg", "png", "pdf"])
        
        if doc1 and doc2:
            st.warning("⚠️ Simulation Mode: Processing images via AI pipeline...")
            
            # Simulated Mismatch Logic for Demonstration
            st.error("❌ Verification Failed: Name Mismatch Detected!")
            st.markdown("""
                * **PAN Card Name:** SAMARTH KUMAR DAVE
                * **Aadhaar Card Name:** SAMARTH DAVE
                
                *The names do not match exactly. Indian banks/brokers will reject this application.*
            """)
            
            # The Problem Solver / Resolution Panel
            st.markdown("---")
            st.markdown("### 💡 Resolution Guide: How to Fix This Mismatch")
            st.markdown(f"""
                To open your **{service}**, your PAN card details must match your Aadhaar exactly. 
                
                **Recommended Action:** Update your PAN Card name to match your Aadhaar card using these officially accepted supporting documents:
                * Matriculation / School Leaving Certificate
                * Passport
                * Central/State Government ID Card
                
                [Click here to apply for an online PAN correction via NSDL portal]
            """)

    else:
        st.info("Service workflow loading... Upload supporting proofs.")
        generic_doc = st.file_uploader("Upload Document Copy", type=["jpg", "jpeg", "png", "pdf"])
        if generic_doc:
            st.success("Document uploaded successfully! AI verification initialized.")

else:
    # Default State Layout
    st.markdown("""
    <div class='feature-card'>
        <h5>How it works:</h5>
        <ol>
            <li>Select the government or banking action you want to complete.</li>
            <li>Snap a photo or upload your documents straight from your mobile gallery.</li>
            <li>Our AI checks your KYC alignment and gives you an instant green light or custom step-by-step correction instructions.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
