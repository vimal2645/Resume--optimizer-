from thefuzz import fuzz
import numpy as np

class AISkillMatcher:
    def __init__(self):
        pass
    
    def intelligent_match(self, job_skill, resume_skills, threshold=75):
        job_skill_lower = str(job_skill).lower().strip()
        for resume_skill in resume_skills:
            resume_skill_lower = str(resume_skill).lower().strip()
            if fuzz.token_set_ratio(job_skill_lower, resume_skill_lower) >= threshold:
                return True
        return False
    
    def calculate_enhanced_ats_score(self, resume_skills, job_keywords):
        must_have = job_keywords.get('must_have', []) or []
        nice_to_have = job_keywords.get('nice_to_have', []) or []
        
        matched = []
        missing = []
        
        for skill in must_have:
            if self.intelligent_match(skill, resume_skills):
                matched.append(skill)
            else:
                missing.append(skill)
        
        for skill in nice_to_have:
            if self.intelligent_match(skill, resume_skills):
                matched.append(skill)
            else:
                missing.append(skill)
        
        total = len(must_have) + len(nice_to_have)
        score = int((len(matched) / total * 100)) if total > 0 else 0
        
        return {
            'ats_score': score,
            'matched_keywords': matched,
            'missing_keywords': missing,
            'matched_count': len(matched),
            'missing_count': len(missing),
            'total_keywords': total,
        }

ai_matcher = AISkillMatcher()
