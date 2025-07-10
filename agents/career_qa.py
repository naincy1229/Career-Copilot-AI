import ollama

def answer_career_question(resume_data, question, model="gemma:2b"):
    if not question:
        return "❗ Please enter a valid career-related question."

    prompt = (
        "You are an expert AI career assistant.\n"
        "Based on the user's resume below, answer their question.\n\n"
        f"📄 Resume:\n{resume_data}\n\n"
        f"💬 Question:\n{question}\n\n"
        "🧠 Give an informative, professional answer."
    )

    try:
        response = ollama.chat(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response["message"]["content"]
    except Exception as e:
        return f"❌ Error generating answer: {e}"
