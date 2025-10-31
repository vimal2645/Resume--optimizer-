from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from datetime import datetime
import io
import re

def extract_user_details(resume_text):
    lines = [line.strip() for line in resume_text.split('\n') if line.strip()]
    for line in lines:
        if 1 < len(line.split()) <= 4 and all(w[0].isupper() for w in line.split() if w[0].isalpha()) and '@' not in line:
            name = line
            break
    else:
        name = "Your Name"
    email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', resume_text)
    phone = re.search(r'(\+91[-\s]?|0)?[6-9]\d{9}', resume_text)
    return {"name": name, "email": email.group(0) if email else "your.email@example.com", "phone": phone.group(0) if phone else "+91-xxxxxx"}

def create_resume_docx(resume_text, job_keywords, score_data):
    user = extract_user_details(resume_text)
    doc = Document()
    for section in doc.sections:
        section.top_margin = Inches(0.6)
        section.bottom_margin = Inches(0.6)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)
    p = doc.add_paragraph()
    run = p.add_run(user['name'])
    run.font.size = Pt(14)
    run.font.bold = True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph(f"{user['email']} | {user['phone']}")
    doc.add_heading('SKILLS', level=1)
    all_skills = sorted(set(score_data['matched_keywords']) | set(score_data['missing_keywords']))
    doc.add_paragraph(', '.join(all_skills))
    doc.add_heading('ORIGINAL RESUME', level=1)
    for line in resume_text.splitlines()[:50]:
        doc.add_paragraph(line)
    doc.add_page_break()
    doc.add_heading('ATS Missing Skills to Add', level=1)
    if score_data['missing_keywords']:
        doc.add_paragraph("Add these to boost ATS score:")
        for skill in score_data['missing_keywords']:
            doc.add_paragraph(skill, style='List Bullet')
    doc_bytes = io.BytesIO()
    doc.save(doc_bytes)
    doc_bytes.seek(0)
    return doc_bytes

def create_cover_letter_docx(resume_text, job_keywords, score_data):
    user = extract_user_details(resume_text)
    doc = Document()
    doc.add_paragraph(user['name'])
    doc.add_paragraph(f"{user['email']} | {user['phone']}")
    doc.add_paragraph(datetime.now().strftime("%B %d, %Y"))
    doc.add_paragraph(f"{job_keywords.get('company', 'Company')}")
    doc.add_paragraph(f"Re: {job_keywords.get('job_title', 'Position')}")
    doc.add_paragraph("Dear Hiring Manager,")
    skills_str = ', '.join(score_data['matched_keywords'][:3]) if score_data['matched_keywords'] else 'relevant skills'
    doc.add_paragraph(f"I am interested in the {job_keywords.get('job_title', 'position')} at {job_keywords.get('company', 'your company')}. I have experience in {skills_str} and am eager to contribute to your team.")
    doc.add_paragraph("Sincerely,")
    doc.add_paragraph(user['name'])
    doc_bytes = io.BytesIO()
    doc.save(doc_bytes)
    doc_bytes.seek(0)
    return doc_bytes

def create_ats_report_docx(score_data, job_keywords):
    doc = Document()
    doc.add_heading('ATS REPORT', level=1)
    doc.add_paragraph(f"Score: {score_data['ats_score']}%")
    if score_data['matched_keywords']:
        doc.add_paragraph(f"Matched: {', '.join(score_data['matched_keywords'])}")
    if score_data['missing_keywords']:
        doc.add_paragraph(f"Missing: {', '.join(score_data['missing_keywords'])}")
    doc_bytes = io.BytesIO()
    doc.save(doc_bytes)
    doc_bytes.seek(0)
    return doc_bytes
