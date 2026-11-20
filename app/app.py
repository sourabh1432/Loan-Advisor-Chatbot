
import sys
import logging
from pathlib import Path
from datetime import datetime
import plotly.graph_objects as go

import streamlit as st


# ==========================================================
# 1. PROJECT CONFIGURATION
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.conversation_manager import LoanConversationManager


st.set_page_config(
    page_title="Loan Advisor AI",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# 2. LOGGING
# ==========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("loan_advisor")


# ==========================================================
# 3. THEME AND CUSTOM CSS
# ==========================================================

st.markdown("""
<style>

/* --------------------------------------------------
   GLOBAL THEME
-------------------------------------------------- */

.stApp {
    background: #F4F7FB;
    color: #172B4D;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Main headings */

h1, h2, h3 {
    color: #142D4E !important;
    font-weight: 700 !important;
}

p, li, label {
    color: #425466;
}

/* --------------------------------------------------
   SIDEBAR
-------------------------------------------------- */

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #10243A 0%,
        #173B55 100%
    );
}

[data-testid="stSidebar"] * {
    color: #F2F6FC;
}

[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
    color: #B7C9D9;
}

[data-testid="stSidebar"] hr {
    border-color: #35516A;
}

/* Sidebar buttons */

[data-testid="stSidebar"] div.stButton > button {
    background: #1E4962;
    color: #FFFFFF;
    border: 1px solid #35647D;
    border-radius: 10px;
    min-height: 42px;
}

[data-testid="stSidebar"] div.stButton > button:hover {
    background: #287184;
    border-color: #49B7B0;
}

/* --------------------------------------------------
   HERO SECTION
-------------------------------------------------- */

.hero {
    background: linear-gradient(120deg, #10243A, #14566C, #147D87);
    padding: 38px;
    border-radius: 20px;
    margin-bottom: 28px;
    box-shadow: 0 10px 28px rgba(16, 36, 58, 0.14);
}

.hero-label {
    color: #65D6CB;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
}

.hero h1 {
    color: #FFFFFF;
    font-size: 35px;
}

.hero p {
    color: #E1EDF4;
    font-size: 15px;
    line-height: 1.7;
}

.hero-tags {
    color: #FFFFFF;
    font-size: 13px;
    font-weight: 600;
}


/* --------------------------------------------------
   FEATURE CARDS
-------------------------------------------------- */

.feature-card {
    background: #FFFFFF;
    padding: 23px;
    border-radius: 16px;
    border: 1px solid #E1E8F0;
    min-height: 160px;
    margin-bottom: 12px;

    box-shadow: 0 4px 15px rgba(20, 45, 78, 0.05);

    transition: all 0.2s ease;
}

.feature-card:hover {
    border-color: #159A9A;
    box-shadow: 0 8px 20px rgba(20, 45, 78, 0.10);
    transform: translateY(-3px);
}

.feature-card h3 {
    color: #173B55 !important;
    font-size: 19px;
    margin-bottom: 10px;
}

.feature-card p {
    color: #64788C !important;
    font-size: 14px;
    line-height: 1.6;
}

/* --------------------------------------------------
   BUTTONS
-------------------------------------------------- */

div.stButton > button {
    background: linear-gradient(
        110deg,
        #147D87,
        #159A9A
    );

    color: #FFFFFF;
    border: none;
    border-radius: 10px;
    min-height: 44px;
    font-weight: 650;

    transition: all 0.2s ease;
}

div.stButton > button:hover {
    background: #116874;
    color: #FFFFFF;
    border: none;
    box-shadow: 0 5px 14px rgba(20, 125, 135, 0.18);
}

/* --------------------------------------------------
   CHAT MESSAGES
-------------------------------------------------- */

[data-testid="stChatMessage"] {
    background: #FFFFFF;
    border: 1px solid #E1E8F0;
    border-radius: 15px;
    padding: 15px;
    margin-bottom: 12px;
    box-shadow: 0 3px 12px rgba(20, 45, 78, 0.04);
}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li {
    color: #263B53;
    line-height: 1.7;
    font-size: 15px;
}

/* --------------------------------------------------
   CHAT INPUT
-------------------------------------------------- */

[data-testid="stChatInput"] {
    background-color: #FFFFFF !important;
    border: 2px solid #159A9A !important;
    border-radius: 15px !important;
}

/* Typed message text */

[data-testid="stChatInput"] textarea,
[data-testid="stChatInput"] textarea:focus,
[data-baseweb="textarea"] textarea {
    color: #172B4D !important;
    -webkit-text-fill-color: #172B4D !important;
    caret-color: #159A9A !important;
    background-color: #FFFFFF !important;
    font-size: 16px !important;
    font-weight: 500 !important;
    opacity: 1 !important;
}

/* Placeholder text */

[data-testid="stChatInput"] textarea::placeholder {
    color: #718397 !important;
    -webkit-text-fill-color: #718397 !important;
    opacity: 1 !important;
}

/* Input focus */

[data-testid="stChatInput"]:focus-within {
    border-color: #159A9A !important;
    box-shadow: 0 0 0 3px rgba(21, 154, 154, 0.15) !important;
}

/* --------------------------------------------------
   PROGRESS BAR
-------------------------------------------------- */

[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(
        90deg,
        #147D87,
        #55C8B5
    );
    border-radius: 20px;
}

/* --------------------------------------------------
   METRICS
-------------------------------------------------- */

[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #E1E8F0;
    border-radius: 13px;
    padding: 15px;
}

/* --------------------------------------------------
   DIVIDERS AND FOOTER
-------------------------------------------------- */

hr {
    border-color: #E1E8F0;
}

.footer {
    text-align: center;
    color: #718397;
    font-size: 13px;
    line-height: 1.8;
    padding: 20px 10px;
}

.footer strong {
    color: #173B55;
    font-size: 17px;
}

/* --------------------------------------------------
   MOBILE RESPONSIVENESS
-------------------------------------------------- */

@media (max-width: 768px) {

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .hero {
        padding: 25px 20px;
    }

    .hero h1 {
        font-size: 27px;
    }

    .feature-card {
        padding: 17px;
        min-height: 140px;
    }
}



/* ==========================================
   CHAT SEND BUTTON - CLARITY FIX
========================================== */

[data-testid="stChatInput"] button {
    opacity: 1 !important;
    filter: none !important;
    -webkit-filter: none !important;
    backdrop-filter: none !important;
    transform: none !important;
    box-shadow: none !important;
    background: transparent !important;
    border: none !important;
    color: #147D87 !important;
    transition: background-color 0.2s ease !important;
}

/* Send icon */

[data-testid="stChatInput"] button svg {
    opacity: 1 !important;
    filter: none !important;
    -webkit-filter: none !important;
    color: #147D87 !important;
    fill: none !important;
    stroke: #147D87 !important;
    stroke-width: 2.5px !important;
}

/* Hover */

[data-testid="stChatInput"] button:hover {
    background: #E5F5F3 !important;
    border-radius: 10px !important;
}

/* Focus */

[data-testid="stChatInput"] button:focus {
    outline: 2px solid #159A9A !important;
    outline-offset: 2px !important;
}


/* ==========================================
   PROFESSIONAL CHAT WINDOW DESIGN
========================================== */

/* Chat message container */

[data-testid="stChatMessage"] {
    background: #FFFFFF !important;
    border: 1px solid #E4EAF1 !important;
    border-radius: 16px !important;
    padding: 18px 20px !important;
    margin: 12px 0 !important;
    box-shadow: 0 3px 12px rgba(16, 36, 58, 0.045) !important;
    transition: border-color 0.2s ease;
}

/* Assistant message */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) {
    background: #F7FAFC !important;
    border-left: 4px solid #159A9A !important;
}

/* User message */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-user"]
) {
    background: #FFFFFF !important;
    border-left: 4px solid #315B83 !important;
}

/* Message text */

[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
    color: #263B53 !important;
    font-size: 15px !important;
    line-height: 1.75 !important;
}

/* Message headings */

[data-testid="stChatMessage"] h1,
[data-testid="stChatMessage"] h2,
[data-testid="stChatMessage"] h3 {
    color: #173B55 !important;
}

/* Message lists */

[data-testid="stChatMessage"] li {
    margin-bottom: 5px !important;
}

/* Message avatars */

[data-testid="chatAvatarIcon-assistant"] {
    background: #DDF2EF !important;
    color: #147D87 !important;
    border-radius: 12px !important;
}

[data-testid="chatAvatarIcon-user"] {
    background: #E7EEF7 !important;
    color: #315B83 !important;
    border-radius: 12px !important;
}


/* Chat input */

[data-testid="stChatInput"] {
    background: #FFFFFF !important;
    border: 1.5px solid #D5E0EA !important;
    border-radius: 15px !important;
    box-shadow: 0 4px 15px rgba(16, 36, 58, 0.06) !important;
}

/* Typed text */

[data-testid="stChatInput"] textarea {
    color: #172B4D !important;
    -webkit-text-fill-color: #172B4D !important;
    font-size: 15px !important;
}

/* Send button */

[data-testid="stChatInput"] button {
    background: #147D87 !important;
    opacity: 1 !important;
    border-radius: 10px !important;
    filter: none !important;
}

[data-testid="stChatInput"] button svg {
    color: #FFFFFF !important;
    stroke: #FFFFFF !important;
    opacity: 1 !important;
    filter: none !important;
}

/* Hover effect */

[data-testid="stChatInput"] button:hover {
    background: #105F69 !important;
}

/* Input focus */

[data-testid="stChatInput"]:focus-within {
    border-color: #159A9A !important;
    box-shadow: 0 0 0 3px rgba(21, 154, 154, 0.12) !important;
}


/* ==========================================
   WHATSAPP-STYLE CHAT DESIGN
========================================== */

/* Common chat message */
[data-testid="stChatMessage"] {
    width: fit-content !important;
    max-width: 78% !important;
    padding: 12px 16px !important;
    margin-top: 9px !important;
    margin-bottom: 9px !important;
    border-radius: 17px !important;
    box-shadow: 0 2px 6px rgba(20, 45, 78, 0.07) !important;
}

/* AI messages - LEFT SIDE */
[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) {
    margin-right: auto !important;
    margin-left: 0 !important;
    background: #FFFFFF !important;
    border: 1px solid #E1E8F0 !important;
    border-left: 4px solid #159A9A !important;
    border-radius: 5px 17px 17px 17px !important;
}

/* User messages - RIGHT SIDE */
[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-user"]
) {
    margin-left: auto !important;
    margin-right: 0 !important;
    background: #DDF5E2 !important;
    border: 1px solid #C8E9D0 !important;
    border-right: 4px solid #25A56A !important;
    border-radius: 17px 5px 17px 17px !important;
}

/* Chat text */
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li {
    color: #263B53 !important;
    font-size: 15px !important;
    line-height: 1.65 !important;
}

/* Chat avatars */
[data-testid="chatAvatarIcon-assistant"] {
    background: #DDF2EF !important;
    border-radius: 50% !important;
}

[data-testid="chatAvatarIcon-user"] {
    background: #D5E6F7 !important;
    border-radius: 50% !important;
}

/* Rounded chat input */
[data-testid="stChatInput"] {
    background: #FFFFFF !important;
    border: 1.5px solid #D5E0EA !important;
    border-radius: 24px !important;
    padding: 5px 10px !important;
    box-shadow: 0 4px 14px rgba(16, 36, 58, 0.09) !important;
}

/* Input text */
[data-testid="stChatInput"] textarea {
    color: #172B4D !important;
    -webkit-text-fill-color: #172B4D !important;
    font-size: 15px !important;
}

/* Send button */
[data-testid="stChatInput"] button {
    background: #159A78 !important;
    border-radius: 50% !important;
    opacity: 1 !important;
}

[data-testid="stChatInput"] button svg {
    stroke: #FFFFFF !important;
    color: #FFFFFF !important;
}

/* Mobile responsive */
@media (max-width: 768px) {
    [data-testid="stChatMessage"] {
        max-width: 92% !important;
    }
}


/* ==========================================
   ACTUAL WHATSAPP-STYLE CHAT BUBBLES
========================================== */

/* AI message bubble */
div[class*="st-key-ai_bubble"] {
    background: #FFFFFF !important;
    border: 1px solid #E1E8F0 !important;
    border-left: 4px solid #159A9A !important;
    border-radius: 5px 18px 18px 18px !important;
    padding: 12px 16px !important;
    margin: 8px 0 12px 0 !important;
    box-shadow: 0 3px 10px rgba(20, 45, 78, 0.06) !important;
}

/* User message bubble */
div[class*="st-key-user_bubble"] {
    background: #DDF5E2 !important;
    border: 1px solid #C8E9D0 !important;
    border-right: 4px solid #25A56A !important;
    border-radius: 18px 5px 18px 18px !important;
    padding: 12px 16px !important;
    margin: 8px 0 12px 0 !important;
    box-shadow: 0 3px 10px rgba(20, 45, 78, 0.05) !important;
}

/* Text inside bubbles */
div[class*="st-key-ai_bubble"] p,
div[class*="st-key-user_bubble"] p {
    color: #263B53 !important;
    font-size: 15px !important;
    line-height: 1.65 !important;
    margin-bottom: 5px !important;
}

/* Timestamp */
.chat-time {
    color: #82918A !important;
    font-size: 11px !important;
    text-align: right !important;
    margin-top: 5px !important;
}

/* Mobile */
@media (max-width: 768px) {
    div[class*="st-key-ai_bubble"],
    div[class*="st-key-user_bubble"] {
        padding: 10px 12px !important;
    }
}


/* ==========================================
   EMI RESULT - CHAT TYPOGRAPHY FIX
========================================== */

/* Normal chatbot text */
div[class*="st-key-ai_bubble"] p {
    font-size: 14px !important;
    line-height: 1.6 !important;
    font-weight: 400 !important;
    color: #34495E !important;
    margin-bottom: 8px !important;
}

/* All headings inside AI chat bubbles */
div[class*="st-key-ai_bubble"] h1 {
    font-size: 21px !important;
    line-height: 1.35 !important;
    font-weight: 700 !important;
    margin: 8px 0 !important;
}

div[class*="st-key-ai_bubble"] h2 {
    font-size: 19px !important;
    line-height: 1.4 !important;
    font-weight: 700 !important;
    margin: 8px 0 !important;
}

div[class*="st-key-ai_bubble"] h3 {
    font-size: 16px !important;
    line-height: 1.4 !important;
    font-weight: 650 !important;
    margin: 8px 0 !important;
}

/* EMI result emphasis */
div[class*="st-key-ai_bubble"] strong {
    color: #173B55 !important;
}

/* EMI result disclaimer */
div[class*="st-key-ai_bubble"] small {
    font-size: 12px !important;
    color: #718397 !important;
}

/* USER CHAT BUBBLE */
[class*="st-key-user_bubble"] {
    background: #DCF8C6 !important;
    border-radius: 16px 4px 16px 16px !important;
    padding: 14px 18px !important;
    margin: 8px 0 14px auto !important;
    border: 1px solid #C5E8B5 !important;
    box-shadow: 0 2px 5px rgba(0,0,0,0.06) !important;
}

/* AI CHAT BUBBLE */
[class*="st-key-ai_bubble"] {
    background: #FFFFFF !important;
    border-radius: 4px 16px 16px 16px !important;
    padding: 14px 18px !important;
    margin: 8px auto 14px 0 !important;
    border: 1px solid #E5EAF0 !important;
    border-left: 4px solid #159A9A !important;
    box-shadow: 0 2px 5px rgba(0,0,0,0.06) !important;
}

/* CHAT TEXT */
[class*="st-key-user_bubble"] p,
[class*="st-key-ai_bubble"] p {
    color: #263B53 !important;
    font-size: 15px !important;
    line-height: 1.6 !important;
}

/* CHAT TIMESTAMP */
.chat-time {
    text-align: right;
    font-size: 11px;
    color: #718397;
    margin-top: 8px;
}

/* =========================================
   LOAN ADVISOR PREMIUM SIDEBAR
========================================= */

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #10263D 0%,
        #153B55 55%,
        #10445A 100%
    ) !important;
    min-width: 290px !important;
    max-width: 290px !important;
}

[data-testid="stSidebar"] > div:first-child {
    background: transparent !important;
}

/* Sidebar branding */
.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 0 20px;
}

.sidebar-logo {
    width: 48px;
    height: 48px;
    border-radius: 13px;
    background: #20516B;
    border: 1px solid #39718A;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 25px;
}

.sidebar-brand-name {
    color: #FFFFFF;
    font-size: 19px;
    font-weight: 800;
}

.sidebar-brand-subtitle {
    color: #B5D0DF;
    font-size: 11px;
    margin-top: 4px;
}

.sidebar-heading {
    color: #80DED3;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.3px;
    margin: 20px 0 10px;
}

.sidebar-divider {
    height: 1px;
    background: rgba(255,255,255,0.16);
    margin: 14px 0;
}

/* All sidebar buttons */
[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    min-height: 45px;
    text-align: left;
    background: transparent !important;
    color: #EAF3F8 !important;
    border: 1px solid transparent !important;
    border-radius: 10px !important;
    padding: 9px 12px !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease;
}

/* Hover effect */
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(128,222,211,0.12) !important;
    border: 1px solid rgba(128,222,211,0.35) !important;
    color: #80DED3 !important;
}

/* New conversation button */
[data-testid="stSidebar"] .st-key-sidebar_new_conversation button {
    background: #167B83 !important;
    border: 1px solid #37A9A5 !important;
    color: #FFFFFF !important;
    text-align: center !important;
    font-weight: 700 !important;
}

[data-testid="stSidebar"] .st-key-sidebar_new_conversation button:hover {
    background: #209B9A !important;
    color: #FFFFFF !important;
}

/* Sidebar text */
[data-testid="stSidebar"] p {
    color: #DCEAF2;
}

[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
    color: #AFC7D8 !important;
}

/* Progress bar */
[data-testid="stSidebar"] [data-testid="stProgressBar"] > div {
    background: #36566C !important;
}

[data-testid="stSidebar"] [data-testid="stProgressBar"] > div > div {
    background: #43C6B7 !important;
}

/* Footer */
.sidebar-footer {
    color: #AFC7D8;
    text-align: center;
    font-size: 11px;
    line-height: 1.8;
    padding: 12px 0;
}

""", unsafe_allow_html=True)


# ==========================================================
# LOAN APPROVAL PROBABILITY CHART
# ==========================================================

def show_prediction_chart(probabilities, prediction):

    approved = float(probabilities.get("Approved", 0))
    rejected = float(probabilities.get("Rejected", 0))

    # Validate probability values
    if (
        not 0 <= approved <= 100
        or not 0 <= rejected <= 100
    ):
        st.warning("Invalid probability values.")
        return

    st.markdown("### 📊 Loan Approval Analysis")

    # Prediction status
    if prediction.lower() == "approved":
        st.success("🎉 Model Prediction: APPROVED")
    else:
        st.error("⚠️ Model Prediction: REJECTED")

    # Probability metrics
    col1, col2 = st.columns(2)

    with col1:
        st.metric("✅ Approved", f"{approved:.2f}%")

    with col2:
        st.metric("❌ Rejected", f"{rejected:.2f}%")

    # Horizontal probability chart
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=[approved],
        y=["Approved"],
        orientation="h",
        marker_color="#16A36A",
        text=[f"{approved:.2f}%"],
        textposition="inside",
        name="Approved"
    ))

    fig.add_trace(go.Bar(
        x=[rejected],
        y=["Rejected"],
        orientation="h",
        marker_color="#DC5555",
        text=[f"{rejected:.2f}%"],
        textposition="inside",
        name="Rejected"
    ))

    fig.update_layout(
        barmode="stack",
        height=170,
        xaxis=dict(
            range=[0, 100],
            title="Estimated Probability (%)",
            ticksuffix="%",
            showgrid=True
        ),
        yaxis=dict(
            title="",
            autorange="reversed"
        ),
        showlegend=False,
        margin=dict(l=20, r=20, t=15, b=45),
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )

    st.caption(
        "Note: These are model estimates, not guaranteed "
        "bank approval decisions or necessarily calibrated "
        "real-world approval probabilities."
    )






