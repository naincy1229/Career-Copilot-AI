def calculate_resume_score(resume_data):
    """
    Score the resume based on key sections and give feedback.

    Args:
        resume_data (dict): Parsed resume fields (skills, experience, education, summary, etc.)

    Returns:
        tuple: (score out of 100, feedback string)
    """
    score = 0
    feedback = []

    # --- Skills Check ---
    skills = resume_data.get("skills", [])
    if isinstance(skills, list) and len(skills) >= 5:
        score += 30
    else:
        feedback.append("🔧 Add at least 5 relevant technical or soft skills.")

    # --- Experience Check ---
    experience = resume_data.get("experience", [])
    if isinstance(experience, list) and len(experience) >= 2:
        score += 30
    else:
        feedback.append("💼 Include at least 2 work/internship experiences.")

    # --- Education Check ---
    education = resume_data.get("education", "")
    if education:
        score += 20
    else:
        feedback.append("🎓 Mention your education background (degree, college).")

    # --- Summary/Objective Check ---
    summary = resume_data.get("summary", "")
    if isinstance(summary, str) and len(summary.split()) > 20:
        score += 20
    else:
        feedback.append("📝 Write a brief summary (at least 20 words) highlighting strengths.")

    return score, "\n".join(feedback)
