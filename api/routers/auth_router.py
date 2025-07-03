# endpoints /register + /login

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.models import user as models
from api.models import schemas
from api.auth.auth import hash_password, verify_password, create_access_token
from api.auth.dependencies import get_db

router = APIRouter()

@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email déjà utilisé")
    hashed_pw = hash_password(user.password)
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pw
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=schemas.Token)
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
    token = create_access_token(data={"sub": str(db_user.id)})
    return {"access_token": token, "token_type": "bearer"}




from api.auth.dependencies import get_current_user
from fastapi import Depends

# 📌 Route protégée : récupère les infos de l’utilisateur connecté
@router.get("/me")
def get_me(user = Depends(get_current_user)):
    print(f"[DEBUG] Utilisateur connecté : {user.username}")
    return {
        "username": user.username,
        "email": user.email,
        "role": user.role
    }