# ==========================================================
# 4. CONSTANTS
# ==========================================================

REQUIRED_FIELDS = [
    "no_of_dependents",
    "education",
    "self_employed",
    "income_annum",
    "loan_amount",
    "loan_term",
    "cibil_score",
    "residential_assets_value",
    "commercial_assets_value",
    "luxury_assets_value",
    "bank_asset_value"
]

QUICK_PROMPTS = [
    "What is EMI?",
    "How does CIBIL score work?",
    "What is loan foreclosure?",
    "How does loan tenure affect EMI?"
]


# ==========================================================
# 5. SESSION STATE INITIALIZATION
# ==========================================================

def initialize_session():

    if "manager" not in st.session_state:
        st.session_state.manager = LoanConversationManager()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "chat_started" not in st.session_state:
        st.session_state.chat_started = False

    if "last_error" not in st.session_state:
        st.session_state.last_error = None


try:
    initialize_session()

except Exception:
    logger.exception("Failed to initialize chatbot")

    st.error(
        "The chatbot could not be initialized. "
        "Please check the application configuration."
    )

    st.stop()


# ==========================================================
# 6. CHAT PROCESSING
# ==========================================================

def send_message(user_message):

    if not isinstance(user_message, str):
        return

    user_message = user_message.strip()

    if not user_message:
        return

    # Store user message

    st.session_state.messages.append({
        "role": "user",
        "content": user_message,
        "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M")
    })

    st.session_state.chat_started = True

    try:

        # Handle exit messages

        if user_message.lower() in ["exit", "quit", "bye"]:

            response = (
                "Thank you for using Loan Advisor AI! "
                "Feel free to start a new conversation whenever "
                "you need assistance."
            )

        else:

            response = st.session_state.manager.process_message(
                user_message
            )

        # Handle empty or unexpected response

        if response is None or not str(response).strip():

            response = (
                "I could not generate a response. "
                "Please try asking your question in another way."
            )

        response = str(response)

        st.session_state.last_error = None

    except Exception:

        # Avoid logging the user's financial message.

        logger.exception("Error while processing chatbot request")

        st.session_state.last_error = (
            "A temporary processing error occurred."
        )

        response = (
            "I'm sorry, I encountered a technical issue while "
            "processing your request. Your conversation is still "
            "available. Please try again."
        )

    # Store assistant response

    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M")
    })

    # Keep session history within a reasonable limit

    MAX_MESSAGES = 200

    if len(st.session_state.messages) > MAX_MESSAGES:

        st.session_state.messages = (
            st.session_state.messages[-MAX_MESSAGES:]
        )


