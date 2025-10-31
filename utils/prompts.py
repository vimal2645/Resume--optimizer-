JD_ANALYSIS_PROMPT = """Analyze this job description and extract keywords in valid JSON format.

Job Description:
{job_description}

Return ONLY valid JSON (no markdown, no code blocks, no extra text) with this exact structure:
{{
    "must_have": ["skill1", "skill2"],
    "nice_to_have": ["skill3", "skill4"],
    "experience": "Entry/Mid/Senior",
    "job_title": "title",
    "company": "company name"
}}

Important:
- must_have: Technical skills, programming languages, frameworks, tools that are REQUIRED
- nice_to_have: Optional skills, preferred qualifications, bonus points
- Extract actual skill names (e.g., "Python", "AWS", "React", "SQL")
- Return ONLY the JSON object, nothing else"""
