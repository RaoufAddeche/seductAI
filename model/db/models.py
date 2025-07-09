# 📄 models.py — Modèle Interaction

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from model.db.database import Base

# 👤 User
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user")

    # 🔁 Reverse link avec interactions
    interactions = relationship("Interaction", back_populates="user")



class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    question = Column(String, nullable=False)
    final_answer = Column(String, nullable=False)
    agents_used = Column(String, default="[]")  # stocké en JSON string


    confiance = Column(Float)
    clarte = Column(Float)
    empathie = Column(Float)
    assertivite = Column(Float)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 🔁 Relation vers l'utilisateur
    user = relationship("User", back_populates="interactions")

