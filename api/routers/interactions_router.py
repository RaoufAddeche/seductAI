from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from api.auth.dependencies import get_current_user, get_db
from model.db.models import Interaction, User, UserScore, Message
from api.models.schemas import (
    InteractionCreate, InteractionOut,
    MessageCreate, MessageRead
)
from typing import List

router = APIRouter()


# 📊 Met à jour les scores de l'utilisateur (moyenne pondérée cumulative)
def update_user_scores(db: Session, user_id: int, new_scores: dict):
    score_obj = db.query(UserScore).filter_by(user_id=user_id).first()
    if not score_obj:
        print(f"[DEBUG] Aucun score trouvé pour user_id={user_id}")
        return

    count = score_obj.interactions_count or 0

    def avg(old, new): return ((old or 0) * count + (new or 0)) / (count + 1)

    score_obj.confiance = avg(score_obj.confiance, new_scores.get("confiance"))
    score_obj.clarte = avg(score_obj.clarte, new_scores.get("clarte"))
    score_obj.empathie = avg(score_obj.empathie, new_scores.get("empathie"))
    score_obj.assertivite = avg(score_obj.assertivite, new_scores.get("assertivite"))
    score_obj.authenticite = avg(score_obj.authenticite, new_scores.get("authenticite"))
    score_obj.creativite = avg(score_obj.creativite, new_scores.get("creativite"))

    score_obj.interactions_count = count + 1
    db.commit()
    print(f"[DEBUG] Scores mis à jour pour user_id={user_id}")


# 📌 POST /interactions : Crée une nouvelle interaction
@router.post("/interactions", response_model=InteractionOut)
def create_interaction(
    interaction: InteractionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_interaction = Interaction(
        **interaction.dict(),
        user_id=current_user.id
    )
    db.add(new_interaction)
    db.commit()
    db.refresh(new_interaction)
    print("[DEBUG] Nouvelle interaction enregistrée :", new_interaction.__dict__)

    update_user_scores(db, user_id=current_user.id, new_scores={
        "confiance": new_interaction.confiance,
        "clarte": new_interaction.clarte,
        "empathie": new_interaction.empathie,
        "assertivite": new_interaction.assertivite,
        "authenticite": new_interaction.authenticite,
        "creativite": new_interaction.creativite
    })

    return new_interaction


# 📌 GET /interactions : Liste paginée des interactions
@router.get("/interactions", response_model=List[InteractionOut])
def get_interactions(
    limit: int = Query(10),
    offset: int = Query(0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Interaction)\
             .filter(Interaction.user_id == current_user.id)\
             .order_by(Interaction.created_at.desc())\
             .offset(offset)\
             .limit(limit)\
             .all()


# 📌 GET /interactions/count : Nombre total d'interactions
@router.get("/interactions/count")
def get_interaction_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    total = db.query(Interaction)\
              .filter(Interaction.user_id == current_user.id)\
              .count()
    return {"total": total}


# 📌 GET /interactions/latest : Dernière interaction
@router.get("/interactions/latest")
def get_latest_interaction(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    latest = (
        db.query(Interaction)
        .filter(Interaction.user_id == current_user.id)
        .order_by(Interaction.created_at.desc())
        .first()
    )

    if not latest:
        return {"message": "Aucune interaction trouvée", "scores": None}

    return {
        "id": latest.id,
        "message": "Dernière interaction récupérée ✅",
        "final_answer": latest.final_answer,
        "scores": {
            "confiance": latest.confiance,
            "clarté": latest.clarte,
            "empathie": latest.empathie,
            "assertivité": latest.assertivite,
            "authenticité": latest.authenticite,
            "créativité": latest.creativite,
        },
    }


# 📌 GET /me/interactions : Historique propre (peu utilisé)
@router.get("/me/interactions", response_model=List[InteractionOut])
def get_my_interactions(
    limit: int = Query(10),
    offset: int = Query(0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    interactions = db.query(Interaction)\
                     .filter(Interaction.user_id == current_user.id)\
                     .order_by(Interaction.created_at.desc())\
                     .offset(offset)\
                     .limit(limit)\
                     .all()
    print(f"[DEBUG] {len(interactions)} interactions récupérées pour {current_user.username}")
    return interactions


# 📌 POST /messages : Enregistre un message (lié à interaction + user)
@router.post("/messages", response_model=MessageRead)
def create_message(
    message: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_msg = Message(
        **message.dict(),
        user_id=current_user.id  # ✅ Ajout indispensable
    )
    db.add(new_msg)
    db.commit()
    db.refresh(new_msg)
    print(f"[DEBUG] Nouveau message enregistré : {new_msg.content[:50]}...")
    return new_msg


# 📌 GET /messages/{interaction_id} : Récupère tous les messages d’une interaction
@router.get("/messages/{interaction_id}", response_model=List[MessageRead])
def get_messages_for_interaction(
    interaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # ⚠️ Ne passe plus par Message.user_id mais par la relation avec Interaction
    messages = (
        db.query(Message)
        .join(Message.interaction)
        .filter(Interaction.user_id == current_user.id)
        .filter(Message.interaction_id == interaction_id)
        .order_by(Message.timestamp.asc())
        .all()
    )

    print(f"[DEBUG] {len(messages)} messages récupérés pour interaction {interaction_id}")
    return messages
