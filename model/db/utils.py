# 📄 utils.py — Helpers pour interactions et messages

import logging
from datetime import datetime, timedelta, timezone
from sqlalchemy.exc import SQLAlchemyError
from model.db.database import SessionLocal
from model.db.models import Interaction, Message

log = logging.getLogger(__name__)

# 💾 Enregistre ou met à jour une interaction (avec scoring et réponse finale)
def save_interaction_to_db(user_id, question, final_answer, scores, agents_used=None, interaction_id=None):
    session = SessionLocal()
    try:
        if interaction_id:
            interaction = session.query(Interaction).get(interaction_id)
            if interaction:
                interaction.question = question
                interaction.final_answer = final_answer
                interaction.confiance = scores.get("confiance")
                interaction.clarte = scores.get("clarte")
                interaction.empathie = scores.get("empathie")
                interaction.assertivite = scores.get("assertivite")
                interaction.authenticite = scores.get("authenticite")
                interaction.creativite = scores.get("creativite")
                interaction.agents_used = agents_used if agents_used else []
                interaction.updated_at = datetime.utcnow()
                # interaction.status = "closed"  # <-- On laisse "open" sauf si explicitement fermé
                session.commit()
                print("[✅] Interaction mise à jour :", interaction.id)
                return interaction.id
            else:
                print("[⚠️] ID interaction non trouvé, création d’une nouvelle…")
        # Nouvelle interaction si pas d’ID valide
        new_interaction = Interaction(
            user_id=user_id,
            question=question,
            final_answer=final_answer,
            confiance=scores.get("confiance"),
            clarte=scores.get("clarte"),
            empathie=scores.get("empathie"),
            assertivite=scores.get("assertivite"),
            authenticite=scores.get("authenticite"),
            creativite=scores.get("creativite"),
            agents_used=agents_used if agents_used else [],
            status="open"
        )
        session.add(new_interaction)
        session.commit()
        session.refresh(new_interaction)
        print("[💾] Nouvelle interaction enregistrée :", new_interaction.id)
        return new_interaction.id

    except SQLAlchemyError as e:
        print("[❌] Erreur DB (interaction) :", e)
        session.rollback()
        return None
    finally:
        session.close()



# 💬 Enregistre un message dans le thread
def save_message_to_db(interaction_id, sender, content, user_id, role=None, timestamp=None):
    session = SessionLocal()
    try:
        message = Message(
            interaction_id=interaction_id,
            sender=sender,
            content=content,
            user_id=user_id,
            role=role,
            timestamp=timestamp or datetime.utcnow(),
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


# 🔁 Récupère une interaction ouverte ou en crée une nouvelle
def get_or_create_open_interaction(user_id: int):
    session = SessionLocal()
    try:
        interaction = (
            session.query(Interaction)
            .filter_by(user_id=user_id, status="open")
            .order_by(Interaction.updated_at.desc())
            .first()
        )

        now_utc = datetime.now(timezone.utc)

        if interaction:
            last_update = interaction.updated_at or interaction.created_at
            print(f"[DEBUG] now_utc = {now_utc} / last_update = {last_update}")

            if now_utc - last_update > timedelta(minutes=20):
                interaction.status = "closed"
                session.commit()
                print(f"[DEBUG] ⏱️ Interaction {interaction.id} fermée automatiquement (>20min)")
            else:
                print(f"[DEBUG] ✅ Réutilisation interaction : {interaction.id}")
                return interaction

        # ➕ Aucune interaction valide → création
        new_interaction = Interaction(
            user_id=user_id,
            status="open",
            created_at=now_utc,
            updated_at=now_utc,
            question="",
            final_answer=""
        )
        session.add(new_interaction)
        session.commit()
        session.refresh(new_interaction)
        print(f"[DEBUG] ➕ Nouvelle interaction créée : {new_interaction.id}")
        return new_interaction

    except Exception as e:
        print("[❌] Erreur get_or_create_open_interaction:", e)
        session.rollback()
        return None
    finally:
        session.close()


# 📥 Récupère une interaction par ID et user_id (pour vérification d’accès)
def get_interaction_by_id(session, interaction_id: int, user_id: int):
    try:
        interaction = (
            session.query(Interaction)
            .filter_by(id=interaction_id, user_id=user_id)
            .first()
        )
        return interaction
    except SQLAlchemyError as e:
        print("[❌] Erreur DB (get_interaction_by_id) :", e)
        return None
