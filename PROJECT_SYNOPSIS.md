# Project Synopsis
## on
# HireLens: AI-Powered Resume Screening, Skill Gap Analysis & Job Matching System

**Submitted in partial fulfillment for the award of the degree of**  
### Bachelor of Technology in Computer Science Engineering (Artificial Intelligence & Machine Learning)

**Submitted By**:  
- **Aryan** (Roll No: `28240533`)  
- **Nitish** (Roll No: `28240529`)  

**Under the Supervision of**:  
- **Prof. (Dr.) Devendra Parsad**, HOD CSE (AI & ML)  

**Panipat Institute of Engineering & Technology (PIET), Samalkha, Panipat**  
*Affiliated to Kurukshetra University Kurukshetra, India (2025–2026)*

---

## 📋 Project Credentials

| Field | Details |
| :--- | :--- |
| **Project Title** | HireLens: AI-Powered Resume Screening, Skill Gap Analysis & Job Matching System |
| **Project Domain/Area** | Natural Language Processing, Machine Learning & AI |
| **Group Members** | 1. Aryan (Roll No: `28240533`)<br/>2. Nitish (Roll No: `28240529`) |
| **Group Id** | *(To be allotted by project coordinator)* |
| **Supervisor's Name** | Prof. (Dr.) Devendra Parsad |
| **Supervisor's Designation** | HOD, CSE (AI & ML) |

---

## ✍️ Supervisor's Consent

> The synopsis of final year project work titled *"HireLens: AI-Powered Resume Screening, Skill Gap Analysis & Job Matching System"* by the students' group id ......... has been written with my consent and every section of this synopsis report is reflecting the work to be carried out by the group.
>  
> *(Signature of supervisor with date)*

---

## 🏛️ Department Project Evaluation Committee (DPEC) Remarks

The project is ……………………….. by DPEC. The group is advised to submit progress of the project work in progress presentation-1 to be held on……………………………………………….

**OR**

The project is ……………………….. by DPEC. The group is advised to submit the synopsis report again after making changes as suggested by DPEC on ……………………………………………………………….

**Name & Signature of DPEC member (s) with date**

---

# HireLens: AI-Powered Resume Screening, Skill Gap Analysis & Job Matching System

## 1. Introduction
Corporate recruitment pipelines routinely process hundreds of candidate resumes for every open position. Manual resume screening is time-consuming, labor-intensive, and inherently subjective. Traditional automated computational tools—such as legacy Applicant Tracking Systems (ATS)—rely strictly on exact keyword matching, frequency counting, or rigid string lookup. Consequently, these legacy ATS engines suffer from severe "synonym blindness", rejecting highly qualified candidates simply because they phrase their skills using different terminology (for example, writing "Deep Learning Neural Networks" instead of "Machine Learning").

Recent advances in Natural Language Processing (NLP) and foundation language models have introduced Sentence-Transformers (SBERT), enabling dense vector representations of textual semantics. SBERT maps sentences into a 384-dimensional dense vector space (`all-MiniLM-L6-v2`), allowing contextual variant effect prediction by computing the cosine similarity between candidate experience and job requirements—a method grounded in deep semantic textual similarity rather than superficial keyword overlap.

This project implements **HireLens**, an end-to-end, production-grade ATS screening platform that integrates SBERT vector embeddings with a 7-domain NLP skill taxonomy, non-capturing regex contact auditing, TF-IDF term frequency analysis, and SQLite audit trail persistence. Delivered as an interactive Streamlit web application and an enterprise FastAPI microservice, HireLens bridges cutting-edge artificial intelligence with recruitment automation to support fair, transparent, and reproducible talent acquisition.

---

## 2. Objective
The primary objective is to deploy a dual-vector semantic matching engine utilizing Sentence-BERT (`all-MiniLM-L6-v2`) for multi-factor resume-job description suitability scoring. Secondary objectives include:

