# 📄 agent_irl.py
# Conseille l'utilisateur pour les interactions en face-à-face ou appels

from model.retrievers.message_retriever import get_message_retriever  # 🧠 retriever partagé pour l’instant
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate

# LLM via Ollama
llm = OllamaLLM(model="mistral")

# 📥 Chargement du prompt
with open("model/prompts/irl_prompt.txt", "r") as f:
    template = f.read()

prompt = PromptTemplate(
    template=template,
    input_variables=["context", "question"]
)

def agent_irl_node(question: str) -> str:
    print("[DEBUG] agent_irl → question :", question)

    retriever = get_message_retriever()
    docs = retriever.invoke(question)
    print(f"[DEBUG] {len(docs)} documents trouvés")

    context = "\n---\n".join([doc.page_content for doc in docs])
    full_prompt = prompt.format(context=context, question=question)

    response = llm.invoke(full_prompt)
    print("[✅] Réponse IRL générée :\n", response)

    return response
