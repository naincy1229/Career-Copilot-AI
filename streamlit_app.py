import streamlit as st
from utils.parse_resume import parse_resume
from agents.career_qa import answer_career_question
from agents.role_recommender import suggest_roles
from agents.roadmap_agent import generate_learning_roadmap
from utils.resume_score import calculate_resume_score
from utils.jd_matcher import compute_jd_match
from utils.pdf_generator import export_chat_to_pdf
from utils.parse_jobdesc import extract_text_from_txt
from utils.ats_score_calculator import calculate_ats_score
from utils.cover_letter_generator import generate_cover_letter
from datetime import datetime
import os
from utils.linkedin_summary_generator import generate_linkedin_summary
from utils.domain_companies import get_companies_by_domain


# Constants
MODEL = "gemma:2b"
LOG_FILE = "chat_log.txt"

# ---- CONFIGURATION ----
st.set_page_config(page_title="Career Copilot AI", layout="wide", initial_sidebar_state="expanded")

# ---- DARK MODE CSS ----

def apply_flat_two_column_theme():
    st.markdown("""
    <style>
    /* Clean flat layout */
    #MainMenu, header, footer {visibility: hidden;}

    .block-container {
        padding: 1.5rem 2rem;
        background-color: #0f172a;
        font-family: 'Segoe UI', sans-serif;
    }

    /* Left pane styling */
    div[data-testid="column"]:first-child {
        background-color: #1e293b;
        border-radius: 12px;
        padding: 2rem 1.5rem;
        color: #f1f5f9;
        border: 1px solid #334155;
    }

    /* Right pane styling */
    div[data-testid="column"]:last-child {
        background-color: #111827;
        padding: 2rem 2rem;
        border-radius: 12px;
        color: #f1f5f9;
        border: 1px solid #334155;
    }

    h1, h2, h3 {
        color: #ffffff;
        font-size: 1.7rem;
        font-weight: 700;
    }

    .stTextInput input, .stTextArea textarea, .stSelectbox div div input {
        background-color: #1e293b;
        color: #f1f5f9;
        border-radius: 6px;
        border: 1px solid #334155;
    }

    .stButton>button {
        background-color: #3b82f6;
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: 600;
        padding: 10px 20px;
        margin-top: 10px;
    }

    .stButton>button:hover {
        background-color: #2563eb;
    }
    </style>
    """, unsafe_allow_html=True)

apply_flat_two_column_theme()


# ---- SESSION STATE ----
for key in ["chat_history", "resume_data", "resume_file", "resume_text", "interview_history"]:
    if key not in st.session_state:
        st.session_state[key] = [] if "history" in key else None

# ---- SIDEBAR INPUTS ----

with st.sidebar:
    st.title("🎯 Career Copilot AI")
    
    st.markdown("## 📄 Resume Upload")
    uploaded_file = st.file_uploader("Upload your resume (PDF only)", type="pdf")
    if uploaded_file:
        st.session_state.resume_file = uploaded_file
        try:
            resume_text = parse_resume(uploaded_file)
            resume_data = {"raw_text": resume_text}
            st.session_state.resume_data = resume_data
            st.session_state.resume_text = resume_text
            st.success("✅ Resume parsed successfully!")
        except Exception as e:
            st.error(f"❌ Error: {e}")

    st.markdown("## 🧰 Resume Tools")

    if st.button("📊 Resume Score"):
        st.session_state.run_resume_score = True

    jd_text = st.text_area("📋 Paste Job Description")
    st.session_state.jd_text = jd_text

    if st.button("🔍 JD Match %"):
        st.session_state.run_jd_match = True

    if st.button("📈 ATS Score"):
        st.session_state.run_ats_score = True

    st.markdown("---")
    st.markdown("## ✉️ Cover Letter")

    job_description_input = st.text_area("Paste JD for Cover Letter")
    if st.button("✍️ Generate Cover Letter"):
        st.session_state.run_cover_letter = True

    st.markdown("---")
    st.markdown("## 🧠 Skill Gap Analyzer")
    gap_role = st.text_input("Target Role")
    if st.button("📉 Analyze Skill Gap"):
        st.session_state.run_gap_analysis = True

    st.markdown("---")
    st.markdown("## 🧹 Maintenance")
    if st.button("🧼 Clear Chat"):
        st.session_state.chat_history = []
        open(LOG_FILE, "w").close()
        st.success("✅ Chat cleared.")

    if st.session_state.chat_history:
        file_path = export_chat_to_pdf(st.session_state.chat_history)
        with open(file_path, "rb") as f:
            st.download_button("📄 Download Chat", f, "career_chat.pdf", mime="application/pdf")



# ---- MAIN UI AREA ----

st.markdown("## 💬 Career Chat Assistant")
for entry in st.session_state.chat_history:
    with st.chat_message(entry["role"]):
        st.markdown(entry["content"])

