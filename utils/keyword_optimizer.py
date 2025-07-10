# utils/keyword_optimizer.py
import re
import string
from collections import Counter

def clean_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = text.split()
    return tokens

def extract_keywords(text, top_n=50):
    stopwords = set([
        'a', 'an', 'the', 'and', 'or', 'in', 'on', 'at', 'to', 'from', 'for',
        'with', 'by', 'of', 'as', 'is', 'are', 'was', 'were', 'this', 'that',
        'it', 'be', 'has', 'have', 'you', 'your', 'will', 'shall'
    ])
    tokens = clean_text(text)
    filtered = [t for t in tokens if t not in stopwords and len(t) > 2]
    freq = Counter(filtered)
    return [word for word, _ in freq.most_common(top_n)]

def suggest_keywords(resume_text, jd_text):
    resume_keywords = extract_keywords(resume_text)
    jd_keywords = extract_keywords(jd_text)

    missing_keywords = [kw for kw in jd_keywords if kw not in resume_keywords]
    common_keywords = [kw for kw in jd_keywords if kw in resume_keywords]

    suggestions = []
    if missing_keywords:
        suggestions.append(f"Consider adding these important keywords from the job description: {', '.join(missing_keywords[:10])}")
    if not suggestions:
        suggestions.append("Your resume already contains most relevant keywords!")

    return {
        "missing_keywords": missing_keywords,
        "matched_keywords": common_keywords,
        "suggestions": suggestions
    }
