# 🔍 HireLens: AI-Powered Resume Screening, Skill Gap Analysis & Job Matching System

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B.svg)](https://streamlit.io/)
[![Sentence-Transformers](https://img.shields.io/badge/SBERT-all--MiniLM--L6--v2-7C3AED.svg)](https://www.sbert.net/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**HireLens** is an advanced, AI-powered Applicant Tracking System (ATS) and resume screening application built for recruiters and candidates. It combines **Sentence-BERT (SBERT)** dense vector embeddings, **TF-IDF keyword frequency matrices**, and an **NLP multi-domain skill taxonomy** to compute accurate, transparent candidate-job match scores.

---

## ✨ Key Features

- **🎯 Single Resume Deep Evaluation**: Instant SBERT semantic similarity matching, skill coverage scoring, and candidate contact extraction (Email, Phone, LinkedIn, GitHub).
- **🏆 Batch Candidate Ranking**: Upload multiple resumes simultaneously to automatically rank candidates on a dynamic leaderboard.
- **🕸️ Multi-Domain Skill Radar**: Plotly polar radar charts comparing candidate skills against job requirements across 7 technical categories.
- **📜 SQLite Audit Trail & One-Click Reset**: Comprehensive evaluation logging saved to `ats_history.db` with one-click clear logs functionality.
- **⚡ Dynamic Weight Sliders**: Real-time adjustment of semantic, skill coverage, and keyword weight formulas.
- **🎨 Glassmorphic Dark UI**: High-contrast, Vercel/Linear AI-inspired dark design system optimized for maximum readability.
- **🌐 FastAPI REST Server**: Optional OpenAPI Swagger endpoints (`/docs`) for programmatic integration.

---

## 🛠️ Architecture & ATS Match Formula

The system calculates a composite ATS match score using the following weighted formula:

$$\text{ATS Score} = (0.45 \times \text{Sim}_{\text{SBERT}}) + (0.35 \times \text{Coverage}_{\text{Skill}}) + (0.20 \times \text{Sim}_{\text{TF-IDF}})$$

- **SBERT Semantic Similarity (45%)**: Captures deep contextual meaning using 384-dimensional embeddings (`all-MiniLM-L6-v2`).
- **Skill Coverage (35%)**: Evaluates technical skill overlap across 7 NLP taxonomy categories.
- **TF-IDF Similarity (20%)**: Classical term frequency matrix cosine similarity for exact keyword matches.

---

## 🚀 Quick Start Guide

### 1. Clone the Repository
```bash
git clone https://github.com/Aryan8182/Hirelens-ai-resume-analyzer.git
cd Hirelens-ai-resume-analyzer
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the Streamlit Web App
```bash
streamlit run app.py
```
Open **`http://localhost:8501`** in your browser.

### 4. (Optional) Launch FastAPI REST API
```bash
uvicorn api:app --reload
```
View Swagger API documentation at **`http://localhost:8000/docs`**.

---

## 📁 Repository Structure

```
Hirelens-ai-resume-analyzer/
├── app.py                      # Main Streamlit Dashboard & High-Contrast UI
├── resume_parser.py            # PDF/DOCX Parsing & Regex Contact Extractor
├── skill_extractor.py          # 7-Category NLP Taxonomy & Skill Coverage Analyzer
├── ats_matcher.py              # SBERT Embedding Generator & TF-IDF Match Formula
├── recommendation_engine.py    # ATS Formatting Audit & Actionable Advice Engine
├── db_manager.py               # SQLite History Logger & Clear Log Manager
├── api.py                      # FastAPI REST API Endpoints
├── test_suite.py               # Automated Unit Test Suite
├── headless_test.py            # 6-Module System Verification Script
├── PROJECT_SYNOPSIS.md         # B.Tech Project Synopsis Report Document
├── requirements.txt            # Python Dependencies
└── sample_data/                # Preset Test Data (ML Job Description & Resume)
```

---

## 🧪 Running Tests

Run the complete 6-module verification test suite:
```bash
python headless_test.py
```

Run unit tests:
```bash
python -m unittest test_suite.py
```

---

## 👤 Author & License

- **Author**: B.Tech 3rd Year AI & ML Minor Project
- **GitHub Repository**: [Aryan8182/Hirelens-ai-resume-analyzer](https://github.com/Aryan8182/Hirelens-ai-resume-analyzer)
- **License**: MIT License
