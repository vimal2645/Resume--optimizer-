from dotenv import load_dotenv
import os
load_dotenv()

import streamlit as st
import streamlit.components.v1 as components  # ADD THIS LINE
from core.parser import parse_resume, parse_job_description
from utils.ai_skill_matcher import ai_matcher
from utils.document_generator import create_resume_docx, create_cover_letter_docx, create_ats_report_docx
from datetime import datetime

st.set_page_config(page_title="AI Resume Optimizer", page_icon="🎯", layout="wide")

# [Keep all your CSS styles here - same as before]
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Animated Background Gradient */
    .stApp {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Main Container */
    .main .block-container {
        padding: 2rem 1rem;
        max-width: 1400px;
    }
    
    /* Header with Color Animation */
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(45deg, #ff6ec4, #7873f5, #4facfe, #00f2fe);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: colorShift 8s ease infinite;
        margin-bottom: 0.5rem;
    }
    
    @keyframes colorShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* [Keep all remaining CSS - same as before] */
    
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🎯 AI Resume Optimizer</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center;color:#fff;font-size:1.1rem;">Upload resume + paste JD. Get accurate ATS score + optimized DOCX.</p>', unsafe_allow_html=True)

# ========== ADSTERRA BANNER AD (TOP) - USING components.html ==========
components.html("""
<div style="text-align: center; margin: 20px 0;">
<script type="text/javascript">
atOptions = {
'key' : '0fffadfc8b3463520518a4244ad1f554',
'format' : 'iframe',
'height' : 90,
'width' : 728,
'params' : {}
};
</script>
<script type="text/javascript" src="//www.highperformanceformat.com/0fffadfc8b3463520518a4244ad1f554/invoke.js"></script>
</div>
""", height=120)

# Initialize session states
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False

# Upload Section
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("#### 📤 Upload Resume")
    uploaded_file = st.file_uploader("Choose file", type=['pdf', 'docx'], label_visibility="collapsed")

with col2:
    st.markdown("#### 📋 Paste Job Description")
    job_description = st.text_area("Job Description", height=200, placeholder="Paste full JD...", label_visibility="collapsed")

# Analyze Button
if st.button("🚀 Analyze", type="primary"):
    if not uploaded_file:
        st.error("Upload a resume")
    elif not job_description or len(job_description) < 20:
        st.error("Paste a job description")
    else:
        with st.spinner("Analyzing..."):
            try:
                resume_bytes = uploaded_file.read()
                resume_out = parse_resume(resume_bytes, uploaded_file.name)
                if not resume_out or not resume_out.get('text'):
                    st.error("Could not extract text")
                    st.stop()
                job_keywords = parse_job_description(job_description)
                if not job_keywords.get('must_have'):
                    st.warning("⚠️ No skills extracted from JD. Using fallback mode.")
                score_data = ai_matcher.calculate_enhanced_ats_score(resume_out.get('skills', []), job_keywords)
                st.session_state.resume_text = resume_out['text']
                st.session_state.job_keywords = job_keywords
                st.session_state.score_data = score_data
                st.session_state.analysis_done = True
                st.success("✅ Analysis complete!")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)[:100]}")

# Results Section
if st.session_state.analysis_done:
    score_data = st.session_state.score_data
    resume_text = st.session_state.resume_text
    job_keywords = st.session_state.job_keywords
    
    st.markdown("---")
    
    # Metrics
    cols = st.columns(4)
    with cols[0]:
        st.markdown(f"<div class='metric-card'><h2>{score_data['ats_score']}%</h2>ATS Score</div>", unsafe_allow_html=True)
    with cols[1]:
        st.metric("Matched", f"{score_data['matched_count']}/{score_data['total_keywords']}")
    with cols[2]:
        st.metric("Missing", score_data['missing_count'])
    with cols[3]:
        st.metric("vs Avg", f"{score_data['ats_score']-67:+}%")
    
    st.markdown("---")

    # Skills Display
    col_l, col_r = st.columns(2)
    with col_l:
        st.write("**✅ Matched Skills**")
        if score_data['matched_keywords']:
            for skill in score_data['matched_keywords'][:10]:
                st.write(f'<span class="matched">{skill}</span>', unsafe_allow_html=True)
        else:
            st.write("None")
    with col_r:
        st.write("**❌ Missing Skills**")
        if score_data['missing_keywords']:
            for skill in score_data['missing_keywords'][:10]:
                st.write(f'<span class="missing">{skill}</span>', unsafe_allow_html=True)
        else:
            st.write("None")
            
    st.markdown("---")

    # Download Section
    tab1, tab2, tab3 = st.tabs(["Download", "Info", "Help"])
    with tab1:
        c1, c2, c3 = st.columns(3)
        with c1:
            resume_docx = create_resume_docx(resume_text, job_keywords, score_data)
            st.download_button("📄 Resume", data=resume_docx, file_name=f"Resume_{score_data['ats_score']}.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        with c2:
            letter_docx = create_cover_letter_docx(resume_text, job_keywords, score_data)
            st.download_button("📝 Letter", data=letter_docx, file_name=f"CoverLetter.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        with c3:
            report_docx = create_ats_report_docx(score_data, job_keywords)
            st.download_button("📊 Report", data=report_docx, file_name=f"Report.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    
    with tab2:
        st.write(f"**Job:** {job_keywords.get('job_title','N/A')}")
        st.write(f"**Company:** {job_keywords.get('company','N/A')}")
        st.write(f"**Must Have:** {len(job_keywords.get('must_have',[]))}")
    
    with tab3:
        st.write("1. Upload resume (PDF/DOCX)")
        st.write("2. Paste job description")
        st.write("3. Click Analyze")
        st.write("4. Download optimized docs")

# ========== ADSTERRA BANNER AD (BOTTOM) - USING components.html ==========
components.html("""
<div style="text-align: center; margin: 30px 0;">
<script type="text/javascript">
atOptions = {
'key' : '0fffadfc8b3463520518a4244ad1f554',
'format' : 'iframe',
'height' : 90,
'width' : 728,
'params' : {}
};
</script>
<script type="text/javascript" src="//www.highperformanceformat.com/0fffadfc8b3463520518a4244ad1f554/invoke.js"></script>
</div>
""", height=120)

