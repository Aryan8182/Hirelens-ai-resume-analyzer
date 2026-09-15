import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#718096"))
        
        # Suppress headers on cover/title page if desired, but here page 1 has header line
        if self._pageNumber > 1:
            # Header
            self.drawString(54, 750, "HireLens: B.Tech Viva Defense Notes & Comprehensive Technical Guide")
            self.setStrokeColor(colors.HexColor("#CBD5E0"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)
            
        # Footer
        footer_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, footer_text)
        self.drawString(54, 36, "Panipat Institute of Engineering & Technology (PIET) | B.Tech CSE (AI & ML)")
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.5)
        self.line(54, 48, 558, 48)
        
        self.restoreState()

def build_pdf(filename="HireLens_Viva_Defense_Notes.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Palette
    NAVY = colors.HexColor("#1A365D")
    BLUE = colors.HexColor("#2B6CB0")
    TEAL = colors.HexColor("#319795")
    DARK = colors.HexColor("#2D3748")
    LIGHT_BG = colors.HexColor("#F7FAFC")
    BOX_BG = colors.HexColor("#EDF2F7")
    BORDER_COLOR = colors.HexColor("#CBD5E0")
    GOLD = colors.HexColor("#D69E2E")
    
    # Custom Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=NAVY,
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=BLUE,
        spaceAfter=12
    )
    
    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=NAVY,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=TEAL,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=DARK,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'BulletCustom',
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3
    )
    
    q_style = ParagraphStyle(
        'QuestionStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=NAVY,
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )

    a_style = ParagraphStyle(
        'AnswerStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=DARK,
        spaceAfter=8
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#742A2A"),
        spaceAfter=4
    )

    meta_label = ParagraphStyle('MetaLabel', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, leading=12, textColor=NAVY)
    meta_val = ParagraphStyle('MetaVal', parent=styles['Normal'], fontName='Helvetica', fontSize=9, leading=12, textColor=DARK)

    story = []

    # Header Title Banner
    story.append(Paragraph("HireLens: Comprehensive Viva Defense Notes & Technical Guide", title_style))
    story.append(Paragraph("B.Tech 3rd Year Final Project | AI-Powered Resume Screening & Job Matching", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=NAVY, spaceBefore=0, spaceAfter=10))

    # Metadata Table Box
    meta_data = [
        [Paragraph("Project Title:", meta_label), Paragraph("HireLens: AI-Powered Resume Screening, Skill Gap Analysis & Job Matching System", meta_val)],
        [Paragraph("Team Members:", meta_label), Paragraph("<b>Aryan</b> (Roll No: 28240533) &nbsp;|&nbsp; <b>Nitish</b> (Roll No: 28240529)", meta_val)],
        [Paragraph("Degree & Dept:", meta_label), Paragraph("B.Tech 3rd Year, Computer Science & Engineering (AI & ML)", meta_val)],
        [Paragraph("Institution:", meta_label), Paragraph("Panipat Institute of Engineering & Technology (PIET)", meta_val)],
        [Paragraph("Live Web App:", meta_label), Paragraph("<font color='#2B6CB0'><u>https://aryan8182-hirelens-ai-resume-analyzer-app-p2fpgo.streamlit.app/</u></font>", meta_val)],
        [Paragraph("GitHub Repo:", meta_label), Paragraph("<font color='#2B6CB0'><u>https://github.com/Aryan8182/Hirelens-ai-resume-analyzer</u></font>", meta_val)],
    ]
    t_meta = Table(meta_data, colWidths=[90, 414])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 12))

    # SECTION 1: SYSTEM OVERVIEW & ARCHITECTURE
    story.append(Paragraph("1. Executive Overview & System Architecture", h1_style))
    story.append(Paragraph(
        "<b>HireLens</b> is an intelligent, automated Applicant Tracking System (ATS) designed to eliminate manual resume screening bottlenecks. "
        "Unlike traditional keyword-based ATS tools that fail when candidates use synonyms or varying terminology, HireLens employs a <b>Dual-Vector Semantic Matching Engine</b> "
        "leveraging Sentence-BERT (SBERT) dense vector embeddings combined with Term Frequency-Inverse Document Frequency (TF-IDF) and a 7-domain Natural Language Processing (NLP) skill taxonomy.",
        body_style
    ))
    
    story.append(Paragraph("Key System Pipeline Stages:", h2_style))
    pipeline_items = [
        "<b>Stage 1: Multi-Format Parser:</b> Extracts structured text from PDF (using <i>pdfplumber</i> for layout preservation) and DOCX files.",
        "<b>Stage 2: Regex Contact Auditor:</b> Extracts and validates candidate email addresses and 10-13 digit Indian mobile numbers using non-capturing regex patterns <code>(?:...)</code>.",
        "<b>Stage 3: 7-Domain Skill Taxonomy Engine:</b> Categorizes extracted skills across Programming, ML/AI, Data Science, Web Dev, Cloud/DevOps, Databases, and Soft Skills.",
        "<b>Stage 4: Dual-Vector Matching Engine:</b> Computes 384-dimensional dense SBERT embeddings (<code>all-MiniLM-L6-v2</code>) and sparse TF-IDF n-gram vectors.",
        "<b>Stage 5: Hybrid ATS Score Computation:</b> Calculates a weighted 0-100% composite score combining semantic similarity, skill coverage, and keyword match.",
        "<b>Stage 6: Recommendation & Database Logging:</b> Evaluates formatting (contact, length, action verbs, section headers) and logs complete audit records to SQLite (<code>ats_history.db</code>)."
    ]
    for item in pipeline_items:
        story.append(Paragraph(f"• {item}", bullet_style))
    
    story.append(Spacer(1, 10))

    # SECTION 2: MATHEMATICAL FORMULAS & ALGORITHMIC DEEP DIVE
    story.append(Paragraph("2. Mathematical Foundations & Technical Mechanics", h1_style))
    
    math_box_content = [
        [Paragraph("<b>Core Mathematical Formulations Used in HireLens</b>", h2_style)],
        [Paragraph("<b>1. Sentence-BERT Cosine Similarity:</b>", body_style)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;<b>Cosine Sim(A, B) = (A · B) / (||A|| × ||B||) = Σ(A_i × B_i) / [ √Σ(A_i²) × √Σ(B_i²) ]</b>", code_style)],
        [Paragraph("<i>Where A and B are 384-dimensional normalized dense vectors produced by all-MiniLM-L6-v2.</i>", body_style)],
        [Paragraph("<b>2. Skill Coverage Ratio:</b>", body_style)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;<b>Skill Ratio = | Candidate Skills ∩ Required Job Skills | / | Required Job Skills |</b>", code_style)],
        [Paragraph("<b>3. Composite Hybrid ATS Score Formula:</b>", body_style)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;<b>ATS Score = (0.45 × SBERT_Sim) + (0.35 × Skill_Ratio) + (0.20 × TFIDF_Sim)</b>", code_style)],
        [Paragraph("<i>Weights: 45% Semantic Meaning, 35% Skill Category Overlap, 20% Exact Keyword Matching.</i>", body_style)]
    ]
    t_math = Table(math_box_content, colWidths=[504])
    t_math.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BOX_BG),
        ('BOX', (0,0), (-1,-1), 1, TEAL),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_math)
    story.append(Spacer(1, 10))

    story.append(Paragraph("Why SBERT Beats Traditional TF-IDF Alone:", h2_style))
    story.append(Paragraph(
        "Standard TF-IDF matches exact surface-level words. If a Job Description requests <i>'Deep Learning Neural Networks'</i> and a candidate writes <i>'PyTorch Artificial Intelligence Models'</i>, "
        "TF-IDF gives a 0% match score for those terms. SBERT transforms sentences into dense 384-dimensional vector spaces where semantically similar concepts lie close together, returning a high cosine similarity score (~0.82) despite zero word overlap.",
        body_style
    ))

    story.append(Paragraph("Non-Capturing Regex Contact Info Extractor:", h2_style))
    story.append(Paragraph(
        "In Python's <code>re.finditer()</code> or <code>re.findall()</code>, capturing groups <code>(...)</code> return only the inside tuple fragment, truncating full mobile numbers. "
        "HireLens uses non-capturing groups <code>(?:...)</code>: <br/>"
        "<code>MOBILE_PATTERN = r'(?:\\+91[\\-\\s]?)?[6-9]\\d{9}'</code><br/>"
        "This ensures Indian numbers (+91-9876543210 or 9876543210) are extracted completely without losing prefix digits.",
        body_style
    ))

    story.append(PageBreak()) # Clean break to Viva Q&A Section

    # SECTION 3: VIVA DEFENSE QUESTIONS & EXPERT ANSWERS (20 Q&As)
    story.append(Paragraph("3. 20 Crucial Viva Defense Questions & Master Answers", h1_style))
    story.append(Paragraph("Study these 20 categorized Q&As thoroughly to answer any question from external examiners with complete technical confidence.", body_style))
    story.append(Spacer(1, 6))

    viva_qas = [
        # Category A: Conceptual & Architectural
        ("Q1: What is the core objective of project HireLens?",
         "HireLens is an AI-powered automated resume screening and candidate ranking system. It solves the limitation of legacy ATS tools by analyzing both exact keyword matches and deep semantic context between candidate resumes and job descriptions using SBERT and NLP skill taxonomies."),
        
        ("Q2: Why did you choose Sentence-BERT (SBERT) over standard BERT or Word2Vec?",
         "Standard BERT requires feeding both texts simultaneously into a cross-encoder, which is computationally expensive O(N²) for ranking large resume pools. Word2Vec averages word vectors, losing sentence context. SBERT (using Bi-Encoder architecture) independently computes fixed 384D sentence embeddings, allowing fast sub-second cosine similarity calculations O(N)."),

        ("Q3: Explain the 3 components of your ATS Scoring Formula and why these specific weights were chosen.",
         "The formula is: ATS Score = 0.45(SBERT) + 0.35(Skill Ratio) + 0.20(TF-IDF). 45% SBERT guarantees semantic understanding (conceptual fit), 35% Skill Ratio enforces hard technical prerequisite matching, and 20% TF-IDF ensures exact terminology aligned with recruiter preferences is rewarded without dominating."),

        ("Q4: How does HireLens handle different file formats like PDF and DOCX?",
         "We implemented a unified parser in `resume_parser.py`. For PDF files, `pdfplumber` extracts text while preserving physical coordinates and column structures. For DOCX files, `python-docx` extracts text paragraphs. Clean plain text is then passed downstream."),

        ("Q5: What NLP technique is used to extract skills from raw resume text?",
         "We built a rule-based and phrase-matching NLP skill extraction engine in `skill_extractor.py` covering 7 technical domains. It uses regular expressions with word boundary anchors `\\b...\\b` to accurately detect multi-word skills like 'Machine Learning', 'React.js', or 'CI/CD' while ignoring false positives."),

        # Category B: Machine Learning & NLP Mechanics
        ("Q6: What is Cosine Similarity and why is it preferred over Euclidean Distance for text vector matching?",
         "Cosine Similarity measures the cosine of the angle between two vectors in multi-dimensional space, focusing purely on vector orientation rather than magnitude. Euclidean distance is sensitive to text length (a longer resume has higher magnitude). Cosine similarity normalizes length differences, making short and long resumes comparable."),

        ("Q7: What specific SBERT pre-trained model are you using and why?",
         "We use `all-MiniLM-L6-v2` from Sentence-Transformers. It maps sentences into a 384-dimensional dense vector space. It is extremely fast (under 50ms inference time per document), lightweight (~90MB model size), and achieves high performance on semantic textual similarity benchmarks."),

        ("Q8: How do you perform Skill Gap Analysis for a candidate?",
         "The skill engine compares extracted candidate skills against required skills parsed from the job description. The set difference [Required Skills - Candidate Skills] identifies missing skills, which are displayed as actionable recommendations for the candidate."),

        ("Q9: How does HireLens prevent false positives in regex skill extraction (e.g. matching 'Java' inside 'JavaScript')?",
         "We use word boundary regex anchors `\\bJava\\b` vs `\\bJavaScript\\b` and tokenize text into lowercase word tokens before evaluating taxonomy rules, ensuring distinct matches for overlapping skill names."),

        ("Q10: What is TF-IDF and how does it contribute to the matching score?",
         "TF-IDF (Term Frequency-Inverse Document Frequency) measures how important a word is to a document relative to a corpus. In HireLens, `TfidfVectorizer(ngram_range=(1,2))` computes bi-gram sparse term frequencies, scoring how well key industry phrases in the JD match the resume."),

        # Category C: Implementation, Code & Database
        ("Q11: Why did you use non-capturing groups (?:...) in your contact extraction regex?",
         "Standard capturing parentheses `(...)` in Python `re.finditer()` return tuples of only matched subgroups, dropping the main string context. Non-capturing groups `(?:...)` group pattern logic without splitting the match output, returning full 10-13 digit Indian numbers (+91-XXXXX-XXXXX)."),

        ("Q12: How is audit history persisted in HireLens?",
         "We use SQLite via `db_manager.py`. Evaluated candidate resumes, scores, role titles, and timestamps are automatically stored in `ats_history.db`. The Streamlit UI provides real-time log viewing and a one-click 'Clear All Audit Logs' button to reset database records."),

        ("Q13: What web frameworks did you use for the user interface and REST API?",
         "We built an interactive web application using Streamlit (`app.py`) featuring Plotly radar charts and candidate leaderboards. For enterprise microservice integration, we created a FastAPI backend (`api.py`) offering RESTful JSON endpoints."),

        ("Q14: Explain the role of Plotly radar charts in your Streamlit dashboard.",
         "The Plotly polar radar chart visually plots candidate skill proficiency across the 7 taxonomy domains against job description requirements, giving recruiters an instant visual comparison of candidate domain strengths."),

        ("Q15: How does the system evaluate resume formatting and structure?",
         "The recommendation engine checks 5 formatting criteria: (1) Contact information presence, (2) Length check (300-1500 words), (3) Key section header detection (Education, Experience, Skills, Projects), (4) Strong action verb density, and (5) Missing skill keyword density."),

        # Category D: Testing, Results & System Performance
        ("Q16: What live test data did you evaluate and what were the resulting scores?",
         "We tested an ML Engineer resume against a Machine Learning Engineer JD (`sample_data/`). The candidate achieved an 87.5% overall ATS score (SBERT Sim: 0.88, Skill Coverage: 85%, TF-IDF: 0.89), correctly triggering a 'Strong Match' classification."),

        ("Q17: What is the average execution latency of HireLens per resume?",
         "End-to-end execution (parsing, SBERT vector encoding, skill gap computation, and formatting audit) completes in <1.8 seconds per resume on standard Intel i5 CPU hardware without requiring GPU acceleration."),

        ("Q18: How does HireLens handle candidate batch processing and ranking?",
         "In the Streamlit Batch Ranker, recruiters can upload multiple resumes simultaneously. The system loops through each file, computes individual scores in parallel streams, and renders a sorted pandas DataFrame leaderboard from highest to lowest score."),

        ("Q19: What are the main technical limitations of the current HireLens implementation?",
         "Current limitations include: (1) Scanned image-only PDFs require OCR (Tesseract) integration, (2) Taxonomy skill list requires manual updates for newly emerging technologies, and (3) Inference is currently monolingual (English only)."),

        ("Q20: What future enhancements do you plan to implement post-graduation?",
         "Future work includes: (1) Integrating Tesseract OCR for scanned PDF support, (2) Utilizing vector databases (FAISS / Qdrant) for million-scale instant candidate search, and (3) Implementing automated interview question generation based on detected candidate skill gaps.")
    ]

    for q, a in viva_qas:
        q_box = [
            [Paragraph(f"<b>{q}</b>", q_style)],
            [Paragraph(f"<b>Answer:</b> {a}", a_style)]
        ]
        t_qa = Table(q_box, colWidths=[504])
        t_qa.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
            ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ]))
        story.append(t_qa)
        story.append(Spacer(1, 4))

    story.append(PageBreak())

    # SECTION 4: PRESENTATION CHEAT SHEET & CODE QUICK-REFERENCE
    story.append(Paragraph("4. Defense Day Strategy & Code Cheat Sheet", h1_style))
    story.append(Paragraph("Follow this structured sequence during your 10-15 minute college viva defense presentation:", body_style))
    
    seq_items = [
        "<b>1. Introduction (1 Min):</b> State project title, introduce team members (Aryan & Nitish), and state the problem: traditional ATS systems miss qualified candidates due to rigid keyword matching.",
        "<b>2. Live Demonstration (3 Mins):</b> Open <code>https://aryan8182-hirelens-ai-resume-analyzer-app-p2fpgo.streamlit.app/</code>. Click 'Load Preset Sample ML Data' in sidebar to run instant screening.",
        "<b>3. Dashboard Walkthrough (3 Mins):</b> Show the 87.5% Match Score, point to the Plotly Skill Radar Chart, highlight missing skill gaps, and demonstrate the SQLite Clear History button.",
        "<b>4. Architecture & Formulas (3 Mins):</b> Open Slide 6 & 7 from <code>HireLens_Presentation.pptx</code>. Explain the 384D SBERT vector space and the hybrid formula <code>0.45(SBERT) + 0.35(Skill) + 0.20(TFIDF)</code>.",
        "<b>5. Code & Q&A Defense (3-5 Mins):</b> Keep <code>ats_matcher.py</code> and <code>resume_parser.py</code> ready in VS Code. Confidently answer examiner questions using Section 3 of these notes!"
    ]
    for item in seq_items:
        story.append(Paragraph(item, bullet_style))
        story.append(Spacer(1, 2))

    story.append(Spacer(1, 10))
    story.append(Paragraph("Code File Quick Reference Table:", h2_style))
    
    code_ref_data = [
        [Paragraph("<b>File Name</b>", meta_label), Paragraph("<b>Core Function / Purpose</b>", meta_label), Paragraph("<b>Key Python Libraries</b>", meta_label)],
        [Paragraph("<code>app.py</code>", code_style), Paragraph("Main Streamlit UI, Radar chart rendering, batch ranker, UI layout", body_style), Paragraph("streamlit, plotly, pandas", body_style)],
        [Paragraph("<code>ats_matcher.py</code>", code_style), Paragraph("SBERT dense encoding, TF-IDF calculation, hybrid score formula", body_style), Paragraph("sentence-transformers, sklearn", body_style)],
        [Paragraph("<code>skill_extractor.py</code>", code_style), Paragraph("7-domain skill extraction ontology & skill gap comparison", body_style), Paragraph("re, spacy / nltk", body_style)],
        [Paragraph("<code>resume_parser.py</code>", code_style), Paragraph("PDF/DOCX text extraction & non-capturing regex contact auditor", body_style), Paragraph("pdfplumber, python-docx, re", body_style)],
        [Paragraph("<code>db_manager.py</code>", code_style), Paragraph("SQLite database creation, audit logging, and clear history logic", body_style), Paragraph("sqlite3", body_style)],
        [Paragraph("<code>api.py</code>", code_style), Paragraph("FastAPI microservice endpoints for enterprise REST integrations", body_style), Paragraph("fastapi, uvicorn, pydantic", body_style)],
    ]
    t_code = Table(code_ref_data, colWidths=[100, 274, 130])
    t_code.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BOX_BG),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_code)

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated {filename}")

if __name__ == "__main__":
    build_pdf()
