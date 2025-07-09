# 📄 ask_router.py
from fastapi import APIRouter
from pydantic import BaseModel
from model.graph.classifier_graph import graph

router = APIRouter()

class AskRequest(BaseModel):
    user_id: int
    question: str

@router.post("/ask")
def ask_question(payload: AskRequest):
    print(f"[🚀] Question reçue : {payload.question}")

    # Lancement du graphe
    output = graph.invoke({
        "user_id": payload.user_id,
        "question": payload.question,
        "response": "",
        "final_answer": "",
        "scores": {},
        "agents_used": []
    })

    return {
        "final_answer": output["final_answer"],
        "scores": output["scores"],
        "agents_used": output["agents_used"]
    }
