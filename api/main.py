from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json
import os

app = FastAPI(title="Quiz API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    id: int
    question: str
    choix: List[str]
    reponse: str
    image: Optional[str] = None

DATA_FILE = os.path.join(os.path.dirname(__file__), "questions.json")

def load_questions():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_questions(questions):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)

@app.get("/questions", response_model=List[Question])
def get_questions():
    return load_questions()

@app.get("/questions/{id}", response_model=Question)
def get_question(id: int):
    for q in load_questions():
        if q["id"] == id:
            return q
    raise HTTPException(status_code=404, detail="Question non trouvée")

@app.post("/questions", response_model=Question, status_code=201)
def add_question(question: Question):
    questions = load_questions()
    for q in questions:
        if q["id"] == question.id:
            raise HTTPException(status_code=400, detail="ID déjà existant")
    questions.append(question.dict())
    save_questions(questions)
    return question

@app.put("/questions/{id}", response_model=Question)
def update_question(id: int, updated: Question):
    questions = load_questions()
    for i, q in enumerate(questions):
        if q["id"] == id:
            questions[i] = updated.dict()
            save_questions(questions)
            return updated
    raise HTTPException(status_code=404, detail="Question non trouvée")

@app.delete("/questions/{id}")
def delete_question(id: int):
    questions = load_questions()
    for i, q in enumerate(questions):
        if q["id"] == id:
            questions.pop(i)
            save_questions(questions)
            return {"message": f"Question {id} supprimée"}
    raise HTTPException(status_code=404, detail="Question non trouvée")
