from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json
import os

app = FastAPI(title="Quiz API")

app.add_middleware(
    CORSMiddlewarefrom fastapi import FastAPI, HTTPException
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

# ✅ CORRECTION : chemin correct vers questions.json
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "questions.json")

def load_questions():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Erreur lecture fichier: {e}")
        return []

def save_questions(questions):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(questions, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Erreur écriture fichier: {e}")

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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "..", "questions.json")

def load_questions():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_questions(questions):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(questions, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

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
