# 📦 interactions_router.py — Endpoints de gestion des threads & messages (version clean)

from fastapi import APIRouter, Depends, Query, HTTPException, Path
from sqlalchemy.orm import Session
from api.auth.dependencies import get_current_user, get_db
from model.db.models import Interaction, User, UserScore, Message
from api.models.schemas import (
    InteractionCreate, InteractionOut,
    MessageCreate, MessageRead
)
from typing import List
from datetime import datetime

router = APIRouter()

# 📊 Met à jour les scores cumulés de l'utilisateur (moyenne pondérée)
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

# ⚡ Garantit que chaque message a un role non-null
def fix_messages_roles(interactions: List[Interaction]):
    for interaction in interactions:
        for msg in interaction.messages:
            if not msg.role:
                msg.role = "user"  # Valeur par défaut

# === INTERACTIONS ===

@router.post("/interactions", response_model=InteractionOut, summary="Créer une nouvelle interaction (thread)")
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

    fix_messages_roles([new_interaction])
    return new_interaction

@router.post("/interactions/start", response_model=InteractionOut, summary="Créer une interaction vide (chat sans message)")
def start_empty_interaction(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_interaction = Interaction(
        user_id=current_user.id,
        question="",
        final_answer="",
        agents_used=[],
        status="open"
    )
    db.add(new_interaction)
    db.commit()
    db.refresh(new_interaction)
    print(f"[DEBUG] 💬 Nouvelle interaction vide créée : {new_interaction.id}")
    return new_interaction

@router.get("/interactions", response_model=List[InteractionOut], summary="Liste paginée des interactions utilisateur")
def get_interactions(
    limit: int = Query(10, description="Nombre de résultats"),
    offset: int = Query(0, description="Décalage pour pagination"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    interactions = (
        db.query(Interaction)
        .filter(Interaction.user_id == current_user.id)
        .filter(Interaction.status != "deleted")
        .order_by(Interaction.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    fix_messages_roles(interactions)
    return interactions

@router.get("/interactions/count", summary="Nombre total d'interactions")
def get_interaction_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    total = (
        db.query(Interaction)
        .filter(Interaction.user_id == current_user.id)
        .filter(Interaction.status != "deleted")
        .count()
    )
    return {"total": total}

@router.get("/interactions/latest", summary="Dernière interaction (thread)")
def get_latest_interaction(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    latest = (
        db.query(Interaction)
        .filter(Interaction.user_id == current_user.id)
        .filter(Interaction.status != "deleted")
        .order_by(Interaction.created_at.desc())
        .first()
    )
    if not latest:
        return {"message": "Aucune interaction trouvée", "scores": None}
    fix_messages_roles([latest])
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

@router.get("/me/interactions", response_model=List[InteractionOut], summary="Historique utilisateur (hors supprimées)")
def get_my_interactions(
    limit: int = Query(10),
    offset: int = Query(0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    interactions = (
        db.query(Interaction)
        .filter(Interaction.user_id == current_user.id)
        .filter(Interaction.status != "deleted")
        .order_by(Interaction.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    print(f"[DEBUG] {len(interactions)} interactions récupérées pour {current_user.username}")
    fix_messages_roles(interactions)
    return interactions

@router.patch("/interactions/{interaction_id}/close", summary="Clôturer un thread (chat)")
def close_interaction(
    interaction_id: int = Path(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    interaction = db.query(Interaction).filter_by(id=interaction_id, user_id=current_user.id).first()
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction non trouvée.")
    if interaction.status == "closed":
        return {"message": "Interaction déjà clôturée."}
    interaction.status = "closed"
    interaction.updated_at = datetime.utcnow()
    db.commit()
    print(f"[DEBUG] 🔒 Interaction clôturée : {interaction.id}")
    return {"message": "Interaction fermée avec succès.", "interaction": interaction.id}

@router.patch("/interactions/{interaction_id}/reopen", summary="Rouvrir un thread fermé")
def reopen_interaction(
    interaction_id: int = Path(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    interaction = db.query(Interaction).filter_by(id=interaction_id, user_id=current_user.id).first()
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction non trouvée.")
    if interaction.status == "open":
        return {"message": "L'interaction est déjà ouverte."}
    if interaction.status == "deleted":
        raise HTTPException(status_code=400, detail="Impossible de rouvrir une interaction supprimée.")
    interaction.status = "open"
    interaction.updated_at = datetime.utcnow()
    db.commit()
    print(f"[DEBUG] 🔄 Interaction rouverte : {interaction.id}")
    return {"message": "Interaction rouverte avec succès.", "interaction": interaction.id}

@router.delete("/interactions/{interaction_id}", summary="Suppression logique (soft-delete)")
def delete_interaction(
    interaction_id: int = Path(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    interaction = db.query(Interaction).filter_by(id=interaction_id, user_id=current_user.id).first()
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction non trouvée.")
    if interaction.status == "deleted":
        return {"message": "Interaction déjà supprimée."}
    interaction.status = "deleted"
    interaction.updated_at = datetime.utcnow()
    db.commit()
    print(f"[DEBUG] 🗑️ Interaction supprimée (soft-delete) : {interaction.id}")
    return {"message": "Interaction supprimée avec succès.", "interaction": interaction.id}

# === MESSAGES ===

@router.post("/messages", response_model=MessageRead, summary="Ajouter un message à un thread")
def create_message(
    message: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Crée et sauvegarde un message lié à une interaction.
    - Garantit que le user_id du message est toujours celui du token JWT courant.
    - Rôle = "user" par défaut si absent (pour éviter les incohérences de front).
    - Empêche le double-passage de kwargs (pas de **dict + field doublé).
    """

    role_value = getattr(message, "role", None) or "user"

    new_msg = Message(
        interaction_id=message.interaction_id,
        user_id=current_user.id,          # Toujours pris du JWT, jamais du front
        sender=message.sender or "user",  # "user" ou "assistant"/agent/...
        content=message.content,
        role=role_value
        # timestamp sera auto par défaut
    )
    db.add(new_msg)
    db.commit()
    db.refresh(new_msg)
    print(f"[DEBUG] Nouveau message enregistré : {new_msg.content[:50]}...")
    return new_msg


@router.get("/messages/{interaction_id}", response_model=List[MessageRead], summary="Récupérer les messages d'un thread")
def get_messages_for_interaction(
    interaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    messages = (
        db.query(Message)
        .join(Message.interaction)
        .filter(Interaction.user_id == current_user.id)
        .filter(Message.interaction_id == interaction_id)
        .order_by(Message.timestamp.asc())
        .all()
    )
    for msg in messages:
        if not msg.role:
            msg.role = "user"
    print(f"[DEBUG] {len(messages)} messages récupérés pour interaction {interaction_id}")
    return messages