# ==========================================================
# 7. RESET CONVERSATION
# ==========================================================

def reset_conversation():

    try:

        st.session_state.manager = LoanConversationManager()
        st.session_state.messages = []
        st.session_state.chat_started = False
        st.session_state.last_error = None

        logger.info("New conversation started")

    except Exception:

        logger.exception("Conversation reset failed")

        st.error(
            "Unable to start a new conversation. "
            "Please refresh the application."
        )

# ==========================================
# PREMIUM LOAN ADVISOR SIDEBAR
# ==========================================
from datetime import datetime

with st.sidebar:

    # -------------------------------------
    # 1. BRANDING
    # -------------------------------------

    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-logo">🏦</div>
        <div>
            <div class="sidebar-brand-name">
                Loan Advisor AI
            </div>
            <div class="sidebar-brand-subtitle">
                Intelligent Financial Assistance
            </div>
        </div>
    </div>
    <div class="sidebar-divider"></div>
    """, unsafe_allow_html=True)

    # -------------------------------------
    # 2. NEW CONVERSATION
    # -------------------------------------

    if st.button(
        "＋  New Conversation",
        key="sidebar_new_conversation",
        use_container_width=True
    ):
        st.session_state.manager = LoanConversationManager()
        st.session_state.messages = []
        st.session_state.chat_started = False
        st.rerun()

    # -------------------------------------
    # SIDEBAR ACTION HANDLER
    # -------------------------------------

    def sidebar_action(prompt):

        send_message(prompt)
        st.rerun()


    # -------------------------------------
    # 4. DASHBOARD
    # -------------------------------------

    if st.button(
        "🏠   Dashboard",
        key="sidebar_dashboard",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.session_state.chat_started = False
        st.rerun()

    # -------------------------------------
    # 5. LOAN ELIGIBILITY
    # -------------------------------------

    if st.button(
        "💰   Loan Eligibility",
        key="sidebar_eligibility",
        use_container_width=True
    ):
        sidebar_action("I want to check my loan eligibility")

    # -------------------------------------
    # 6. EMI CALCULATOR
    # -------------------------------------

    if st.button(
        "📊   EMI Calculator",
        key="sidebar_emi",
        use_container_width=True
    ):
        sidebar_action("Calculate EMI")

    # -------------------------------------
    # 7. CIBIL GUIDANCE
    # -------------------------------------

    if st.button(
        "🪪   CIBIL Guidance",
        key="sidebar_cibil",
        use_container_width=True
    ):
        sidebar_action("What is CIBIL score?")

    # -------------------------------------
    # 8. LOAN INFORMATION
    # -------------------------------------

    if st.button(
        "📚   Loan Information",
        key="sidebar_information",
        use_container_width=True
    ):
        sidebar_action("Tell me about different types of loans")

    st.markdown(
        '<div class="sidebar-divider"></div>',
        unsafe_allow_html=True
    )

    # -------------------------------------
    # 9. APPLICATION PROGRESS
    # -------------------------------------

    st.markdown(
        '<div class="sidebar-heading">APPLICATION PROGRESS</div>',
        unsafe_allow_html=True
    )

    applicant = st.session_state.manager.applicant

    total_fields = len(applicant)

    completed_fields = sum(
        value is not None
        for value in applicant.values()
    )

    progress = (
        completed_fields / total_fields
        if total_fields else 0
    )

    st.progress(progress)

    st.caption(
        f"{completed_fields} / {total_fields} details completed"
    )

    # -------------------------------------
    # 10. FOOTER
    # -------------------------------------

    st.markdown("""
    <div class="sidebar-divider"></div>

    <div class="sidebar-footer">
        🔒 Secure AI-powered assistance
        <br>
        <b>Loan Advisor AI</b>
        <br>
        Portfolio Project
    </div>
    """, unsafe_allow_html=True)

# with st.sidebar:

#     # BRANDING
#     st.markdown("""
#     <div class="sidebar-brand">
#         <div class="sidebar-logo">🏦</div>
#         <div>
#             <div class="sidebar-brand-name">
#                 Loan Advisor AI
#             </div>
#             <div class="sidebar-brand-subtitle">
#                 Intelligent Financial Assistance
#             </div>
#         </div>
#     </div>