- **Multi-Format Document Ingestion**: Developing a unified parsing engine (`pdfplumber` for PDF layout preservation, `python-docx` for DOCX) to extract clean raw text.
- **7-Domain Skill Taxonomy**: Constructing an NLP ontology engine (Programming, ML/AI, Web Dev, Cloud/DevOps, Databases, Tools, Soft Skills) to perform automated skill gap analysis.
- **Non-Capturing Regex Contact Audit**: Implementing regex patterns `(?:...)` to extract 10-13 digit Indian mobile numbers (+91-XXXXX-XXXXX) and emails without tuple truncation.
- **Hybrid ATS Scoring Algorithm**: Computing a weighted composite match score combining SBERT Semantic Match (45%), Skill Coverage Ratio (35%), and TF-IDF Keyword Match (20%).
- **Interactive Web UI & Logging**: Building a Streamlit Web Application featuring Plotly skill radar charts, batch candidate ranking leaderboards, and SQLite evaluation history logging (`ats_history.db`).
- **Enterprise REST Microservice**: Exposing FastAPI REST endpoints (`/api/v1/parse-resume`, `/api/v1/analyze-match`, `/api/v1/batch-rank`) for third-party HR integration.

---

## 3. Scope
The scope of this project encompasses the following key technical domains:

- **Theoretical Foundation**: Study of Sentence-BERT transformer architectures, cosine distance metric spaces, and NLP taxonomy rule engineering.
- **Model Integration**: Deployment of pre-trained `all-MiniLM-L6-v2` dense bi-encoder models for sub-second semantic vector generation.
- **Data Pipeline**: Multi-format document parsing (`pdfplumber`/`python-docx`) and regex-based entity cleaning for contact validation.
- **Inference System**: Implementation of a high-performance scoring algorithm calculating weighted composite ATS suitability scores.
- **Frontend Application**: Development of an interactive Streamlit web dashboard featuring dynamic role selection, Plotly polar radar charts, and candidate leaderboards.
- **Audit & Persistence**: Integration of SQLite (`ats_history.db`) for complete evaluation history logging with one-click clear log functionality.
- **REST API Infrastructure**: Creation of a FastAPI microservice backend providing OpenAPI Swagger documentation (`/docs`) for enterprise HR software integration.

---

## 4. Architecture
The HireLens architecture follows a modular, decoupled pipeline design comprising four core layers:

- **Backend Stack**: Python 3.10+, FastAPI microservice, SQLite database (`ats_history.db`).
- **AI & NLP Stack**: Sentence-Transformers (`all-MiniLM-L6-v2`), Scikit-Learn (TF-IDF vectorizer), SpaCy / NLTK, Regular Expressions (`re`).
- **Frontend Stack**: Streamlit web application, Plotly polar radar chart framework, Pandas dataframes.
- **Document Parsers**: `pdfplumber` (layout-aware PDF parsing), `python-docx` (DOCX paragraph & table parser).

### Prediction & Matching Logic:
1. Extract raw text from candidate resume & target job description.
2. Execute non-capturing regex contact auditor for Email and 10-13 digit Phone Numbers.
3. Categorize candidate skills across 7 technical taxonomy buckets.
4. Compute 384D SBERT dense vector embeddings & Cosine Similarity score.
5. Calculate composite score: $\text{ATS Score} = (0.45 \times \text{SBERT}) + (0.35 \times \text{Skill Ratio}) + (0.20 \times \text{TF-IDF})$.
6. Persist evaluation record to SQLite database and render Plotly radar chart.

---

## 5. Methodology

### 5.1 Data Preparation and Text Integration
- **Input Specification**: Candidate submits resume file (PDF, DOCX, or plain TXT) and target Job Description text.
- **Layout-Preserving Parsing**: `pdfplumber` extracts text streams while maintaining bounding box coordinate alignments across multi-column layouts.
- **Non-Capturing Contact Audit**: Implements non-capturing regex pattern `(?:\+91[\-\s]?)?[6-9]\d{9}` to extract full 10-13 digit Indian numbers without tuple truncation.

### 5.2 7-Domain Skill Extraction & Gap Analysis
Candidate skills are extracted using regex word boundary anchors `\b...\b` across 7 technical ontology categories: Programming Languages, ML & AI, Web Development, Cloud & DevOps, Databases, Frameworks & Tools, and Soft Skills. Skill Gap Ratio is computed as:
$$\text{Skill Ratio} = \frac{|\text{Candidate Skills} \cap \text{Required Job Skills}|}{|\text{Required Job Skills}|}$$

