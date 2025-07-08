from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from model.db.database import SessionLocal
from model.db.models import Interaction

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# POST : pour insérer manuellement une interaction (optionnel mais tu l'as déjà)
@router.post("/interactions")
def create_interaction(interaction: dict, db: Session = Depends(get_db)):
    new_interaction = Interaction(**interaction)
    db.add(new_interaction)
    db.commit()
    db.refresh(new_interaction)
    return new_interaction

# GET avec pagination
@router.get("/interactions")
def get_interactions(
    limit: int = Query(10, description="Nombre d’éléments par page"),
    offset: int = Query(0, description="Décalage"),
    db: Session = Depends(get_db)
):
    return db.query(Interaction)\
             .order_by(Interaction.created_at.desc())\
             .offset(offset)\
             .limit(limit)\
             .all()


# 🔢 GET : Nombre total d'interactions (utile pour la pagination front)
@router.get("/interactions/count")
def get_interaction_count(db: Session = Depends(get_db)):
    total = db.query(Interaction).count()
    return {"total": total}