#     <div class="sidebar-divider"></div>
#     """, unsafe_allow_html=True)

#     # NEW CONVERSATION
#     if st.button(
#         "＋  New Conversation",
#         use_container_width=True,
#         key="sidebar_new_conversation"
#     ):
#         st.session_state.manager = LoanConversationManager()
#         st.session_state.messages = []
#         st.session_state.chat_started = False
#         st.rerun()

#     st.markdown("""
#     <div class="sidebar-divider"></div>

#     <div class="sidebar-section-title">
#         MAIN MENU
#     </div>

#     <div class="sidebar-item">
#         <div class="sidebar-icon">🏠</div>
#         <div>
#             <div class="sidebar-item-title">Dashboard</div>
#             <div class="sidebar-item-description">
#                 Your loan assistant home
#             </div>
#         </div>
#     </div>

#     <div class="sidebar-item">
#         <div class="sidebar-icon">💰</div>
#         <div>
#             <div class="sidebar-item-title">Loan Eligibility</div>
#             <div class="sidebar-item-description">
#                 Check estimated eligibility
#             </div>
#         </div>
#     </div>

#     <div class="sidebar-item">
#         <div class="sidebar-icon">📊</div>
#         <div>
#             <div class="sidebar-item-title">EMI Calculator</div>
#             <div class="sidebar-item-description">
#                 Calculate monthly repayments
#             </div>
#         </div>
#     </div>

