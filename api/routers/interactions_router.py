from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from api.auth.dependencies import get_current_user, get_db
from model.db.models import Interaction, User
from api.models.schemas import InteractionCreate

router = APIRouter()


# 📌 POST : Crée une nouvelle interaction liée à l'utilisateur connecté
@router.post("/interactions")
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
    return new_interaction


# 📌 GET : Liste les interactions avec pagination
@router.get("/interactions")
def get_interactions(
    limit: int = Query(10, description="Nombre d’éléments par page"),
    offset: int = Query(0, description="Décalage"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Interaction)\
             .filter(Interaction.user_id == current_user.id)\
             .order_by(Interaction.created_at.desc())\
             .offset(offset)\
             .limit(limit)\
             .all()


# 📌 GET : Nombre total d’interactions (utile pour la pagination front)
@router.get("/interactions/count")
def get_interaction_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    total = db.query(Interaction)\
              .filter(Interaction.user_id == current_user.id)\
              .count()
    return {"total": total}


# 📌 GET : Dernière interaction enregistrée
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
        "message": "Dernière interaction récupérée ✅",
        "scores": {
            "confiance": latest.confiance,
            "clarté": latest.clarte,
            "empathie": latest.empathie,
            "assertivité": latest.assertivite
        }
    }
