# 📄 confiance_retriever.py
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

def get_confiance_retriever():
    embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(
        persist_directory="data/vectorstore/agent_message",  # 🧠 temporairement partagé
        embedding_function=embedding
    )
    return db.as_retriever(search_kwargs={"k": 3})
