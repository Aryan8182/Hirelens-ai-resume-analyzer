"""
=============================================================================
Minor Project 1: AI-Powered Resume Screening & ATS Optimizer
File: skill_extractor.py
Author: B.Tech 3rd Year AI & ML Project
Description: Extracts hard & soft skills from resume and job description text
             using a curated skill taxonomy and regex pattern matching.
=============================================================================
"""

import re

# Comprehensive Tech Skill Taxonomy for AI/ML, Data Science, and Software Engineering
SKILL_TAXONOMY = {
    "Programming Languages": [
        "python", "java", "c++", "c#", "c", "javascript", "typescript", "r", 
        "go", "rust", "scala", "kotlin", "sql", "bash", "html", "css"
    ],
    "Machine Learning & AI": [
        "machine learning", "deep learning", "artificial intelligence", "nlp", 
        "natural language processing", "computer vision", "tensorflow", "pytorch", 
        "keras", "scikit-learn", "sklearn", "opencv", "spacy", "nltk", 
        "huggingface", "transformers", "xgboost", "lightgbm", "random forest", 
        "neural networks", "cnn", "rnn", "lstm", "gan", "bert", "llm", "rag", 
        "langchain", "reinforcement learning"
    ],
    "Data Engineering & Analytics": [
        "pandas", "numpy", "scipy", "matplotlib", "seaborn", "plotly", "tableau", 
        "power bi", "spark", "pyspark", "hadoop", "airflow", "etl", "data warehousing", 
        "data analytics", "excel", "bigquery"
    ],
    "Web Frameworks & APIs": [
        "fastapi", "flask", "django", "streamlit", "gradio", "react", "angular", 
        "vue", "node.js", "express", "rest api", "graphql", "microservices"
    ],
    "Databases": [
        "postgresql", "mysql", "mongodb", "sqlite", "redis", "dynamodb", 
        "oracle", "cassandra", "vector db", "chromadb", "pinecone"
    ],
    "Cloud & DevOps": [
        "aws", "azure", "gcp", "google cloud", "docker", "kubernetes", "git", 
        "github", "gitlab", "ci/cd", "jenkins", "terraform", "linux", "unix"
    ],
    "Soft Skills & Management": [
        "problem solving", "critical thinking", "communication", "leadership", 
        "teamwork", "collaboration", "agile", "scrum", "time management"
    ]
}


def extract_skills_by_category(text: str) -> dict:
    """
    Scans input text for occurrences of skills defined in the taxonomy.
    Returns a dictionary mapping category names to lists of detected skills.
    """
    text_lower = text.lower()
    extracted = {}
    
    for category, skill_list in SKILL_TAXONOMY.items():
        found = set()
        for skill in skill_list:
            # Word boundary regex to prevent partial matching (e.g., "c" in "cat")
            escaped_skill = re.escape(skill)
            pattern = r'\b' + escaped_skill + r'\b'
            if re.search(pattern, text_lower):
                found.add(skill.title())
        extracted[category] = list(found)
        
    return extracted


def extract_all_skills_list(text: str) -> list:
    """
    Returns a flat list of all unique skills found in the text.
    """
    cat_skills = extract_skills_by_category(text)
    all_skills = []
    for category, skill_set in cat_skills.items():
        all_skills.extend(skill_set)
    return list(set(all_skills))


def compare_skills(resume_text: str, jd_text: str) -> dict:
    """
    Compares skills extracted from a resume against skills extracted from a Job Description.
    Identifies matched skills, missing skills, and skill coverage ratio.
    """
    resume_skills = set(extract_all_skills_list(resume_text))
    jd_skills = set(extract_all_skills_list(jd_text))

    matched = list(resume_skills.intersection(jd_skills))
    missing = list(jd_skills.difference(resume_skills))
    additional = list(resume_skills.difference(jd_skills))

    coverage_ratio = (len(matched) / len(jd_skills) * 100) if jd_skills else 100.0

    return {
        "matched_skills": sorted(matched),
        "missing_skills": sorted(missing),
        "additional_skills": sorted(additional),
        "resume_skills_count": len(resume_skills),
        "jd_skills_count": len(jd_skills),
        "skill_coverage_pct": round(coverage_ratio, 2)
    }


if __name__ == "__main__":
    sample_resume = "Skilled in Python, TensorFlow, PyTorch, Docker, SQL, and Streamlit. Passionate about machine learning."
    sample_jd = "Looking for ML Engineer proficient in Python, PyTorch, Kubernetes, SQL, Docker, AWS, and RAG."

    result = compare_skills(sample_resume, sample_jd)
    print("--- Skill Comparison Result ---")
    print(f"Matched Skills ({len(result['matched_skills'])}): {result['matched_skills']}")
    print(f"Missing Skills ({len(result['missing_skills'])}): {result['missing_skills']}")
    print(f"Coverage: {result['skill_coverage_pct']}%")
