# 📄 message_retriever.py
# Récupère les chunks vectorisés de l'agent_message via Chroma + embeddings HuggingFace

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


def get_message_retriever():
    embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(
        persist_directory="data/vectorstore/agent_message",
        embedding_function=embedding
    )
    return db.as_retriever(search_kwargs={"k": 3})
