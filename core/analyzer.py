"""
ATS scoring and optimization logic
"""

import re
import string

STOPWORDS = {
    'with', 'and', 'the', 'for', 'to', 'of', 'a', 'an', 'in', 'is', 'on',
    'using', 'as', 'by', 'at', 'or', 'from', 'that', 'this', 'be'
}

def clean_keywords(keywords):
    cleaned = set()
    for kw in keywords:
        kw = kw.lower().strip(string.punctuation + " ")
        if kw and kw not in STOPWORDS:
            cleaned.add(kw)
    return list(cleaned)

def keyword_in_text(keyword, text):
    pattern = r'\b' + re.escape(keyword) + r'\b'
    if re.search(pattern, text, flags=re.IGNORECASE):
        return True
    return keyword.lower() in text.lower()

def calculate_ats_score(resume_data: dict, job_data: dict) -> dict:
    resume_text = resume_data.get('raw_text', '').lower()
    resume_skills = set([skill.lower() for skill in resume_data.get('skills', [])])

    must_have_raw = job_data.get('must_have', [])
    nice_to_have_raw = job_data.get('nice_to_have', [])

    must_have = clean_keywords(must_have_raw)
    nice_to_have = clean_keywords(nice_to_have_raw)
    all_keywords = list(set(must_have + nice_to_have))

    matched_keywords = []
    missing_keywords = []

    for kw in all_keywords:
        if keyword_in_text(kw, resume_text) or kw in resume_skills:
            matched_keywords.append(kw)
        else:
            missing_keywords.append(kw)

    total = len(all_keywords)
    matched_count = len(matched_keywords)
    score = int((matched_count / total) * 100) if total > 0 else 0

    return {
        "score": score,
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,
        "matched_count": matched_count,
        "total_count": total,
    }

def get_optimization_suggestions(resume_data: dict, job_data: dict) -> list:
    from utils.llm import get_llm_response
    from utils.prompts import OPTIMIZATION_PROMPT

    resume_excerpt = resume_data.get('raw_text', '')[:2000]
    missing_keywords = calculate_ats_score(resume_data, job_data).get('missing_keywords', [])
    missing_keywords_str = ", ".join(missing_keywords[:10]) if missing_keywords else "None"

    prompt = OPTIMIZATION_PROMPT.format(
        resume_text=resume_excerpt,
        missing_keywords=missing_keywords_str
    )

    response = get_llm_response(prompt)
    suggestions = _parse_suggestions(response)
    return suggestions

def _parse_suggestions(text: str) -> list:
    lines = text.split("\n")
    suggestions = []
    current = None

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line[0] in ('-', '•') or (len(line) >= 2 and line[:2].isdigit()):
            if current:
                suggestions.append(current)
            current = {"title": line, "description": ""}
        else:
            if current:
                current["description"] += line + " "
            else:
                current = {"title": "Suggestion", "description": line + " "}
    if current:
        suggestions.append(current)
    return suggestions[:5]
