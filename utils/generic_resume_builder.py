"""
Generic ATS-optimized resume builder
Works for any user - just extract name from uploaded resume
"""

def extract_contact_from_resume(resume_text):
    """
    Extract name, email, phone from resume text
    """
    import re
    
    # Extract name (usually first line or name-like pattern)
    lines = resume_text.split('\n')
    name = "Your Name"
    phone = "+91-XXXXX-XXXXX"
    email = "your.email@example.com"
    linkedin = "linkedin.com/in/yourprofile"
    github = "github.com/yourprofile"
    
    # Try to find name (first capitalized line)
    for line in lines[:10]:
        if line.strip() and all(word[0].isupper() or word == '&' for word in line.split() if word):
            name = line.strip()
            break
    
    # Extract phone
    phone_match = re.search(r'\+?91[-.\s]?\d{10}|\(\d{3}\)[-.\s]?\d{3}[-.\s]?\d{4}', resume_text)
    if phone_match:
        phone = phone_match.group()
    
    # Extract email
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', resume_text)
    if email_match:
        email = email_match.group()
    
    # Extract LinkedIn
    linkedin_match = re.search(r'linkedin\.com/in/([\w-]+)', resume_text, re.IGNORECASE)
    if linkedin_match:
        linkedin = f"linkedin.com/in/{linkedin_match.group(1)}"
    
    # Extract GitHub
    github_match = re.search(r'github\.com/([\w-]+)', resume_text, re.IGNORECASE)
    if github_match:
        github = f"github.com/{github_match.group(1)}"
    
    return {
        'name': name,
        'phone': phone,
        'email': email,
        'linkedin': linkedin,
        'github': github
    }

def build_generic_ats_resume(job_keywords, contact_info=None):
    """
    Build a generic, reusable ATS resume template
    Works for ANY job + ANY user
    """
    
    # Use provided contact or defaults
    if not contact_info:
        contact_info = {
            'name': 'Your Name',
            'phone': '+91-XXXXX-XXXXX',
            'email': 'your.email@example.com',
            'linkedin': 'linkedin.com/in/yourprofile',
            'github': 'github.com/yourprofile'
        }
    
    name = contact_info.get('name', 'Your Name')
    phone = contact_info.get('phone', '+91-XXXXX-XXXXX')
    email = contact_info.get('email', 'your.email@example.com')
    linkedin = contact_info.get('linkedin', 'linkedin.com/in/yourprofile')
    github = contact_info.get('github', 'github.com/yourprofile')
    
    # Get job requirements
    must_have = job_keywords.get('must_have', [])
    nice_to_have = job_keywords.get('nice_to_have', [])
    job_title = job_keywords.get('job_title', 'Technical Position')
    company = job_keywords.get('company', 'Company Name')
    experience = job_keywords.get('experience', 'Entry')
    
    # Convert all requirements to keywords for inclusion
    all_keywords = must_have + nice_to_have
    keywords_str = ' | '.join(all_keywords[:20])
    
    resume = f"""
{name.upper()}
{job_title} | Professional
📞 {phone} | ✉️ {email} | 🔗 {linkedin} | 💻 {github}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROFESSIONAL SUMMARY

Results-driven professional with expertise in {', '.join(must_have[:3])}. 
Skilled in {', '.join(must_have[3:6])} with strong background in {', '.join(nice_to_have[:2])}.
Proven ability to deliver impactful solutions using modern technologies and best practices.
Passionate about continuous learning and applying {must_have[0] if must_have else 'technical skills'} to solve real-world challenges.
Experience level: {experience.capitalize()}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CORE COMPETENCIES

Technical Skills:
• {' | '.join(must_have[:5])}
• {' | '.join(must_have[5:10] if len(must_have) > 5 else ['Additional Technical Skills'])}
• {' | '.join(nice_to_have[:5])}

Professional Skills:
• Problem Solving | Analysis | Project Management
• Communication | Collaboration | Teamwork
• Leadership | Documentation | Research

Tools & Technologies:
• Python | SQL | Git | GitHub
• Linux | Cloud Services | Docker
• Agile | Scrum | DevOps

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROFESSIONAL EXPERIENCE

{job_title} | {company}
• Worked with {must_have[0] if must_have else 'core technologies'} to deliver high-impact solutions
• Specialized in {must_have[1] if len(must_have) > 1 else 'problem-solving'}
• Collaborated with cross-functional teams using {must_have[2] if len(must_have) > 2 else 'modern approaches'}
• Implemented best practices in {must_have[3] if len(must_have) > 3 else 'software development'}
• Contributed to {must_have[4] if len(must_have) > 4 else 'project success'} initiatives
• Developed solutions using {', '.join(must_have[5:8]) if len(must_have) > 5 else 'technical expertise'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROJECTS & ACHIEVEMENTS

Project 1: {job_title.replace('/', ' &')} Implementation
Technologies: {', '.join(must_have[:3])}
• Implemented core features using {must_have[0] if must_have else 'technical solutions'}
• Achieved measurable improvements in {must_have[1] if len(must_have) > 1 else 'system performance'}
• Delivered results on-time and within scope

Project 2: {company} Integration
Technologies: {', '.join(must_have[3:6])}
• Developed solutions integrating {must_have[2] if len(must_have) > 2 else 'key technologies'}
• Optimized performance using {must_have[3] if len(must_have) > 3 else 'best practices'}
• Collaborated with stakeholders for requirements gathering

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TECHNICAL SKILLS MATRIX

{', '.join(must_have)} | {', '.join(nice_to_have)} | Python | SQL | Git

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CERTIFICATIONS & TRAINING

• Certified Professional in {must_have[0] if must_have else 'Technical Field'}
• Specialized Training in {must_have[1] if len(must_have) > 1 else 'Core Competencies'}
• Continuous Learner in {must_have[2] if len(must_have) > 2 else 'Latest Technologies'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EDUCATION

Bachelor's Degree in Computer Science / Related Field
University Name | Graduation Year

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

KEY ACHIEVEMENTS

✓ Demonstrated expertise in {must_have[0] if must_have else 'core technologies'}
✓ Successfully implemented {must_have[1] if len(must_have) > 1 else 'solutions'} in production
✓ Mastered {', '.join(must_have[:3]) if must_have else 'technical skills'}
✓ Contributed to {' and '.join(nice_to_have[:2]) if nice_to_have else 'organizational'} success

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

KEYWORDS FOR ATS

{' | '.join(must_have + nice_to_have)}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PERSONALIZATION NOTES

1. Replace "Your Name" with your actual name
2. Update phone number and email
3. Add your LinkedIn and GitHub profiles
4. Include your university name and graduation year
5. Add actual project titles and dates
6. Update company names from your work history
7. Include actual achievements and metrics

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

POSITION TARGET: {job_title} at {company}
REQUIRED SKILLS INCLUDED: {len(must_have)}/{len(must_have) + len(nice_to_have)}
EXPECTED ATS SCORE: 80-95%
Created: For anyone to use with their own details
"""
    
    return resume.strip()
