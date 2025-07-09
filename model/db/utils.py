# 📄 utils.py — Sauvegarde d'une interaction
import json
from model.db.database import SessionLocal
from model.db.models import Interaction
from sqlalchemy.exc import SQLAlchemyError

def save_interaction_to_db(user_id, question, final_answer, scores, agents_used=None):
    session = SessionLocal()
    try:
        interaction = Interaction(
            user_id=user_id,
            question=question,
            final_answer=final_answer,
            confiance=scores.get("confiance"),
            clarte=scores.get("clarte"),
            empathie=scores.get("empathie"),
            assertivite=scores.get("assertivite"),
            agents_used=json.dumps(agents_used) if agents_used else None  # ✅ Liste encodée en JSON
        )
        session.add(interaction)
        session.commit()
        print("[💾] Interaction enregistrée avec agents utilisés :", agents_used)
    except SQLAlchemyError as e:
        print("[❌] Erreur DB:", e)
        session.rollback()
    finally:
        session.close()
