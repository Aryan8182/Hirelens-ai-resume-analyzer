"""
=============================================================================
Minor Project 1: AI-Powered Resume Screening & ATS Optimizer
File: app.py
Author: B.Tech 3rd Year AI & ML Project
Description: Ultra-modern Vercel/Linear-inspired dark glassmorphism frontend
             with ambient neon glow, Plotly charts, and ATS analysis.
=============================================================================
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

from resume_parser import parse_resume_file, extract_contact_info, clean_text
from ats_matcher import compute_ats_score
from skill_extractor import extract_skills_by_category
from recommendation_engine import generate_recommendations
from db_manager import save_evaluation, get_evaluation_history

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
# ULTRA-PREMIUM FRONTEND STYLING (VERCEL / LINEAR AI AESTHETIC)
# -----------------------------------------------------------------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&family=JetBrains+Mono:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* Ambient Gradient Mesh Background */
    .stApp {
        background: #030712;
        background-image: 
            radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.18) 0px, transparent 50%),
            radial-gradient(at 100% 0%, rgba(168, 85, 247, 0.15) 0px, transparent 50%),
            radial-gradient(at 50% 100%, rgba(236, 72, 153, 0.12) 0px, transparent 50%);
        background-attachment: fixed;
        color: #F9FAFB;
    }

    /* Sleek Custom Scrollbar */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #030712; }
    ::-webkit-scrollbar-thumb { background: #1F2937; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #374151; }

    /* Input & Text Area Enhancements */
    .stTextArea textarea, .stTextInput input, div[data-baseweb="select"] {
        background: rgba(17, 24, 39, 0.75) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 14px !important;
        color: #F3F4F6 !important;
        font-size: 0.95rem !important;
        backdrop-filter: blur(16px);
        transition: all 0.25s ease-in-out !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #6366F1 !important;
        box-shadow: 0 0 25px rgba(99, 102, 241, 0.35) !important;
    }

    /* Primary Glowing Button */
    .stButton>button[kind="primary"], .stButton>button {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 50%, #D946EF 100%) !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 28px !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.02em !important;
        box-shadow: 0 4px 25px rgba(124, 58, 237, 0.45) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px) scale(1.01) !important;
        box-shadow: 0 8px 35px rgba(124, 58, 237, 0.65) !important;
    }

    /* Hero Header Component */
    .hero-wrapper {
        position: relative;
        padding: 15px 0 10px 0;
    }
    .hero-status-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 6px 16px;
        border-radius: 30px;
        background: rgba(99, 102, 241, 0.1);
        border: 1px solid rgba(99, 102, 241, 0.3);
        color: #A5B4FC;
        font-size: 0.82rem;
        font-weight: 600;
        margin-bottom: 12px;
    }
    .pulse-dot {
        width: 8px;
        height: 8px;
        background-color: #10B981;
        border-radius: 50%;
        box-shadow: 0 0 10px #10B981;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }
    .hero-heading {
        font-size: 3.1rem;
        font-weight: 800;
        line-height: 1.15;
        background: linear-gradient(135deg, #FFFFFF 20%, #A5B4FC 60%, #E879F9 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.03em;
        margin-bottom: 6px;
    }
    .hero-sub {
        font-size: 1.1rem;
        color: #9CA3AF;
        font-weight: 500;
        margin-bottom: 20px;
    }

    /* Glass Cards */
    .sexiest-card {
        background: rgba(17, 24, 39, 0.65);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 15px;
    }
    .sexiest-card:hover {
        border-color: rgba(168, 85, 247, 0.4);
        transform: translateY(-4px);
        box-shadow: 0 25px 60px rgba(124, 58, 237, 0.25);
    }
    .card-label {
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #9CA3AF;
        font-weight: 700;
        margin-bottom: 6px;
    }
    .card-value {
        font-size: 2.6rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        line-height: 1;
    }
    .grad-cyan { color: #38BDF8; }
    .grad-indigo { color: #818CF8; }
    .grad-emerald { color: #34D399; }
    .grad-pink { color: #F472B6; }

    /* Interactive Badges */
    .badge-matched {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid rgba(16, 185, 129, 0.4);
        color: #34D399;
        font-size: 0.85rem;
        font-weight: 600;
        padding: 6px 14px;
        border-radius: 30px;
        margin: 4px;
        box-shadow: 0 0 12px rgba(16, 185, 129, 0.15);
        transition: all 0.2s ease;
    }
    .badge-matched:hover {
        background: rgba(16, 185, 129, 0.25);
        transform: scale(1.03);
    }

    .badge-missing {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(239, 68, 68, 0.12);
        border: 1px solid rgba(239, 68, 68, 0.4);
        color: #FCA5A5;
        font-size: 0.85rem;
        font-weight: 600;
        padding: 6px 14px;
        border-radius: 30px;
        margin: 4px;
        box-shadow: 0 0 12px rgba(239, 68, 68, 0.15);
        transition: all 0.2s ease;
    }
    .badge-missing:hover {
        background: rgba(239, 68, 68, 0.25);
        transform: scale(1.03);
    }

    /* Sidebar Dark Styling */
    [data-testid="stSidebar"] {
        background-color: #030712 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
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
                <span class="pulse-dot"></span> SBERT & TF-IDF NLP Engine v2.4 Active
            </div>
            <div class="hero-heading">ResumeAI ATS Engine</div>
            <div class="hero-sub">AI-Powered Resume Screening & Skill Taxonomy Optimizer • B.Tech Minor Project 1</div>
        </div>
    """, unsafe_allow_html=True)

    # Sidebar Controls
    st.sidebar.header("⚡ Navigation & Engine Mode")
    mode = st.sidebar.radio("Select Application Mode", ["Single Resume Evaluation", "Batch Candidate Ranking", "Evaluation History & Logs"])

    st.sidebar.markdown("---")
    st.sidebar.subheader("🚀 Demo Preset")
    if st.sidebar.button("Load ML Engineer Preset Data", use_container_width=True):
        st.session_state["sample_loaded"] = True

    # Sample Data Paths
    sample_jd_path = os.path.join("sample_data", "sample_jd_ml.txt")
    sample_resume_path = os.path.join("sample_data", "sample_resume_ml.txt")
    sample_jd_text = load_sample_file(sample_jd_path)
    sample_resume_text = load_sample_file(sample_resume_path)

    # -----------------------------------------------------------------------------
    # MODE 1: SINGLE RESUME EVALUATION
    # -----------------------------------------------------------------------------
    if mode == "Single Resume Evaluation":
        st.subheader("📥 Input Candidates & Job Requirements")
        col_input1, col_input2 = st.columns(2)

        with col_input1:
            uploaded_file = st.file_uploader("Upload Resume (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])
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
                resume_text = st.text_area("Or paste raw resume text:", height=200, placeholder="Paste resume text...")

        with col_input2:
            if st.session_state.get("sample_loaded", False):
                jd_text = st.text_area("Target Job Description (JD):", value=sample_jd_text, height=265)
            else:
                jd_text = st.text_area("Paste Target Job Description (JD):", height=265, placeholder="Paste job requirements...")

        jd_title = st.text_input("Job Role Name:", value="Machine Learning Engineer")

        st.markdown("---")

        if st.button("✨ Run Deep AI Analysis & Match", type="primary", use_container_width=True):
            if not resume_text.strip() or not jd_text.strip():
                st.warning("Please provide both a Resume and a Job Description.")
                return

            with st.spinner("Executing SBERT vector embeddings & NLP taxonomy match..."):
                results = compute_ats_score(resume_text, jd_text)
                contact_info = extract_contact_info(resume_text)
                recommendations = generate_recommendations(results, resume_text, contact_info)
                save_evaluation(candidate_name, jd_title, results)

            # Results Section
            st.subheader("⚡ Live Match Analytics & Intelligence")

            # Executive Score Cards
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.markdown(f"""
                    <div class="sexiest-card">
                        <div class="card-label">Overall ATS Score</div>
                        <div class="card-big-number grad-emerald">{results['final_ats_score']}%</div>
                        <div style="color: #9CA3AF; font-size: 0.85rem; margin-top: 8px;">Grade: <b>{results['match_grade']}</b></div>
                    </div>
                """, unsafe_allow_html=True)

            with m2:
                st.markdown(f"""
                    <div class="sexiest-card">
                        <div class="card-label">SBERT Semantic Match</div>
                        <div class="card-big-number grad-indigo">{results['semantic_similarity_pct']}%</div>
                        <div style="color: #9CA3AF; font-size: 0.85rem; margin-top: 8px;">Context Vectors</div>
                    </div>
                """, unsafe_allow_html=True)

            with m3:
                st.markdown(f"""
                    <div class="sexiest-card">
                        <div class="card-label">Skill Coverage</div>
                        <div class="card-big-number grad-cyan">{results['skill_coverage_pct']}%</div>
                        <div style="color: #9CA3AF; font-size: 0.85rem; margin-top: 8px;">Taxonomy Match</div>
                    </div>
                """, unsafe_allow_html=True)

            with m4:
                st.markdown(f"""
                    <div class="sexiest-card">
                        <div class="card-label">TF-IDF Similarity</div>
                        <div class="card-big-number grad-pink">{results['tfidf_similarity_pct']}%</div>
                        <div style="color: #9CA3AF; font-size: 0.85rem; margin-top: 8px;">Keyword Frequency</div>
                    </div>
                """, unsafe_allow_html=True)

            st.write("")

            # Visual Radar & Skill Badges
            col_chart, col_details = st.columns([1.3, 1])

            with col_chart:
                st.markdown("### 🕸️ Multi-Domain Skill Radar")
                res_cats = results["resume_skill_breakdown"]
                jd_cats = results["jd_skill_breakdown"]

                categories = list(jd_cats.keys())
                jd_counts = [len(jd_cats[cat]) for cat in categories]
                res_counts = [len(res_cats[cat]) for cat in categories]

                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(
                    r=res_counts, theta=categories, fill='toself', name='Candidate Resume',
                    fillcolor='rgba(99, 102, 241, 0.35)', line=dict(color='#818CF8', width=2.5)
                ))
                fig.add_trace(go.Scatterpolar(
                    r=jd_counts, theta=categories, fill='toself', name='Job Description',
                    fillcolor='rgba(236, 72, 153, 0.2)', line=dict(color='#EC4899', width=2.5, dash='dash')
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
                st.markdown("### 👤 Contact Audit")
                st.json(contact_info)

                st.markdown("### 🏷️ Skill Gap Breakdown")
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
            st.markdown("### 💡 AI Recommendations & ATS Formatting Audit")
            st.info(recommendations["summary_advice"])

            for rec in recommendations["recommendations"]:
                st.warning(f"**[{rec['category']}] (Priority: {rec['priority']})**: {rec['message']}")

            for warn in recommendations["formatting_warnings"]:
                st.error(f"**[Format Warning]**: {warn}")

    # -----------------------------------------------------------------------------
    # MODE 2: BATCH CANDIDATE RANKING
    # -----------------------------------------------------------------------------
    elif mode == "Batch Candidate Ranking":
        st.subheader("👥 Batch Candidate Resume Leaderboard")
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
    elif mode == "Evaluation History & Logs":
        st.subheader("📜 Audit History & Database Logs")
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
