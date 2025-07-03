# 📄 vectorize_agent.py
# Ce script vectorise un ou plusieurs PDF pour un agent IA
# Les sources sont anonymisées pour rester confidentielles

import argparse
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import os

parser = argparse.ArgumentParser(description="Vectorisation pour un agent IA.")
parser.add_argument("--agent", required=True, help="Nom de l'agent (ex: agent_message)")
parser.add_argument("--files", nargs="+", required=True, help="PDF à vectoriser (chemins)")
args = parser.parse_args()

# 📦 Configuration
VECTOR_DIR = f"data/vectorstore/{args.agent}"
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)
all_chunks = []

for i, path in enumerate(args.files):
    if not os.path.exists(path):
        print(f"[❌] Fichier introuvable : {path}")
        continue

    print(f"[📥] Chargement : {path}")
    loader = PyPDFLoader(path)
    docs = loader.load()

    # 🔒 Anonymisation des métadonnées
    for doc in docs:
        doc.metadata["source"] = f"{args.agent}_doc_{i}"
        doc.metadata["agent"] = args.agent

    chunks = splitter.split_documents(docs)
    print(f"[✅] {len(chunks)} chunks extraits de {os.path.basename(path)}")
    all_chunks.extend(chunks)

# 🧠 Vectorisation
print(f"[🧠] Vectorisation totale : {len(all_chunks)} chunks pour {args.agent}")
db = Chroma.from_documents(documents=all_chunks, embedding=embedding, persist_directory=VECTOR_DIR)
db.persist()

print(f"[✅] Vectorisation terminée → stockée dans : {VECTOR_DIR}")
