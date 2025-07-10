# main.py

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse

from agents.career_qa import answer_career_question
from agents.roadmap_agent import generate_learning_roadmap
from agents.role_recommender import suggest_roles
from resume_parser import parse_resume

import tempfile

app = FastAPI()

@app.post("/analyze/")
async def analyze_resume(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    parsed = parse_resume(tmp_path)
    return JSONResponse(content=parsed)

@app.post("/ask/")
async def ask_question(
    file: UploadFile = File(...),
    question: str = Form(...)
):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    resume = parse_resume(tmp_path)
    answer = answer_career_question(resume, question)
    return {"question": question, "answer": answer}

@app.post("/roles/")
async def recommend_roles(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    resume = parse_resume(tmp_path)
    roles = suggest_roles(resume)
    return {"recommended_roles": roles}

@app.post("/roadmap/")
async def roadmap(file: UploadFile = File(...), goal: str = Form(...)):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    resume = parse_resume(tmp_path)
    roadmap = generate_learning_roadmap(resume, goal)
    return {"goal": goal, "roadmap": roadmap}
