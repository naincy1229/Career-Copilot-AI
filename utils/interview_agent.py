from transformers import pipeline
import random

BASIC_QUESTIONS = [
    "Tell me about yourself.",
    "Why do you want this job?",
    "What are your strengths and weaknesses?",
    "Where do you see yourself in 5 years?",
    "Why should we hire you?"
]

TECHNICAL_QUESTIONS = [
    "Explain a recent project you've worked on.",
    "How do you approach debugging a problem?",
    "What are your favorite programming languages and why?",
    "Explain the difference between OOP and Functional Programming.",
    "How do you keep up with the latest tech trends?"
]

# Load classifier globally (better for Render)
classifier = pipeline(
    "text-classification",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

def generate_mock_interview_question(resume_data):
    """
    Select a random question based on resume data.
    """
    skills = resume_data.get("skills", [])
    if skills:
        selected = random.choice(TECHNICAL_QUESTIONS + BASIC_QUESTIONS)
    else:
        selected = random.choice(BASIC_QUESTIONS)
    return f"🎤 Interview Question: {selected}"

def analyze_interview_response(response):
    """
    Evaluate the quality of a user's interview answer.
    """
    try:
        result = classifier(response)
        label = result[0]["label"]
        score = result[0]["score"]
        sentiment = "✅ Positive" if label == "POSITIVE" else "⚠️ Needs Improvement"
        return f"🧠 Analysis: {sentiment} (Confidence: {score:.2f})"
    except Exception as e:
        return f"❌ Error analyzing response: {e}"
