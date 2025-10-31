"""
Cover letter generation
"""

def generate_cover_letter(resume_data: dict, job_data: dict, tone: str = 'professional') -> str:
    """Generate tailored cover letter"""
    from utils.llm import get_llm_response
    from utils.prompts import COVER_LETTER_PROMPT
    
    # Extract key info
    skills = ", ".join(resume_data['skills'][:5])
    job_title = job_data.get('job_title', 'the position')
    company = job_data.get('company', 'your company')
    
    prompt = COVER_LETTER_PROMPT.format(
        tone=tone,
        job_title=job_title,
        company=company,
        candidate_skills=skills,
        resume_summary=resume_data['raw_text'][:1000]
    )
    
    cover_letter = get_llm_response(prompt, temperature=0.7)
    
    return cover_letter
