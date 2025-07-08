# 📄 models.py
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from model.db.database import Base

class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, nullable=False)
    final_answer = Column(String, nullable=False)

    confiance = Column(Float)
    clarte = Column(Float)
    empathie = Column(Float)
    assertivite = Column(Float)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
