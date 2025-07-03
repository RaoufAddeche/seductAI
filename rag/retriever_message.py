# 📄 retriever_message.py
# Teste le corpus vectorisé de agent_message avec une requête RAG

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


VECTOR_DIR = "data/vectorstore/agent_message"
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = Chroma(persist_directory=VECTOR_DIR, embedding_function=embedding)

query = "Que dire après un match Tinder ?"
results = db.similarity_search(query, k=3)

print("\n[🔍] Résultats RAG :\n")
for i, doc in enumerate(results, 1):
    print(f"🔹 Résultat {i}: {doc.page_content[:200]}...")
    print(f"   🔍 source: {doc.metadata.get('source')}")
