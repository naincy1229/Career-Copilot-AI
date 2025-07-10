import ollama

def suggest_roles(resume_data, model="gemma:2b"):
    if not resume_data:
        return "Resume data is missing. Please upload a valid resume."

    prompt = (
        f"You are a career advisor. Based on the following resume data:\n\n"

        f"{resume_data}\n\n"
        f"Suggest the top 3 most suitable job roles for this candidate and explain why."
    )

    try:
        response = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response["message"]["content"]

    except Exception as e:
        return f"Error generating role recommendations: {str(e)}"
