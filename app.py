"""
=============================================================================
Minor Project 1: AI-Powered Resume Screening & ATS Optimizer
File: app.py
Author: B.Tech 3rd Year AI & ML Project
Description: Ultra-high contrast, interactive Vercel/Linear-inspired ATS Dashboard
             with dynamic weightage sliders, high-contrast sidebar, and Plotly charts.
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
from db_manager import save_evaluation, get_evaluation_history

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="ResumeAI Engine | Next-Gen ATS Optimizer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# HIGH-CONTRAST ULTRA-PREMIUM FRONTEND STYLING (CSS)
# -----------------------------------------------------------------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* Ambient Dark Background */
    .stApp {
        background: #050814;
        background-image: 
            radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.22) 0px, transparent 50%),
            radial-gradient(at 100% 0%, rgba(168, 85, 247, 0.18) 0px, transparent 50%),
            radial-gradient(at 50% 100%, rgba(236, 72, 153, 0.15) 0px, transparent 50%);
        background-attachment: fixed;
        color: #F8FAFC !important;
    }

    /* Scrollbars */
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: #050814; }
    ::-webkit-scrollbar-thumb { background: #334155; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #475569; }

    /* ==========================================
       SIDEBAR HIGH-CONTRAST VISIBILITY FIX
       ========================================== */
    [data-testid="stSidebar"] {
        background-color: #0B0F1D !important;
        border-right: 1px solid rgba(255, 255, 255, 0.12) !important;
    }
    
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] span, [data-testid="stSidebar"] p, [data-testid="stSidebar"] label {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }

    /* Sidebar Radio Buttons High Contrast Styling */
    div[data-testid="stRadio"] > label {
        font-size: 1rem !important;
        color: #F8FAFC !important;
        font-weight: 700 !important;
        margin-bottom: 10px !important;
    }

    div[data-testid="stRadio"] div[role="radiogroup"] > label {
        background: rgba(30, 41, 59, 0.85) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px !important;
        padding: 12px 18px !important;
        margin-bottom: 10px !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        transition: all 0.25s ease-in-out !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
    }

    div[data-testid="stRadio"] div[role="radiogroup"] > label:hover {
        background: rgba(99, 102, 241, 0.3) !important;
        border-color: #818CF8 !important;
        color: #FFFFFF !important;
        transform: translateX(4px) !important;
    }

    /* Selected Active Navigation Card */
    div[data-testid="stRadio"] div[role="radiogroup"] label[aria-checked="true"],
    div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%) !important;
        border-color: #C084FC !important;
        color: #FFFFFF !important;
        font-weight: 800 !important;
        box-shadow: 0 4px 20px rgba(124, 58, 237, 0.5) !important;
    }

    /* Input Fields & Text Areas High Contrast */
    .stTextArea textarea, .stTextInput input {
        background: rgba(15, 23, 42, 0.9) !important;
        border: 1.5px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 14px !important;
        color: #FFFFFF !important;
        font-size: 0.98rem !important;
        backdrop-filter: blur(16px);
        transition: all 0.25s ease-in-out !important;
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #818CF8 !important;
        box-shadow: 0 0 25px rgba(99, 102, 241, 0.45) !important;
    }

    /* Primary Interactive Button */
    .stButton>button[kind="primary"], .stButton>button {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 50%, #D946EF 100%) !important;
        color: #FFFFFF !important;
        font-weight: 800 !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 14px 30px !important;
        font-size: 1rem !important;
        letter-spacing: 0.02em !important;
        box-shadow: 0 4px 25px rgba(124, 58, 237, 0.5) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px) scale(1.01) !important;
        box-shadow: 0 8px 35px rgba(124, 58, 237, 0.75) !important;
    }

    /* Hero Header */
    .hero-wrapper {
        padding: 15px 0 10px 0;
    }
    .hero-status-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 6px 16px;
        border-radius: 30px;
        background: rgba(99, 102, 241, 0.15);
        border: 1px solid rgba(99, 102, 241, 0.4);
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
        box-shadow: 0 0 12px #10B981;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }
    .hero-heading {
        font-size: 3.2rem;
        font-weight: 800;
        line-height: 1.15;
        background: linear-gradient(135deg, #FFFFFF 20%, #A5B4FC 60%, #F472B6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.03em;
        margin-bottom: 6px;
    }
    .hero-sub {
        font-size: 1.15rem;
        color: #CBD5E1;
        font-weight: 500;
        margin-bottom: 20px;
    }

    /* Glass Metric Cards */
    .sexiest-card {
        background: rgba(15, 23, 42, 0.75);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1.5px solid rgba(255, 255, 255, 0.12);
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 15px;
    }
    .sexiest-card:hover {
        border-color: rgba(168, 85, 247, 0.5);
        transform: translateY(-4px);
        box-shadow: 0 25px 60px rgba(124, 58, 237, 0.3);
    }
    .card-label {
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #94A3B8;
        font-weight: 700;
        margin-bottom: 8px;
    }
    .card-value {
        font-size: 2.8rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        line-height: 1;
    }
    .grad-cyan { color: #38BDF8; }
    .grad-indigo { color: #818CF8; }
    .grad-emerald { color: #34D399; }
    .grad-pink { color: #F472B6; }

    /* Interactive Skill Badges */
    .badge-matched {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(16, 185, 129, 0.18);
        border: 1px solid #10B981;
        color: #34D399;
        font-size: 0.88rem;
        font-weight: 700;
        padding: 7px 16px;
        border-radius: 30px;
        margin: 5px;
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.25);
        transition: all 0.2s ease;
    }
    .badge-matched:hover {
        background: rgba(16, 185, 129, 0.3);
        transform: scale(1.05);
    }

    .badge-missing {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(239, 68, 68, 0.18);
        border: 1px solid #EF4444;
        color: #FCA5A5;
        font-size: 0.88rem;
        font-weight: 700;
        padding: 7px 16px;
        border-radius: 30px;
        margin: 5px;
        box-shadow: 0 0 15px rgba(239, 68, 68, 0.25);
        transition: all 0.2s ease;
    }
    .badge-missing:hover {
        background: rgba(239, 68, 68, 0.3);
        transform: scale(1.05);
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
                <span class="pulse-dot"></span> SBERT & TF-IDF NLP Engine Active
            </div>
            <div class="hero-heading">ResumeAI Engine</div>
            <div class="hero-sub">AI-Powered Resume Screening & Skill Taxonomy Optimizer • Minor Project 1</div>
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
    st.sidebar.caption("Adjust weightages to customize ATS evaluation formula live:")
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
        st.subheader("📥 Input Candidate Resume & Job Requirements")
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
            st.subheader("⚡ Live Match Intelligence & Score Analytics")

            # Executive Metric Cards
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.markdown(f"""
                    <div class="sexiest-card">
                        <div class="card-label">Custom ATS Score</div>
                        <div class="card-big-number grad-emerald">{results['final_ats_score']}%</div>
                        <div style="color: #CBD5E1; font-size: 0.88rem; margin-top: 8px;">Grade: <b style="color: #34D399;">{results['match_grade']}</b></div>
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
                st.markdown("### 🕸️ Multi-Domain Skill Radar")
                res_cats = results["resume_skill_breakdown"]
                jd_cats = results["jd_skill_breakdown"]

                categories = list(jd_cats.keys())
                jd_counts = [len(jd_cats[cat]) for cat in categories]
                res_counts = [len(res_cats[cat]) for cat in categories]

                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(
                    r=res_counts, theta=categories, fill='toself', name='Candidate Resume',
                    fillcolor='rgba(99, 102, 241, 0.4)', line=dict(color='#818CF8', width=3)
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
            st.markdown("### 💡 AI Recommendations & Formatting Audit")
            st.info(recommendations["summary_advice"])

            for rec in recommendations["recommendations"]:
                st.warning(f"**[{rec['category']}] (Priority: {rec['priority']})**: {rec['message']}")

            for warn in recommendations["formatting_warnings"]:
                st.error(f"**[Format Warning]**: {warn}")

    # -----------------------------------------------------------------------------
    # MODE 2: BATCH CANDIDATE RANKING
    # -----------------------------------------------------------------------------
    elif "Batch Candidate Ranking" in mode:
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
    elif "Evaluation History & Logs" in mode:
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
