"""
=============================================================================
Minor Project 1: AI-Powered Resume Screening & ATS Optimizer
File: ats_matcher.py
Author: B.Tech 3rd Year AI & ML Project
Description: Core ATS scoring engine combining Sentence-Transformers (SBERT),
             TF-IDF Cosine Similarity, and Skill Coverage percentage.
=============================================================================
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from skill_extractor import compare_skills, extract_skills_by_category

# Global variable to lazy-load Sentence-Transformers model
SBERT_MODEL = None


def load_sbert_model():
    """
    Lazy-loads the Sentence-Transformers model ('all-MiniLM-L6-v2').
    Returns None if sentence-transformers package is not installed.
    """
    global SBERT_MODEL
    if SBERT_MODEL is None:
        try:
            from sentence_transformers import SentenceTransformer
            print("[INFO] Loading Sentence-Transformers model (all-MiniLM-L6-v2)...")
            SBERT_MODEL = SentenceTransformer('all-MiniLM-L6-v2')
        except Exception as e:
            print(f"[Warning] Could not load SentenceTransformer: {e}. Falling back to TF-IDF.")
            SBERT_MODEL = False
    return SBERT_MODEL if SBERT_MODEL is not False else None


def calculate_tfidf_similarity(text1: str, text2: str) -> float:
    """
    Calculates classical TF-IDF cosine similarity between two text documents.
    Returns float score between 0.0 and 1.0 (converted to percentage float 0 - 100).
    """
    if not text1.strip() or not text2.strip():
        return 0.0

    vectorizer = TfidfVectorizer(stop_words='english')
    try:
        tfidf_matrix = vectorizer.fit_transform([text1, text2])
        sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return round(float(sim) * 100.0, 2)
    except Exception as e:
        print(f"[Error] TF-IDF Calculation Error: {e}")
        return 0.0


def calculate_semantic_similarity(text1: str, text2: str) -> float:
    """
    Calculates dense vector embedding similarity using SBERT (all-MiniLM-L6-v2).
    Falls back to TF-IDF similarity if SBERT is unavailable.
    """
    model = load_sbert_model()
    if model is None:
        return calculate_tfidf_similarity(text1, text2)

    try:
        embeddings = model.encode([text1, text2])
        sim = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
        # Normalize score between 0 and 100
        sim_pct = max(0.0, min(100.0, float(sim) * 100.0))
        return round(sim_pct, 2)
    except Exception as e:
        print(f"[Warning] SBERT encoding failed: {e}. Using TF-IDF.")
        return calculate_tfidf_similarity(text1, text2)


def compute_ats_score(resume_text: str, jd_text: str) -> dict:
    """
    Computes final ATS score by combining:
    1. Semantic Similarity (SBERT) - 45% weight
    2. Skill Coverage Percentage - 35% weight
    3. TF-IDF Keyword Match - 20% weight
    """
    tfidf_score = calculate_tfidf_similarity(resume_text, jd_text)
    semantic_score = calculate_semantic_similarity(resume_text, jd_text)
    skill_analysis = compare_skills(resume_text, jd_text)
    skill_score = skill_analysis["skill_coverage_pct"]

    # Weighted composite score formula
    final_score = (0.45 * semantic_score) + (0.35 * skill_score) + (0.20 * tfidf_score)
    final_score = round(max(0.0, min(100.0, final_score)), 1)

    # Determine match rating category
    if final_score >= 80:
        match_grade = "Exceptional Fit"
        badge_color = "green"
    elif final_score >= 65:
        match_grade = "Strong Fit"
        badge_color = "blue"
    elif final_score >= 50:
        match_grade = "Moderate Fit"
        badge_color = "orange"
    else:
        match_grade = "Low Fit / High Rejection Risk"
        badge_color = "red"

    return {
        "final_ats_score": final_score,
        "semantic_similarity_pct": semantic_score,
        "skill_coverage_pct": skill_score,
        "tfidf_similarity_pct": tfidf_score,
        "match_grade": match_grade,
        "badge_color": badge_color,
        "skill_analysis": skill_analysis,
        "resume_skill_breakdown": extract_skills_by_category(resume_text),
        "jd_skill_breakdown": extract_skills_by_category(jd_text)
    }


if __name__ == "__main__":
    test_res = """
    John Doe - AI/ML Engineer
    Proficient in Python, TensorFlow, PyTorch, Scikit-learn, SQL, Docker, Streamlit.
    Experience with NLP model training, RAG pipelines, and REST APIs.
    B.Tech in Artificial Intelligence.
    """

    test_jd = """
    Hiring Senior ML Engineer:
    Must have experience in Python, PyTorch, Docker, Kubernetes, AWS, SQL, and LLMs.
    Building scalable AI services and REST APIs.
    """

    results = compute_ats_score(test_res, test_jd)
    print("--- ATS Match Results ---")
    print(f"Final Score: {results['final_ats_score']}% ({results['match_grade']})")
    print(f"Semantic Match: {results['semantic_similarity_pct']}%")
    print(f"Skill Coverage: {results['skill_coverage_pct']}%")
    print(f"TF-IDF Match: {results['tfidf_similarity_pct']}%")
