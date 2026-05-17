from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

app = FastAPI(title="Quiz API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== Init Firebase =====
if not firebase_admin._apps:
    firebase_json = os.environ.get("FIREBASE_CREDENTIALS")
    cred = credentials.Certificate(json.loads(firebase_json))
    firebase_admin.initialize_app(cred)

db = firestore.client()
COLLECTION = "questions"

# ===== Modèle =====
class Question(BaseModel):
    id: int
    question: str
    choix: List[str]
    reponse: str
    image: Optional[str] = None

# ===== Données par défaut (seed si collection vide) =====
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

def seed_if_empty():
    docs = db.collection(COLLECTION).limit(1).get()
    if not docs:
        for q in DEFAULT_QUESTIONS:
            db.collection(COLLECTION).document(str(q["id"])).set(q)

seed_if_empty()

# ===== HELPERS =====
def get_all() -> List[dict]:
    docs = db.collection(COLLECTION).order_by("id").get()
    return [doc.to_dict() for doc in docs]

def get_one(id: int):
    doc = db.collection(COLLECTION).document(str(id)).get()
    if doc.exists:
        return doc.to_dict()
    return None

# ===== ENDPOINTS =====

@app.get("/questions", response_model=List[Question])
def get_questions():
    return get_all()

@app.get("/questions/{id}", response_model=Question)
def get_question(id: int):
    q = get_one(id)
    if not q:
        raise HTTPException(status_code=404, detail="Question non trouvée")
    return q

@app.post("/questions", response_model=Question, status_code=201)
def add_question(question: Question):
    if get_one(question.id):
        raise HTTPException(status_code=400, detail="ID déjà existant")
    db.collection(COLLECTION).document(str(question.id)).set(question.dict())
    return question

@app.put("/questions/{id}", response_model=Question)
def update_question(id: int, updated: Question):
    if not get_one(id):
        raise HTTPException(status_code=404, detail="Question non trouvée")
    db.collection(COLLECTION).document(str(id)).set(updated.dict())
    return updated

@app.delete("/questions/{id}")
def delete_question(id: int):
    if not get_one(id):
        raise HTTPException(status_code=404, detail="Question non trouvée")
    db.collection(COLLECTION).document(str(id)).delete()
    return {"message": f"Question {id} supprimée"}
