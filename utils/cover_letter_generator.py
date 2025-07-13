from transformers import pipeline

# Use a more suitable model for text generation
generator = pipeline(
    "text-generation",
    model="gpt2",  # You can also try 'EleutherAI/gpt-neo-125M' or 'tiiuae/falcon-7b-instruct' if memory allows
    tokenizer="gpt2"
)

def generate_cover_letter(resume_text, job_description):
    """
    Generate a concise, professional cover letter from resume and JD.
    """
    resume_text = resume_text[:1000]
    job_description = job_description[:1000]

    prompt = f"""
Write a concise and professional cover letter tailored to the following job.

Job Description:
{job_description}

Candidate Resume:
{resume_text}

Cover Letter:
"""

    try:
        output = generator(prompt, max_length=400, num_return_sequences=1, do_sample=True)
        letter = output[0]["generated_text"].replace(prompt, "").strip()
        return letter
    except Exception as e:
        return f"❌ Error generating cover letter: {e}"