### 5.3 Model Inference & Scoring Engine
- **SBERT Encoding**: Resumes and JDs are passed through pre-trained `all-MiniLM-L6-v2` bi-encoders to generate 384-dimensional dense vectors.
- **Cosine Similarity**: Calculated as $\text{Cosine Sim}(A, B) = \frac{A \cdot B}{\|A\| \|B\|}$.
- **TF-IDF Similarity**: `TfidfVectorizer(ngram_range=(1,2))` computes bi-gram sparse term frequencies.
- **Composite Weighted Score**:
$$\text{ATS Score} = (0.45 \times \text{SBERT Sim}) + (0.35 \times \text{Skill Ratio}) + (0.20 \times \text{TF-IDF Sim})$$

### 5.4 Deployment, UI & Database Logging
- **Web Dashboard**: Interactive Streamlit UI featuring Plotly polar radar charts and batch candidate leaderboards.
- **Audit Trail**: Automatic logging of candidate name, role, ATS score, and timestamp to SQLite (`ats_history.db`).
- **REST Microservice**: Enterprise FastAPI backend (`api.py`) exposing OpenAPI JSON endpoints.

---

## 6. Conclusion

### 6.1 Key Highlights
- **Cutting-Edge SBERT AI**: Dense 384D vector space embeddings for contextual resume-job matching.
- **7-Domain Skill Ontology**: Automated skill extraction & gap analysis across 7 technical categories.
- **Non-Capturing Regex Auditor**: Robust parsing of full 10-13 digit Indian mobile numbers (`+91-XXXXX-XXXXX`) & emails.
- **Sub-1.8s Latency**: Fast end-to-end CPU execution without requiring expensive GPU infrastructure.
- **SQLite Audit Logger**: Persistent history database with one-click clear log functionality.

### 6.2 Limitations
- **Language Constraint**: Current NLP taxonomy models are monolingual (English text only).
- **Scanned Image PDFs**: Image-only scanned PDFs require optical character recognition (OCR) pre-processing.

---

## 7. Future Scope
- **Tesseract OCR Integration**: Add automated OCR image processing for scanned PDF resumes.
- **Vector DB Scaling**: Integrate FAISS or Qdrant vector databases for instant similarity search across 1,000,000+ resumes.
- **Multilingual Support**: Extend SBERT sentence transformers to support multi-language resume screening.
- **Automated Interview Generation**: Generate custom technical interview questions tailored to detected candidate skill gaps.

---

## 8. Hardware / Software Requirements
- **Programming Language**: Python 3.10+, SQL
- **ML & NLP Frameworks**: PyTorch / Sentence-Transformers (`all-MiniLM-L6-v2`), Scikit-Learn, SpaCy / NLTK
- **Web Frameworks**: Streamlit 1.28+, FastAPI 0.100+
- **Database**: SQLite3 (`ats_history.db`)
- **Libraries**: `pdfplumber`, `python-docx`, `plotly`, `pandas`, `numpy`, `requests`
- **Development Environment**: VS Code, PyCharm, PowerShell
- **Hardware Requirements**: Standard x86_64 CPU (Intel i5/i7 or AMD Ryzen 5/7, 8GB+ RAM), Serverless Cloud (Streamlit Cloud)

---

## 9. References
1. Reimers, N., & Gurevych, I. (2019). *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks*. arXiv preprint arXiv:1908.10084.
2. Salton, G., & Buckley, C. (1988). *Term-weighting approaches in automatic text retrieval*. Information Processing & Management, 24(5), 513-523.
3. Devlin, J., et al. (2019). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*. NAACL-HLT.
4. Bird, S., Klein, E., & Loper, E. (2009). *Natural Language Processing with Python*. O'Reilly Media.
5. Streamlit Documentation (2024). *Building Interactive Machine Learning Apps*. https://docs.streamlit.io/
6. FastAPI Framework (2024). *High Performance Python Web APIs*. https://fastapi.tiangolo.com/
