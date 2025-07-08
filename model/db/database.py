# 📄 database.py
# Sert à initialiser la connexion SQLAlchemy à la base PostgreSQL

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.config import DATABASE_URL

# 🧱 Base pour les modèles (User, Interaction...)
Base = declarative_base()

# 🔌 Connexion à PostgreSQL via DATABASE_URL (depuis le .env)
engine = create_engine(DATABASE_URL)

# 🌀 Créateur de session pour les opérations DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ⚠️ Import forcé pour que Alembic détecte les modèles (effet de bord)
from model.db import models

# 🐞 DEBUG (optionnel)
if __name__ == "__main__":
    print("[DEBUG] Base et engine initialisés")
    print("DATABASE_URL =", DATABASE_URL)
