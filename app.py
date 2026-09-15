"""
=============================================================================
Minor Project 1: AI-Powered Resume Screening & ATS Optimizer
File: app.py
Author: B.Tech 3rd Year AI & ML Project
Description: Bulletproof file uploader dropzone contrast CSS override,
             interactive job role selector + custom input persistence,
             ultra-high contrast dark theme, and interactive ATS engine.
=============================================================================
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

from resume_parser import parse_resume_file, extract_contact_info, clean_text
from ats_matcher import compute_ats_score, calculate_semantic_similarity, calculate_tfidf_similarity
from skill_extractor import extract_skills_by_category, compare_skills
from recommendation_engine import generate_recommendations
from db_manager import save_evaluation, get_evaluation_history, clear_evaluation_history

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="ResumeAI Engine | Next-Gen ATS Optimizer",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# MAXIMUM CONTRAST FRONTEND CSS INJECTION
# -----------------------------------------------------------------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* Ambient Dark Background */
    .stApp {
        background: #030712;
        background-image: 
            radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.25) 0px, transparent 45%),
            radial-gradient(at 100% 0%, rgba(168, 85, 247, 0.22) 0px, transparent 45%),
            radial-gradient(at 50% 100%, rgba(236, 72, 153, 0.18) 0px, transparent 50%);
        background-attachment: fixed;
        color: #FFFFFF !important;
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: #030712; }
    ::-webkit-scrollbar-thumb { background: #334155; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #475569; }

    /* ==========================================================================
       LABEL & TEXT AREA HIGH CONTRAST FIXES (BRIGHT WHITE & NEON)
       ========================================================================== */
    label, p, span, small, div {
        color: #FFFFFF !important;
    }

    /* Text Area & Input Labels */
    div[data-testid="stTextArea"] label, 
    div[data-testid="stTextInput"] label,
    div[data-testid="stFileUploader"] label,
    div[data-testid="stSelectbox"] label,
    div[data-baseweb="select"] label {
        color: #FFFFFF !important;
        font-size: 1.05rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.01em !important;
        margin-bottom: 8px !important;
    }

    /* Text Area & Input Fields */
    .stTextArea textarea, .stTextInput input {
        background: rgba(15, 23, 42, 0.95) !important;
        border: 2px solid rgba(255, 255, 255, 0.25) !important;
        border-radius: 14px !important;
        color: #FFFFFF !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        backdrop-filter: blur(20px);
        transition: all 0.25s ease-in-out !important;
        box-shadow: 0 6px 25px rgba(0, 0, 0, 0.4);
    }

    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #A855F7 !important;
        box-shadow: 0 0 30px rgba(168, 85, 247, 0.5) !important;
    }

    .stTextArea textarea::placeholder, .stTextInput input::placeholder {
        color: #94A3B8 !important;
        opacity: 1 !important;
    }

    /* ==========================================================================
       JOB ROLE SELECTBOX & BASEWEB DROPDOWN HIGH CONTRAST OVERRIDE
       ========================================================================== */
    div[data-testid="stSelectbox"] {
        margin-bottom: 20px !important;
    }

    /* Main Select Input Box */
    div[data-baseweb="select"] {
        background-color: #0F172A !important;
        border-radius: 14px !important;
    }

    div[data-baseweb="select"] > div {
        background-color: #0F172A !important;
        border: 2px solid rgba(255, 255, 255, 0.25) !important;
        border-radius: 14px !important;
        color: #FFFFFF !important;
        font-weight: 800 !important;
        box-shadow: 0 6px 25px rgba(0, 0, 0, 0.4) !important;
    }

    div[data-baseweb="select"] > div:hover {
        border-color: #A855F7 !important;
        box-shadow: 0 0 25px rgba(168, 85, 247, 0.4) !important;
    }

    div[data-baseweb="select"] * {
        color: #FFFFFF !important;
        font-weight: 800 !important;
        background-color: transparent !important;
    }

    div[data-baseweb="select"] svg {
        fill: #FFFFFF !important;
        color: #FFFFFF !important;
    }

    /* Floating Dropdown Popover & Options Menu (FORCE TRANSPARENT INNER DIVS & WHITE TEXT) */
    div[data-baseweb="popover"],
    div[data-baseweb="menu"],
    ul[role="listbox"],
    div[role="listbox"] {
        background-color: #0F172A !important;
        border: 2px solid #818CF8 !important;
        border-radius: 14px !important;
        box-shadow: 0 16px 45px rgba(0, 0, 0, 0.9) !important;
        overflow: hidden !important;
    }

    /* Force all child elements inside popover menu (nested divs, spans) to be transparent with white text */
    div[data-baseweb="popover"] *,
    div[data-baseweb="menu"] *,
    ul[role="listbox"] *,
    div[role="listbox"] * {
        background-color: transparent !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 0.98rem !important;
        opacity: 1 !important;
    }

    /* Individual List Options */
    ul[role="listbox"] li,
    div[role="listbox"] li,
    div[data-baseweb="menu"] li,
    div[data-baseweb="menu"] [role="option"],
    li[role="option"],
    div[role="option"],
    [data-baseweb="option"] {
        background-color: #0F172A !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 0.98rem !important;
        padding: 12px 18px !important;
        margin: 2px 0 !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
    }

    /* Hover & Active / Selected Option State */
    ul[role="listbox"] li:hover,
    ul[role="listbox"] li[aria-selected="true"],
    div[data-baseweb="menu"] li:hover,
    div[data-baseweb="menu"] [role="option"]:hover,
    div[data-baseweb="menu"] [aria-selected="true"],
    li[role="option"]:hover,
    li[role="option"][aria-selected="true"],
    div[role="option"]:hover,
    div[role="option"][aria-selected="true"],
    [data-baseweb="option"]:hover {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%) !important;
        color: #FFFFFF !important;
    }

    ul[role="listbox"] li:hover *,
    li[role="option"]:hover *,
    div[role="option"]:hover *,
    div[data-baseweb="menu"] [role="option"]:hover * {
        background-color: transparent !important;
        color: #FFFFFF !important;
    }

    /* ==========================================================================
       BULLETPROOF FILE UPLOADER DROPZONE & SUBMIT BOX CONTRAST OVERRIDE
       ========================================================================== */
    div[data-testid="stFileUploader"],
    section[data-testid="stFileUploader"] {
        margin-bottom: 24px !important;
    }

    div[data-testid="stFileUploader"] label,
    section[data-testid="stFileUploader"] label {
        color: #FFFFFF !important;
        font-size: 1.05rem !important;
        font-weight: 800 !important;
        margin-bottom: 10px !important;
        display: block !important;
    }

    /* Outer Dropzone Container */
    div[data-testid="stFileUploaderDropzone"],
    section[data-testid="stFileUploaderDropzone"] {
        background-color: #0F172A !important;
        border: 2px dashed #818CF8 !important;
        border-radius: 16px !important;
        padding: 26px 20px !important;
        text-align: center !important;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.45) !important;
        transition: all 0.3s ease !important;
    }

    div[data-testid="stFileUploaderDropzone"]:hover,
    section[data-testid="stFileUploaderDropzone"]:hover {
        border-color: #EC4899 !important;
        background-color: #1E1B4B !important;
        box-shadow: 0 0 30px rgba(236, 72, 153, 0.45) !important;
    }

    /* Target all text elements inside file uploader dropzone */
    div[data-testid="stFileUploader"] *,
    div[data-testid="stFileUploaderDropzone"] *,
    section[data-testid="stFileUploaderDropzone"] *,
    div[data-testid="stFileUploaderDropzoneInstructions"] *,
    div[data-testid="stFileUploaderDropzoneInstructions"] div,
    div[data-testid="stFileUploaderDropzoneInstructions"] span,
    div[data-testid="stFileUploaderDropzoneInstructions"] p,
    div[data-testid="stFileUploaderDropzoneInstructions"] small {
        color: #FFFFFF !important;
        font-size: 0.98rem !important;
        font-weight: 700 !important;
        opacity: 1 !important;
        visibility: visible !important;
    }

    /* Small info subtext (Limit 200MB per file...) */
    div[data-testid="stFileUploaderDropzoneInstructions"] small,
    section[data-testid="stFileUploaderDropzone"] small {
        color: #CBD5E1 !important;
        font-size: 0.88rem !important;
        font-weight: 600 !important;
        margin-top: 6px !important;
        display: block !important;
    }

    /* Browse files button inside dropzone */
    div[data-testid="stFileUploaderDropzone"] button,
    section[data-testid="stFileUploaderDropzone"] button,
    div[data-testid="stFileUploader"] button[data-testid="baseButton-secondary"] {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%) !important;
        color: #FFFFFF !important;
        border: 1.5px solid #A855F7 !important;
        font-weight: 800 !important;
        border-radius: 12px !important;
        padding: 10px 22px !important;
        box-shadow: 0 4px 20px rgba(124, 58, 237, 0.5) !important;
        margin-top: 10px !important;
    }

    div[data-testid="stFileUploaderDropzone"] button *,
    section[data-testid="stFileUploaderDropzone"] button * {
        color: #FFFFFF !important;
        font-weight: 800 !important;
    }

    div[data-testid="stFileUploaderDropzone"] button:hover,
    section[data-testid="stFileUploaderDropzone"] button:hover {
        background: linear-gradient(135deg, #6366F1 0%, #EC4899 100%) !important;
        border-color: #F472B6 !important;
        transform: scale(1.04) !important;
    }

    /* Attached File Item Container Card (when file is uploaded) */
    div[data-testid="stFileUploaderFileData"],
    section[data-testid="stFileUploaderFileData"],
    div[data-testid="stUploadedFile"] {
        background-color: #1E293B !important;
        border: 1.5px solid #818CF8 !important;
        border-radius: 12px !important;
        padding: 12px 18px !important;
        margin-top: 12px !important;
    }

    div[data-testid="stFileUploaderFileData"] *,
    section[data-testid="stFileUploaderFileData"] *,
    div[data-testid="stUploadedFile"] * {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }

    /* Delete / Remove icon button on uploaded file */
    div[data-testid="stFileUploaderDeleteBtn"] button,
    button[aria-label="Remove file"] {
        background: rgba(239, 68, 68, 0.25) !important;
        border: 1.5px solid #EF4444 !important;
        border-radius: 8px !important;
    }

    div[data-testid="stFileUploaderDeleteBtn"] button *,
    button[aria-label="Remove file"] * {
        color: #FCA5A5 !important;
    }

    div[data-testid="stFileUploaderDeleteBtn"] button:hover,
    button[aria-label="Remove file"]:hover {
        background: rgba(239, 68, 68, 0.6) !important;
    }

    div[data-testid="stFileUploaderDeleteBtn"] button:hover *,
    button[aria-label="Remove file"]:hover * {
        color: #FFFFFF !important;
    }

    /* ==========================================================================
       SIDEBAR HIGH CONTRAST & NEON CARDS
       ========================================================================== */
    [data-testid="stSidebar"] {
        background-color: #030712 !important;
        border-right: 1.5px solid rgba(255, 255, 255, 0.14) !important;
    }

    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }

    div[data-testid="stRadio"] > label {
        font-size: 1.05rem !important;
        color: #FFFFFF !important;
        font-weight: 800 !important;
        margin-bottom: 12px !important;
    }

    div[data-testid="stRadio"] div[role="radiogroup"] > label {
        background: rgba(15, 23, 42, 0.95) !important;
        border: 1.5px solid rgba(255, 255, 255, 0.18) !important;
        border-radius: 14px !important;
        padding: 14px 20px !important;
        margin-bottom: 10px !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 0.98rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3) !important;
    }

    div[data-testid="stRadio"] div[role="radiogroup"] > label:hover {
        background: rgba(99, 102, 241, 0.3) !important;
        border-color: #818CF8 !important;
        color: #FFFFFF !important;
        transform: translateX(6px) !important;
    }

    div[data-testid="stRadio"] div[role="radiogroup"] label[aria-checked="true"],
    div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 50%, #D946EF 100%) !important;
        border-color: #E879F9 !important;
        color: #FFFFFF !important;
        font-weight: 800 !important;
        box-shadow: 0 6px 30px rgba(124, 58, 237, 0.6) !important;
    }

    /* Primary Action Button */
    .stButton>button[kind="primary"], .stButton>button {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 50%, #D946EF 100%) !important;
        color: #FFFFFF !important;
        font-weight: 800 !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 16px 32px !important;
        font-size: 1.05rem !important;
        box-shadow: 0 6px 30px rgba(124, 58, 237, 0.55) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    .stButton>button:hover {
        transform: translateY(-3px) scale(1.01) !important;
        box-shadow: 0 12px 40px rgba(124, 58, 237, 0.8) !important;
    }

    /* Hero Component */
    .hero-wrapper { padding: 10px 0 15px 0; }
    .hero-status-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 6px 18px;
        border-radius: 30px;
        background: rgba(99, 102, 241, 0.15);
        border: 1.5px solid rgba(99, 102, 241, 0.4);
        color: #C7D2FE;
        font-size: 0.85rem;
        font-weight: 700;
        margin-bottom: 12px;
    }
    .pulse-dot {
        width: 10px;
        height: 10px;
        background-color: #10B981;
        border-radius: 50%;
        box-shadow: 0 0 14px #10B981;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.8); }
        70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }
    .hero-heading {
        font-size: 3.4rem;
        font-weight: 800;
        line-height: 1.12;
        background: linear-gradient(135deg, #FFFFFF 15%, #A5B4FC 50%, #F472B6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.035em;
        margin-bottom: 6px;
    }
    .hero-sub {
        font-size: 1.15rem;
        color: #CBD5E1;
        font-weight: 500;
        margin-bottom: 24px;
    }

    /* Executive Glass Metric Cards */
    .sexiest-card {
        background: rgba(15, 23, 42, 0.88);
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border: 1.5px solid rgba(255, 255, 255, 0.16);
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.45);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 15px;
    }
    .sexiest-card:hover {
        border-color: rgba(168, 85, 247, 0.6);
        transform: translateY(-5px);
        box-shadow: 0 25px 65px rgba(124, 58, 237, 0.35);
    }
    .card-label {
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #CBD5E1;
        font-weight: 700;
        margin-bottom: 8px;
    }
    .card-big-number {
        font-size: 2.9rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        line-height: 1;
    }
    .grad-cyan { color: #38BDF8; text-shadow: 0 0 20px rgba(56, 189, 248, 0.3); }
    .grad-indigo { color: #818CF8; text-shadow: 0 0 20px rgba(129, 140, 248, 0.3); }
    .grad-emerald { color: #34D399; text-shadow: 0 0 20px rgba(52, 211, 153, 0.3); }
    .grad-pink { color: #F472B6; text-shadow: 0 0 20px rgba(244, 114, 182, 0.3); }

    /* Interactive Skill Badges */
    .badge-matched {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(16, 185, 129, 0.2);
        border: 1.5px solid #10B981;
        color: #34D399;
        font-size: 0.9rem;
        font-weight: 700;
        padding: 8px 18px;
        border-radius: 30px;
        margin: 5px;
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.3);
        transition: all 0.25s ease;
    }
    .badge-matched:hover {
        background: rgba(16, 185, 129, 0.35);
        transform: scale(1.06);
    }

    .badge-missing {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(239, 68, 68, 0.2);
        border: 1.5px solid #EF4444;
        color: #FCA5A5;
        font-size: 0.9rem;
        font-weight: 700;
        padding: 8px 18px;
        border-radius: 30px;
        margin: 5px;
        box-shadow: 0 0 15px rgba(239, 68, 68, 0.3);
        transition: all 0.25s ease;
    }
    .badge-missing:hover {
        background: rgba(239, 68, 68, 0.35);
        transform: scale(1.06);
    }

    /* Contact Audit Executive Glass Card */
    .contact-audit-box {
        background: rgba(15, 23, 42, 0.95) !important;
        border: 1.5px solid rgba(129, 140, 248, 0.35) !important;
        border-radius: 18px !important;
        padding: 20px 24px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.45) !important;
    }
    .contact-field-row {
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        gap: 14px !important;
        padding: 12px 0 !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    .contact-field-row:last-child {
        border-bottom: none !important;
    }
    .contact-field-icon {
        font-size: 1.3rem !important;
        display: inline-block !important;
    }
    .contact-field-label {
        color: #818CF8 !important;
        font-weight: 800 !important;
        font-size: 1rem !important;
        min-width: 90px !important;
    }
    .contact-field-val {
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 0.98rem !important;
        word-break: break-all !important;
        background: rgba(99, 102, 241, 0.15) !important;
        padding: 4px 12px !important;
        border-radius: 8px !important;
        border: 1px solid rgba(99, 102, 241, 0.3) !important;
    }
    .contact-val-missing {
        color: #94A3B8 !important;
        font-style: italic !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
        background: rgba(255, 255, 255, 0.05) !important;
        padding: 4px 12px !important;
        border-radius: 8px !important;
    }

    /* Streamlit JSON Tree View High Contrast Override */
    div[data-testid="stJson"],
    div.stJson {
        background-color: #0F172A !important;
        border: 1.5px solid rgba(129, 140, 248, 0.35) !important;
        border-radius: 14px !important;
        padding: 18px !important;
    }
    .section-header {
        font-size: 1.4rem;
        font-weight: 800;
        color: #FFFFFF;
        margin-top: 15px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    </style>
""", unsafe_allow_html=True)


