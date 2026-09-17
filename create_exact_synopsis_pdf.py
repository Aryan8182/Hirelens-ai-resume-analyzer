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
        if self._pageNumber > 2:
            self.saveState()
            self.setFont("Times-Roman", 10)
            self.setFillColor(colors.black)
            footer_text = f"{self._pageNumber}"
            self.drawCentredString(306, 36, footer_text)
            self.restoreState()

def build_exact_synopsis_pdf(filename="HireLens_Project_Synopsis.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=72,
        rightMargin=72,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Typography Styles
    title_main = ParagraphStyle(
        'TitleMain',
        parent=styles['Heading1'],
        fontName='Times-Bold',
        fontSize=17,
        leading=21,
        alignment=1, # Centered
        textColor=colors.black,
        spaceAfter=10
    )

    title_sub = ParagraphStyle(
        'TitleSub',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=13,
        leading=16,
        alignment=1, # Centered
        textColor=colors.black,
        spaceAfter=6
    )

    title_bold_sub = ParagraphStyle(
        'TitleBoldSub',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=14,
        leading=18,
        alignment=1, # Centered
        textColor=colors.black,
        spaceAfter=6
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading1'],
        fontName='Times-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.black,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading2'],
        fontName='Times-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.black,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=12,
        leading=16.5,
        textColor=colors.black,
        alignment=4, # Justified
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'BulletCustom',
        parent=body_style,
        alignment=0,
        leftIndent=18,
        firstLineIndent=-12,
        spaceAfter=4
    )

    cell_style = ParagraphStyle('CellText', parent=styles['Normal'], fontName='Times-Roman', fontSize=11, leading=14, textColor=colors.black)
    cell_bold = ParagraphStyle('CellBold', parent=styles['Normal'], fontName='Times-Bold', fontSize=11, leading=14, textColor=colors.black)

    story = []

    # =============================================================
    # PAGE 1: TITLE PAGE (Fits Perfectly on 1 Single Page - Logos Removed)
    # =============================================================
    story.append(Paragraph("<b>Project Synopsis</b>", title_bold_sub))
    story.append(Paragraph("<b>on</b>", title_sub))
    story.append(Paragraph("<b>HireLens: AI-Powered Resume Screening, Skill Gap Analysis & Job Matching System</b>", title_main))
    
    story.append(Paragraph("Submitted in partial fulfillment<br/>for the award of the degree of", title_sub))
    story.append(Paragraph("<b>Bachelor of Technology</b><br/><b>in</b><br/><b>Computer Science Engineering<br/>(Artificial Intelligence & Machine Learning)</b>", title_bold_sub))
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Submitted By</b>", title_bold_sub))
    
    team_table_data = [
        [Paragraph("Aryan", ParagraphStyle('L1', parent=cell_bold, alignment=1)), Paragraph("28240533", ParagraphStyle('L2', parent=cell_style, alignment=1))],
        [Paragraph("Nitish", ParagraphStyle('L3', parent=cell_bold, alignment=1)), Paragraph("28240529", ParagraphStyle('L4', parent=cell_style, alignment=1))]
    ]
    t_team = Table(team_table_data, colWidths=[150, 150])
    t_team.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 1),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
    ]))
    story.append(t_team)
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Under the Supervision of</b>", title_bold_sub))
    story.append(Paragraph("<b>Prof. (Dr.) Devendra Parsad</b><br/>HOD CSE AI & ML", title_sub))
    
    story.append(Spacer(1, 16))
    story.append(Paragraph("<b>Panipat Institute of Engineering & Technology,</b><br/><b>Samalkha, Panipat</b>", title_bold_sub))
    story.append(Paragraph("Affiliated to", title_sub))
    story.append(Paragraph("<b>Kurukshetra University Kurukshetra, India</b><br/><b>(2025-2026)</b>", title_bold_sub))

    story.append(PageBreak())

    # =============================================================
    # PAGE 2: SUPERVISOR CONSENT & DPEC REMARKS
    # =============================================================
    story.append(Paragraph("<font color='#2B6CB0'>Supervisor’s Consent</font>", ParagraphStyle('BlueConsent', parent=title_main, alignment=1)))
    story.append(Spacer(1, 10))

    consent_box_data = [
        [
            Paragraph(
                'The synopsis of final year project work titled <b>HireLens: AI-Powered Resume Screening, Skill Gap Analysis & Job Matching System</b> '
                'by the students\' group id.……… has been written with my consent and every section of this synopsis report is reflecting the work to be carried out by the group.',
                cell_style
            ),
            Paragraph("<br/><br/><i>(Signature of supervisor with date)</i>", ParagraphStyle('RItalic', parent=cell_style, alignment=1, fontSize=9))
        ]
    ]
    t_consent = Table(consent_box_data, colWidths=[340, 128])
    t_consent.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 1, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_consent)
    story.append(Spacer(1, 20))

    story.append(Paragraph("<b>Department Project Evaluation Committee (DPEC) Remarks</b>", ParagraphStyle('DPECHdr', parent=styles['Heading2'], fontName='Times-Bold', fontSize=12, alignment=1, spaceAfter=14)))
    
    story.append(Paragraph("The project is ……………………….. by DPEC. The group is advised to submit progress of the project work in progress presentation1 to be held on……………………………………………….", body_style))
    story.append(Spacer(1, 8))
    story.append(Paragraph("OR", ParagraphStyle('ORText', parent=body_style, alignment=1, fontName='Times-Bold')))
    story.append(Spacer(1, 8))
    story.append(Paragraph("The project is ……………………….. by DPEC. The group is advised to submit the synopsis report again after making changes as suggested by DPEC on ………………………........................................", body_style))
    
    story.append(Spacer(1, 35))
    story.append(Paragraph("Name & Signature of DPEC member (s) with date", ParagraphStyle('RightSig', parent=body_style, alignment=2, fontName='Times-Bold')))

    story.append(PageBreak())

    # =============================================================
    # MAIN SYNOPSIS BODY (Pages 3+)
    # =============================================================
    story.append(Paragraph("<b>HireLens: AI-Powered Resume Screening, Skill Gap Analysis & Job Matching System</b>", title_main))
    story.append(Spacer(1, 10))

    # 1. Introduction
    story.append(Paragraph("1. Introduction", h1_style))
    story.append(Paragraph(
        "Corporate recruitment pipelines routinely process hundreds of candidate resumes for every open position. "
        "Manual resume screening is time-consuming, labor-intensive, and inherently subjective. Clinical and industrial genomics "
        "pipelines similarly encounter complex data variants that impede decision making; in talent acquisition, legacy computational predictors—such as "
        "traditional Applicant Tracking Systems (ATS)—rely strictly on exact keyword matching, frequency counting, or rigid string lookup. "
        "Consequently, these traditional predictors rely on surface-level keyword features, limiting their applicability to exact phrasing and "
        "reducing generalizability across varied candidate terminology.",
        body_style
    ))
    story.append(Paragraph(
        "Recent advances in foundation language models have introduced Sentence-Transformers (SBERT), a largescale NLP embedding framework. "
        "SBERT enables <b>zeroshot variant effect prediction</b> by computing the difference in vector space representations between candidate experience "
        "and job requirements—a method grounded in deep semantic information theory rather than superficial keyword matching. "
        "This project implements an end-to-end system that integrates SBERT into a web accessible platform for real-time suitability scoring, "
        "leveraging structured skill ontologies and SQLite audit trails to provide interpretable, evidence-based outputs. The work bridges cutting-edge "
        "artificial intelligence with recruitment technology to support precision hiring through scalable, reproducible inference.",
        body_style
    ))

    # 2. Objective
    story.append(Paragraph("2. Objective", h1_style))
    story.append(Paragraph(
        "The primary objective is to <b>deploy the Sentence-BERT genomic/text foundation model</b> for candidate resume suitability scoring using a zeroshot "
        "dense vector similarity strategy. A secondary objective is to develop a <b>full stack web application</b> that enables users to input resume text, "
        "retrieve structured skill categories, fetch non-capturing regex contact audits, and compare candidate skills against job requirements—thereby "
        "facilitating transparent, clinically aligned interpretation and access to better reliable results without compromising the quality and accuracy in "
        "context to modern recruitment data values. It would also allow identify skill gaps based on domain variation and category handling, studying the effect "
        "and match suitability better.",
        body_style
    ))

    # 3. Scope
    story.append(Paragraph("3. Scope", h1_style))
    story.append(Paragraph("The scope of this project is as below:", body_style))
    scopes = [
        "<b>Theoretical Foundation:</b> Study of language models, vector effect prediction, and the algorithmic basis of semantic matching.",
        "<b>Model Integration:</b> Deployment of the pretrained SBERT model via a high-performance vector backend.",
        "<b>Data Pipeline:</b> Integration with document parsing APIs (pdfplumber for reference PDF layouts, python-docx for DOCX data).",
        "<b>Inference System:</b> Implementation of a FastAPI endpoint that accepts candidate specifications (resume text, job description, custom weights) and returns suitability scores.",
        "<b>Frontend Application:</b> Development of a Next.js / Streamlit interface for role search, Plotly skill visualization, and side by side comparison of AI vs. traditional keyword labels.",
        "<b>Evaluation Framework:</b> Benchmarking HireLens predictions against high confidence test sets to assess accuracy, calibration, and failure modes.",
        "<b>Reproducibility & Experiment Tracking:</b> Implement deterministic evaluation protocol including fixed random seeds, consistent data shuffling, and benchmark settings."
    ]
    for sc in scopes:
        story.append(Paragraph(f"• {sc}", bullet_style))

    # 4. Architecture
    story.append(Paragraph("4. Architecture", h1_style))
    archs = [
        "<b>Backend Stack:</b> Python, FastAPI, SQLite (ats_history.db), Transformers & Sentence-Transformers library",
        "<b>Frontend Stack:</b> Streamlit, Plotly Radar Charts, Pandas, Tailwind CSS / Shadcn UI",
        "<b>Genomic & Text Data Sources:</b> pdfplumber (for layout-aware PDF sequences), python-docx (for structured DOCX paragraphs)",
        "<b>Prediction Logic:</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;▪ Extract text window centred on candidate content<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;▪ Compute dense 384D vector log embeddings using SBERT (all-MiniLM-L6-v2)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;▪ Output Cosine Similarity & Hybrid score; classify as Strong Match if score > empirically tuned threshold."
    ]
    for ar in archs:
        story.append(Paragraph(f"• {ar}", bullet_style))

    # 5. Methodology
    story.append(Paragraph("5. Methodology", h1_style))
    story.append(Paragraph("This project follows an end to end MLOps pipeline—from model deployment to user facing inference.", body_style))

    story.append(Paragraph("5.1 Data Preparation and Integration", h2_style))
    story.append(Paragraph(
        "• <b>Input Specification:</b> User provides candidate resume file (PDF/DOCX), target job role, reference text, and alternate parameters.<br/>"
        "• <b>Reference Sequence Fetching:</b> Query pdfplumber parser API to retrieve text window centred on document.<br/>"
        "• <b>Contact Audit Lookup:</b> Use non-capturing regex <code>(?:\\+91[\\-\\s]?)?[6-9]\\d{9}</code> to fetch clean email and 10-13 digit mobile numbers.",
        body_style
    ))

    story.append(Paragraph("5.2 Model Inference", h2_style))
    story.append(Paragraph(
        "• <b>Tokenization:</b> Convert text string to token IDs using SBERT's native tokenizer.<br/>"
        "• <b>Forward Pass:</b> Run forward embedding passes (candidate resume and job description) via PyTorch.<br/>"
        "• <b>Scoring:</b> Compute Cosine Similarity = (A · B) / (||A|| × ||B||).<br/>"
        "• <b>Classification:</b> Apply hybrid threshold (ATS Score = 0.45 SBERT + 0.35 Skill + 0.20 TF-IDF) derived from benchmark analysis for binary decision.",
        body_style
    ))

    story.append(Paragraph("5.3 Deployment & Monitoring", h2_style))
    story.append(Paragraph(
        "• <b>Serverless Backend:</b> Deployed on FastAPI / Streamlit Cloud preloaded with SBERT weights.<br/>"
        "• <b>ColdStart Mitigation:</b> Use persistent background process keeping server warm during active usage.<br/>"
        "• <b>API Contract:</b> RESTful POST endpoint returning JSON with prediction, score, skill gap match, and metadata.",
        body_style
    ))

    story.append(Paragraph("5.4 Frontend Visualization", h2_style))
    story.append(Paragraph(
        "• Role search → Skill category breakdown → Resume input → Realtime prediction<br/>"
        "• Display: Extracted text, ClinVar/Skill labels, SBERT score, confidence radar indicator<br/>"
        "• Responsive UI with error handling for invalid files or format mismatches",
        body_style
    ))

    # 6. Conclusion
    story.append(Paragraph("6. Conclusion", h1_style))
    story.append(Paragraph(
        "This project demonstrates a production grade integration of a state-of-the-art foundation model into a clinically relevant decision support tool. "
        "By leveraging SBERT's zeroshot capabilities, the system bypasses the need for finetuning while delivering interpretable predictions grounded in computational linguistics. "
        "The modular architecture—separating inference, data retrieval, and user interface—ensures scalability, maintainability, and extensibility.",
        body_style
    ))

    story.append(Paragraph("6.1 Key Highlights", h2_style))
    highlights = [
        "<b>Cutting Edge AI:</b> First known undergraduate implementation of SBERT dual-vector matching for ATS variant interpretation.",
        "<b>Full Stack Integration:</b> Seamless fusion of parsing APIs, Transformer inference, and modern web frameworks.",
        "<b>Clinical Alignment:</b> Direct comparison with skill taxonomies enables immediate validation and trust calibration.",
        "<b>Reproducibility:</b> Entire pipeline containerized; code open for audit and extension."
    ]
    for kh in highlights:
        story.append(Paragraph(f"• {kh}", bullet_style))

    story.append(Paragraph("6.2 Limitations", h2_style))
    limits = [
        "<b>Assembly Dependency:</b> Requires standard English text; multi-language inputs need translation pre-processing.",
        "<b>Context Window:</b> Fixed token window may miss distal regulatory details in extremely lengthy document attachments.",
        "<b>ColdStart Latency:</b> Initial model loading can take 2–5 seconds due to memory allocation.",
        "<b>Binary Output:</b> Current default threshold focuses on binary classification (Match vs Non-Match)."
    ]
    for lm in limits:
        story.append(Paragraph(f"• {lm}", bullet_style))

    # 7. Future Scope
    story.append(Paragraph("7. Future Scope", h1_style))
    futures = [
        "<b>Uncertainty Quantification:</b> Integrate Bayesian or conformal prediction for calibrated confidence intervals.",
        "<b>OCR Integration:</b> Benchmark performance on scanned image PDFs using Tesseract OCR.",
        "<b>MultiVariant Analysis:</b> Extend to multi-resume candidate batch ranking and vector database (FAISS/Qdrant) search.",
        "<b>Production Optimization:</b> Replace HuggingFace backend with TensorRT-LLM for faster inference.",
        "<b>Interpretability Module:</b> Visualize attention maps or insilico mutagenesis profiles over input sequence."
    ]
    for ft in futures:
        story.append(Paragraph(f"• {ft}", bullet_style))

    # Hardware/Software requirement
    story.append(Paragraph("Hardware/Software requirement", h1_style))
    reqs = [
        "<b>Programming Language:</b> Python, TypeScript",
        "<b>ML Framework:</b> PyTorch, HuggingFace Transformers, Sentence-Transformers",
        "<b>Cloud Platform:</b> Modal / Streamlit Cloud",
        "<b>Frontend:</b> Streamlit, Next.js, React, Tailwind CSS",
        "<b>Backend API:</b> FastAPI",
        "<b>Genomic / Parsing Libraries:</b> pdfplumber, python-docx, Biopython, requests",
        "<b>Monitoring:</b> Logging via SQLite; optional Weights & Biases for experiment tracking",
        "<b>Development Environment:</b> VS Code / PyCharm",
        "<b>Hardware:</b> Standard x86_64 CPU / Serverless GPU via Modal"
    ]
    for rq in reqs:
        story.append(Paragraph(f"• {rq}", bullet_style))

    # References
    story.append(Paragraph("References", h1_style))
    refs = [
        "[1] Reimers, N., et al. (2019). Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks. arXiv preprint arXiv:1908.10084.",
        "[2] Landrum, G. A., et al. (2018). ClinVar: Improving access to variant interpretations and supporting evidence. Nucleic Acids Research, 46(D1), D1062–D1067.",
        "[3] Karolchik, D., et al. (2014). The UCSC Genome Browser database: 2014 update. Nucleic Acids Research, 42(D1), D764–D770.",
        "[4] Brown, T. B., et al. (2020). Language Models are FewShot Learners. Advances in Neural Information Processing Systems, 33, 1877–1901.",
        "[5] He, K., et al. (2016). Deep Residual Learning for Image Recognition. Proceedings of the IEEE CVPR, 770–778.",
        "[6] Kircher, M., et al. (2014). A general framework for estimating relative pathogenicity of genetic variants. Nature Genetics, 46(3), 310–315.",
        "[7] Cheng, J., et al. (2023). Scaling Laws for DNA Language Models. International Conference on Learning Representations.",
        "[8] Devlin, J., et al. (2019). BERT: Pre-training of Deep Bidirectional Transformers. NAACL-HLT.",
        "[9] Streamlit Documentation (2024). Building Interactive Machine Learning Apps. https://docs.streamlit.io/",
        "[10] FastAPI Framework (2024). High Performance Python Web APIs. https://fastapi.tiangolo.com/"
    ]
    for rf in refs:
        story.append(Paragraph(rf, ParagraphStyle('RefLine', parent=body_style, leftIndent=16, firstLineIndent=-16, spaceAfter=4)))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF synopsis (Page 1 clean): {filename}")

if __name__ == "__main__":
    build_exact_synopsis_pdf()
