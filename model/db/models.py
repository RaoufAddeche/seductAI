# 📄 models.py — Modèle Interaction

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from model.db.database import Base
from datetime import datetime

# 👤 User
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user")

    # Champs modifiables :
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)  # homme, femme, non-binaire, autre
    orientation = Column(String, nullable=True)  # hétéro, bi, homo…
    style_langage = Column(String, nullable=True)  # formel, jeune, chill…
    centre_interets = Column(ARRAY(String), nullable=True)  # ["dating", "confiance"]
    situation = Column(String, nullable=True)  # célibataire, en couple, etc.


    # Champ IA : non modifiable par l'utilisateur
    classe = Column(String, nullable=True)

    # 🔁 Reverse link avec interactions
    interactions = relationship("Interaction", back_populates="user")



class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    question = Column(String, nullable=False)
    final_answer = Column(String, nullable=False)

    agents_used = Column(ARRAY(String), default="[]")
    confiance = Column(Float)
    clarte = Column(Float)
    empathie = Column(Float)
    assertivite = Column(Float)
    authenticite = Column(Float)
    creativite = Column(Float)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 🔁 Relations
    user = relationship("User", back_populates="interactions")
    messages = relationship("Message", back_populates="interaction", cascade="all, delete-orphan") 




# 📊 Score cumulé par utilisateur
class UserScore(Base):
    __tablename__ = "user_scores"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)

    confiance = Column(Float, default=0.0)
    clarte = Column(Float, default=0.0)
    empathie = Column(Float, default=0.0)
    assertivite = Column(Float, default=0.0)
    authenticite = Column(Float, default=0.0)
    creativite = Column(Float, default=0.0)
    interactions_count = Column(Integer, default=0)

    user = relationship("User", backref="score")



class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    interaction_id = Column(Integer, ForeignKey("interactions.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))  # ✅ Ajoute bien cette ligne
    sender = Column(String, nullable=False)  # "user", "ai", "fusion", "agent_message"...
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    role = Column(String, nullable=True)  # "user" ou "assistant"


    interaction = relationship("Interaction", back_populates="messages")
    user = relationship("User")  # 👈 Optionnel mais utile
