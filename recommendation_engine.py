"""
=============================================================================
Minor Project 1: AI-Powered Resume Screening & ATS Optimizer
File: recommendation_engine.py
Author: B.Tech 3rd Year AI & ML Project
Description: Generates actionable feedback, missing keyword advice, and section
             audit to optimize resumes for Applicant Tracking Systems.
=============================================================================
"""


def generate_recommendations(match_results: dict, resume_text: str, contact_info: dict) -> dict:
    """
    Analyzes match results and raw resume text to produce structured actionable advice.
    """
    recommendations = []
    formatting_warnings = []
    missing_skills = match_results["skill_analysis"]["missing_skills"]
    final_score = match_results["final_ats_score"]

    # 1. Missing Keyword Recommendations
    if missing_skills:
        top_missing = missing_skills[:5]
        recommendations.append({
            "category": "Missing Critical Keywords",
            "priority": "High",
            "message": f"Add missing domain keywords: {', '.join(top_missing)}. Including these can significantly boost your ATS score."
        })

    # 2. Contact Info Audit
    if contact_info.get("linkedin") == "Not Found":
        formatting_warnings.append("Missing LinkedIn Profile link. ATS algorithms heavily reward completed social profile links.")
    if contact_info.get("github") == "Not Found":
        formatting_warnings.append("Missing GitHub / Portfolio link. Adding project repositories increases credibility for technical roles.")

    # 3. Resume Length & Section Check
    word_count = len(resume_text.split())
    if word_count < 250:
        formatting_warnings.append(f"Resume appears short ({word_count} words). Aim for 350 - 600 words to provide enough context for NLP parsers.")
    elif word_count > 900:
        formatting_warnings.append(f"Resume is long ({word_count} words). Consider streamlining to 1-2 pages for maximum ATS & HR readability.")

    # 4. Action Verbs & Quantifiable Achievements Check
    action_verbs = ["developed", "built", "implemented", "designed", "engineered", "optimized", "increased", "reduced", "led", "created"]
    verb_count = sum(1 for verb in action_verbs if verb in resume_text.lower())
    if verb_count < 3:
        recommendations.append({
            "category": "Impact & Action Verbs",
            "priority": "Medium",
            "message": "Use strong action verbs (e.g., 'Engineered', 'Optimized', 'Deployed') to describe your work experience and projects."
        })

    # 5. Quantification check (% or numbers)
    import re
    metrics_found = re.findall(r'\b(\d+%\b|\$\d+|\d+\+|\b\d+\s+users\b|\b\d+\s+percent\b)', resume_text.lower())
    if len(metrics_found) < 2:
        recommendations.append({
            "category": "Quantifiable Results",
            "priority": "Medium",
            "message": "Add measurable outcomes to project bullets (e.g., 'Improved accuracy by 15%', 'Reduced latency by 40%')."
        })

    # 6. Overall Fit Advisory
    if final_score < 50:
        summary_advice = "Your profile currently shows significant skill gaps for this specific job description. Focus on adding core required tools and tailoring project descriptions."
    elif final_score < 75:
        summary_advice = "Your resume is a solid match! Incorporate 2-3 of the missing keywords highlighted above to reach the top candidate tier."
    else:
        summary_advice = "Excellent match! Your resume is strongly aligned with the job requirements and ready for submission."

    return {
        "summary_advice": summary_advice,
        "recommendations": recommendations,
        "formatting_warnings": formatting_warnings,
        "total_recommendations_count": len(recommendations) + len(formatting_warnings)
    }


if __name__ == "__main__":
    dummy_match = {
        "final_ats_score": 62.0,
        "skill_analysis": {"missing_skills": ["Docker", "Kubernetes", "GraphQL"]}
    }
    dummy_contact = {"linkedin": "Not Found", "github": "https://github.com/test"}
    res = generate_recommendations(dummy_match, "Short resume text without numbers", dummy_contact)
    print("--- Generated Recommendations ---")
    print(res)