def load_sample_file(path: str) -> str:
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""


def main():
    # Hero Title Component
    st.markdown("""
        <div class="hero-wrapper">
            <div class="hero-status-pill">
                <span class="pulse-dot"></span> SBERT & TF-IDF NLP Engine Active • Latency: 12ms
            </div>
            <div class="hero-heading">ResumeAI ATS Engine</div>
            <div class="hero-sub">AI-Powered Resume Screening & Multi-Domain Skill Optimizer • Minor Project 1</div>
        </div>
    """, unsafe_allow_html=True)

    # -----------------------------------------------------------------------------
    # SIDEBAR CONTROLS WITH HIGH-CONTRAST NAVIGATION
    # -----------------------------------------------------------------------------
    st.sidebar.markdown("### ⚡ Navigation Panel")
    mode = st.sidebar.radio(
        "Select Application View",
        ["🎯 Single Resume Evaluation", "🏆 Batch Candidate Ranking", "📊 Evaluation History & Logs"]
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎛️ Dynamic Scoring Weights")
    st.sidebar.caption("Tweak weightages to adjust ATS formula live:")
    w_semantic = st.sidebar.slider("SBERT Semantic Weight (%)", 10, 80, 45, 5)
    w_skill = st.sidebar.slider("Skill Coverage Weight (%)", 10, 80, 35, 5)
    w_tfidf = st.sidebar.slider("TF-IDF Keyword Weight (%)", 5, 50, 20, 5)

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🚀 Preset Demo Data")
    if st.sidebar.button("Load ML Engineer Preset Data", use_container_width=True):
        st.session_state["sample_loaded"] = True

    # Sample Data Paths
    sample_jd_path = os.path.join("sample_data", "sample_jd_ml.txt")
    sample_resume_path = os.path.join("sample_data", "sample_resume_ml.txt")
    sample_jd_text = load_sample_file(sample_jd_path)
    sample_resume_text = load_sample_file(sample_resume_path)

    # Normalize weights to sum to 1.0
    total_w = w_semantic + w_skill + w_tfidf
    w_sem_norm = w_semantic / total_w
    w_skill_norm = w_skill / total_w
    w_tfidf_norm = w_tfidf / total_w

    # -----------------------------------------------------------------------------
    # MODE 1: SINGLE RESUME EVALUATION
    # -----------------------------------------------------------------------------
    if "Single Resume Evaluation" in mode:
        st.markdown('<div class="section-header">📥 Input Candidate Resume & Job Requirements</div>', unsafe_allow_html=True)
        col_input1, col_input2 = st.columns(2)

        with col_input1:
            uploaded_file = st.file_uploader("Upload Resume File (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])
            resume_text = ""
            candidate_name = "Candidate Resume"

            if uploaded_file is not None:
                file_bytes = uploaded_file.read()
                candidate_name = uploaded_file.name
                try:
                    resume_text = parse_resume_file(uploaded_file.name, file_bytes)
                    st.success(f"Loaded {uploaded_file.name} ({len(resume_text)} characters)")
                except Exception as e:
                    st.error(f"Error parsing file: {e}")
            elif st.session_state.get("sample_loaded", False):
                resume_text = sample_resume_text
                st.info("Preset ML Candidate Resume Loaded")
            else:
                resume_text = st.text_area("Or paste raw resume text:", height=200, placeholder="Paste candidate resume text...")

        with col_input2:
            if st.session_state.get("sample_loaded", False):
                jd_text = st.text_area("Target Job Description (JD):", value=sample_jd_text, height=275)
            else:
                jd_text = st.text_area("Paste Target Job Description (JD):", height=275, placeholder="Paste job requirements...")

        # Dynamic Job Role Selector + Custom Write-In Input
        role_preset_options = [
            "Machine Learning Engineer",
            "Data Scientist",
            "Full Stack Developer",
            "Software Engineer",
            "Data Engineer",
            "DevOps Engineer",
            "Custom Role / Write-In..."
        ]

        selected_role_preset = st.selectbox("Select or Customize Target Job Role:", role_preset_options, index=0)

        if selected_role_preset == "Custom Role / Write-In...":
            jd_title = st.text_input("Enter Custom Job Role Title:", value="AI Researcher", key="custom_role_input")
        else:
            jd_title = selected_role_preset

        st.markdown("---")

        if st.button("✨ Run Deep AI Analysis & Match", type="primary", use_container_width=True):
            if not resume_text.strip() or not jd_text.strip():
                st.warning("Please provide both a Resume and a Job Description.")
                return

            with st.spinner("Executing SBERT vector embeddings & NLP taxonomy match..."):
                # Compute individual scores
                tfidf_score = calculate_tfidf_similarity(resume_text, jd_text)
                semantic_score = calculate_semantic_similarity(resume_text, jd_text)
                skill_analysis = compare_skills(resume_text, jd_text)
                skill_score = skill_analysis["skill_coverage_pct"]

                # Apply dynamic slider weight formula
                custom_ats_score = (w_sem_norm * semantic_score) + (w_skill_norm * skill_score) + (w_tfidf_norm * tfidf_score)
                custom_ats_score = round(max(0.0, min(100.0, custom_ats_score)), 1)

                if custom_ats_score >= 80:
                    match_grade = "Exceptional Fit"
                elif custom_ats_score >= 65:
                    match_grade = "Strong Fit"
                elif custom_ats_score >= 50:
                    match_grade = "Moderate Fit"
                else:
                    match_grade = "Low Fit / High Risk"

                results = {
                    "final_ats_score": custom_ats_score,
                    "semantic_similarity_pct": semantic_score,
                    "skill_coverage_pct": skill_score,
                    "tfidf_similarity_pct": tfidf_score,
                    "match_grade": match_grade,
                    "skill_analysis": skill_analysis,
                    "resume_skill_breakdown": extract_skills_by_category(resume_text),
                    "jd_skill_breakdown": extract_skills_by_category(jd_text)
                }

                contact_info = extract_contact_info(resume_text)
                recommendations = generate_recommendations(results, resume_text, contact_info)
                save_evaluation(candidate_name, jd_title, results)

            # Results Section
            st.markdown('<div class="section-header">⚡ Live Match Intelligence & Score Analytics</div>', unsafe_allow_html=True)

            # Executive Metric Cards
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.markdown(f"""
                    <div class="sexiest-card">
                        <div class="card-label">Custom ATS Score</div>
                        <div class="card-big-number grad-emerald">{results['final_ats_score']}%</div>
                        <div style="color: #CBD5E1; font-size: 0.88rem; margin-top: 8px;">Role: <b style="color: #E2E8F0;">{jd_title}</b></div>
                        <div style="color: #CBD5E1; font-size: 0.88rem;">Grade: <b style="color: #34D399;">{results['match_grade']}</b></div>
                    </div>
                """, unsafe_allow_html=True)

            with m2:
                st.markdown(f"""
                    <div class="sexiest-card">
                        <div class="card-label">SBERT Semantic Match</div>
                        <div class="card-big-number grad-indigo">{results['semantic_similarity_pct']}%</div>
                        <div style="color: #CBD5E1; font-size: 0.88rem; margin-top: 8px;">Weight: {int(w_semantic)}%</div>
                    </div>
                """, unsafe_allow_html=True)

            with m3:
                st.markdown(f"""
                    <div class="sexiest-card">
                        <div class="card-label">Skill Coverage</div>
                        <div class="card-big-number grad-cyan">{results['skill_coverage_pct']}%</div>
                        <div style="color: #CBD5E1; font-size: 0.88rem; margin-top: 8px;">Weight: {int(w_skill)}%</div>
                    </div>
                """, unsafe_allow_html=True)

            with m4:
                st.markdown(f"""
                    <div class="sexiest-card">
                        <div class="card-label">TF-IDF Similarity</div>
                        <div class="card-big-number grad-pink">{results['tfidf_similarity_pct']}%</div>
                        <div style="color: #CBD5E1; font-size: 0.88rem; margin-top: 8px;">Weight: {int(w_tfidf)}%</div>
                    </div>
                """, unsafe_allow_html=True)

            st.write("")

            # Visual Radar & Skill Badges
            col_chart, col_details = st.columns([1.3, 1])

            with col_chart:
                st.markdown('<div class="section-header">🕸️ Multi-Domain Skill Radar</div>', unsafe_allow_html=True)
                res_cats = results["resume_skill_breakdown"]
                jd_cats = results["jd_skill_breakdown"]

                categories = list(jd_cats.keys())
                jd_counts = [len(jd_cats[cat]) for cat in categories]
                res_counts = [len(res_cats[cat]) for cat in categories]

                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(
                    r=res_counts, theta=categories, fill='toself', name='Candidate Resume',
                    fillcolor='rgba(99, 102, 241, 0.45)', line=dict(color='#818CF8', width=3)
                ))
                fig.add_trace(go.Scatterpolar(
                    r=jd_counts, theta=categories, fill='toself', name='Job Description',
                    fillcolor='rgba(236, 72, 153, 0.25)', line=dict(color='#EC4899', width=3, dash='dash')
                ))
                fig.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    polar=dict(radialaxis=dict(visible=True, range=[0, max(max(jd_counts + [1]), max(res_counts + [1]))])),
                    showlegend=True,
                    height=420,
                    margin=dict(l=40, r=40, t=30, b=30)
                )
                st.plotly_chart(fig, use_container_width=True)

            with col_details:
                st.markdown('<div class="section-header">👤 Contact Audit</div>', unsafe_allow_html=True)
                
                email_val = contact_info.get("email", "Not Found")
                phone_val = contact_info.get("phone", "Not Found")
                linkedin_val = contact_info.get("linkedin", "Not Found")
                github_val = contact_info.get("github", "Not Found")

                contact_card_html = f"""
                    <div class="contact-audit-box">
                        <div class="contact-field-row">
                            <span class="contact-field-icon">📧</span>
                            <span class="contact-field-label">Email:</span>
                            <span class="{'contact-field-val' if email_val != 'Not Found' else 'contact-val-missing'}">{email_val}</span>
                        </div>
                        <div class="contact-field-row">
                            <span class="contact-field-icon">📱</span>
                            <span class="contact-field-label">Phone:</span>
                            <span class="{'contact-field-val' if phone_val != 'Not Found' else 'contact-val-missing'}">{phone_val}</span>
                        </div>
                        <div class="contact-field-row">
                            <span class="contact-field-icon">💼</span>
                            <span class="contact-field-label">LinkedIn:</span>
                            <span class="{'contact-field-val' if linkedin_val != 'Not Found' else 'contact-val-missing'}">{linkedin_val}</span>
                        </div>
                        <div class="contact-field-row">
                            <span class="contact-field-icon">🐙</span>
                            <span class="contact-field-label">GitHub:</span>
                            <span class="{'contact-field-val' if github_val != 'Not Found' else 'contact-val-missing'}">{github_val}</span>
                        </div>
                    </div>
                """
                st.markdown(contact_card_html, unsafe_allow_html=True)

                st.markdown('<div class="section-header">🏷️ Skill Gap Breakdown</div>', unsafe_allow_html=True)
                matched = results["skill_analysis"]["matched_skills"]
                missing = results["skill_analysis"]["missing_skills"]

                st.write("**Matched Competencies:**")
                if matched:
                    badges_html = "".join([f'<span class="badge-matched">✓ {s}</span>' for s in matched])
                    st.markdown(badges_html, unsafe_allow_html=True)
                else:
                    st.write("No exact skills matched.")

                st.write("")
                st.write("**Missing Critical Keywords:**")
                if missing:
                    badges_missing_html = "".join([f'<span class="badge-missing">✗ {s}</span>' for s in missing])
                    st.markdown(badges_missing_html, unsafe_allow_html=True)
                else:
                    st.success("No missing critical keywords!")

            st.markdown("---")
            st.markdown('<div class="section-header">💡 AI Recommendations & ATS Formatting Audit</div>', unsafe_allow_html=True)
            st.info(recommendations["summary_advice"])

            for rec in recommendations["recommendations"]:
                st.warning(f"**[{rec['category']}] (Priority: {rec['priority']})**: {rec['message']}")

            for warn in recommendations["formatting_warnings"]:
                st.error(f"**[Format Warning]**: {warn}")

    # -----------------------------------------------------------------------------
    # MODE 2: BATCH CANDIDATE RANKING
    # -----------------------------------------------------------------------------
    elif "Batch Candidate Ranking" in mode:
        st.markdown('<div class="section-header">👥 Batch Candidate Resume Leaderboard</div>', unsafe_allow_html=True)
        st.write("Upload multiple candidate resumes to rank them against a single target Job Description.")

        target_jd = st.text_area("Target Job Description (JD):", value=sample_jd_text if st.session_state.get("sample_loaded", False) else "", height=150)
        uploaded_files = st.file_uploader("Upload Resumes (Multiple PDF/DOCX files)", type=["pdf", "docx", "txt"], accept_multiple_files=True)

        if st.button("✨ Rank All Candidates Now", type="primary", use_container_width=True):
            if not target_jd.strip() or not uploaded_files:
                st.warning("Please provide a Job Description and at least one Resume file.")
                return

            results_list = []
            progress_bar = st.progress(0)

            for idx, file in enumerate(uploaded_files):
                file_bytes = file.read()
                r_text = parse_resume_file(file.name, file_bytes)
                eval_res = compute_ats_score(r_text, target_jd)

                results_list.append({
                    "Rank": 0,
                    "Candidate File": file.name,
                    "ATS Score (%)": eval_res["final_ats_score"],
                    "Match Grade": eval_res["match_grade"],
                    "Semantic Score (%)": eval_res["semantic_similarity_pct"],
                    "Skill Coverage (%)": eval_res["skill_coverage_pct"],
                    "Matched Skills": len(eval_res["skill_analysis"]["matched_skills"]),
                    "Missing Skills": len(eval_res["skill_analysis"]["missing_skills"])
                })
                progress_bar.progress((idx + 1) / len(uploaded_files))

            df_results = pd.DataFrame(results_list).sort_values(by="ATS Score (%)", ascending=False)
            df_results["Rank"] = range(1, len(df_results) + 1)

            st.markdown("### 🏆 Candidate Leaderboard")
            st.dataframe(df_results, use_container_width=True)

            fig_bar = px.bar(
                df_results, x="Candidate File", y="ATS Score (%)", color="Match Grade",
                title="Candidate Match Leaderboard", text_auto=True, template="plotly_dark"
            )
            fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_bar, use_container_width=True)

    # -----------------------------------------------------------------------------
    # MODE 3: EVALUATION HISTORY & LOGS
    # -----------------------------------------------------------------------------
    elif "Evaluation History & Logs" in mode:
        st.markdown('<div class="section-header">📜 Audit History & Database Logs</div>', unsafe_allow_html=True)
        
        col_hist_title, col_hist_btn = st.columns([3, 1])
        with col_hist_btn:
            if st.button("🗑️ Clear Evaluation History", use_container_width=True):
                clear_evaluation_history()
                st.success("Evaluation history cleared successfully!")
                st.rerun()

        df_hist = get_evaluation_history()

        if df_hist.empty:
            st.info("No evaluations logged yet. Run a single or batch evaluation to populate history.")
        else:
            st.dataframe(df_hist, use_container_width=True)

            st.markdown("### 📈 Evaluation Score Distribution")
            fig_hist = px.histogram(
                df_hist, x="ats_score", nbins=10, title="Distribution of Evaluated ATS Scores",
                labels={"ats_score": "ATS Match Score (%)"}, template="plotly_dark", color_discrete_sequence=["#818CF8"]
            )
            fig_hist.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_hist, use_container_width=True)


if __name__ == "__main__":
    main()
