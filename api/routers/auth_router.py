from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from api.models import schemas
from model.db.models import User, UserScore
from api.auth.auth import (
    hash_password,
    verify_password,
    create_access_token
)
from api.auth.dependencies import get_db, get_current_user

router = APIRouter()

# 🔐 ✅ Enregistrement d'un nouvel utilisateur
@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email déjà utilisé")
    
    hashed_pw = hash_password(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pw
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    # ✅ Création du score initial pour ce user
    new_score = UserScore(
        user_id=new_user.id,
        confiance=0.0,
        clarte=0.0,
        empathie=0.0,
        assertivite=0.0,
        authenticite=0.0,
        creativite=0.0,
        interactions_count=0
    )
    db.add(new_score)
    db.commit()

    return new_user


# 🔐 ✅ Connexion (retourne un token JWT)
@router.post("/login", response_model=schemas.Token)
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.email == username).first()
    
    if not db_user or not verify_password(password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
    
    token = create_access_token(data={"sub": str(db_user.id)})
    return {"access_token": token, "token_type": "bearer"}


# 👤 ✅ Récupérer les infos de l'utilisateur connecté
@router.get("/me", response_model=schemas.UserOut)
def get_me(user: User = Depends(get_current_user)):
    print(f"[DEBUG] Utilisateur connecté : {user.username}")
    return user


# 🛠 ✅ Modifier son profil (age, genre, style, etc.)
@router.put("/update-profile", response_model=schemas.UserOut)
def update_profile(
    update_data: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user = db.query(User).filter(User.id == current_user.id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    # Mise à jour uniquement des champs envoyés
    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    print(f"[DEBUG] Profil mis à jour : {update_data.dict(exclude_unset=True)}")
    return user
