import re
import string
from collections import Counter

def clean_text(text):
    """Lowercase, remove punctuation and tokenize."""
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = text.split()
    return tokens

def extract_keywords(text, top_n=30):
    """Extract most frequent words as keywords, excluding stopwords."""
    stopwords = set([
        'a', 'an', 'the', 'and', 'or', 'in', 'on', 'at', 'to', 'from', 'for',
        'with', 'by', 'of', 'as', 'is', 'are', 'was', 'were', 'this', 'that',
        'it', 'be', 'has', 'have', 'you', 'your', 'will', 'shall'
    ])
    tokens = clean_text(text)
    filtered_tokens = [t for t in tokens if t not in stopwords]
    freq = Counter(filtered_tokens)
    keywords = [word for word, _ in freq.most_common(top_n)]
    return keywords

def calculate_ats_score(resume_text, jd_text):
    resume_keywords = extract_keywords(resume_text)
    jd_keywords = extract_keywords(jd_text)

    matched_keywords = [kw for kw in jd_keywords if kw in resume_keywords]
    missing_keywords = [kw for kw in jd_keywords if kw not in resume_keywords]

    score = int((len(matched_keywords) / len(jd_keywords)) * 100) if jd_keywords else 0

    suggestions = []
    if score < 70:
        suggestions.append("Add more relevant keywords from the job description.")
    if len(missing_keywords) > 0:
        suggestions.append("Include missing skills like: " + ", ".join(missing_keywords[:5]) + "...")
    if any(word in resume_text.lower() for word in ["table", "image", "graphic"]):
        suggestions.append("Avoid using tables or images in resume — not ATS-friendly.")
    if len(resume_text) > 2000:
        suggestions.append("Consider shortening your resume for better readability.")

    return {
        "ats_score": score,
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,
        "suggestions": suggestions
    }
