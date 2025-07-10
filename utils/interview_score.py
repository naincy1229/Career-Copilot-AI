# utils/interview_score.py

def calculate_interview_score(answer):
    score = 0
    suggestions = []

    if len(answer.split()) > 50:
        score += 30
    else:
        suggestions.append("Provide more detailed answers with examples.")

    if any(phrase in answer.lower() for phrase in ["team", "collaboration", "project", "responsibility"]):
        score += 30
    else:
        suggestions.append("Mention teamwork, responsibilities or projects you've handled.")

    if any(phrase in answer.lower() for phrase in ["improved", "achieved", "resolved", "led", "created"]):
        score += 30
    else:
        suggestions.append("Include action-oriented keywords to highlight achievements.")

    if answer.strip().endswith('.'):
        score += 10
    else:
        suggestions.append("Ensure proper sentence completion.")

    total_score = min(score, 100)
    return total_score, suggestions
