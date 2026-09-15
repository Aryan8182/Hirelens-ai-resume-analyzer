"""
=============================================================================
Minor Project 1: AI-Powered Resume Screening & ATS Optimizer
File: resume_parser.py
Author: B.Tech 3rd Year AI & ML Project
Description: Handles extraction of clean text from PDF and DOCX resume files,
             regex-based contact details extraction, and basic sectioning.
=============================================================================
"""

import sys
import site
if site.USER_SITE not in sys.path:
    sys.path.append(site.USER_SITE)

import re
import io

try:
    import pdfplumber
except ImportError:
    pdfplumber = None

try:
    from docx import Document
except ImportError:
    Document = None


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extracts raw text from PDF file bytes using pdfplumber.
    """
    text = ""
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"[Error] PDF Parsing Failed: {e}")
    return text.strip()


def extract_text_from_docx(file_bytes: bytes) -> str:
    """
    Extracts raw text from DOCX file bytes using python-docx.
    """
    text = ""
    try:
        doc = Document(io.BytesIO(file_bytes))
        for para in doc.paragraphs:
            if para.text.strip():
                text += para.text.strip() + "\n"
    except Exception as e:
        print(f"[Error] DOCX Parsing Failed: {e}")
    return text.strip()


def parse_resume_file(file_name: str, file_bytes: bytes) -> str:
    """
    Determines file extension and routes to appropriate parser function.
    """
    ext = file_name.lower().split('.')[-1]
    if ext == 'pdf':
        return extract_text_from_pdf(file_bytes)
    elif ext in ['docx', 'doc']:
        return extract_text_from_docx(file_bytes)
    elif ext == 'txt':
        return file_bytes.decode('utf-8', errors='ignore')
    else:
        raise ValueError(f"Unsupported file format: .{ext}. Please upload PDF, DOCX, or TXT.")


def clean_text(text: str) -> str:
    """
    Preprocesses raw text by removing excessive whitespace, special characters,
    and converting to lowercase for normalized NLP analysis.
    """
    # Replace newlines and tabs with spaces
    text = re.sub(r'[\r\n\t]+', ' ', text)
    # Remove bullet points and special symbols
    text = re.sub(r'[•▪■►❖*]', ' ', text)
    # Collapse multiple spaces
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_contact_info(raw_text: str) -> dict:
    """
    Extracts email, phone number, LinkedIn profile, and GitHub profile from raw resume text using robust non-capturing regular expressions.
    """
    # 1. Email Extraction
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
    emails = [m.group(0).strip() for m in re.finditer(email_pattern, raw_text)]

    # 2. Phone Extraction (Full 10-13 digit numbers with country code/formatting)
    phone_pattern = r'(?:\+?\d{1,3}[\s.-]?)?(?:\(?\d{2,4}\)?[\s.-]?)?\d{3,4}[\s.-]?\d{3,4}'
    phone_matches = [m.group(0).strip() for m in re.finditer(phone_pattern, raw_text)]
    valid_phones = [p for p in phone_matches if 10 <= len(re.sub(r'\D', '', p)) <= 13]

    # 3. LinkedIn Profile URL Extraction
    linkedin_pattern = r'(?:https?://)?(?:www\.)?linkedin\.com/in/[a-zA-Z0-9\-_/]+'
    linkedins = [m.group(0).strip() for m in re.finditer(linkedin_pattern, raw_text, re.IGNORECASE)]

    # 4. GitHub Profile URL Extraction
    github_pattern = r'(?:https?://)?(?:www\.)?github\.com/[a-zA-Z0-9\-_/]+'
    githubs = [m.group(0).strip() for m in re.finditer(github_pattern, raw_text, re.IGNORECASE)]

    # Normalize URLs
    linkedin_url = "Not Found"
    if linkedins:
        url = linkedins[0].rstrip('/.')
        if not url.startswith('http'):
            url = f"https://{url}"
        linkedin_url = url

    github_url = "Not Found"
    if githubs:
        url = githubs[0].rstrip('/.')
        if not url.startswith('http'):
            url = f"https://{url}"
        github_url = url

    return {
        "email": emails[0] if emails else "Not Found",
        "phone": valid_phones[0] if valid_phones else "Not Found",
        "linkedin": linkedin_url,
        "github": github_url
    }


def extract_resume_sections(raw_text: str) -> dict:
    """
    Segments resume text into key sections based on standard section headers.
    """
    sections = {
        "summary": "",
        "skills": "",
        "experience": "",
        "education": "",
        "projects": "",
        "certifications": ""
    }

    # Standard section headers regex
    headers = {
        "summary": r'(summary|profile|about me|objective)',
        "skills": r'(skills|technical skills|key competencies|technologies)',
        "experience": r'(work experience|experience|employment history|work history)',
        "education": r'(education|academic background|qualifications)',
        "projects": r'(projects|personal projects|academic projects)',
        "certifications": r'(certifications|licenses|certifications & courses)'
    }

    lines = raw_text.split('\n')
    current_section = None

    for line in lines:
        line_clean = line.strip().lower()
        matched_header = False
        for sec_name, pattern in headers.items():
            if re.match(r'^' + pattern + r'[:\s]*$', line_clean):
                current_section = sec_name
                matched_header = True
                break

        if not matched_header and current_section:
            sections[current_section] += line + " "

    return {k: v.strip() for k, v in sections.items()}


if __name__ == "__main__":
    # Test script with dummy text
    sample_text = """
    John Doe
    Email: john.doe@email.com | Phone: +1 123-456-7890
    LinkedIn: linkedin.com/in/johndoe | GitHub: github.com/johndoe

    TECHNICAL SKILLS
    Python, Java, Machine Learning, TensorFlow, PyTorch, SQL, Pandas, NumPy, Git.

    WORK EXPERIENCE
    Data Science Intern - Tech Corp (2023 - Present)
    Developed predictive models using scikit-learn and SpaCy for text classification.

    EDUCATION
    B.Tech in Artificial Intelligence & Machine Learning - 2024
    """

    print("--- Contact Info Extracted ---")
    print(extract_contact_info(sample_text))
    print("\n--- Cleaned Text Snippet ---")
    print(clean_text(sample_text)[:150])
