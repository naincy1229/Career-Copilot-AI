def compute_jd_match(jd_text, resume_data):
    """
    Compute the match percentage between a job description (JD) and resume content.

    Args:
        jd_text (str): The job description input text.
        resume_data (dict): Parsed resume data (dict of sections like education, skills, etc.).

    Returns:
        tuple: (match_percentage as int, insight string)
    """
    # Combine all resume values into one text block
    resume_text = " ".join([
        " ".join(v) if isinstance(v, list) else str(v)
        for v in resume_data.values()
    ]).lower()

    # Preprocess JD text to extract significant keywords
    jd_words = [word.lower() for word in jd_text.split() if len(word) > 3]
    jd_keywords = list(set(jd_words))  # remove duplicates

    # Match JD keywords with resume content
    matched = [word for word in jd_keywords if word in resume_text]
    missing = list(set(jd_keywords) - set(matched))

    # Calculate percentage
    percent = int((len(matched) / len(jd_keywords)) * 100) if jd_keywords else 0

    # Insights message
    insights = (
        f"✅ Matched {len(matched)} out of {len(jd_keywords)} keywords.\n\n"
        f"❌ Missing Examples: {', '.join(missing[:10])}..."
        if missing else "🎉 All keywords from the JD were found in the resume!"
    )

    return percent, insights
