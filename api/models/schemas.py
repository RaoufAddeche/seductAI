# 📦 schemas.py — Pydantic models (entrées/sorties API, version enrichie & robuste)

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, List, Literal
from datetime import datetime

# === Utilisateur ===

class UserCreate(BaseModel):
    username: str = Field(..., description="Nom d'utilisateur unique")
    email: EmailStr = Field(..., description="Adresse email de l'utilisateur")
    password: str = Field(..., description="Mot de passe (hashé côté backend)")

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

class UserUpdate(BaseModel):
    username: Optional[str]
    age: Optional[int]
    gender: Optional[str]
    orientation: Optional[str]
    style_langage: Optional[str]
    centre_interets: Optional[List[str]] = Field(default_factory=list)
    situation: Optional[str]

# === Auth ===

class Token(BaseModel):
    access_token: str
    token_type: str

# === Thread & messages ===

class MessageItem(BaseModel):
    role: Optional[Literal["user", "assistant", "agent", "fusion"]] = Field(None, description="Type d'émetteur")
    sender: Optional[str] = Field(None, description="Nom de l'agent IA ou 'user'")
    content: str = Field(..., description="Texte du message")

class InteractionCreate(BaseModel):
    question: str = Field("", description="Question de départ (optionnel)")
    final_answer: str = Field("", description="Réponse IA finale (optionnel)")
    messages: List[MessageItem] = Field(default_factory=list, description="Fil de discussion")
    confiance: Optional[float] = None
    clarte: Optional[float] = None
    empathie: Optional[float] = None
    assertivite: Optional[float] = None
    authenticite: Optional[float] = None
    creativite: Optional[float] = None

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
    agents_used: List[str]  # Si tu veux : List[Literal["agent_message", ...]]
    created_at: datetime

    class Config:
        orm_mode = True

# === Requête/réponse IA ===

class AskRequest(BaseModel):
    question: str = Field(..., description="Message envoyé à l'IA (prompt utilisateur)")

class AskResponse(BaseModel):
    final_answer: str = Field(..., description="Réponse générée par l'IA")
    scores: Dict[str, float] = Field(..., description="Dictionnaire des scores par axe relationnel")
    agents_used: List[str] = Field(..., description="Liste des agents IA sollicités")

# === Progression / scoring ===

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

# === CRUD message individuel ===

class MessageCreate(BaseModel):
    interaction_id: int = Field(..., description="ID du thread cible")
    sender: str = Field(..., description="'user' ou nom d'agent IA")
    content: str

class MessageRead(BaseModel):
    id: int
    interaction_id: int
    sender: str
    content: str
    timestamp: datetime
    role: Optional[str]  # Peut-être "user", "assistant", etc.

    class Config:
        orm_mode = True
