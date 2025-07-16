# 📄 agent_redflag.py
# Vérifie les signaux d'alerte et aide à poser des limites relationnelles

from model.retrievers.message_retriever import get_message_retriever  # 🧠 temporaire
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from model.agents.llm_loader import get_llm


llm = get_llm()

# 📥 Chargement du prompt
with open("model/prompts/redflag_prompt.txt", "r") as f:
    template = f.read()

prompt = PromptTemplate(
    template=template,
    input_variables=["context", "question"]
)

def agent_redflag_node(question: str) -> str:
    print("[DEBUG] agent_redflag → question :", question)

    # 🔁 Utilisation temporaire du retriever agent_message
    retriever = get_message_retriever()
    docs = retriever.invoke(question)
    print(f"[DEBUG] {len(docs)} documents trouvés")

    context = "\n---\n".join([doc.page_content for doc in docs])
    full_prompt = prompt.format(context=context, question=question)

    response = llm.invoke(full_prompt)
    print("[✅] Réponse redflag générée :\n", response.content)

    return response.content