user_input = st.chat_input("Ask about roles, roadmaps, or job advice...")
if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        with st.spinner("🤖 Thinking..."):
            try:
                if "roadmap" in user_input.lower():
                    response = generate_learning_roadmap(st.session_state.resume_data, user_input, model=MODEL)
                elif "role" in user_input.lower():
                    response = suggest_roles(st.session_state.resume_data, model=MODEL)
                else:
                    response = answer_career_question(st.session_state.resume_data, user_input, model=MODEL)

                st.markdown(response)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"❌ Error: {e}")

st.markdown("<hr />", unsafe_allow_html=True)


# ----------------- Feature 5: Location-Based Salary Insights -----------------
st.subheader("📍 Location-Based Salary Insights")
col1, col2 = st.columns(2)
with col1:
    job_role_input = st.text_input("💼 Enter Job Role", placeholder="e.g., Data Analyst")
with col2:
    location_input = st.text_input("🌍 Enter Location", placeholder="e.g., Bangalore")

if st.button("💰 Get Salary Estimate"):
    if job_role_input and location_input:
        try:
            # Mocked salary data for demonstration
            role = job_role_input.lower()
            city = location_input.lower()

            base_salary = {
                "data analyst": 6,
                "frontend developer": 7,
                "backend developer": 8,
                "ui ux designer": 7,
                "machine learning engineer": 9
            }

            multiplier = {
                "bangalore": 1.2,
                "delhi": 1.1,
                "mumbai": 1.15,
                "pune": 1.0,
                "hyderabad": 1.1
            }

            base = base_salary.get(role, 6)
            mult = multiplier.get(city, 1.0)
            est_salary = base * mult

            st.success(f"💰 Estimated Salary for **{job_role_input.title()}** in **{location_input.title()}** is ₹{est_salary:.1f} LPA")
        except Exception as e:
            st.error(f"❌ Error estimating salary: {e}")
    else:
        st.warning("⚠️ Please enter both job role and location.")


# ----------------- Feature 6: Project Impact Estimator -----------------
st.subheader(" Project Impact Estimator")

project_input = st.text_area("📝 Describe Your Project", placeholder="e.g., Built a predictive model to forecast sales for XYZ Corp...")

if st.button("📊 Estimate Impact"):
    if project_input:
        try:
            # Mocked logic: pretend we're analyzing using rules
            impact_phrases = {
                "automation": "🔧 Saved significant manual effort",
                "forecast": "📈 Improved business planning & decision-making",
                "dashboard": "📊 Enhanced real-time insights for stakeholders",
                "model": "🧠 Data-driven decision support",
                "reduced": "💸 Cost-saving achievement",
                "increased": "📈 Revenue growth impact",
            }

            insights = []
            for key, phrase in impact_phrases.items():
                if key in project_input.lower():
                    insights.append(phrase)

            if not insights:
                insights = ["🤔 Unable to detect impact keywords. Try making the description more detailed."]

            st.markdown("### 💡 Estimated Business Impact")
            for insight in insights:
                st.success(insight)

            st.markdown("### 🔧 Suggested Improvements")
            st.info("✅ Add metrics (e.g., 'reduced time by 30%') to make the impact clearer.")
            st.info("✅ Include scale (e.g., users impacted, amount saved, or time reduced).")

        except Exception as e:
            st.error(f"❌ Error estimating impact: {e}")
    else:
        st.warning("⚠️ Please enter a project description.")


# ----------------- Feature 7: Career Timeline Builder -----------------
st.subheader(" Career Timeline Builder")

if st.button("🗂️ Build Career Timeline"):
    if st.session_state.resume_text:
        try:
            import re
            from collections import OrderedDict

            resume_text = st.session_state.resume_text

            # Very basic job-experience regex extraction logic
            pattern = r'(?P<year>\d{4})[^.\n]*?(?P<title>intern|engineer|developer|analyst|manager|designer|consultant)[^\n.]*?(at|@)?\s*(?P<company>[A-Za-z0-9 &]+)?'
            matches = re.finditer(pattern, resume_text, re.IGNORECASE)

            timeline = OrderedDict()
            for match in matches:
                year = match.group("year")
                title = match.group("title").title()
                company = match.group("company") or "Unknown Company"
                key = f"{year} - {title} at {company}"
                timeline[year] = key

            if timeline:
                st.markdown("###  Your Career Timeline")
                for year, entry in sorted(timeline.items()):
                    st.markdown(f"🔹 **{year}**: {entry}")
            else:
                st.info("🤔 No clear job entries found. Please check your resume format.")

        except Exception as e:
            st.error(f"❌ Timeline generation failed: {e}")
    else:
        st.warning("⚠️ Upload and parse a resume first.")
        
        
        # 📌 FEATURE 8: LinkedIn Summary Generator
