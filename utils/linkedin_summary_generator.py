# utils/linkedin_summary_generator.py

def generate_linkedin_summary(resume_text):
    """
    Generate a professional LinkedIn summary based on resume content.
    """
    from transformers import pipeline
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

    # Use only the first 1024 characters (limitation of summarization model)
    input_text = resume_text[:1024]

    summary = summarizer(input_text, max_length=130, min_length=30, do_sample=False)
    return summary[0]["summary_text"]
