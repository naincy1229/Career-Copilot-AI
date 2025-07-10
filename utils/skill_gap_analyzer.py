import re
import string
from collections import Counter

def clean_and_tokenize(text):
    """Clean and tokenize text into keywords."""
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = text.split()
    stopwords = {
        'a', 'an', 'the', 'and', 'or', 'in', 'on', 'at', 'to', 'from', 'for',
        'with', 'by', 'of', 'as', 'is', 'are', 'was', 'were', 'this', 'that',
        'it', 'be', 'has', 'have', 'you', 'your', 'will', 'shall'
    }
    return [t for t in tokens if t not in stopwords and len(t) > 2]

def analyze_skill_gap(resume_text, jd_text):
    """Compare resume and JD to detect missing or weak skills."""
    resume_tokens = clean_and_tokenize(resume_text)
    jd_tokens = clean_and_tokenize(jd_text)

    resume_freq = Counter(resume_tokens)
    jd_keywords = set(jd_tokens)

    matched = [kw for kw in jd_keywords if kw in resume_freq]
    missing = [kw for kw in jd_keywords if kw not in resume_freq]
    weak = [kw for kw in matched if resume_freq[kw] < 2]

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "weak_skills": weak
    }
