# 🧠 AI Resume Screener Web App

Live Demo
(https://resume-screener-functrsplr6yssbs5ju7po.streamlit.app/)

This is a smart resume screener built with Python and Streamlit that:
- ✅ ranks resumes based on job descriptions using NLP (TF-IDF + cosine similarity)
- 📄 supports `.txt` and `.pdf` files
- 💬 gives personalized improvement suggestions for each resume
- 🧪 runs locally or can be deployed on Streamlit Cloud

## 🚀 Features

- Upload job descriptions and multiple resumes
- Ranks resumes by how well they match
- Supports `.pdf` and `.txt`
- Feedback on missing keywords
- Clean browser interface

## 🛠 Built With

- Python
- Streamlit
- scikit-learn
- PyPDF2

## 📦 To Run Locally

```bash
pip install streamlit scikit-learn PyPDF2
streamlit run app.py
