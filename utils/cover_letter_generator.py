from transformers import pipeline

def generate_cover_letter(resume_text, job_description, model="microsoft/DialoGPT-medium"):
    # Limit input to avoid long delays
    resume_text = resume_text[:1000]
    job_description = job_description[:1000]

    prompt = f"""
Write a professional and concise cover letter for the job described below.

Job Description:
{job_description}

Candidate Resume:
{resume_text}

Cover Letter:
"""

    generator = pipeline("text-generation", model=model)
    output = generator(prompt, max_length=400, num_return_sequences=1, do_sample=True)
    return output[0]["generated_text"].replace(prompt, "").strip()

