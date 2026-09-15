"""
Generate HireLens PowerPoint Presentation (16:9 Widescreen)
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Theme Colors
    BG_DARK = RGBColor(3, 7, 18)
    CARD_BG = RGBColor(15, 23, 42)
    BORDER_COLOR = RGBColor(129, 140, 248)
    COLOR_INDIGO = RGBColor(129, 140, 248)
    COLOR_EMERALD = RGBColor(52, 211, 153)
    COLOR_PINK = RGBColor(244, 114, 182)
    COLOR_CYAN = RGBColor(56, 189, 248)
    TEXT_WHITE = RGBColor(255, 255, 255)
    TEXT_MUTED = RGBColor(203, 213, 225)

    def set_bg(slide):
        bg = slide.background
        fill = bg.fill
        fill.solid()
        fill.fore_color.rgb = BG_DARK

    def add_header(slide, title_text, category_text="HIRELENS MINOR PROJECT 1"):
        # Header category tag
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11), Inches(0.4))
        tf_tag = tag_box.text_frame
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = category_text.upper()
        p_tag.font.size = Pt(11)
        p_tag.font.bold = True
        p_tag.font.color.rgb = COLOR_INDIGO

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.5), Inches(0.8))
        tf_title = title_box.text_frame
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(26)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_WHITE

    # -------------------------------------------------------------------------
    # SLIDE 1: TITLE SLIDE
    # -------------------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1)

    # Big Card Container
    card1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(1.0), Inches(11.333), Inches(5.5))
    card1.fill.solid()
    card1.fill.fore_color.rgb = CARD_BG
    card1.line.color.rgb = BORDER_COLOR
    card1.line.width = Pt(2)

    # Title text box
    tb1 = s1.shapes.add_textbox(Inches(1.5), Inches(1.4), Inches(10.333), Inches(4.5))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p1 = tf1.paragraphs[0]
    p1.text = "🔍 HireLens"
    p1.font.size = Pt(44)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_INDIGO
    p1.space_after = Pt(10)

    p2 = tf1.add_paragraph()
    p2.text = "AI-Powered Resume Screening, Skill Gap Analysis & Job Matching System"
    p2.font.size = Pt(22)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_WHITE
    p2.space_after = Pt(25)

    p3 = tf1.add_paragraph()
    p3.text = "Minor Project 1 Presentation • Department of Artificial Intelligence & Machine Learning"
    p3.font.size = Pt(14)
    p3.font.color.rgb = COLOR_CYAN
    p3.space_after = Pt(30)

    p4 = tf1.add_paragraph()
    p4.text = "👥 Project Team:  Aryan (Roll: 28240533)  |  Nitish (Roll: 28240529)\n🏛️ Institution: Panipat Institute of Engineering & Technology (PIET)"
    p4.font.size = Pt(14)
    p4.font.bold = True
    p4.font.color.rgb = TEXT_WHITE

    # -------------------------------------------------------------------------
    # SLIDE 2: INTRODUCTION & PROBLEM STATEMENT
    # -------------------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2)
    add_header(s2, "Introduction & Problem Statement")

    # Card Left: Problem
    c_left = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2))
    c_left.fill.solid()
    c_left.fill.fore_color.rgb = CARD_BG
    c_left.line.color.rgb = COLOR_PINK
    c_left.line.width = Pt(1.5)

    tb_left = s2.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.8))
    tf_l = tb_left.text_frame
    tf_l.word_wrap = True

    p = tf_l.paragraphs[0]
    p.text = "⚠️ Challenges in Modern Recruitment"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_PINK
    p.space_after = Pt(14)

    bullets_l = [
        "High Application Volume: Recruiters receive 250+ resumes per job posting.",
        "Keyword Inflexibility: Traditional ATS tools use rigid exact-string matching.",
        "False Disqualifications: Candidates writing 'Neural Networks' get 0 score if JD says 'Deep Learning'.",
        "Lack of Transparency: Proprietary black-box algorithms provide zero explainability to job seekers."
    ]
    for b in bullets_l:
        p = tf_l.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(10)

    # Card Right: Solution
    c_right = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), Inches(1.6), Inches(5.6), Inches(5.2))
    c_right.fill.solid()
    c_right.fill.fore_color.rgb = CARD_BG
    c_right.line.color.rgb = COLOR_EMERALD
    c_right.line.width = Pt(1.5)

    tb_right = s2.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.2), Inches(4.8))
    tf_r = tb_right.text_frame
    tf_r.word_wrap = True

    p = tf_r.paragraphs[0]
    p.text = "✨ The HireLens AI Solution"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_EMERALD
    p.space_after = Pt(14)

    bullets_r = [
        "Deep Semantic Vectors: Sentence-Transformers (all-MiniLM-L6-v2) for context matching.",
        "7-Domain NLP Taxonomy: Multi-domain technical & soft skill coverage analysis.",
        "Hybrid ATS Scoring: Weighted fusion of SBERT, Skill Coverage, and TF-IDF similarity.",
        "Actionable Feedback: Missing keyword detection & interactive Streamlit web dashboard."
    ]
    for b in bullets_r:
        p = tf_r.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(10)

    # -------------------------------------------------------------------------
    # SLIDE 3: SYSTEM ARCHITECTURE & METHODOLOGY
    # -------------------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3)
    add_header(s3, "System Architecture & Processing Pipeline")

    steps = [
        ("1. Document Ingestion", "PDF & DOCX parsing via pdfplumber and python-docx text extraction engines.", COLOR_INDIGO),
        ("2. NLP Entity Mining", "Non-capturing regex contact extractor (Phone, Email, LinkedIn, GitHub).", COLOR_CYAN),
        ("3. Taxonomy Matching", "Categorizes candidate skills across 7 technical & soft skill domains.", COLOR_EMERALD),
        ("4. Hybrid ATS Scoring", "Weighted fusion of SBERT (45%), Skill Coverage (35%), and TF-IDF (20%).", COLOR_PINK)
    ]

    for idx, (title, desc, color) in enumerate(steps):
        left_pos = Inches(0.8 + idx * 3.0)
        c_step = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, left_pos, Inches(1.8), Inches(2.7), Inches(4.8))
        c_step.fill.solid()
        c_step.fill.fore_color.rgb = CARD_BG
        c_step.line.color.rgb = color
        c_step.line.width = Pt(1.5)

        tb_step = s3.shapes.add_textbox(left_pos + Inches(0.15), Inches(2.0), Inches(2.4), Inches(4.4))
        tf_s = tb_step.text_frame
        tf_s.word_wrap = True

        p = tf_s.paragraphs[0]
        p.text = title
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = color
        p.space_after = Pt(14)

        p2 = tf_s.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(13)
        p2.font.color.rgb = TEXT_MUTED

    # -------------------------------------------------------------------------
    # SLIDE 4: MATHEMATICAL ATS FORMULA & SBERT MECHANICS
    # -------------------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4)
    add_header(s4, "Mathematical ATS Formula & SBERT Embeddings")

    # Formula Card Top
    c_f = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.6), Inches(11.6), Inches(1.6))
    c_f.fill.solid()
    c_f.fill.fore_color.rgb = CARD_BG
    c_f.line.color.rgb = COLOR_INDIGO
    c_f.line.width = Pt(2)

    tb_f = s4.shapes.add_textbox(Inches(1.0), Inches(1.75), Inches(11.2), Inches(1.3))
    tf_f = tb_f.text_frame
    tf_f.word_wrap = True

    p = tf_f.paragraphs[0]
    p.text = "📐 Composite ATS Match Formula"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_INDIGO
    p.space_after = Pt(6)

    p2 = tf_f.add_paragraph()
    p2.text = "ATS Score = (0.45 × SBERT Cosine Sim) + (0.35 × Skill Coverage Ratio) + (0.20 × TF-IDF Cosine Sim)"
    p2.font.size = Pt(18)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_EMERALD

    # Card Left: SBERT
    c_sbert = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(3.5), Inches(5.6), Inches(3.4))
    c_sbert.fill.solid()
    c_sbert.fill.fore_color.rgb = CARD_BG
    c_sbert.line.color.rgb = COLOR_CYAN

    tb_sb = s4.shapes.add_textbox(Inches(1.0), Inches(3.7), Inches(5.2), Inches(3.0))
    tf_sb = tb_sb.text_frame
    tf_sb.word_wrap = True

    p = tf_sb.paragraphs[0]
    p.text = "🤖 SBERT Semantic Embeddings (45%)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN
    p.space_after = Pt(10)

    sb_points = [
        "Model: all-MiniLM-L6-v2 (384-dimensional dense vectors).",
        "Calculates cosine distance in deep vector space.",
        "Understands context & synonyms (e.g. PyTorch ≈ Deep Learning)."
    ]
    for pt in sb_points:
        p = tf_sb.add_paragraph()
        p.text = "• " + pt
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(6)

    # Card Right: Skill & TF-IDF
    c_tfidf = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), Inches(3.5), Inches(5.6), Inches(3.4))
    c_tfidf.fill.solid()
    c_tfidf.fill.fore_color.rgb = CARD_BG
    c_tfidf.line.color.rgb = COLOR_PINK

    tb_tf = s4.shapes.add_textbox(Inches(7.0), Inches(3.7), Inches(5.2), Inches(3.0))
    tf_tf = tb_tf.text_frame
    tf_tf.word_wrap = True

    p = tf_tf.paragraphs[0]
    p.text = "📊 Skill Coverage (35%) & TF-IDF (20%)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_PINK
    p.space_after = Pt(10)

    tf_points = [
        "Skill Coverage: Ratio of candidate matched skills vs total required skills.",
        "TF-IDF Vectorizer: Term Frequency-Inverse Document Frequency matrix.",
        "Verifies exact hard-keyword frequency presence in resume."
    ]
    for pt in tf_points:
        p = tf_tf.add_paragraph()
        p.text = "• " + pt
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(6)

    # -------------------------------------------------------------------------
    # SLIDE 5: MULTI-DOMAIN SKILL TAXONOMY ENGINE
    # -------------------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5)
    add_header(s5, "Multi-Domain Skill Taxonomy Engine")

    tax_box = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.6), Inches(11.6), Inches(5.2))
    tax_box.fill.solid()
    tax_box.fill.fore_color.rgb = CARD_BG
    tax_box.line.color.rgb = COLOR_INDIGO
    tax_box.line.width = Pt(1.5)

    tb_tax = s5.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.2), Inches(4.8))
    tf_tax = tb_tax.text_frame
    tf_tax.word_wrap = True

    p = tf_tax.paragraphs[0]
    p.text = "🏷️ 7 Standardized Technical & Soft Skill Categories"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_INDIGO
    p.space_after = Pt(14)

    cats = [
        ("Programming Languages", "Python, C++, Java, JavaScript, TypeScript, Go, Rust, R, SQL, Swift"),
        ("Machine Learning & AI", "PyTorch, TensorFlow, Scikit-Learn, OpenCV, SpaCy, HuggingFace, RAG, LLM"),
        ("Web Development", "React, Node.js, FastAPI, Flask, Django, HTML5, CSS3, Tailwind, REST API"),
        ("Cloud & DevOps", "AWS, Azure, GCP, Docker, Kubernetes, CI/CD, Terraform, Linux, Git, GitHub"),
        ("Databases", "PostgreSQL, MySQL, MongoDB, Redis, SQLite, Pinecone, ChromaDB"),
        ("Frameworks & Tools", "Pandas, NumPy, Matplotlib, Seaborn, Jupyter Notebooks, VS Code, JIRA"),
        ("Soft Skills", "Leadership, Problem Solving, Critical Thinking, Communication, Teamwork")
    ]

    for cat, items in cats:
        p = tf_tax.add_paragraph()
        p.text = f"• {cat}: {items}"
        p.font.size = Pt(13)
        p.font.bold = False
        p.font.color.rgb = TEXT_WHITE
        p.space_after = Pt(6)

    # -------------------------------------------------------------------------
    # SLIDE 6: STREAMLIT DASHBOARD & KEY FEATURES
    # -------------------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6)
    add_header(s6, "Interactive Dashboard & Key Application Features")

    f1 = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.6), Inches(2.4))
    f1.fill.solid()
    f1.fill.fore_color.rgb = CARD_BG
    f1.line.color.rgb = COLOR_CYAN

    tf = f1.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🎯 Single Resume Evaluation"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN
    p.space_after = Pt(6)
    p2 = tf.add_paragraph()
    p2.text = "Instant SBERT semantic score, match grade, skill coverage percentage, and non-capturing contact audit card."
    p2.font.size = Pt(12)
    p2.font.color.rgb = TEXT_MUTED

    f2 = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), Inches(1.6), Inches(5.6), Inches(2.4))
    f2.fill.solid()
    f2.fill.fore_color.rgb = CARD_BG
    f2.line.color.rgb = COLOR_EMERALD

    tf = f2.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🏆 Batch Candidate Leaderboard"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_EMERALD
    p.space_after = Pt(6)
    p2 = tf.add_paragraph()
    p2.text = "Upload multiple PDF/DOCX resumes to rank all candidates automatically against a single job description."
    p2.font.size = Pt(12)
    p2.font.color.rgb = TEXT_MUTED

    f3 = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(4.3), Inches(5.6), Inches(2.4))
    f3.fill.solid()
    f3.fill.fore_color.rgb = CARD_BG
    f3.line.color.rgb = COLOR_PINK

    tf = f3.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🕸️ Multi-Domain Skill Radar"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_PINK
    p.space_after = Pt(6)
    p2 = tf.add_paragraph()
    p2.text = "Plotly polar radar charts comparing candidate skills directly against target role requirements across 7 categories."
    p2.font.size = Pt(12)
    p2.font.color.rgb = TEXT_MUTED

    f4 = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), Inches(4.3), Inches(5.6), Inches(2.4))
    f4.fill.solid()
    f4.fill.fore_color.rgb = CARD_BG
    f4.line.color.rgb = COLOR_INDIGO

    tf = f4.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "📜 SQLite Log & Clear History"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_INDIGO
    p.space_after = Pt(6)
    p2 = tf.add_paragraph()
    p2.text = "Automatic audit trail persistence in ats_history.db with one-click clear evaluation history button."
    p2.font.size = Pt(12)
    p2.font.color.rgb = TEXT_MUTED

    # -------------------------------------------------------------------------
    # SLIDE 7: EXPERIMENTAL RESULTS & DEMO METRICS
    # -------------------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    set_bg(s7)
    add_header(s7, "Experimental Evaluation & Sample Results")

    res_box = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.6), Inches(11.6), Inches(5.2))
    res_box.fill.solid()
    res_box.fill.fore_color.rgb = CARD_BG
    res_box.line.color.rgb = COLOR_EMERALD
    res_box.line.width = Pt(1.5)

    tb_res = s7.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.2), Inches(4.8))
    tf_res = tb_res.text_frame
    tf_res.word_wrap = True

    p = tf_res.paragraphs[0]
    p.text = "📊 Sample Evaluation Output (ML Engineer Candidate)"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_EMERALD
    p.space_after = Pt(14)

    metrics = [
        ("Candidate Name", "Alex (Email: alex.dev@gmail.com | Phone: +91-7058291048)"),
        ("Target Role", "Machine Learning Engineer"),
        ("Final Composite ATS Score", "87.5%  [Grade: Exceptional Fit]"),
        ("SBERT Semantic Match", "84.3%  (Dense 384D Vector Cosine Sim)"),
        ("Skill Coverage Ratio", "90.0%  (9 Matched Skills / 10 Required)"),
        ("TF-IDF Keyword Similarity", "89.2%  (Term Frequency Matrix Cosine Sim)"),
        ("Matched Competencies", "Python, PyTorch, TensorFlow, Scikit-Learn, Docker, Kubernetes, AWS, Git, SQL"),
        ("Missing Skill Alert", "MLflow (Recommended for optimization)")
    ]

    for label, val in metrics:
        p = tf_res.add_paragraph()
        p.text = f"• {label}: {val}"
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_WHITE
        p.space_after = Pt(6)

    # -------------------------------------------------------------------------
    # SLIDE 8: FASTAPI REST MICROSERVICE
    # -------------------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    set_bg(s8)
    add_header(s8, "FastAPI REST Microservice Architecture")

    api_box = s8.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.6), Inches(11.6), Inches(5.2))
    api_box.fill.solid()
    api_box.fill.fore_color.rgb = CARD_BG
    api_box.line.color.rgb = COLOR_CYAN
    api_box.line.width = Pt(1.5)

    tb_api = s8.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.2), Inches(4.8))
    tf_api = tb_api.text_frame
    tf_api.word_wrap = True

    p = tf_api.paragraphs[0]
    p.text = "🌐 Headless REST API Endpoints (api.py)"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN
    p.space_after = Pt(14)

    api_points = [
        "GET / : Health check status & service metadata.",
        "GET /docs : Interactive Swagger UI API documentation.",
        "POST /api/v1/parse-resume : Accepts PDF/DOCX file upload, extracts raw text & non-capturing contact audit.",
        "POST /api/v1/analyze-match : Accepts JSON payload (resume text + JD text), calculates composite ATS scores, maps skill gaps, logs to SQLite database, and returns JSON response."
    ]

    for ap in api_points:
        p = tf_api.add_paragraph()
        p.text = "• " + ap
        p.font.size = Pt(14)
        p.font.color.rgb = TEXT_WHITE
        p.space_after = Pt(12)

    # -------------------------------------------------------------------------
    # SLIDE 9: FUTURE SCOPE & ENHANCEMENTS
    # -------------------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    set_bg(s9)
    add_header(s9, "Future Scope & System Enhancements")

    fut_box = s9.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.6), Inches(11.6), Inches(5.2))
    fut_box.fill.solid()
    fut_box.fill.fore_color.rgb = CARD_BG
    fut_box.line.color.rgb = COLOR_PINK
    fut_box.line.width = Pt(1.5)

    tb_fut = s9.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.2), Inches(4.8))
    tf_fut = tb_fut.text_frame
    tf_fut.word_wrap = True

    p = tf_fut.paragraphs[0]
    p.text = "🚀 Future Research & Technical Roadmap"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_PINK
    p.space_after = Pt(14)

    roadmap = [
        "1. Domain Fine-Tuning: Fine-tuning SBERT models on 100k+ technical resume datasets for industry specificity.",
        "2. LLM Bullet Optimizer: Integrating Llama-3 / Gemini models to auto-rewrite resume bullet points for high impact.",
        "3. Auto-Formatting PDF Generator: Exporting tailored ATS-compliant PDF resumes with missing keywords added.",
        "4. Enterprise HRMS Integration: Connectors for Workday, Greenhouse, and Lever recruiting pipelines."
    ]

    for rm in roadmap:
        p = tf_fut.add_paragraph()
        p.text = rm
        p.font.size = Pt(14)
        p.font.color.rgb = TEXT_WHITE
        p.space_after = Pt(14)

    # -------------------------------------------------------------------------
    # SLIDE 10: CONCLUSION & THANK YOU
    # -------------------------------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    set_bg(s10)

    card10 = s10.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(1.0), Inches(11.333), Inches(5.5))
    card10.fill.solid()
    card10.fill.fore_color.rgb = CARD_BG
    card10.line.color.rgb = COLOR_EMERALD
    card10.line.width = Pt(2)

    tb10 = s10.shapes.add_textbox(Inches(1.5), Inches(1.5), Inches(10.333), Inches(4.5))
    tf10 = tb10.text_frame
    tf10.word_wrap = True

    p = tf10.paragraphs[0]
    p.text = "🎓 Thank You!"
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = COLOR_EMERALD
    p.space_after = Pt(14)

    p2 = tf10.add_paragraph()
    p2.text = "HireLens: AI-Powered Resume Screening, Skill Gap Analysis & Job Matching System"
    p2.font.size = Pt(20)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_WHITE
    p2.space_after = Pt(20)

    p3 = tf10.add_paragraph()
    p3.text = "👥 Presented By: Aryan (Roll: 28240533) & Nitish (Roll: 28240529)\n🏛️ Panipat Institute of Engineering & Technology (PIET)\n🌐 GitHub: https://github.com/Aryan8182/Hirelens-ai-resume-analyzer\n🚀 Live Demo App: https://hirelens-ai-resume-analyzer.streamlit.app/"
    p3.font.size = Pt(14)
    p3.font.color.rgb = COLOR_INDIGO

    prs.save("HireLens_Presentation.pptx")
    print("HireLens_Presentation.pptx successfully created!")

if __name__ == "__main__":
    create_deck()
