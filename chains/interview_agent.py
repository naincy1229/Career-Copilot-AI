# chains/interview_agent.py

from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import torch

def run_mock_interview(question):
    tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
    model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

    inputs = tokenizer.encode(question + tokenizer.eos_token, return_tensors="pt")
    outputs = model.generate(inputs, max_length=1000, pad_token_id=tokenizer.eos_token_id)

    reply = tokenizer.decode(outputs[:, inputs.shape[-1]:][0], skip_special_tokens=True)
    return reply
