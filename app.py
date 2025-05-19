# AI Resume Screener Web App (cleaned + professional version)

import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
import re

st.title("📄 AI Resume Screener")
st.write("Upload a job description and multiple resumes (.txt or .pdf). The app will rank resumes and give feedback to improve them.")

# upload job description
job_description_file = st.file_uploader("Upload Job Description (.txt or .pdf)", type=["txt", "pdf"])

# extract job description text
job_text = ""
if job_description_file:
    if job_description_file.name.endswith(".txt"):
        raw_data = job_description_file.read()
        for encoding in ["utf-8", "latin-1", "utf-16"]:
            try:
                job_text = raw_data.decode(encoding)
                break
            except UnicodeDecodeError:
                continue
    elif job_description_file.name.endswith(".pdf"):
        pdf_reader = PyPDF2.PdfReader(job_description_file)
        for page in pdf_reader.pages:
            job_text += page.extract_text() or ""

# upload resumes
resume_files = st.file_uploader("Upload Resumes (.txt or .pdf)", type=["txt", "pdf"], accept_multiple_files=True)

if job_description_file and resume_files:
    resume_texts = {}

    for file in resume_files:
        filename = file.name
        if filename.endswith(".txt"):
            raw_resume = file.read()
            for encoding in ["utf-8", "latin-1", "utf-16"]:
                try:
                    text = raw_resume.decode(encoding)
                    break
                except UnicodeDecodeError:
                    continue
        elif filename.endswith(".pdf"):
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
        else:
            text = ""
        resume_texts[filename] = text

    # combine job + resumes
    documents = [job_text] + list(resume_texts.values())

    # convert text to tf-idf matrix
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)

    # calculate similarity
    scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    ranked_resumes = sorted(zip(resume_texts.keys(), scores), key=lambda x: x[1], reverse=True)

    # show ranking
    st.subheader("🏆 Ranked Resumes")
    for i, (name, score) in enumerate(ranked_resumes, start=1):
        st.write(f"{i}. **{name}** — Match Score: `{score:.2f}`")

    # feedback function (cleaned up)
    def give_feedback(resume, job):
        job_words = set(re.findall(r'\b[a-zA-Z]{2,}\b', job.lower()))
        resume_words = set(re.findall(r'\b[a-zA-Z]{2,}\b', resume.lower()))

        # words to ignore
        boring_words = {
            "the", "and", "are", "you", "for", "not", "but", "from", "that", "this", "they", "their", "also",
            "must", "should", "will", "can", "who", "with", "your", "has", "have", "our", "all", "any", "other",
            "those", "each", "such", "very", "able", "been", "being", "make", "made", "more", "most", "some",
            "into", "over", "under", "about", "after", "before", "between", "through", "during", "while", "where",
            "what", "when", "which", "because", "etc", "etc.", "use", "used", "using", "it's", "its", "adjust",
            "acknowledge", "abilities", "accommodations", "access", "application", "anyone", "soft", "skills",
            "ability", "support", "assist", "communicate", "testing", "agile", "team", "environment",
            "work", "helping", "positive", "attitude", "collaborative"
        }

        # skills/tools we actually care about
        allowed_keywords = {
            "python", "java", "c", "c++", "c#", "sql", "mysql", "html", "css", "javascript", "js",
            "react", "node", "flask", "django", "mongodb", "aws", "azure", "git", "github", "linux",
            "docker", "kubernetes", "cloud", "machine", "learning", "data", "api", "testing", "debugging",
            "devops", "frontend", "backend", "security", "cybersecurity", "excel", "powerbi", "nosql", "pandas"
        }

        # check missing words
        missing = job_words - resume_words
        clean = [word for word in missing if word in allowed_keywords and word not in boring_words]

        if clean:
            return "📝 Consider adding these keywords: " + ", ".join(sorted(clean))
        else:
            return "✅ Your resume already matches the job description well!"

    # show suggestions
    st.subheader("🛠 Suggestions for Improvement")
    for name, resume in resume_texts.items():
        st.markdown(f"**{name}**")
        st.write(give_feedback(resume, job_text))