# 📄 agent_style.py
# Donne des conseils sur le look, la vibe, le style personnel ou Insta

from model.retrievers.message_retriever import get_message_retriever  # 🧠 retriever partagé pour l’instant
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from model.agents.llm_loader import get_llm


llm = get_llm()

# 📝 Chargement du prompt style
with open("model/prompts/style_prompt.txt", "r") as f:
    template = f.read()

prompt = PromptTemplate(
    template=template,
    input_variables=["context", "question"]
)

def agent_style_node(question: str) -> str:
    print("[DEBUG] agent_style → question :", question)

    retriever = get_message_retriever()
    docs = retriever.invoke(question)
    print(f"[DEBUG] {len(docs)} documents trouvés")

    context = "\n---\n".join([doc.page_content for doc in docs])
    full_prompt = prompt.format(context=context, question=question)

    response = llm.invoke(full_prompt)
    print("[✅] Réponse style générée :\n", response.content)

    return response.content
