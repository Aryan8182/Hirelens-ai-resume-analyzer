"""
=============================================================================
Minor Project 1: AI-Powered Resume Screening & ATS Optimizer
File: app.py
Author: B.Tech 3rd Year AI & ML Project
Description: Streamlit interactive web application for ATS resume analysis,
             multi-candidate ranking, skill radar visualization, and history.
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

# Set Streamlit Page Configuration
st.set_page_config(
    page_title="AI Resume ATS Optimizer | Minor Project 1",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
    <style>
    .main-title {
        font-size: 2.3rem;
        color: #1E88E5;
        font-weight: 700;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #555555;
        margin-bottom: 25px;
    }
    .score-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        border-left: 5px solid #1E88E5;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .stBadge {
        font-size: 1rem !important;
    }
    </style>
""", unsafe_allow_html=True)


def load_sample_file(path: str) -> str:
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""


def main():
    # Header Section
    st.markdown('<div class="main-title">🎯 AI-Powered Resume Screening & ATS Optimizer</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">B.Tech 3rd Year Minor Project 1 | Department of AI & ML</div>', unsafe_allow_html=True)

    # Sidebar Controls
    st.sidebar.header("⚙️ Control Panel")
    mode = st.sidebar.radio("Select Mode", ["Single Resume Evaluation", "Batch Candidate Ranking", "Evaluation History & Logs", "Methodology & Viva Info"])

    # Sample Data Helper Button
    st.sidebar.markdown("---")
    st.sidebar.subheader("💡 Demo Quick-Start")
    if st.sidebar.button("Load Preset Sample ML Data"):
        st.session_state["sample_loaded"] = True

    # Load Sample Paths
    sample_jd_path = os.path.join("sample_data", "sample_jd_ml.txt")
    sample_resume_path = os.path.join("sample_data", "sample_resume_ml.txt")

    sample_jd_text = load_sample_file(sample_jd_path)
    sample_resume_text = load_sample_file(sample_resume_path)

    # -----------------------------------------------------------------------------
    # TAB 1: SINGLE RESUME EVALUATION
    # -----------------------------------------------------------------------------
    if mode == "Single Resume Evaluation":
        st.subheader("📋 Step 1: Upload Resume & Input Job Description")
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
                resume_text = st.text_area("Or paste resume text here:", height=200, placeholder="Paste resume content...")

        with col_input2:
            if st.session_state.get("sample_loaded", False):
                jd_text = st.text_area("Job Description:", value=sample_jd_text, height=265)
            else:
                jd_text = st.text_area("Paste Target Job Description (JD):", height=265, placeholder="Paste job description requirements here...")

        jd_title = st.text_input("Job Title / Role Name:", value="Machine Learning Engineer")

        st.markdown("---")

        if st.button("🚀 Run AI ATS Match & Analysis", type="primary", use_container_width=True):
            if not resume_text.strip() or not jd_text.strip():
                st.warning("Please provide both a Resume and a Job Description to proceed.")
                return

            with st.spinner("Analyzing semantic embeddings, extracting skills, and calculating ATS score..."):
                results = compute_ats_score(resume_text, jd_text)
                contact_info = extract_contact_info(resume_text)
                recommendations = generate_recommendations(results, resume_text, contact_info)

                # Save to database log
                save_evaluation(candidate_name, jd_title, results)

            # Results Section
            st.subheader("📊 Step 2: Evaluation Results & Match Summary")

            # Score Metric Cards
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Overall ATS Score", f"{results['final_ats_score']}%", results['match_grade'])
            m2.metric("Semantic Similarity (SBERT)", f"{results['semantic_similarity_pct']}%")
            m3.metric("Skill Coverage", f"{results['skill_coverage_pct']}%")
            m4.metric("TF-IDF Keyword Match", f"{results['tfidf_similarity_pct']}%")

            st.write("")

            # Visualizations & Breakdown Columns
            col_chart, col_details = st.columns([1.2, 1])

            with col_chart:
                st.markdown("### 🕸️ Skill Coverage Radar Chart")
                # Prepare data for Radar Chart
                res_cats = results["resume_skill_breakdown"]
                jd_cats = results["jd_skill_breakdown"]

                categories = list(jd_cats.keys())
                jd_counts = [len(jd_cats[cat]) for cat in categories]
                res_counts = [len(res_cats[cat]) for cat in categories]

                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(
                    r=res_counts, theta=categories, fill='toself', name='Candidate Resume'
                ))
                fig.add_trace(go.Scatterpolar(
                    r=jd_counts, theta=categories, fill='toself', name='Job Description'
                ))
                fig.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, max(max(jd_counts + [1]), max(res_counts + [1]))])),
                    showlegend=True,
                    height=400,
                    margin=dict(l=40, r=40, t=30, b=30)
                )
                st.plotly_chart(fig, use_container_width=True)

            with col_details:
                st.markdown("### 👤 Contact & Profile Audit")
                st.json(contact_info)

                st.markdown("### 🏷️ Skill Gap Breakdown")
                matched = results["skill_analysis"]["matched_skills"]
                missing = results["skill_analysis"]["missing_skills"]

                st.write(f"**Matched Skills ({len(matched)}):**")
                if matched:
                    st.success(", ".join(matched))
                else:
                    st.write("No exact skills matched.")

                st.write(f"**Missing Critical Skills ({len(missing)}):**")
                if missing:
                    st.error(", ".join(missing))
                else:
                    st.success("No critical skill gaps identified!")

            st.markdown("---")
            st.markdown("### 💡 Actionable AI Recommendations & Formatting Audit")
            st.info(recommendations["summary_advice"])

            for rec in recommendations["recommendations"]:
                st.warning(f"**[{rec['category']}] (Priority: {rec['priority']})**: {rec['message']}")

            for warn in recommendations["formatting_warnings"]:
                st.error(f"**[Format Warning]**: {warn}")

    # -----------------------------------------------------------------------------
    # TAB 2: BATCH CANDIDATE RANKING
    # -----------------------------------------------------------------------------
    elif mode == "Batch Candidate Ranking":
        st.subheader("👥 Batch Candidate Resume Ranking")
        st.write("Upload multiple candidate resumes to rank them against a single target Job Description.")

        target_jd = st.text_area("Target Job Description (JD):", value=sample_jd_text if st.session_state.get("sample_loaded", False) else "", height=150)
        uploaded_files = st.file_uploader("Upload Resumes (Multiple PDF/DOCX files)", type=["pdf", "docx", "txt"], accept_multiple_files=True)

        if st.button("Rank Candidates Now", type="primary"):
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
                    "Matched Skills Count": len(eval_res["skill_analysis"]["matched_skills"]),
                    "Missing Skills Count": len(eval_res["skill_analysis"]["missing_skills"])
                })
                progress_bar.progress((idx + 1) / len(uploaded_files))

            # Sort results by ATS score descending
            df_results = pd.DataFrame(results_list).sort_values(by="ATS Score (%)", ascending=False)
            df_results["Rank"] = range(1, len(df_results) + 1)

            st.markdown("### 🏆 Candidate Leaderboard")
            st.dataframe(df_results, use_container_width=True)

            fig_bar = px.bar(
                df_results, x="Candidate File", y="ATS Score (%)", color="Match Grade",
                title="Candidate Match Comparison Score", text_auto=True
            )
            st.plotly_chart(fig_bar, use_container_width=True)

    # -----------------------------------------------------------------------------
    # TAB 3: EVALUATION HISTORY & LOGS
    # -----------------------------------------------------------------------------
    elif mode == "Evaluation History & Logs":
        st.subheader("📜 Audit History & Database Logs")
        df_hist = get_evaluation_history()

        if df_hist.empty:
            st.info("No evaluations logged yet. Run a single or batch evaluation to populate history.")
        else:
            st.dataframe(df_hist, use_container_width=True)

            st.markdown("### 📈 Evaluation Score Distribution")
            fig_hist = px.histogram(df_hist, x="ats_score", nbins=10, title="Distribution of Evaluated ATS Scores", labels={"ats_score": "ATS Match Score (%)"})
            st.plotly_chart(fig_hist, use_container_width=True)

    # -----------------------------------------------------------------------------
    # TAB 4: METHODOLOGY & VIVA INFO
    # -----------------------------------------------------------------------------
    elif mode == "Methodology & Viva Info":
        st.subheader("📚 Technical Architecture & Methodology (For Project Viva Defense)")
        st.markdown("""
        ### 🔬 How the ATS Optimization System Works

        1. **Text Parsing & Extraction (`pdfplumber` & `python-docx`)**:
           - Extract raw text streams from PDF and DOCX files.
           - Apply Regex normalization to extract contact details (email, phone, LinkedIn, GitHub).

        2. **NLP Skill Extraction & Taxonomy**:
           - Categorizes hard skills across 7 domains: *Programming Languages, AI/ML, Data Analytics, Web APIs, Databases, Cloud & DevOps, Soft Skills*.
           - Uses word-boundary Regex matching to prevent false positives.

        3. **Hybrid ATS Scoring Formula**:
           $$\\text{ATS Score} = 0.45 \\times \\text{Semantic Score (SBERT)} + 0.35 \\times \\text{Skill Coverage \\%} + 0.20 \\times \\text{TF-IDF Cosine Similarity}$$

        4. **Sentence-Transformers (SBERT - `all-MiniLM-L6-v2`)**:
           - Encodes text into 384-dimensional dense vector embeddings.
           - Computes cosine similarity between candidate experience context and job description context.

        5. **Actionable Feedback Generator**:
           - Identifies missing critical skills.
           - Audits contact links, word counts, and metric quantification.
        """)


if __name__ == "__main__":
    main()