#     <div class="sidebar-item">
#         <div class="sidebar-icon">🪪</div>
#         <div>
#             <div class="sidebar-item-title">CIBIL Guidance</div>
#             <div class="sidebar-item-description">
#                 Understand your credit score
#             </div>
#         </div>
#     </div>

#     <div class="sidebar-item">
#         <div class="sidebar-icon">📚</div>
#         <div>
#             <div class="sidebar-item-title">Loan Information</div>
#             <div class="sidebar-item-description">
#                 Explore loans, fees and documents
#             </div>
#         </div>
#     </div>

#     <div class="sidebar-divider"></div>

#     <div class="sidebar-section-title">
#         APPLICATION PROGRESS
#     </div>
#     """, unsafe_allow_html=True)

#     # APPLICATION PROGRESS
#     applicant = st.session_state.manager.applicant

#     total_fields = len(applicant)

#     completed_fields = sum(
#         value is not None
#         for value in applicant.values()
#     )

#     progress = (
#         completed_fields / total_fields
#         if total_fields else 0
#     )

#     st.progress(progress)

#     st.markdown(
#         f"""
#         <div class="sidebar-progress-text">
#             {completed_fields} of {total_fields}
#             application details completed
#         </div>
#         """,
#         unsafe_allow_html=True
#     )

#     st.markdown("""
#     <div class="sidebar-divider"></div>

#     <div class="sidebar-footer">
#         🔒 AI-powered financial assistance
#         <br><br>
#         Loan Advisor AI · Portfolio Project
#     </div>
#     """, unsafe_allow_html=True)

# ==========================================================
# 9. HERO HEADER - PERMANENT HTML FIX
# ==========================================================

st.html("""
<div class="hero">
    <p class="hero-label">YOUR PERSONAL FINANCIAL ASSISTANT</p>

    <h1>Welcome to Loan Advisor AI 👋</h1>

    <p>
        Make informed borrowing decisions with intelligent
        loan eligibility estimates, EMI calculations and
        personalized loan guidance.
    </p>

    <div class="hero-tags">
        ✦ Machine Learning &nbsp;&nbsp;
        ✦ Natural Language Processing &nbsp;&nbsp;
        ✦ Smart Loan Assistance
    </div>
</div>
""")





# ==========================================================
# 10. WELCOME DASHBOARD
# ==========================================================
from textwrap import dedent

