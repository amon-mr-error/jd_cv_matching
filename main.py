import streamlit as st
import pandas as pd
from processing.parser import FileParser
from processing.processor import TextProcessor
from processing.matching import Matcher
import os

st.set_page_config(page_title="AI Recruiter", layout="wide")

def process_files(jd_file, cv_files):
    # Process Job Description (JD)
    if jd_file.name.endswith('.pdf'):
        jd_text = FileParser.parse_pdf(jd_file)
    else:
        jd_text = FileParser.parse_docx(jd_file)
    
    # Create an instance of TextProcessor (which loads skills.json)
    processor = TextProcessor()
    
    # Extract skills and experience from JD
    jd_data = processor.extract_entities(jd_text)
    jd_data['embedding'] = processor.get_embeddings(jd_text)

    # Process Candidate CVs
    cvs = []
    for cv_file in cv_files:
        if cv_file.name.endswith('.pdf'):
            cv_text = FileParser.parse_pdf(cv_file)
        else:
            cv_text = FileParser.parse_docx(cv_file)
       
        cv_data = processor.extract_entities(cv_text)
        cv_data['embedding'] = processor.get_embeddings(cv_text)
        cv_data['name'] = os.path.basename(cv_file.name)
        cvs.append(cv_data)

    return jd_data, cvs

# UI Components
st.title("AI-Powered JD/CV Matching System")

# File Upload Section
col1, col2 = st.columns(2)
with col1:
    jd_file = st.file_uploader("Upload Job Description", type=['pdf', 'docx'])
with col2:
    cv_files = st.file_uploader("Upload Candidate CVs", type=['pdf', 'docx'], accept_multiple_files=True)

if jd_file and cv_files:
    with st.spinner("Processing files..."):
        jd_data, cvs_data = process_files(jd_file, cv_files)
        rankings = Matcher.rank_candidates(jd_data, cvs_data)

    # Display Rankings
    st.subheader("Candidate Rankings")
    df = pd.DataFrame([{
        'Candidate': r['name'],
        'Match Score': f"{1.2 * r.get('final_score', 0):.1f}%",
        'Skills Matched': ", ".join(r['skills_matched']),
        'Experience Details': "; ".join(r['experience'])
    } for r in rankings])
    
    st.dataframe(df, use_container_width=True)

    # Detailed View
    st.subheader("Candidate Details")
    selected_candidate = st.selectbox("Choose candidate", [r['name'] for r in rankings])
    candidate = next(r for r in rankings if r['name'] == selected_candidate)
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Skills Matched:**")
        st.write(", ".join(candidate['skills_matched']))
    with col2:
        st.write("**Experience Summary:**")
        st.write("; ".join(candidate['experience']))

else:
    st.info("Please upload both a JD and CVs to get started")
