# 📄 progression_router.py — Progression et classe IA utilisateur

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.auth.dependencies import get_current_user, get_db
from model.db.models import Interaction, User
from typing import Optional
from statistics import mean

router = APIRouter()

def safe_mean(values: list[Optional[float]]) -> float:
    """
    Calcule la moyenne arrondie à 2 décimales sur une liste, en filtrant les None.
    Retourne 0.0 si la liste est vide ou sans valeurs valides.
    """
    values = [v for v in values if v is not None]
    return round(mean(values), 2) if values else 0.0

def update_user_class_if_ready(db: Session, user: User):
    """
    Attribue automatiquement une classe IA à l'utilisateur s'il a >10 interactions,
    selon son score dominant. Ne met à jour que si pas déjà attribuée.
    """
    interactions = db.query(Interaction).filter(Interaction.user_id == user.id).all()
    if len(interactions) < 10:
        print(f"[DEBUG] Moins de 10 interactions, pas encore de classe attribuée")
        return
    if user.classe:
        print(f"[DEBUG] Classe déjà attribuée ({user.classe}), pas de mise à jour")
        return

    # Calcul scores moyens
    scores = {
        "confiance": safe_mean([i.confiance for i in interactions]),
        "clarte": safe_mean([i.clarte for i in interactions]),
        "empathie": safe_mean([i.empathie for i in interactions]),
        "assertivite": safe_mean([i.assertivite for i in interactions]),
        "authenticite": safe_mean([i.authenticite for i in interactions]),
        "creativite": safe_mean([i.creativite for i in interactions])
    }
    mapping = {
        "confiance": "Charismatique",
        "clarte": "Direct",
        "empathie": "Émotionnel",
        "assertivite": "Déterminé",
        "authenticite": "Sincère",
        "creativite": "Inattendu"
    }
    dominante = max(scores, key=scores.get)
    classe_finale = mapping.get(dominante, "Inconnu")
    user.classe = classe_finale
    db.commit()
    print(f"[DEBUG] Classe attribuée : {classe_finale}")

@router.get(
    "/me/progression",
    summary="Récupère la progression globale, scores et classe IA utilisateur"
)
def get_user_progression(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retourne la progression et les scores moyens utilisateur :
    - scores (dict avec confiance, clarté, etc.)
    - profil dominant calculé
    - classe IA si attribuée
    - analyse_complete (True/False selon nombre d'interactions)
    """
    print(f"[DEBUG] Calcul progression pour user {current_user.username} ({current_user.id})")

    interactions = db.query(Interaction)\
        .filter(Interaction.user_id == current_user.id)\
        .all()

    if not interactions:
        return {
            "message": "Aucune interaction enregistrée.",
            "scores": None,
            "profil_relationnel": "Inconnu",
            "analyse_complete": False,
            "classe_actuelle": None
        }

    # Récupération et moyenne scores
    scores = {
        "confiance": safe_mean([i.confiance for i in interactions]),
        "clarte": safe_mean([i.clarte for i in interactions]),
        "empathie": safe_mean([i.empathie for i in interactions]),
        "assertivite": safe_mean([i.assertivite for i in interactions]),
        "authenticite": safe_mean([i.authenticite for i in interactions]),
        "creativite": safe_mean([i.creativite for i in interactions])
    }

    print("[DEBUG] Moyennes calculées :", scores)

    # Profil dominant
    mapping = {
        "confiance": "Charismatique",
        "clarte": "Direct",
        "empathie": "Émotionnel",
        "assertivite": "Déterminé",
        "authenticite": "Sincère",
        "creativite": "Inattendu"
    }
    max_score = max(scores, key=scores.get)
    profil_relationnel = mapping.get(max_score, "Inconnu")

    # Update classe si prêt
    update_user_class_if_ready(db, current_user)

    return {
        "scores": scores,
        "profil_relationnel": profil_relationnel,
        "analyse_complete": len(interactions) >= 10,
        "classe_actuelle": current_user.classe
    }
