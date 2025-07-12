from transformers import pipeline

# Load the model once globally
qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

def answer_career_question(resume_data, question):
    if not question:
        return "❗ Please enter a valid career-related question."

    prompt = f"{resume_data}"

    try:
        result = qa_pipeline(question=question, context=prompt)
        return f"💡 Answer: {result['answer']}"
    except Exception as e:
        return f"❌ Error generating answer: {e}"
