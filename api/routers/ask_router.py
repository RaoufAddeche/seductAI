# 📄 ask_router.py

from fastapi import APIRouter, Depends, HTTPException, Request
from model.graph.classifier_graph import graph  # ⚙️ Graphe LangGraph
from model.db.models import User
from api.auth.dependencies import get_current_user
from api.models.schemas import AskRequest, AskResponse

router = APIRouter()

@router.post("/ask", response_model=AskResponse)
def ask_question(payload: AskRequest, current_user: User = Depends(get_current_user), request: Request = None):
    """
    Endpoint principal pour interroger l'IA.
    🔐 Protégé : nécessite un token JWT valide.
    """
    question = payload.question

    if not question:
        raise HTTPException(status_code=400, detail="Champ 'question' requis")

    print(f"[DEBUG] Question reçue : {question}")
    print(f"[DEBUG] Utilisateur : {current_user.username} (ID: {current_user.id})")

    # 👇 State transmis au graphe LangGraph
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    state = {
        "question": question,
        "response": "",
        "final_answer": "",
        "scores": {},
        "agents_used": [],
        "user_id": current_user.id,
        "token" : token
    }

    output = graph.invoke(state)

    return {
        "final_answer": output["final_answer"],
        "scores": output["scores"],
        "agents_used": output.get("agents_used", [])
    }
