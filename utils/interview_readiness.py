def calculate_interview_readiness(resume_data):
    """
    Calculate interview readiness score based on key factors in resume.
    """
    score = 0
    tips = []

    # Evaluate key components
    summary = resume_data.get("summary", "")
    skills = resume_data.get("skills", [])
    experience = resume_data.get("experience", [])
    education = resume_data.get("education", "")

    # Score for summary
    if summary and len(summary.split()) >= 20:
        score += 20
    else:
        tips.append("✅ Add a strong professional summary (at least 20 words).")

    # Score for skills
    if skills and len(skills) >= 5:
        score += 20
    else:
        tips.append("✅ List at least 5 relevant technical and soft skills.")

    # Score for experience
    if experience and len(experience) >= 1:
        score += 30
    else:
        tips.append("✅ Include relevant work experience or internships.")

    # Score for education
    if education:
        score += 10
    else:
        tips.append("✅ Add your educational qualifications.")

    # Bonus for project section or certifications
    projects = resume_data.get("projects", [])
    certifications = resume_data.get("certifications", [])

    if projects:
        score += 10
    if certifications:
        score += 10

    # Clamp score to 100
    final_score = min(score, 100)

    return {
        "score": final_score,
        "tips": tips or ["🎯 You're all set! Keep practicing interview questions."]
    }
