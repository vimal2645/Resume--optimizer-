AI Resume Optimizer is a web app that helps job seekers compare their resume against a target job description, calculate an ATS-style match score, highlight matched and missing skills, and download optimized DOCX files (resume, cover letter, and ATS report).

Tech Stack
Language: Python 3

Frontend/UI: Streamlit (custom CSS for animated, modern UI)

Core Logic:

core.parser – parses resume (PDF/DOCX) and job description into clean text and skills

utils.ai_skill_matcher – computes enhanced ATS score, matched skills, and missing skills

utils.document_generator – generates DOCX resume, cover letter, and ATS report

Libraries: python-docx, python-dotenv, datetime, re, io

Deployment: Streamlit Cloud (auto-deploy from GitHub)

Monetization: Adsterra banner ads embedded via streamlit.components.v1.components.html

What the App Does
Input:

User uploads a resume (PDF or DOCX).

User pastes a job description into a text area.

Processing:

The app extracts text and skills from the resume and JD.

It compares JD “must-have” skills with resume skills.

It calculates an ATS score, total keywords, matched count, missing count, and lists of matched/missing skills.

UI Output:

Animated ATS score card.

Metrics for matched, missing, and score vs average.

Badges for matched skills and missing skills in two columns.

Downloads:

Optimized Resume (DOCX): Includes basic user info, skills section (matched + missing), and original resume content snippet, plus ATS-based suggestions.

Cover Letter (DOCX): Auto-generated letter using extracted name, company, job title, and key matched skills.

ATS Report (DOCX): Contains ATS score, matched/missing skills, and job details summary.

Ads:

Banner ads shown at the top and bottom of the app using Adsterra JS code wrapped in components.html().

How to Run (Local)
bash
git clone https://github.com/<your-username>/Resume--optimizer-.git
cd Resume--optimizer-
pip install -r requirements.txt
streamlit run app.py
