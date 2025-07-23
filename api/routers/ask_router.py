from fastapi import APIRouter, Depends, HTTPException, Request, Path
from model.graph.classifier_graph import graph
from model.db.models import User, Message
from api.auth.dependencies import get_current_user
from api.models.schemas import AskResponse
from model.db.utils import get_interaction_by_id
from sqlalchemy.orm import Session
from api.auth.dependencies import get_db

router = APIRouter()

@router.post("/ask/{interaction_id}", response_model=AskResponse)
def ask_from_existing_interaction(
    interaction_id: int = Path(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    request: Request = None
):
    print(f"[DEBUG] Demande d'IA pour interaction ID={interaction_id}")

    # ✅ Vérifie que l'interaction existe et appartient à l'utilisateur
    interaction = get_interaction_by_id(db, interaction_id, current_user.id)
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction non trouvée.")

    # 🧾 Récupère TOUS les messages du thread, triés par timestamp (mémoire complète)
    thread_messages = (
        db.query(Message)
        .filter_by(interaction_id=interaction_id)
        .order_by(Message.timestamp.asc())
        .all()
    )

    if not thread_messages:
        raise HTTPException(status_code=400, detail="Aucun message dans ce thread.")

    # 🔁 Formatte pour le LLM
    full_thread = [
        {
            "role": msg.role or msg.sender,
            "content": msg.content.strip()
        }
        for msg in thread_messages if msg.content.strip()
    ]

    print(f"[DEBUG] Contexte transmis à l'IA :")
    for m in full_thread:
        print(m)

    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    state = {
        "messages": full_thread,  # 🆕 On passe tout le thread
        "response": "",
        "final_answer": "",
        "scores": {},
        "agents_used": [],
        "user_id": current_user.id,
        "interaction_id": interaction_id,
        "token": token
    }

    # 🚀 Lancement du graphe (le prompt ou l’agent doit utiliser state["messages"])
    output = graph.invoke(state)

    return {
        "final_answer": output["final_answer"],
        "scores": output["scores"],
        "agents_used": output.get("agents_used", [])
    }
