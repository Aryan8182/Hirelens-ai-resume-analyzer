"""
=============================================================================
Minor Project 1: AI-Powered Resume Screening & ATS Optimizer
File: api.py
Author: B.Tech 3rd Year AI & ML Project
Description: FastAPI REST API service for ATS resume evaluation endpoints.
             Run via: uvicorn api:app --reload
=============================================================================
"""

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from resume_parser import parse_resume_file, extract_contact_info
from ats_matcher import compute_ats_score
from recommendation_engine import generate_recommendations
from db_manager import save_evaluation

app = FastAPI(
    title="AI Resume Screening & ATS Optimizer API",
    description="Minor Project 1 - B.Tech 3rd Year AI & ML REST API Service",
    version="1.0.0"
)


class MatchRequest(BaseModel):
    candidate_name: Optional[str] = "Candidate"
    jd_title: Optional[str] = "Job Description"
    resume_text: str
    jd_text: str


@app.get("/")
def read_root():
    return {
        "project": "AI-Powered Resume Screening & ATS Optimizer API",
        "author": "3rd Year B.Tech AI & ML",
        "status": "Online",
        "documentation": "/docs"
    }


@app.post("/api/v1/parse-resume")
async def parse_resume_endpoint(file: UploadFile = File(...)):
    """
    Upload a PDF/DOCX resume file and extract raw text and contact details.
    """
    try:
        content = await file.read()
        raw_text = parse_resume_file(file.filename, content)
        contact_info = extract_contact_info(raw_text)
        return {
            "filename": file.filename,
            "contact_info": contact_info,
            "raw_text_length": len(raw_text),
            "text_snippet": raw_text[:300] + "..."
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/v1/analyze-match")
def analyze_match_endpoint(request: MatchRequest):
    """
    Analyze semantic and skill match between candidate resume text and job description.
    """
    if not request.resume_text.strip() or not request.jd_text.strip():
        raise HTTPException(status_code=400, detail="Resume text and JD text cannot be empty.")

    match_results = compute_ats_score(request.resume_text, request.jd_text)
    contact_info = extract_contact_info(request.resume_text)
    recommendations = generate_recommendations(match_results, request.resume_text, contact_info)

    # Save to SQLite database
    save_evaluation(request.candidate_name, request.jd_title, match_results)

    return {
        "candidate_name": request.candidate_name,
        "jd_title": request.jd_title,
        "ats_score": match_results["final_ats_score"],
        "match_grade": match_results["match_grade"],
        "metrics": {
            "semantic_match_pct": match_results["semantic_similarity_pct"],
            "skill_coverage_pct": match_results["skill_coverage_pct"],
            "tfidf_similarity_pct": match_results["tfidf_similarity_pct"]
        },
        "matched_skills": match_results["skill_analysis"]["matched_skills"],
        "missing_skills": match_results["skill_analysis"]["missing_skills"],
        "recommendations": recommendations
    }