if not st.session_state.messages:

    st.subheader("How can I help you today?")

    st.write(
        "Select a service or start by typing your question below."
    )

    col1, col2 = st.columns(2)

    with col1:

       
        st.markdown(dedent("""
        <div class="feature-card">
            <h3>💰 Loan Eligibility</h3>
            <p>
                Share your financial information and receive
                an ML-based eligibility estimate.
            </p>
        </div>
        """), unsafe_allow_html=True)

        
        if st.button(
            "Check Loan Eligibility →",
            key="eligibility",
            use_container_width=True
        ):

            send_message(
                "I want to check my loan eligibility."
            )

            st.rerun()

    with col2:

        st.markdown(dedent("""
        <div class="feature-card">
            <h3>📊 EMI Calculator</h3>
            <p>
                Share your financial information and receive
                an ML-based eligibility estimate.
            </p>
        </div>
        """), unsafe_allow_html=True)

        if st.button(
            "Calculate My EMI →",
            key="emi",
            use_container_width=True
        ):

            send_message(
                "I want to calculate my loan EMI."
            )

            st.rerun()

    col3, col4 = st.columns(2)

    with col3:

        st.markdown(dedent("""
        <div class="feature-card">
            <h3>🪪 CIBIL Score</h3>
            <p>
                Share your financial information and receive
                an ML-based eligibility estimate.
            </p>
        </div>
        """), unsafe_allow_html=True)

        if st.button(
            "Understand CIBIL Score →",
            key="cibil",
            use_container_width=True
        ):

            send_message(
                "What is CIBIL score?"
            )

            st.rerun()

    with col4:

        st.markdown(dedent("""
        <div class="feature-card">
            <h3>💬 Loan Information</h3>
            <p>
                Share your financial information and receive
                an ML-based eligibility estimate.
            </p>
        </div>
        """), unsafe_allow_html=True)

        if st.button(
            "Explore Loan Information →",
            key="loan_info",
            use_container_width=True
        ):

            send_message(
                "Tell me about different types of loans."
            )

            st.rerun()

    st.divider()

    st.subheader("Popular Questions")

    suggestion_cols = st.columns(2)

    for index, suggestion in enumerate(QUICK_PROMPTS):

        with suggestion_cols[index % 2]:

            if st.button(
                suggestion,
                key=f"quick_prompt_{index}",
                use_container_width=True
            ):

                send_message(suggestion)
                st.rerun()



# ==========================================================
# 11. PROFESSIONAL CHAT HISTORY
# ==========================================================

if st.session_state.messages:

    st.markdown("### 💬 Your Conversation")

    st.caption(
        "Chat with your personal AI-powered loan assistant."
    )

    for index, message in enumerate(st.session_state.messages):

        role = message.get("role", "assistant")
        content = message.get("content", "")

        timestamp = message.get("timestamp", "")

        # --------------------------------------
        # USER MESSAGE - RIGHT SIDE
        # --------------------------------------

        if role == "user":

            left_space, right_message = st.columns([2, 3])

            with right_message:

                with st.container(
                    key=f"user_bubble_{index}"
                ):

                    st.markdown("**👤 You**")

                    st.markdown(content)

                    st.markdown(
                        f'<div class="chat-time">{timestamp} ✓✓</div>',
                        unsafe_allow_html=True
                    )

        # --------------------------------------
        # AI MESSAGE - LEFT SIDE
        # --------------------------------------

        else:

            left_message, right_space = st.columns([3, 2])

            with left_message:

                with st.container(
                    key=f"ai_bubble_{index}"
                ):

                    st.markdown("**🏦 Loan Advisor AI**")

                    st.markdown(content)

                    st.markdown(
                        f'<div class="chat-time">{timestamp}</div>',
                        unsafe_allow_html=True
                    )

                    # Keep probability chart support
                    if message.get("probabilities"):

                        show_prediction_chart(
                            probabilities=message["probabilities"],
                            prediction=message["prediction"]
                        )




# ==========================================================
# 12. CHAT INPUT
# ==========================================================

user_input = st.chat_input(
    "Ask about loans, EMI, eligibility or CIBIL score..."
)

if user_input:

    send_message(user_input)
    st.rerun()


# ==========================================================
# 13. FINANCIAL DISCLAIMER
# ==========================================================

st.divider()

st.html("""
<div class="footer">
    <strong>Loan Advisor AI</strong>

    <p>
        Powered by Machine Learning and Natural Language Processing.
    </p>

    <p>
        This application provides educational information and
        model-based estimates only. It does not guarantee loan
        approval, interest rates or actual lender decisions.
    </p>

    <p>
        Final loan eligibility and approval are determined
        by the respective financial institution.
    </p>
</div>
""")



# st.divider()

# st.markdown("""
# <div class="footer">

#     <strong>Loan Advisor AI</strong><br>

#     Powered by Machine Learning and Natural Language Processing.

#     <br><br>

#     This application provides educational information and
#     model-based estimates only. It does not guarantee loan
#     approval, interest rates or actual lender decisions.

#     <br>

#     Final loan eligibility and approval are determined
#     by the respective financial institution.

# </div>
# """, unsafe_allow_html=True)









# import sys
# from pathlib import Path
# from textwrap import dedent
# import streamlit as st

# # --------------------------------------------------
# # PROJECT IMPORT
# # --------------------------------------------------

# PROJECT_ROOT = Path(__file__).resolve().parent.parent
# sys.path.insert(0, str(PROJECT_ROOT))

# from src.conversation_manager import LoanConversationManager


# # --------------------------------------------------
# # PAGE CONFIGURATION
# # --------------------------------------------------

# st.set_page_config(
#     page_title="Loan Advisor AI",
#     page_icon="🏦",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )



# # --------------------------------------------------
# # PREMIUM FINTECH UI - CUSTOM CSS
# # --------------------------------------------------

# st.markdown("""
# <style>

# /* Main application background */

# .stApp {
#     background: linear-gradient(
#         135deg,
#         #EAF1F8 0%,
#         #F4F7FC 45%,
#         #E8F2F5 100%
#     );
#     color: #193047;
# }

# /* Main content width and spacing */

# .block-container {
#     max-width: 1250px;
#     padding-top: 2rem;
#     padding-bottom: 2rem;
# }

# /* Sidebar */

# [data-testid="stSidebar"] {
#     background: linear-gradient(
#         180deg,
#         #10243A 0%,
#         #173B55 100%
#     );
# }

