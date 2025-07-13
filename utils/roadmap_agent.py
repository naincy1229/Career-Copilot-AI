# chains/roadmap_agent.py

import streamlit as st
from transformers import pipeline, set_seed

@st.cache_resource
def load_text_gen_model():
    try:
        return pipeline("text-generation", model="distilgpt2")
    except Exception as e:
        st.error(f"🚨 Error loading model: {e}")
        return None

generator = load_text_gen_model()

def generate_learning_roadmap(resume_data, user_query):
    if not generator:
        return "❌ Model loading failed. Please try again later."

    prompt = f"""
Resume Summary:
{resume_data}

Career Goal:
{user_query}

Create a detailed and personalized 3-month learning roadmap to help the user achieve the goal. Include:
- Weekly milestones
- Skills to focus on
- Recommended online resources (e.g., Coursera, YouTube, GitHub)
- Tools or projects to build
"""

    try:
        set_seed(42)
        output = generator(prompt, max_length=512, num_return_sequences=1, do_sample=True)[0]["generated_text"]

        # Clean and return only the relevant part
        roadmap = output.split("Career Goal:")[-1].strip()
        return "🧭 **Your AI Learning Roadmap**\n\n" + roadmap

    except Exception as e:
        return f"❌ Failed to generate roadmap: {e}"
