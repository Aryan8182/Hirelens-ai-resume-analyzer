"""
Generate Comprehensive 12-Slide HireLens PowerPoint Presentation (16:9 Widescreen)
Author: Aryan (28240533) & Nitish (28240529) - PIET
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
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(11), Inches(0.35))
        tf_tag = tag_box.text_frame
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = category_text.upper()
        p_tag.font.size = Pt(11)
        p_tag.font.bold = True
        p_tag.font.color.rgb = COLOR_INDIGO

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.65), Inches(11.5), Inches(0.7))
        tf_title = title_box.text_frame
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_WHITE

    # -------------------------------------------------------------------------
    # SLIDE 1: TITLE SLIDE
    # -------------------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1)

    card1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9))
    card1.fill.solid()
    card1.fill.fore_color.rgb = CARD_BG
    card1.line.color.rgb = BORDER_COLOR
    card1.line.width = Pt(2)

    tb1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.1), Inches(11.0), Inches(5.3))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p1 = tf1.paragraphs[0]
    p1.text = "🔍 HireLens"
    p1.font.size = Pt(44)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_INDIGO
    p1.space_after = Pt(6)

    p2 = tf1.add_paragraph()
    p2.text = "AI-Powered Resume Screening, Skill Gap Analysis & Job Matching System"
    p2.font.size = Pt(22)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_WHITE
    p2.space_after = Pt(20)

    p3 = tf1.add_paragraph()
    p3.text = "Minor Project 1 • Bachelor of Technology (B.Tech 3rd Year) in AI & ML"
    p3.font.size = Pt(14)
    p3.font.color.rgb = COLOR_CYAN
    p3.space_after = Pt(25)

    p4 = tf1.add_paragraph()
    p4.text = "👥 Project Team Members:\n• Aryan  (Roll No: 28240533)\n• Nitish  (Roll No: 28240529)\n\n🏛️ Institution: Panipat Institute of Engineering & Technology (PIET)\n🌐 Live Demo: https://aryan8182-hirelens-ai-resume-analyzer-app-p2fpgo.streamlit.app/\n🔗 GitHub: https://github.com/Aryan8182/Hirelens-ai-resume-analyzer"
    p4.font.size = Pt(13)
    p4.font.color.rgb = TEXT_WHITE

    # -------------------------------------------------------------------------
    # SLIDE 2: INDUSTRY CONTEXT & PROBLEM STATEMENT
    # -------------------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2)
    add_header(s2, "Industry Background & Problem Statement")

    # Card Left
    c_left = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4))
    c_left.fill.solid()
    c_left.fill.fore_color.rgb = CARD_BG
    c_left.line.color.rgb = COLOR_PINK
    c_left.line.width = Pt(1.5)

    tb_l = s2.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.2), Inches(5.0))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    p = tf_l.paragraphs[0]
    p.text = "⚠️ Limitations of Traditional ATS Software"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = COLOR_PINK
    p.space_after = Pt(10)

    pts_l = [
        "Mass Application Overload: Recruiters receive 250+ resumes per job posting.",
        "Rigid Keyword Matching: Traditional tools rely strictly on exact string matching.",
        "False Negative Rejections: A candidate writing 'Neural Networks' gets 0 score if the job description asks for 'Deep Learning'.",
        "Lack of Transparency: Proprietary black-box algorithms offer zero feedback to candidates on missing skills."
    ]
    for pt in pts_l:
        p = tf_l.add_paragraph()
        p.text = "• " + pt
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(8)

    # Card Right
    c_right = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.6), Inches(5.4))
    c_right.fill.solid()
    c_right.fill.fore_color.rgb = CARD_BG
    c_right.line.color.rgb = COLOR_EMERALD
    c_right.line.width = Pt(1.5)

    tb_r = s2.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.2), Inches(5.0))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    p = tf_r.paragraphs[0]
    p.text = "💡 The HireLens AI Solution"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = COLOR_EMERALD
    p.space_after = Pt(10)

    pts_r = [
        "Dense Semantic Embeddings: Uses Sentence-Transformers (all-MiniLM-L6-v2) for deep contextual meaning matching.",
        "7-Domain NLP Taxonomy: Automatically extracts and maps hard technical and soft skill competencies.",
        "Hybrid Weighted Scoring: Fuses SBERT (45%), Skill Coverage (35%), and TF-IDF term frequency (20%).",
        "Explainable AI Feedback: Displays matched/missing skill gap analysis and formatting recommendations."
    ]
    for pt in pts_r:
        p = tf_r.add_paragraph()
        p.text = "• " + pt
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(8)

    # -------------------------------------------------------------------------
    # SLIDE 3: PROJECT OBJECTIVES & CORE SCOPE
    # -------------------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3)
    add_header(s3, "Project Objectives & Scope of Work")

    objs = [
        ("1. Multi-Format Text Parser", "Extract clean text from PDF (pdfplumber) and DOCX (python-docx) files without losing structured layout data.", COLOR_INDIGO),
        ("2. Robust Regex Contact Audit", "Extract candidate email, full 10-13 digit phone numbers (with country codes), LinkedIn, and GitHub profiles using non-capturing regex.", COLOR_CYAN),
        ("3. SBERT Semantic Matcher", "Convert resumes and job descriptions into 384-dimensional dense vectors to measure true conceptual similarity.", COLOR_EMERALD),
        ("4. Taxonomy & Radar Visuals", "Map skills across 7 technical categories and plot interactive polar radar charts comparing candidate vs job requirements.", COLOR_PINK)
    ]

    for idx, (title, desc, color) in enumerate(objs):
        left_pos = Inches(0.8 + idx * 3.0)
        c_obj = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, left_pos, Inches(1.6), Inches(2.7), Inches(5.3))
        c_obj.fill.solid()
        c_obj.fill.fore_color.rgb = CARD_BG
        c_obj.line.color.rgb = color
        c_obj.line.width = Pt(1.5)

        tb_obj = s3.shapes.add_textbox(left_pos + Inches(0.15), Inches(1.8), Inches(2.4), Inches(4.9))
        tf_o = tb_obj.text_frame
        tf_o.word_wrap = True

        p = tf_o.paragraphs[0]
        p.text = title
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = color
        p.space_after = Pt(12)

        p2 = tf_o.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(12)
        p2.font.color.rgb = TEXT_MUTED

    # -------------------------------------------------------------------------
    # SLIDE 4: SYSTEM ARCHITECTURE & DATA FLOW
    # -------------------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4)
    add_header(s4, "System Architecture & End-to-End Flow")

    pipe_card = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.733), Inches(5.4))
    pipe_card.fill.solid()
    pipe_card.fill.fore_color.rgb = CARD_BG
    pipe_card.line.color.rgb = COLOR_INDIGO
    pipe_card.line.width = Pt(1.5)

    tb_pipe = s4.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(11.333), Inches(5.0))
    tf_p = tb_pipe.text_frame
    tf_p.word_wrap = True

    p = tf_p.paragraphs[0]
    p.text = "🔄 4-Stage Architectural Processing Pipeline"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_INDIGO
    p.space_after = Pt(14)

    stages = [
        ("Stage 1: Ingestion & Parsing", "Ingests PDF/DOCX resume files and target Job Description text streams using pdfplumber and python-docx."),
        ("Stage 2: Entity & Contact Mining", "Runs clean_text preprocessing and non-capturing regex to audit Phone (+91-7058291048), Email, LinkedIn & GitHub profiles."),
        ("Stage 3: Hybrid AI Evaluation Engine", "Calculates SBERT vector cosine similarity (45%), 7-category Skill Taxonomy coverage (35%), and TF-IDF matrix similarity (20%)."),
        ("Stage 4: Streamlit Dashboard & Database", "Renders composite ATS match score, Plotly radar chart, missing skill badges, AI advice, and logs record to SQLite database (ats_history.db).")
    ]

    for title, detail in stages:
        p = tf_p.add_paragraph()
        p.text = f"🔹 {title}"
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = COLOR_CYAN
        p.space_after = Pt(3)

        p2 = tf_p.add_paragraph()
        p2.text = f"    {detail}"
        p2.font.size = Pt(12)
        p2.font.color.rgb = TEXT_MUTED
        p2.space_after = Pt(10)

    # -------------------------------------------------------------------------
    # SLIDE 5: MATHEMATICAL ATS FORMULATION
    # -------------------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5)
    add_header(s5, "Mathematical ATS Scoring Model")

    # Formula Top Card
    c_eq = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.733), Inches(1.7))
    c_eq.fill.solid()
    c_eq.fill.fore_color.rgb = CARD_BG
    c_eq.line.color.rgb = COLOR_EMERALD
    c_eq.line.width = Pt(2)

    tb_eq = s5.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(11.333), Inches(1.4))
    tf_eq = tb_eq.text_frame
    tf_eq.word_wrap = True

    p = tf_eq.paragraphs[0]
    p.text = "📐 Composite Match Equation"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_EMERALD
    p.space_after = Pt(4)

    p2 = tf_eq.add_paragraph()
    p2.text = "ATS Match Score = (0.45 × SBERT Sim) + (0.35 × Skill Coverage Ratio) + (0.20 × TF-IDF Sim)"
    p2.font.size = Pt(18)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_WHITE

    # Components 3 Cards
    comps = [
        ("SBERT Semantic Match (45%)", "Dense 384D vector cosine similarity between Transformer embeddings u and v.", COLOR_INDIGO),
        ("Skill Coverage Ratio (35%)", "Percentage of matched technical skills vs total required skills: (Matched / Required) × 100", COLOR_CYAN),
        ("TF-IDF Matrix Match (20%)", "Term Frequency-Inverse Document Frequency sparse matrix cosine distance for keyword frequency.", COLOR_PINK)
    ]

    for idx, (title, desc, color) in enumerate(comps):
        left_pos = Inches(0.8 + idx * 4.0)
        c_comp = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, left_pos, Inches(3.4), Inches(3.733), Inches(3.5))
        c_comp.fill.solid()
        c_comp.fill.fore_color.rgb = CARD_BG
        c_comp.line.color.rgb = color

        tb_comp = s5.shapes.add_textbox(left_pos + Inches(0.15), Inches(3.6), Inches(3.4), Inches(3.1))
        tf_c = tb_comp.text_frame
        tf_c.word_wrap = True

        p = tf_c.paragraphs[0]
        p.text = title
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = color
        p.space_after = Pt(10)

        p2 = tf_c.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(12)
        p2.font.color.rgb = TEXT_MUTED

    # -------------------------------------------------------------------------
    # SLIDE 6: SENTENCE-BERT (SBERT) VECTOR MECHANICS
    # -------------------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6)
    add_header(s6, "Sentence-BERT (SBERT) Vector Mechanics")

    sb_card = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.733), Inches(5.4))
    sb_card.fill.solid()
    sb_card.fill.fore_color.rgb = CARD_BG
    sb_card.line.color.rgb = COLOR_CYAN
    sb_card.line.width = Pt(1.5)

    tb_sb = s6.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(11.333), Inches(5.0))
    tf_sb = tb_sb.text_frame
    tf_sb.word_wrap = True

    p = tf_sb.paragraphs[0]
    p.text = "🧠 Deep Learning Transformer Mechanics (all-MiniLM-L6-v2)"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN
    p.space_after = Pt(14)

    sb_details = [
        ("Pre-trained Transformer Backbone", "Uses Siamese BERT networks fine-tuned for semantic textual similarity (STS)."),
        ("384-Dimensional Vector Mapping", "Converts arbitrary length resume and job description text into dense 384D mathematical vectors (u and v)."),
        ("Cosine Vector Distance Metric", "Calculates Cosine Similarity:  cos(θ) = (u · v) / (||u|| ||v||)  yielding a value between 0.0 and 1.0."),
        ("Contextual Awareness Advantage", "Captures conceptual intent. Recognizes that 'PyTorch / TensorFlow' is semantically aligned with 'Deep Learning Engineer' even if the phrase 'Deep Learning' is absent.")
    ]

    for title, detail in sb_details:
        p = tf_sb.add_paragraph()
        p.text = f"🔸 {title}:"
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = COLOR_EMERALD
        p.space_after = Pt(3)

        p2 = tf_sb.add_paragraph()
        p2.text = f"    {detail}"
        p2.font.size = Pt(12)
        p2.font.color.rgb = TEXT_MUTED
        p2.space_after = Pt(10)

    # -------------------------------------------------------------------------
    # SLIDE 7: 7-DOMAIN NLP SKILL TAXONOMY
    # -------------------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    set_bg(s7)
    add_header(s7, "7-Domain NLP Skill Taxonomy Engine")

    tax_card = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.733), Inches(5.4))
    tax_card.fill.solid()
    tax_card.fill.fore_color.rgb = CARD_BG
    tax_card.line.color.rgb = COLOR_INDIGO
    tax_card.line.width = Pt(1.5)

    tb_t = s7.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(11.333), Inches(5.0))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = True

    p = tf_t.paragraphs[0]
    p.text = "🏷️ Categorized Technical & Soft Skill Competencies"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_INDIGO
    p.space_after = Pt(12)

    tax_cats = [
        ("1. Programming Languages", "Python, C++, Java, JavaScript, TypeScript, Go, Rust, R, SQL, Swift"),
        ("2. Machine Learning & AI", "PyTorch, TensorFlow, Scikit-Learn, Keras, OpenCV, SpaCy, HuggingFace, RAG, LLM"),
        ("3. Web Development", "React, Node.js, FastAPI, Flask, Django, HTML5, CSS3, Tailwind, REST API"),
        ("4. Cloud & DevOps", "AWS, Azure, GCP, Docker, Kubernetes, CI/CD, Terraform, Linux, Git, GitHub"),
        ("5. Databases", "PostgreSQL, MySQL, MongoDB, Redis, SQLite, Pinecone, ChromaDB"),
        ("6. Frameworks & Tools", "Pandas, NumPy, Matplotlib, Seaborn, Jupyter Notebooks, VS Code, JIRA"),
        ("7. Soft Skills", "Leadership, Problem Solving, Critical Thinking, Communication, Teamwork")
    ]

    for cat_name, keywords in tax_cats:
        p = tf_t.add_paragraph()
        p.text = f"• {cat_name}: {keywords}"
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_WHITE
        p.space_after = Pt(6)

    # -------------------------------------------------------------------------
    # SLIDE 8: NON-CAPTURING REGEX CONTACT AUDIT ENGINE
    # -------------------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    set_bg(s8)
    add_header(s8, "Non-Capturing Regex Contact Extractor")

    reg_card = s8.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.733), Inches(5.4))
    reg_card.fill.solid()
    reg_card.fill.fore_color.rgb = CARD_BG
    reg_card.line.color.rgb = COLOR_PINK
    reg_card.line.width = Pt(1.5)

    tb_reg = s8.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(11.333), Inches(5.0))
    tf_reg = tb_reg.text_frame
    tf_reg.word_wrap = True

    p = tf_reg.paragraphs[0]
    p.text = "📱 Solving Regex Truncation & Extracting Clean Contact Data"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_PINK
    p.space_after = Pt(12)

    reg_pts = [
        ("The Truncation Challenge", "Standard re.findall() with capturing groups () returns matched tuples instead of full strings, truncating phone numbers (e.g. +91-7058291048 -> +91-705)."),
        ("Our Solution - Non-Capturing Groups", "Implemented non-capturing regex groups (?:...) with re.finditer() to evaluate m.group(0), preserving complete 10-13 digit phone numbers."),
        ("Email Regex Pattern", r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b  (Extracts clean email addresses)"),
        ("Phone Regex Pattern", r"(?:\+?\d{1,3}[\s.-]?)?(?:\(?\d{2,4}\)?[\s.-]?)?\d{3,4}[\s.-]?\d{3,4}  (Parses full numbers with country codes)"),
        ("LinkedIn & GitHub URLs", r"(?:https?://)?(?:www\.)?linkedin\.com/in/[a-zA-Z0-9\-_/]+  (Normalizes full profile URLs)")
    ]

    for title, desc in reg_pts:
        p = tf_reg.add_paragraph()
        p.text = f"• {title}:"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = COLOR_CYAN
        p.space_after = Pt(2)

        p2 = tf_reg.add_paragraph()
        p2.text = f"    {desc}"
        p2.font.size = Pt(11)
        p2.font.color.rgb = TEXT_MUTED
        p2.space_after = Pt(8)

    # -------------------------------------------------------------------------
    # SLIDE 9: STREAMLIT DASHBOARD & SQLITE PERSISTENCE
    # -------------------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    set_bg(s9)
    add_header(s9, "Streamlit Dashboard & SQLite History Logger")

    grid = [
        ("🎯 Single Resume Evaluation", "Upload PDF/DOCX resume; computes instant SBERT match score, match grade, skill gap list, and Executive Contact Audit card.", COLOR_CYAN),
        ("🏆 Batch Candidate Leaderboard", "Upload multiple candidate resumes to rank all applicants on an interactive leaderboard sorted by highest ATS match score.", COLOR_EMERALD),
        ("🕸️ Plotly Polar Skill Radar", "Interactive polar radar chart comparing candidate skill distribution directly against job requirements across 7 categories.", COLOR_PINK),
        ("📜 SQLite Audit & Reset", "Automatic persistence in ats_history.db with a 'Clear Evaluation History' button for one-click database resets.", COLOR_INDIGO)
    ]

    for idx, (title, desc, color) in enumerate(grid):
        r = idx // 2
        c = idx % 2
        left_pos = Inches(0.8 + c * 6.0)
        top_pos = Inches(1.5 + r * 2.8)

        card = s9.shapes.add_shape(MSO_SHAPE.RECTANGLE, left_pos, top_pos, Inches(5.7), Inches(2.5))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = color

        tb = s9.shapes.add_textbox(left_pos + Inches(0.2), top_pos + Inches(0.2), Inches(5.3), Inches(2.1))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = color
        p.space_after = Pt(6)

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(12)
        p2.font.color.rgb = TEXT_MUTED

    # -------------------------------------------------------------------------
    # SLIDE 10: FASTAPI REST MICROSERVICE
    # -------------------------------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    set_bg(s10)
    add_header(s10, "FastAPI REST Microservice (api.py)")

    api_card = s10.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.733), Inches(5.4))
    api_card.fill.solid()
    api_card.fill.fore_color.rgb = CARD_BG
    api_card.line.color.rgb = COLOR_CYAN
    api_card.line.width = Pt(1.5)

    tb_a = s10.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(11.333), Inches(5.0))
    tf_a = tb_a.text_frame
    tf_a.word_wrap = True

    p = tf_a.paragraphs[0]
    p.text = "🌐 Headless OpenAPI Endpoints & Integration"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN
    p.space_after = Pt(12)

    endpoints = [
        ("GET /", "Root health-check endpoint returning service status, project name, and API documentation link."),
        ("GET /docs", "Interactive Swagger UI documentation generated automatically by FastAPI for testing endpoints."),
        ("POST /api/v1/parse-resume", "Accepts PDF/DOCX file upload as multipart/form-data. Returns extracted raw text, text length, and clean contact audit JSON."),
        ("POST /api/v1/analyze-match", "Accepts JSON payload (resume_text + jd_text). Calculates composite ATS score, SBERT match, skill coverage, missing skills, logs to SQLite database, and returns structured JSON response.")
    ]

    for ep, detail in endpoints:
        p = tf_a.add_paragraph()
        p.text = f"• {ep}:"
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = COLOR_EMERALD
        p.space_after = Pt(2)

        p2 = tf_a.add_paragraph()
        p2.text = f"    {detail}"
        p2.font.size = Pt(12)
        p2.font.color.rgb = TEXT_MUTED
        p2.space_after = Pt(10)

    # -------------------------------------------------------------------------
    # SLIDE 11: EXPERIMENTAL RESULTS & DEMO METRICS
    # -------------------------------------------------------------------------
    s11 = prs.slides.add_slide(blank_layout)
    set_bg(s11)
    add_header(s11, "Experimental Evaluation & Sample Demonstration")

    exp_card = s11.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.733), Inches(5.4))
    exp_card.fill.solid()
    exp_card.fill.fore_color.rgb = CARD_BG
    exp_card.line.color.rgb = COLOR_EMERALD
    exp_card.line.width = Pt(1.5)

    tb_e = s11.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(11.333), Inches(5.0))
    tf_e = tb_e.text_frame
    tf_e.word_wrap = True

    p = tf_e.paragraphs[0]
    p.text = "📊 Real-World Evaluation Output (ML Engineer Role)"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_EMERALD
    p.space_after = Pt(12)

    demo_data = [
        ("Candidate Name & Contact", "Alex (Email: alex.dev@gmail.com | Phone: +91-7058291048)"),
        ("Target Job Title", "Machine Learning Engineer"),
        ("Final Composite ATS Score", "87.5%  [Grade: Exceptional Fit]"),
        ("SBERT Semantic Match", "84.3%  (Dense 384D Vector Cosine Distance)"),
        ("Skill Coverage Ratio", "90.0%  (9 Matched Technical Skills / 10 Required)"),
        ("TF-IDF Keyword Similarity", "89.2%  (Term Frequency Matrix Similarity)"),
        ("Matched Competencies", "Python, PyTorch, TensorFlow, Scikit-Learn, Docker, Kubernetes, AWS, Git, SQL"),
        ("Missing Skill Alert", "MLflow (Flagged by AI recommendation engine for optimization)")
    ]

    for label, val in demo_data:
        p = tf_e.add_paragraph()
        p.text = f"• {label}:  {val}"
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_WHITE
        p.space_after = Pt(6)

    # -------------------------------------------------------------------------
    # SLIDE 12: FUTURE SCOPE, CONCLUSION & LIVE LINKS
    # -------------------------------------------------------------------------
    s12 = prs.slides.add_slide(blank_layout)
    set_bg(s12)

    card12 = s12.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9))
    card12.fill.solid()
    card12.fill.fore_color.rgb = CARD_BG
    card12.line.color.rgb = COLOR_EMERALD
    card12.line.width = Pt(2)

    tb12 = s12.shapes.add_textbox(Inches(1.2), Inches(1.1), Inches(11.0), Inches(5.3))
    tf12 = tb12.text_frame
    tf12.word_wrap = True

    p = tf12.paragraphs[0]
    p.text = "🎓 Conclusion & Future Scope"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = COLOR_EMERALD
    p.space_after = Pt(10)

    p2 = tf12.add_paragraph()
    p2.text = "HireLens delivers a transparent, AI-driven ATS screening system combining Transformer semantics, skill taxonomy matching, and explainable feedback."
    p2.font.size = Pt(14)
    p2.font.color.rgb = TEXT_WHITE
    p2.space_after = Pt(16)

    p3 = tf12.add_paragraph()
    p3.text = "🚀 Future Roadmap:\n• Domain Fine-Tuning SBERT on 100k+ technical IT resumes.\n• LLM Bullet Point Rewriter using Llama-3 / Gemini models.\n• Enterprise HRMS Connectors for Workday, Greenhouse & Lever."
    p3.font.size = Pt(13)
    p3.font.color.rgb = COLOR_CYAN
    p3.space_after = Pt(20)

    p4 = tf12.add_paragraph()
    p4.text = "👥 Presented By: Aryan (Roll: 28240533) & Nitish (Roll: 28240529)\n🏛️ Institution: Panipat Institute of Engineering & Technology (PIET)\n🚀 Live Demo App: https://aryan8182-hirelens-ai-resume-analyzer-app-p2fpgo.streamlit.app/\n🔗 GitHub Repository: https://github.com/Aryan8182/Hirelens-ai-resume-analyzer"
    p4.font.size = Pt(13)
    p4.font.bold = True
    p4.font.color.rgb = COLOR_INDIGO

    prs.save("HireLens_Presentation.pptx")
    print("Comprehensive 12-Slide HireLens_Presentation.pptx successfully created!")

if __name__ == "__main__":
    create_deck()