st.subheader("🔗 LinkedIn Summary Generator")
if st.button("📝 Generate LinkedIn Summary"):
    if st.session_state.resume_text:
        with st.spinner("Creating professional LinkedIn summary..."):
            try:
                summary = generate_linkedin_summary(st.session_state.resume_text)
                st.markdown("### ✍️ Your LinkedIn Summary")
                st.success(summary)
            except Exception as e:
                st.error(f"❌ Error: {e}")
    else:
        st.warning("⚠️ Upload and parse your resume first.")


# --------------------------------------------
# 🏢 Domain-Based Company Suggestion
# --------------------------------------------

st.subheader("🏢 Domain-Based Company Suggestions")

domain_input = st.selectbox("Choose your domain", 
    ["", "Data Analyst", "UI UX", "Web Developer", "Machine Learning", "Cybersecurity", "DevOps"])

if st.button("🔍 Show Companies Hiring"):
    if domain_input:
        companies = get_companies_by_domain(domain_input)
        if companies:
            st.markdown("###  Top Companies Hiring:")
            for company in companies:
                st.success(f"✅ {company}")

       # 🔗 Multi-platform Job Search Links
            encoded_domain = domain_input.replace(" ", "+")
            st.markdown("### 🔗 Search Jobs on Popular Platforms:")
            st.markdown(f"- [LinkedIn](https://www.linkedin.com/jobs/search/?keywords={encoded_domain})")
            st.markdown(f"- [Indeed](https://www.indeed.com/jobs?q={encoded_domain})")
            st.markdown(f"- [Naukri](https://www.naukri.com/{encoded_domain}-jobs)")

        else:
            st.warning("⚠️ No data available for this domain yet.")
    else:
        st.warning("⚠️ Please select a domain first.")




# ---- OUTPUTS ----
if st.session_state.get("run_resume_score") and st.session_state.resume_data:
    score, feedback = calculate_resume_score(st.session_state.resume_data)
    st.markdown("## 📊 Resume Score")
    st.success(f"**Score:** {score}/100\n\n{feedback}")
    st.session_state.run_resume_score = False

if st.session_state.get("run_jd_match") and st.session_state.resume_data and jd_text:
    percent, insights = compute_jd_match(jd_text, st.session_state.resume_data)
    st.markdown("## 📋 JD Match")
    st.success(f"**Match:** {percent}%\n\n{insights}")
    st.session_state.run_jd_match = False

if st.session_state.get("run_ats_score") and st.session_state.resume_text and jd_text:
    try:
        ats_result = calculate_ats_score(st.session_state.resume_text, jd_text)
        st.markdown("## 📈 ATS Score")
        st.metric("ATS Score", f"{ats_result['ats_score']} / 100")
        st.progress(ats_result['ats_score'])
        st.markdown("### ✅ Matched Keywords")
        st.write(", ".join(ats_result["matched_keywords"]) or "None")
        st.markdown("### ❌ Missing Keywords")
        st.write(", ".join(ats_result["missing_keywords"]) or "All matched!")
        st.markdown("### 💡 Suggestions")
        for suggestion in ats_result["suggestions"]:
            st.warning(suggestion)
    except Exception as e:
        st.error(f"❌ Error: {e}")
    st.session_state.run_ats_score = False

if st.session_state.get("run_cover_letter") and st.session_state.resume_text and job_description_input:
    try:
        st.markdown("## ✉️ Cover Letter")
        cover_letter = generate_cover_letter(st.session_state.resume_text, job_description_input)
        st.code(cover_letter)
    except Exception as e:
        st.error(f"❌ Error: {e}")
    st.session_state.run_cover_letter = False

if st.session_state.get("run_gap_analysis") and st.session_state.resume_text and gap_role:
    TOP_SKILLS = {
        "data analyst": ["SQL", "Excel", "Power BI", "Python", "Statistics"],
        "frontend developer": ["HTML", "CSS", "JavaScript", "React", "Figma"],
        "machine learning engineer": ["Python", "Scikit-learn", "Pandas", "Numpy", "ML Algorithms"],
        "backend developer": ["Python", "Django", "APIs", "SQL", "Docker"],
        "ui ux designer": ["Figma", "Adobe XD", "Prototyping", "Wireframing", "User Research"]
    }
    role_skills = TOP_SKILLS.get(gap_role.lower(), [])
    matched = [skill for skill in role_skills if skill.lower() in st.session_state.resume_text.lower()]
    missing = list(set(role_skills) - set(matched))

    st.markdown("## 📉 Skill Gap Analysis")
    st.success("✅ Matched Skills: " + ", ".join(matched) if matched else "None")
    st.error("❌ Missing Skills: " + ", ".join(missing) if missing else "All top skills matched!")
    if missing:
        st.markdown("### 📚 Suggested Learning:")
        for skill in missing:
            st.info(f"[Learn {skill} on Coursera](https://www.coursera.org/search?query={skill})")
    st.session_state.run_gap_analysis = False
