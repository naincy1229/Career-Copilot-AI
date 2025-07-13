# 🚀 Career Copilot AI

**Career Copilot AI** is an intelligent, Streamlit-based career assistant that helps job seekers analyze resumes, match them with job descriptions, optimize ATS scores, and prepare for interviews using generative AI.

![Render Status](https://img.shields.io/badge/Deployed-Live-green)  
🔗 [Live App on Render](https://career-copilot-ai-1.onrender.com)

---

## 🎯 Features

- 📄 **Resume Parser** – Extracts structured data from uploaded resumes.
- 📋 **JD Matching & ATS Score** – Analyzes match between resume and job description.
- 🧠 **AI-Powered Career Q&A** – Ask career-related questions and get contextual answers.
- 🧰 **Keyword Optimizer** – Suggests keywords to improve ATS compatibility.
- 📊 **Skill Gap Analyzer** – Compares resume skills with job requirements.
- 🛣️ **Learning Roadmap Generator** – AI-generated personalized learning plans.
- 💼 **Cover Letter Generator** – Auto-generates a professional cover letter.
- 🎤 **Mock Interview Agent** – Practice with AI-driven interview questions.
- 📝 **Interview Readiness Score** – Rates your preparedness.
- 📎 **PDF Export Report** – Download a full career analysis in PDF format.

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **AI & NLP**: HuggingFace Transformers, spaCy, Sentence Transformers
- **PDF & Doc Parsing**: PyMuPDF (fitz), pdfplumber, PyPDF2, python-docx
- **Deployment**: Render

---

## 📂 Project Structure

```bash
career-copilot-ai/
├── app.py
├── streamlit_app.py
├── chains/
│   ├── resume_feedback.py
│   ├── cover_letter_generator.py
│   └── interview_agent.py
├── utils/
│   ├── parse_resume.py
│   ├── parse_jobdesc.py
│   └── rag_utils.py
├── data/
│   ├── sample_resumes/
│   └── sample_jds/
├── agents/
│   └── career_qa.py
├── requirements.txt
└── README.md
