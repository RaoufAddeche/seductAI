# 📄 utils.py — Helpers pour interactions et messages

import json
from model.db.database import SessionLocal
from model.db.models import Interaction , Message
from sqlalchemy.exc import SQLAlchemyError
import logging



log = logging.getLogger(__name__)

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
            authenticite=scores.get("authenticite"),
            creativite=scores.get("creativite"),
            agents_used=json.dumps(agents_used) if agents_used else None
        )
        session.add(interaction)
        session.commit()

        session.refresh(interaction)  # ✅ POUR OBTENIR L'ID APRÈS COMMIT
        print("[💾] Interaction enregistrée avec ID :", interaction.id)

        return interaction.id  # ✅ POUR QUE LE GRAPHE PUISSE L’UTILISER
    except SQLAlchemyError as e:
        print("[❌] Erreur DB:", e)
        session.rollback()
        return None  # ✅ Bonne pratique en cas d’erreur
    finally:
        session.close()



def save_message_to_db(interaction_id, sender, content, user_id, role=None):
    session = SessionLocal()
    try:
        message = Message(
            interaction_id=interaction_id,
            sender=sender,
            content=content,
            user_id=user_id,
            role=role  # ← ici on le passe aussi
        )
        log.warning(message)
        session.add(message)
        session.commit()
        print(f"[💬] Message de {sender} enregistré (interaction {interaction_id})")
    except SQLAlchemyError as e:
        print("[❌] Erreur DB (message) :", e)
        session.rollback()
    finally:
        session.close()

