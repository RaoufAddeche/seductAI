# 📄 model/db/utils.py

from model.db.database import SessionLocal
from model.db.models import Interaction

def save_interaction_to_db(question, final_answer, scores):
    from sqlalchemy.exc import SQLAlchemyError
    session = SessionLocal()
    try:
        interaction = Interaction(
            question=question,
            final_answer=final_answer,
            confiance=scores.get("confiance"),
            clarte=scores.get("clarte"),
            empathie=scores.get("empathie"),
            assertivite=scores.get("assertivite"),
        )
        session.add(interaction)
        session.commit()
        print("[💾] Interaction enregistrée en BDD.")
    except SQLAlchemyError as e:
        print("[❌] Erreur lors de l'enregistrement :", e)
        session.rollback()
    finally:
        session.close()
