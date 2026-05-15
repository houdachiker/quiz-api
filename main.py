from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Structure d'une question
class Question(BaseModel):
    id: int
    question: str
    choix: list[str]
    reponse: str

questions_db = [
    {
        "id": 1,
        "question": "Qu'est-ce qu'un ordinateur ?",
        "choix": [
            "Une machine électronique qui traite des informations",
            "Un appareil photo",
            "Un instrument de musique",
            "Un véhicule"
        ],
        "reponse": "Une machine électronique qui traite des informations"
    },
    {
        "id": 2,
        "question": "Quel composant est le cerveau de l'ordinateur ?",
        "choix": ["RAM", "CPU", "GPU", "SSD"],
        "reponse": "CPU"
    },
    {
        "id": 3,
        "question": "Quel système d'exploitation est développé par Microsoft ?",
        "choix": ["Linux", "MacOS", "Windows", "Android"],
        "reponse": "Windows"
    },
    {
        "id": 4,
        "question": "Que signifie WWW ?",
        "choix": ["World Wide Web", "World War Web", "Wide World Web", "Web Wide World"],
        "reponse": "World Wide Web"
    },
    {
        "id": 5,
        "question": "Quel langage est utilisé pour Android ?",
        "choix": ["Python", "Swift", "Java", "PHP"],
        "reponse": "Java"
    },
    {
        "id": 6,
        "question": "Que signifie RAM ?",
        "choix": ["Random Access Memory", "Read Access Memory", "Run Access Memory", "Remote Access Memory"],
        "reponse": "Random Access Memory"
    },
    {
        "id": 7,
        "question": "Quel protocole est utilisé pour naviguer sur internet ?",
        "choix": ["FTP", "SMTP", "HTTP", "SSH"],
        "reponse": "HTTP"
    },
    {
        "id": 8,
        "question": "Quel est le système d'exploitation de Apple pour iPhone ?",
        "choix": ["Android", "iOS", "Windows Phone", "HarmonyOS"],
        "reponse": "iOS"
    },
    {
        "id": 9,
        "question": "Combien de bits contient un octet ?",
        "choix": ["4", "8", "16", "32"],
        "reponse": "8"
    },
    {
        "id": 10,
        "question": "Quel langage est principalement utilisé pour les pages web ?",
        "choix": ["Python", "Java", "HTML", "C++"],
        "reponse": "HTML"
    }

]
# ✅ GET - Récupérer toutes les questions
@app.get("/questions")
def get_questions():
    return questions_db

# ✅ GET - Récupérer une question par ID
@app.get("/questions/{id}")
def get_question(id: int):
    for q in questions_db:
        if q["id"] == id:
            return q
    return {"erreur": "Question non trouvée"}

# ✅ POST - Ajouter une question
@app.post("/questions")
def add_question(question: Question):
    questions_db.append(question.dict())
    return {"message": "Question ajoutée avec succès", "question": question}

# ✅ PUT - Modifier une question
@app.put("/questions/{id}")
def update_question(id: int, question: Question):
    for i, q in enumerate(questions_db):
        if q["id"] == id:
            questions_db[i] = question.dict()
            return {"message": "Question modifiée avec succès"}
    return {"erreur": "Question non trouvée"}

# ✅ DELETE - Supprimer une question
@app.delete("/questions/{id}")
def delete_question(id: int):
    for i, q in enumerate(questions_db):
        if q["id"] == id:
            questions_db.pop(i)
            return {"message": "Question supprimée avec succès"}
    return {"erreur": "Question non trouvée"}