# [data-testid="stSidebar"] * {
#     color: #F0F6FC;
# }

# [data-testid="stSidebar"] [data-testid="stProgressBar"] {
#     background-color: #35516A;
# }

# /* Hero banner */


# .hero {
#     background: linear-gradient(
#         120deg,
#         #10243A,
#         #14566C,
#         #147D87
#     ) !important;
#     padding: 42px 38px !important;
#     border-radius: 22px !important;
#     color: #FFFFFF !important;
#     margin-bottom: 30px !important;
#     box-shadow: 0 12px 30px rgba(16, 36, 58, 0.16);
# }

# .hero h1 {
#     color: #FFFFFF !important;
#     font-size: 34px !important;
# }

# .hero p {
#     color: #E0F0F4 !important;
#     font-size: 16px !important;
# }

# .hero .hero-label {
#     color: #65D6CB !important;
#     font-size: 13px !important;
#     font-weight: 700 !important;
#     letter-spacing: 2px !important;
# }

# .hero .hero-features {
#     color: #FFFFFF !important;
#     font-size: 13px !important;
#     margin-top: 22px !important;
# }


# /* Feature cards */

# .feature-card {
#     background: rgba(255, 255, 255, 0.94);
#     padding: 25px;
#     border-radius: 18px;
#     border: 1px solid #DCE7F0;
#     min-height: 155px;
#     margin-bottom: 15px;
#     box-shadow: 0 5px 18px rgba(35, 65, 90, 0.06);
#     transition: all 0.25s ease;
# }

# .feature-card:hover {
#     transform: translateY(-4px);
#     box-shadow: 0 12px 25px rgba(35, 65, 90, 0.12);
#     border-color: #56B8B1;
# }

# .feature-card h3 {
#     color: #173B55 !important;
#     font-size: 20px;
#     font-weight: 700;
# }

# .feature-card p {
#     color: #64788C !important;
#     font-size: 14px;
#     line-height: 1.6;
# }

# /* Section headings */

# h1, h2, h3 {
#     color: #173B55;
# }

# h2 {
#     font-weight: 700;
# }

# /* Buttons */

# div.stButton > button {
#     background: linear-gradient(
#         110deg,
#         #147D87,
#         #159A9A
#     );
#     color: white;
#     border: none;
#     border-radius: 11px;
#     min-height: 46px;
#     font-weight: 650;
#     transition: all 0.2s ease;
#     box-shadow: 0 4px 12px rgba(20, 125, 135, 0.12);
# }

# div.stButton > button:hover {
#     background: linear-gradient(
#         110deg,
#         #116874,
#         #117D87
#     );
#     color: white;
#     transform: translateY(-2px);
#     box-shadow: 0 7px 16px rgba(20, 125, 135, 0.22);
# }


# /* CHAT MESSAGE CONTAINER */

# [data-testid="stChatMessage"] {
#     background: #FFFFFF !important;
#     border: 1px solid #DCE6EF !important;
#     border-radius: 16px !important;
#     padding: 16px !important;
#     margin-bottom: 14px !important;
#     box-shadow: 0 4px 14px rgba(16, 36, 58, 0.07);
# }

# /* CHAT MESSAGE TEXT */

# [data-testid="stChatMessage"] p,
# [data-testid="stChatMessage"] li,
# [data-testid="stChatMessage"] span {
#     color: #193047 !important;
#     font-size: 15px !important;
#     line-height: 1.7 !important;
# }

# /* CHAT INPUT AREA */

# [data-testid="stChatInput"] {
#     background: #FFFFFF !important;
#     border: 2px solid #D5E3ED !important;
#     border-radius: 15px !important;
# }

# [data-testid="stChatInput"] textarea {
#     color: #193047 !important;
#     background: #FFFFFF !important;
#     font-size: 15px !important;
# }

# [data-testid="stChatInput"] textarea::placeholder {
#     color: #8193A5 !important;
# }

# /* CHAT INPUT FOCUS */

# [data-testid="stChatInput"]:focus-within {
#     border-color: #159A9A !important;
#     box-shadow: 0 0 0 3px rgba(21, 154, 154, 0.12);
# }

# /* Progress bar */

# [data-testid="stProgressBar"] > div > div {
#     background: linear-gradient(
#         90deg,
#         #147D87,
#         #55C8B5
#     );
#     border-radius: 20px;
# }

# /* Dividers */

# hr {
#     border-color: #D8E4ED;
# }

# /* Footer */

# .small-note {
#     color: #718397;
#     font-size: 13px;
# }

# /* Mobile responsiveness */

# @media (max-width: 768px) {

#     .block-container {
#         padding-left: 1rem;
#         padding-right: 1rem;
#     }

#     .hero {
#         padding: 26px 20px;
#     }

#     .hero h1 {
#         font-size: 27px;
#     }

#     .feature-card {
#         padding: 18px;
#         min-height: 140px;
#     }
# }

# </style>
# """, unsafe_allow_html=True)



# # --------------------------------------------------
# # SESSION STATE
# # --------------------------------------------------

# if "manager" not in st.session_state:
#     st.session_state.manager = LoanConversationManager()

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# if "chat_started" not in st.session_state:
#     st.session_state.chat_started = False


# # --------------------------------------------------
# # CHAT PROCESSING FUNCTION
# # --------------------------------------------------

# def send_message(user_message):

#     user_message = user_message.strip()

#     if not user_message:
#         return

#     st.session_state.chat_started = True

#     st.session_state.messages.append({
#         "role": "user",
#         "content": user_message
#     })

#     try:

#         if user_message.lower() in ["exit", "quit", "bye"]:

#             response = (
#                 "Thank you for using Loan Advisor AI! "
#                 "You can start a new conversation whenever you need."
#             )

#         else:

#             response = st.session_state.manager.process_message(
#                 user_message
#             )

#         response = str(response)

#     except Exception as error:

#         print("Chatbot error:", error)

#         response = (
#             "Sorry, something went wrong while processing "
#             "your request. Please try again."
#         )

#     st.session_state.messages.append({
#         "role": "assistant",
#         "content": response
#     })


# # --------------------------------------------------
# # SIDEBAR
# # --------------------------------------------------

# with st.sidebar:

