# 📦 schemas.py — Pydantic models (entrées/sorties API)

from pydantic import BaseModel, EmailStr, Field
from typing import Optional,Dict,List
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
    age: Optional[int]
    gender: Optional[str]
    orientation: Optional[str]
    style_langage: Optional[str]
    centre_interets: Optional[List[str]]
    situation: Optional[str]
    classe: Optional[str]  # ℹ️ affiché mais pas modifiable

    class Config:
        orm_mode = True

# ✅ Schéma de mise à jour profil (ce que l’utilisateur peut modifier)
class UserUpdate(BaseModel):
    username: Optional[str]
    age: Optional[int]
    gender: Optional[str]
    orientation: Optional[str]
    style_langage: Optional[str]
    centre_interets: Optional[List[str]] = Field(default_factory=list)
    situation: Optional[str]


# ✅ Token de réponse
class Token(BaseModel):
    access_token: str
    token_type: str


# 🧠 Nouveau format d’un message dans le thread
class MessageItem(BaseModel):
    role: str  # "user" ou "assistant"
    content: str


# ✅ Données d'entrée pour une interaction
class InteractionCreate(BaseModel):
    question: str
    final_answer: str
    messages: List[MessageItem]
    confiance: Optional[float] = None
    clarte: Optional[float] = None
    empathie: Optional[float] = None
    assertivite: Optional[float] = None
    authenticite: Optional[float] = None
    creativite: Optional[float] = None



# ✅ Réponse complète pour une interaction
class InteractionOut(BaseModel):
    id: int
    user_id: int
    question: str
    final_answer: str
    messages: List[MessageItem]
    confiance: Optional[float]
    clarte: Optional[float]
    empathie: Optional[float]
    assertivite: Optional[float]
    authenticite: Optional[float]
    creativite: Optional[float]

    agents_used: List[str]
    created_at: datetime

    class Config:
        orm_mode = True


# 📩 Input utilisateur
class AskRequest(BaseModel):
    question: str

# 📤 Réponse finale
class AskResponse(BaseModel):
    final_answer: str
    scores: Dict[str, float]
    agents_used: List[str]


# 📤 Pour afficher les scores cumulés d’un utilisateur
class UserScoreOut(BaseModel):
    user_id: int
    confiance: float
    clarte: float
    empathie: float
    assertivite: float
    authenticite: float
    creativite: float
    interactions_count: int

    class Config:
        orm_mode = True


class MessageCreate(BaseModel):
    interaction_id : int
    sender: str  # "user" ou "ai"
    content: str

class MessageRead(BaseModel):
    id: int
    interaction_id: int
    sender: str
    content: str
    timestamp: datetime
    role: Optional[str]  # ← ici si tu veux exposer le rôle aussi

    class Config:
        orm_mode = True