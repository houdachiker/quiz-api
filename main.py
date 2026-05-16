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

# ===== Modèle avec champ image =====
class Question(BaseModel):
    id: int
    question: str
    choix: List[str]
    reponse: str
    image: Optional[str] = None  # URL image (optionnel)

# ===== Fichier JSON pour persistance =====
DATA_FILE = "questions.json"

def load_questions() -> List[dict]:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return DEFAULT_QUESTIONS

def save_questions(questions: List[dict]):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)

# ===== Données par défaut =====
DEFAULT_QUESTIONS = [
    {"id":1,"question":"Qu'est-ce qu'un ordinateur ?","choix":["Une machine électronique qui traite des informations","Un appareil photo","Un instrument de musique","Un véhicule"],"reponse":"Une machine électronique qui traite des informations","image":None},
    {"id":2,"question":"Quel composant est le cerveau de l'ordinateur ?","choix":["RAM","CPU","GPU","SSD"],"reponse":"CPU","image":None},
    {"id":3,"question":"Quel système d'exploitation est développé par Microsoft ?","choix":["Linux","MacOS","Windows","Android"],"reponse":"Windows","image":None},
    {"id":4,"question":"Que signifie WWW ?","choix":["World Wide Web","World War Web","Wide World Web","Web Wide World"],"reponse":"World Wide Web","image":None},
    {"id":5,"question":"Quel langage est utilisé pour Android ?","choix":["Python","Swift","Java","PHP"],"reponse":"Java","image":None},
    {"id":6,"question":"Que signifie RAM ?","choix":["Random Access Memory","Read Access Memory","Run Access Memory","Remote Access Memory"],"reponse":"Random Access Memory","image":None},
    {"id":7,"question":"Quel protocole est utilisé pour naviguer sur internet ?","choix":["FTP","SMTP","HTTP","SSH"],"reponse":"HTTP","image":None},
    {"id":8,"question":"Quel est le système d'exploitation de Apple pour iPhone ?","choix":["Android","iOS","Windows Phone","HarmonyOS"],"reponse":"iOS","image":None},
    {"id":9,"question":"Combien de bits contient un octet ?","choix":["4","8","16","32"],"reponse":"8","image":None},
    {"id":10,"question":"Quel langage est principalement utilisé pour les pages web ?","choix":["Python","Java","HTML","C++"],"reponse":"HTML","image":None},
]

# ===== ENDPOINTS =====

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
