# 📄 main.py
# Point d’entrée principal de l’API FastAPI pour SeductAI

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 🐞 DEBUG : Chargement initial de FastAPI
print("[DEBUG] Initialisation FastAPI app")

app = FastAPI(
    title="SeductAI",
    description="Coach IA multi-agent en séduction",
    version="0.1.0"
)

# Middleware CORS pour permettre les requêtes front/backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔐 à restreindre en prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔗 Import des routers ici, après avoir défini `app`
from api.routers import auth_router

# 📌 Ajout des routes auth à l'application
app.include_router(auth_router.router)

# 🧪 Route test /ping
@app.get("/ping")
def ping():
    print("[DEBUG] /ping appelé")
    return {"message": "SeductAI backend is alive 🔥"}
