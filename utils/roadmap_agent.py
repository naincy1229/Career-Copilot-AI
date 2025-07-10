from transformers import pipeline

def generate_learning_roadmap(resume_data, user_query, model="distilgpt2"):
    """
    Generate a learning roadmap based on resume content and career goal.
    """
    text_input = f"""
    Resume Summary:
    {resume_data}

    User Goal:
    {user_query}

    Based on the resume and user's career goal, create a step-by-step 3-month personalized learning roadmap including resources, skills to focus on, and weekly goals.
    """

    try:
        generator = pipeline("text-generation", model=model)
        response = generator(text_input, max_length=512, num_return_sequences=1, do_sample=True)
        roadmap = response[0]["generated_text"].split("User Goal:")[-1].strip()
        return "🧭 **Your AI Learning Roadmap**\n\n" + roadmap
    except Exception as e:
        return f"❌ Failed to generate roadmap: {e}"
