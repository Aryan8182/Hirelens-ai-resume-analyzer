# Minor Project 1 Synopsis & Report

**Title**: HireLens: AI-Powered Resume Screening, Skill Gap Analysis & Job Matching System  
**Degree**: Bachelor of Technology (B.Tech) in Artificial Intelligence & Machine Learning  
**Academic Year**: 3rd Year (Semester 5/6)  
**Live Demo URL**: [https://hirelens-ai-resume-analyzer.streamlit.app/](https://hirelens-ai-resume-analyzer.streamlit.app/)  

---

## 1. Abstract
In modern hiring workflows, corporate recruiters receive hundreds of candidate resumes for every open position. Manual screening of resumes is time-consuming, prone to human bias, and inefficient. While automated Applicant Tracking Systems (ATS) exist, many rely solely on rigid keyword matching, frequently eliminating qualified candidates who use alternative terminology or non-standard formatting.

This project presents **HireLens: AI-Powered Resume Screening, Skill Gap Analysis & Job Matching System** designed using Natural Language Processing (NLP) and Deep Learning text embeddings. The system extracts structured entities from PDF/DOCX resumes, maps technical competencies using a multi-domain skill taxonomy, and computes a composite ATS score utilizing Sentence-Transformers (`all-MiniLM-L6-v2`) and TF-IDF Cosine Similarity. Furthermore, the system provides candidate-centric feedback including skill gap analysis, missing keyword alerts, and an interactive Streamlit web dashboard.

---

## 2. Problem Statement
Job seekers often struggle to align their resumes with automated ATS algorithms, resulting in high rejection rates prior to human recruiter review. Conversely, hiring managers lack transparent tools to visually audit why a candidate was ranked high or low. Existing commercial tools are either expensive proprietary software or lack explainability.

**Core Objectives**:
1. Develop an automated parser capable of extracting clean text and contact details from PDF and DOCX resume formats.
2. Implement an NLP skill extraction engine to map candidate competencies across technical and soft skill categories.
3. Compute a weighted semantic similarity score using Sentence-Transformers (SBERT) embeddings and TF-IDF matrix representation.
4. Provide candidates with actionable recommendations to optimize missing keywords and improve ATS compliance.
5. Create an interactive web application featuring single-resume evaluation, batch candidate ranking, and Plotly skill radar charts.

---

## 3. System Architecture & Methodology

```
                          ┌───────────────────────────┐
                          │   Input Resume (PDF/DOCX) │
                          └─────────────┬─────────────┘
                                        │
                                        ▼
                          ┌───────────────────────────┐
                          │  Document Ingestion Engine│
                          │   (pdfplumber / docx)     │
                          └─────────────┬─────────────┘
                                        │
                                        ▼
                          ┌───────────────────────────┐
                          │ NLP Skill Taxonomy & NER  │
                          │    Skill Extraction       │
                          └─────────────┬─────────────┘
                                        │
                                        ▼
                          ┌───────────────────────────┐
                          │ ATS Scoring Hybrid Engine │
                          │ - SBERT Embeddings (45%)  │
                          │ - Skill Coverage (35%)    │
                          │ - TF-IDF Similarity (20%) │
                          └─────────────┬─────────────┘
                                        │
                                        ▼
                          ┌───────────────────────────┐
                          │  Streamlit Dashboard UI   │
                          │ - ATS Score & Rating      │
                          │ - Skill Radar Chart       │
                          │ - Missing Skill List      │
                          │ - Actionable AI Advice    │
                          └───────────────────────────┘
```

### Mathematical Formulation of ATS Score:
$$\text{ATS Score} = (0.45 \times \text{Sim}_{\text{SBERT}}) + (0.35 \times \text{Coverage}_{\text{Skill}}) + (0.20 \times \text{Sim}_{\text{TF-IDF}})$$

Where:
- $\text{Sim}_{\text{SBERT}}$: Cosine similarity between 384-dimensional dense SBERT embeddings of Resume and JD.
- $\text{Coverage}_{\text{Skill}}$: Percentage ratio of matched skills to total required job skills.
- $\text{Sim}_{\text{TF-IDF}}$: Classical term frequency-inverse document frequency cosine similarity.

---

## 4. Software & Hardware Requirements

### Software Requirements:
- **Operating System**: Windows 10/11, Linux, or macOS
- **Programming Language**: Python 3.10+
- **NLP & ML Libraries**: `sentence-transformers`, `scikit-learn`, `spacy`, `pdfplumber`, `python-docx`
- **Frontend & Visualization**: `streamlit`, `plotly`, `pandas`
- **Database**: `sqlite3`

### Hardware Requirements:
- **Processor**: Intel Core i5 / AMD Ryzen 5 or higher
- **RAM**: Minimum 8 GB (16 GB recommended for fast Transformer embedding computation)
- **Storage**: 2 GB free disk space

---

## 5. Module Description

| Module Name | File | Key Functions |
| :--- | :--- | :--- |
| **Document Parser** | `resume_parser.py` | Text extraction from PDF/DOCX, Regex contact info detection |
| **Skill Extractor** | `skill_extractor.py` | Taxonomy mapping across 7 technical categories, skill gap finder |
| **ATS Matcher Engine** | `ats_matcher.py` | SBERT embedding generator, TF-IDF matrix, weighted ATS scoring |
| **Recommendation Engine**| `recommendation_engine.py` | Formatting audit, missing keyword recommendations, impact advice |
| **Database Manager** | `db_manager.py` | SQLite database logging for evaluation history |
| **Web Dashboard** | `app.py` | Streamlit UI, Plotly radar charts, batch candidate ranker |
| **REST API Server** | `api.py` | FastAPI endpoints for external integration |

---

## 6. Expected Outcomes & Future Enhancements
- **Expected Outcomes**: A fully functional end-to-end web application that evaluates candidate resume compatibility against any job description, generates visually intuitive radar charts, and highlights missing keywords.
- **Future Scope**:
  - Fine-tuning SBERT on domain-specific IT resume datasets.
  - Adding automatic resume PDF rewriting with inserted keywords.
  - Integrating LLM-powered bullet point optimization using Llama-3 / Gemini models.

---

## 7. References
1. Reimers, N., & Gurevych, I. (2019). *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks*. arXiv preprint arXiv:1908.10084.
2. Pedregosa, F., et al. (2011). *Scikit-learn: Machine learning in Python*. Journal of Machine Learning Research, 12, 2825-2830.
3. Streamlit Documentation: *https://docs.streamlit.io/*
