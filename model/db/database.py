# 📄 database.py — Init SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.config import DATABASE_URL

# 🧱 Base des modèles
Base = declarative_base()

# 🔌 Connexion PostgreSQL
engine = create_engine(DATABASE_URL)

# 🎛️ Session locale
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ⚠️ Ne pas oublier d'importer tous les modèles pour Alembic
# ✅ Pour forcer l'import des modèles SANS boucle
from model.db import models  # 👈 suffit largement

# 🐞 DEBUG
if __name__ == "__main__":
    print("[DEBUG] Base et engine initialisés")
    print("DATABASE_URL =", DATABASE_URL)
