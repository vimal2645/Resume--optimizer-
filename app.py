from dotenv import load_dotenv
import os
load_dotenv()

import streamlit as st
from core.parser import parse_resume, parse_job_description
from utils.ai_skill_matcher import ai_matcher
from utils.document_generator import create_resume_docx, create_cover_letter_docx, create_ats_report_docx
from datetime import datetime

st.set_page_config(page_title="AI Resume Optimizer", page_icon="🎯", layout="wide")

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
    
    /* Subtitle */
    p[style*="text-align:center"] {
        color: #ffffff !important;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        opacity: 0.95;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    /* Section Headers */
    h4 {
        color: white !important;
        font-weight: 600;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    /* Metric Card with Color Animation */
    .metric-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        background-size: 200% 200%;
        animation: cardGlow 4s ease infinite;
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
    }
    
    @keyframes cardGlow {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .metric-card:hover {
        transform: scale(1.08) rotate(2deg);
        box-shadow: 0 15px 40px rgba(0,0,0,0.4);
    }
    
    .metric-card h2 {
        font-size: 2.5rem;
        margin: 0;
        font-weight: 700;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
    }
    
    /* Matched Skills with Animation */
    .matched {
        background: linear-gradient(135deg, #11998e, #38ef7d, #06beb6, #48f585);
        background-size: 300% 300%;
        animation: skillPulse 6s ease infinite;
        color: white;
        padding: 0.6rem 1.2rem;
        border-radius: 25px;
        margin: 0.3rem;
        display: inline-block;
        font-weight: 500;
        box-shadow: 0 4px 15px rgba(17, 153, 142, 0.4);
        transition: all 0.3s ease;
    }
    
    @keyframes skillPulse {
        0%, 100% { background-position: 0% 50%; transform: scale(1); }
        50% { background-position: 100% 50%; transform: scale(1.05); }
    }
    
    .matched:hover {
        transform: translateY(-5px) scale(1.1);
        box-shadow: 0 8px 25px rgba(17, 153, 142, 0.6);
    }
    
    /* Missing Skills with Animation */
    .missing {
        background: linear-gradient(135deg, #f857a6, #ff5858, #ff6a88, #ff9966);
        background-size: 300% 300%;
        animation: missingPulse 6s ease infinite;
        color: white;
        padding: 0.6rem 1.2rem;
        border-radius: 25px;
        margin: 0.3rem;
        display: inline-block;
        font-weight: 500;
        box-shadow: 0 4px 15px rgba(248, 87, 166, 0.4);
        transition: all 0.3s ease;
    }
    
    @keyframes missingPulse {
        0%, 100% { background-position: 0% 50%; transform: scale(1); }
        50% { background-position: 100% 50%; transform: scale(1.05); }
    }
    
    .missing:hover {
        transform: translateY(-5px) scale(1.1);
        box-shadow: 0 8px 25px rgba(248, 87, 166, 0.6);
    }
    
    /* Primary Button with Glow Animation */
    .stButton>button {
        background: linear-gradient(135deg, #f093fb, #f5576c, #ff6b95, #f76b8a) !important;
        background-size: 300% 300%;
        animation: buttonGlow 5s ease infinite;
        color: white !important;
        font-weight: 600;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 30px;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 5px 20px rgba(245, 87, 108, 0.4);
    }
    
    @keyframes buttonGlow {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .stButton>button:hover {
        transform: translateY(-5px) scale(1.05);
        box-shadow: 0 10px 35px rgba(245, 87, 108, 0.7);
    }
    
    /* Download Buttons with Animation */
    .stDownloadButton>button {
        background: linear-gradient(135deg, #667eea, #764ba2, #7b68ee, #9370db) !important;
        background-size: 300% 300%;
        animation: downloadShine 5s ease infinite;
        color: white !important;
        font-weight: 500;
        border: none;
        padding: 0.6rem 1.5rem;
        border-radius: 20px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    @keyframes downloadShine {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .stDownloadButton>button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.6);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(255, 255, 255, 0.15);
        border-radius: 15px;
        padding: 0.5rem;
        backdrop-filter: blur(10px);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        color: white;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    
    /* File Uploader */
    .stFileUploader {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Text Area */
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        border: 2px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Metrics */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.2);
    }
    
    [data-testid="stMetricValue"] {
        color: white;
        font-size: 2rem;
        font-weight: 700;
    }
    
    [data-testid="stMetricLabel"] {
        color: rgba(255, 255, 255, 0.9);
    }
    
    /* Divider with Animation */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.5), transparent);
        margin: 2rem 0;
        animation: dividerGlow 3s ease infinite;
    }
    
    @keyframes dividerGlow {
        0%, 100% { opacity: 0.5; }
        50% { opacity: 1; }
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
        }
        
        .metric-card h2 {
            font-size: 2rem;
        }
        
        .stButton>button {
            font-size: 1rem;
            padding: 0.6rem 1.5rem;
        }
        
        .main .block-container {
            padding: 1rem 0.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🎯 AI Resume Optimizer</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center;color:#fff;font-size:1.1rem;">Upload resume + paste JD. Get accurate ATS score + optimized DOCX.</p>', unsafe_allow_html=True)

# ========== ADSTERRA BANNER AD (TOP) ==========
st.markdown("""
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
""", unsafe_allow_html=True)

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

# ========== ADSTERRA BANNER AD (BOTTOM) ==========
st.markdown("""
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
""", unsafe_allow_html=True)