#     st.markdown(
#         '<div class="sidebar-title">🏦 Loan Advisor AI</div>',
#         unsafe_allow_html=True
#     )

#     st.caption("Your intelligent loan assistant")

#     st.divider()

#     st.subheader("Quick Navigation")

#     if st.button(
#         "＋ New Conversation",
#         use_container_width=True
#     ):

#         st.session_state.manager = LoanConversationManager()
#         st.session_state.messages = []
#         st.session_state.chat_started = False
#         st.rerun()

#     st.divider()

#     st.subheader("What I can help with")

#     st.markdown("""
#     💰 **Loan Eligibility**

#     Estimate your loan eligibility using our ML model.

#     📊 **EMI Calculator**

#     Understand monthly instalments and repayment.

#     🪪 **CIBIL Score**

#     Learn about credit scores and their importance.

#     🏦 **Loan Information**

#     Get answers to common loan questions.
#     """)

#     st.divider()

#     st.subheader("Application Progress")

#     applicant = getattr(
#         st.session_state.manager,
#         "applicant",
#         {}
#     )

#     required_fields = [
#         "no_of_dependents",
#         "education",
#         "self_employed",
#         "income_annum",
#         "loan_amount",
#         "loan_term",
#         "cibil_score",
#         "residential_assets_value",
#         "commercial_assets_value",
#         "luxury_assets_value",
#         "bank_asset_value"
#     ]

#     completed = sum(
#         applicant.get(field) is not None
#         for field in required_fields
#     )

#     progress = completed / len(required_fields)

#     st.progress(progress)

#     st.caption(
#         f"{completed} of {len(required_fields)} details collected"
#     )

#     st.divider()

#     st.caption("🔒 Your chatbot provides estimates, not bank approvals.")





# # --------------------------------------------------
# # PREMIUM WELCOME HEADER
# # --------------------------------------------------

# hero_html = dedent("""
# <div class="hero">
#     <p class="hero-label">
#         YOUR PERSONAL FINANCIAL ASSISTANT
#     </p>

#     <h1>Welcome to Loan Advisor AI 👋</h1>

#     <p>
#         Make smarter borrowing decisions with intelligent
#         loan eligibility estimates, EMI calculations and
#         personalized loan guidance.
#     </p>

#     <div class="hero-features">
#         ✦ AI Powered &nbsp;&nbsp;
#         ✦ Smart Loan Assistance &nbsp;&nbsp;
#         ✦ Instant Guidance
#     </div>
# </div>
# """)

# st.html(hero_html)



# # --------------------------------------------------
# # WELCOME SCREEN
# # --------------------------------------------------

# if not st.session_state.chat_started:

#     st.subheader("How can I help you today?")

#     st.write(
#         "Choose a service below or type your question in the chat."
#     )

#     col1, col2 = st.columns(2)

#     with col1:

#         st.markdown("""
#         <div class="feature-card">
#             <h3>💰 Loan Eligibility</h3>
#             <p>
#                 Share your financial details and get an
#                 ML-based loan eligibility estimate.
#             </p>
#         </div>
#         """, unsafe_allow_html=True)

#         if st.button(
#             "Check Loan Eligibility →",
#             key="eligibility",
#             use_container_width=True
#         ):

#             send_message(
#                 "I want to check my loan eligibility."
#             )

#             st.rerun()

#     with col2:

#         st.markdown("""
#         <div class="feature-card">
#             <h3>📊 EMI Calculation</h3>
#             <p>
#                 Understand your monthly EMI, total interest
#                 and repayment amount.
#             </p>
#         </div>
#         """, unsafe_allow_html=True)

#         if st.button(
#             "Calculate My EMI →",
#             key="emi",
#             use_container_width=True
#         ):

#             send_message(
#                 "I want to calculate my loan EMI."
#             )

#             st.rerun()

#     col3, col4 = st.columns(2)

#     with col3:

#         st.markdown("""
#         <div class="feature-card">
#             <h3>🪪 CIBIL Score</h3>
#             <p>
#                 Understand CIBIL scores and how lenders
#                 may consider your credit history.
#             </p>
#         </div>
#         """, unsafe_allow_html=True)

#         if st.button(
#             "Understand CIBIL Score →",
#             key="cibil",
#             use_container_width=True
#         ):

#             send_message(
#                 "What is CIBIL score?"
#             )

#             st.rerun()

#     with col4:

#         st.markdown("""
#         <div class="feature-card">
#             <h3>💬 General Loan Queries</h3>
#             <p>
#                 Ask questions about interest rates,
#                 loan tenure and repayment.
#             </p>
#         </div>
#         """, unsafe_allow_html=True)

#         if st.button(
#             "Ask a Question →",
#             key="question",
#             use_container_width=True
#         ):

#             send_message(
#                 "Tell me about different types of loans."
#             )

#             st.rerun()


#     st.divider()

#     st.subheader("Try asking")

#     suggestions = [
#         "What is EMI?",
#         "How does CIBIL score work?",
#         "What is loan foreclosure?",
#         "How does loan tenure affect EMI?"
#     ]

#     suggestion_cols = st.columns(2)

#     for index, suggestion in enumerate(suggestions):

#         with suggestion_cols[index % 2]:

#             if st.button(
#                 suggestion,
#                 key=f"suggestion_{index}",
#                 use_container_width=True
#             ):

#                 send_message(suggestion)
#                 st.rerun()


# # --------------------------------------------------
# # CHAT HISTORY
# # --------------------------------------------------

# if st.session_state.chat_started:

#     st.subheader("Your Conversation")

#     for message in st.session_state.messages:

#         with st.chat_message(message["role"]):

#             st.markdown(message["content"])


# # --------------------------------------------------
# # CHAT INPUT
# # --------------------------------------------------

# user_input = st.chat_input(
#     "Type your message here..."
# )

# if user_input:

#     send_message(user_input)

#     st.rerun()


# # --------------------------------------------------
# # FOOTER
# # --------------------------------------------------

# st.divider()

# st.markdown(
#     """
#     <div style="text-align:center;color:#64748B;font-size:13px;">
#         Loan Advisor AI | Powered by Machine Learning and NLP
#         <br>
#         Educational estimates only. Final loan decisions are made by lenders.
#     </div>
#     """,
#     unsafe_allow_html=True
# )
