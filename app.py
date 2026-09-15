"""
=============================================================================
Minor Project 1: AI-Powered Resume Screening & ATS Optimizer
File: app.py
Author: B.Tech 3rd Year AI & ML Project
Description: Streamlit interactive web application with custom futuristic
             glassmorphism dark UI theme, Plotly charts, and ATS analysis.
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
    page_title="AI Resume ATS Optimizer | Minor Project 1",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# CUSTOM FUTURISTIC GLASSMORPHISM STYLING (CSS)
# -----------------------------------------------------------------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Main App Dark Background Gradient */
    .stApp {
        background: radial-gradient(circle at 15% 15%, #1E1B4B 0%, #0F172A 55%, #020617 100%);
        color: #F8FAFC;
    }

    /* Hero Header Styling */
    .hero-container {
        padding: 20px 0px 10px 0px;
    }
    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6366F1 0%, #A855F7 50%, #EC4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.02em;
        margin-bottom: 5px;
    }
    .hero-subtitle {
        font-size: 1.1rem;
        color: #94A3B8;
        margin-bottom: 20px;
        font-weight: 500;
    }
    .glow-badge {
        display: inline-block;
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        background: rgba(99, 102, 241, 0.15);
        color: #818CF8;
        border: 1px solid rgba(99, 102, 241, 0.4);
        margin-right: 8px;
    }

    /* Glassmorphic Cards */
    .glass-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 22px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: all 0.3s ease;
        margin-bottom: 15px;
    }
    .glass-card:hover {
        border-color: rgba(99, 102, 241, 0.5);
        box-shadow: 0 12px 40px 0 rgba(99, 102, 241, 0.2);
    }

    /* Custom Metric Displays */
    .metric-value {
        font-size: 2.4rem;
        font-weight: 800;
        letter-spacing: -0.02em;
    }
    .metric-label-text {
        font-size: 0.85rem;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
    }
    .text-emerald { color: #34D399; }
    .text-indigo { color: #818CF8; }
    .text-cyan { color: #38BDF8; }
    .text-pink { color: #F472B6; }

    /* Interactive Skill Badges */
    .skill-badge-match {
        display: inline-block;
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid #10B981;
        color: #34D399;
        font-size: 0.85rem;
        font-weight: 600;
        padding: 6px 14px;
        border-radius: 20px;
        margin: 4px;
        box-shadow: 0 0 10px rgba(16, 185, 129, 0.2);
    }
    .skill-badge-missing {
        display: inline-block;
        background: rgba(239, 68, 68, 0.15);
        border: 1px solid #EF4444;
        color: #FCA5A5;
        font-size: 0.85rem;
        font-weight: 600;
        padding: 6px 14px;
        border-radius: 20px;
        margin: 4px;
        box-shadow: 0 0 10px rgba(239, 68, 68, 0.2);
    }

    /* Sidebar Dark Theme Styling */
    [data-testid="stSidebar"] {
        background-color: #0B0F19 !important;
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
    # Hero Title Header
    st.markdown("""
        <div class="hero-container">
            <div class="hero-title">⚡ AI Resume ATS Optimizer</div>
            <div class="hero-subtitle">B.Tech 3rd Year Minor Project 1 | Department of AI & ML</div>
            <div>
                <span class="glow-badge">🔥 SBERT Embeddings</span>
                <span class="glow-badge">🧠 TF-IDF NLP</span>
                <span class="glow-badge">⚡ Real-Time Skill Radar</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.write("")

    # Sidebar Controls
    st.sidebar.header("⚙️ Dashboard Controls")
    mode = st.sidebar.radio("Select Application Mode", ["Single Resume Evaluation", "Batch Candidate Ranking", "Evaluation History & Logs"])

    st.sidebar.markdown("---")
    st.sidebar.subheader("💡 Demo Quick-Start")
    if st.sidebar.button("Load Preset Sample ML Data", use_container_width=True):
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
        st.subheader("📋 Step 1: Input Resume & Job Description")
        col_input1, col_input2 = st.columns(2)

        with col_input1:
            uploaded_file = st.file_uploader("Upload Candidate Resume (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])
            resume_text = ""
            candidate_name = "Candidate Resume"

            if uploaded_file is not None:
                file_bytes = uploaded_file.read()
                candidate_name = uploaded_file.name
                try:
                    resume_text = parse_resume_file(uploaded_file.name, file_bytes)
                    st.success(f"Successfully loaded {uploaded_file.name} ({len(resume_text)} chars)")
                except Exception as e:
                    st.error(f"Error parsing resume: {e}")
            elif st.session_state.get("sample_loaded", False):
                resume_text = sample_resume_text
                st.info("Loaded Preset ML Candidate Resume")
            else:
                resume_text = st.text_area("Or paste raw resume text:", height=200, placeholder="Paste resume content...")

        with col_input2:
            if st.session_state.get("sample_loaded", False):
                jd_text = st.text_area("Target Job Description (JD):", value=sample_jd_text, height=265)
            else:
                jd_text = st.text_area("Paste Target Job Description (JD):", height=265, placeholder="Paste job description requirements...")

        jd_title = st.text_input("Job Role Name:", value="Machine Learning Engineer")

        st.markdown("---")

        if st.button("🚀 Analyze ATS Compatibility Now", type="primary", use_container_width=True):
            if not resume_text.strip() or not jd_text.strip():
                st.warning("Please provide both a Resume and a Job Description to proceed.")
                return

            with st.spinner("Processing deep learning embeddings & calculating ATS score..."):
                results = compute_ats_score(resume_text, jd_text)
                contact_info = extract_contact_info(resume_text)
                recommendations = generate_recommendations(results, resume_text, contact_info)
                save_evaluation(candidate_name, jd_title, results)

            # Results Section
            st.subheader("📊 Step 2: ATS Match Score & Analytics")

            # Custom Metric Cards
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.markdown(f"""
                    <div class="glass-card">
                        <div class="metric-label-text">Overall ATS Score</div>
                        <div class="metric-value text-emerald">{results['final_ats_score']}%</div>
                        <div style="color: #94A3B8; font-size: 0.85rem; margin-top: 4px;">Grade: <b>{results['match_grade']}</b></div>
                    </div>
                """, unsafe_allow_html=True)

            with m2:
                st.markdown(f"""
                    <div class="glass-card">
                        <div class="metric-label-text">SBERT Semantic Match</div>
                        <div class="metric-value text-indigo">{results['semantic_similarity_pct']}%</div>
                        <div style="color: #94A3B8; font-size: 0.85rem; margin-top: 4px;">Context Similarity</div>
                    </div>
                """, unsafe_allow_html=True)

            with m3:
                st.markdown(f"""
                    <div class="glass-card">
                        <div class="metric-label-text">Skill Coverage</div>
                        <div class="metric-value text-cyan">{results['skill_coverage_pct']}%</div>
                        <div style="color: #94A3B8; font-size: 0.85rem; margin-top: 4px;">Taxonomy Ratio</div>
                    </div>
                """, unsafe_allow_html=True)

            with m4:
                st.markdown(f"""
                    <div class="glass-card">
                        <div class="metric-label-text">TF-IDF Similarity</div>
                        <div class="metric-value text-pink">{results['tfidf_similarity_pct']}%</div>
                        <div style="color: #94A3B8; font-size: 0.85rem; margin-top: 4px;">Keyword Weights</div>
                    </div>
                """, unsafe_allow_html=True)

            st.write("")

            # Visualizations & Skill Badges
            col_chart, col_details = st.columns([1.3, 1])

            with col_chart:
                st.markdown("### 🕸️ Skill Coverage Polar Radar")
                res_cats = results["resume_skill_breakdown"]
                jd_cats = results["jd_skill_breakdown"]

                categories = list(jd_cats.keys())
                jd_counts = [len(jd_cats[cat]) for cat in categories]
                res_counts = [len(res_cats[cat]) for cat in categories]

                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(
                    r=res_counts, theta=categories, fill='toself', name='Candidate Resume',
                    fillcolor='rgba(99, 102, 241, 0.3)', line=dict(color='#818CF8', width=2)
                ))
                fig.add_trace(go.Scatterpolar(
                    r=jd_counts, theta=categories, fill='toself', name='Job Description',
                    fillcolor='rgba(236, 72, 153, 0.2)', line=dict(color='#EC4899', width=2, dash='dash')
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
                st.markdown("### 👤 Contact Details Extracted")
                st.json(contact_info)

                st.markdown("### 🏷️ Skill Breakdown")
                matched = results["skill_analysis"]["matched_skills"]
                missing = results["skill_analysis"]["missing_skills"]

                st.write("**Matched Skills:**")
                if matched:
                    badges_html = "".join([f'<span class="skill-badge-match">✓ {s}</span>' for s in matched])
                    st.markdown(badges_html, unsafe_allow_html=True)
                else:
                    st.write("No exact skills matched.")

                st.write("")
                st.write("**Missing Critical Skills:**")
                if missing:
                    badges_missing_html = "".join([f'<span class="skill-badge-missing">✗ {s}</span>' for s in missing])
                    st.markdown(badges_missing_html, unsafe_allow_html=True)
                else:
                    st.success("No missing critical skill gaps!")

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

        if st.button("Rank All Candidates Now", type="primary", use_container_width=True):
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

            st.markdown("### 🏆 Candidate Ranking Leaderboard")
            st.dataframe(df_results, use_container_width=True)

            fig_bar = px.bar(
                df_results, x="Candidate File", y="ATS Score (%)", color="Match Grade",
                title="Candidate Match Comparison Score", text_auto=True, template="plotly_dark"
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
