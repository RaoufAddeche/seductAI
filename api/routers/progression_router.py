# 📄 progression_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.auth.dependencies import get_current_user, get_db
from model.db.models import Interaction, User
from typing import Optional
from statistics import mean

router = APIRouter()

# 💡 Fonction utilitaire : calcule la moyenne si valeurs disponibles
def safe_mean(values: list[Optional[float]]) -> float:
    values = [v for v in values if v is not None]
    return round(mean(values), 2) if values else 0.0

# 🧠 Met à jour la classe IA de l'utilisateur s’il a assez d'interactions
def update_user_class_if_ready(db: Session, user: User):
    interactions = db.query(Interaction).filter(Interaction.user_id == user.id).all()

    if len(interactions) < 10:
        print(f"[DEBUG] Moins de 10 interactions, pas encore de classe attribuée")
        return

    # Vérifie si la classe a déjà été attribuée
    if user.classe:
        print(f"[DEBUG] Classe déjà attribuée ({user.classe}), pas de mise à jour")
        return

    # Calcul des moyennes
    confiance = safe_mean([i.confiance for i in interactions])
    clarte = safe_mean([i.clarte for i in interactions])
    empathie = safe_mean([i.empathie for i in interactions])
    assertivite = safe_mean([i.assertivite for i in interactions])
    authenticite = safe_mean([i.authenticite for i in interactions])
    creativite = safe_mean([i.creativite for i in interactions])

    scores = {
        "confiance": confiance,
        "clarte": clarte,
        "empathie": empathie,
        "assertivite": assertivite,
        "authenticite": authenticite,
        "creativite": creativite
    }

    # 🎭 Mapping des classes IA selon la dominante
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

    # Mise à jour du user
    user.classe = classe_finale
    db.commit()
    print(f"[DEBUG] Classe attribuée : {classe_finale}")


# 📌 GET : Récupère la progression globale de l’utilisateur
@router.get("/me/progression")
def get_user_progression(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    print(f"[DEBUG] Calcul progression pour user {current_user.username} ({current_user.id})")

    interactions = db.query(Interaction)\
        .filter(Interaction.user_id == current_user.id)\
        .all()

    if not interactions:
        return {
            "message": "Aucune interaction enregistrée.",
            "scores": None,
            "profil_relationnel": "Inconnu"
        }

    # 🎯 Récupération des scores
    confiance_list = [i.confiance for i in interactions]
    clarte_list = [i.clarte for i in interactions]
    empathie_list = [i.empathie for i in interactions]
    assertivite_list = [i.assertivite for i in interactions]
    authenticite_list = [i.authenticite for i in interactions]
    creativite_list = [i.creativite for i in interactions]


    # ✅ Moyennes sécurisées
    scores = {
        "confiance": safe_mean(confiance_list),
        "clarte": safe_mean(clarte_list),
        "empathie": safe_mean(empathie_list),
        "assertivite": safe_mean(assertivite_list),
        "authenticite": safe_mean(authenticite_list),
        "creativite": safe_mean(creativite_list)
    }


    print("[DEBUG] Moyennes calculées :", scores)

    # 📌 Déduction d’un style basé sur le score dominant
    max_score = max(scores, key=scores.get)
    mapping = {
        "confiance": "Charismatique",
        "clarte": "Direct",
        "empathie": "Émotionnel",
        "assertivite": "Déterminé",
        "authenticite": "Sincère",
        "creativite": "Inattendu"
    }


    profil_relationnel = mapping.get(max_score, "Inconnu")
    update_user_class_if_ready(db, current_user)

    return {
        "scores": scores,
        "profil_relationnel": profil_relationnel,
        "classe_actuelle" : current_user.classe
    }
