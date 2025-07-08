from dotenv import load_dotenv
import os

# 🐞 DEBUG : on charge les variables d’environnement
load_dotenv()
print("[DEBUG] .env loaded")

# 🔐 Variables essentielles pour tout le projet
DATABASE_URL = os.getenv("DATABASE_URL")
CHROMA_DIR = os.getenv("CHROMA_DIR")
OLLAMA_HOST = os.getenv("OLLAMA_HOST")
SECRET_KEY = os.getenv("SECRET_KEY")

# 🐞 Affichage debug de la connexion BDD
print("[DEBUG] DATABASE_URL:", DATABASE_URL)

# ✅ Vérification critique de la config BDD
assert DATABASE_URL.startswith("postgresql://"), "[ERROR] DATABASE_URL mal formée"
