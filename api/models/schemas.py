# 📦 schemas.py — Pydantic models (entrées/sorties API)

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# ✅ Requête d'inscription
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

# ✅ Réponse utilisateur
class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

    class Config:
        orm_mode = True

# ✅ Token de réponse
class Token(BaseModel):
    access_token: str
    token_type: str

# ✅ Données d'entrée pour une interaction
class InteractionCreate(BaseModel):
    question: str
    final_answer: str
    confiance: Optional[float] = None
    clarte: Optional[float] = None
    empathie: Optional[float] = None
    assertivite: Optional[float] = None


# ✅ Réponse complète pour une interaction
class InteractionOut(BaseModel):
    id: int
    user_id: int
    question: str
    final_answer: str
    confiance: Optional[float]
    clarte: Optional[float]
    empathie: Optional[float]
    assertivite: Optional[float]
    created_at: datetime

    class Config:
        orm_mode = True
