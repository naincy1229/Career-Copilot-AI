import ollama

def generate_learning_roadmap(resume_data, query, model="gemma:2b"):
    if not query:
        return "Please provide a valid learning goal or topic."

    prompt = (
        f"You are a career guidance AI. A user has provided their resume data below:\n"

        f"{resume_data}\n\n"
        f"They are asking for a learning roadmap with this query:\n{query}\n"
        f"Generate a detailed and actionable learning roadmap tailored to their background."
    )

    response = ollama.chat(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response["message"]["content"]
