# 📄 agent_message.py
# Agent LangGraph : récupère les sources + génère une réponse via LLM Mistral (Ollama)

from model.retrievers.message_retriever import get_message_retriever
from langchain.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
from model.agents.llm_loader import get_llm


llm = get_llm()

# 📥 Chargement du prompt
with open("model/prompts/message_prompt.txt", "r") as f:
    template = f.read()

prompt = PromptTemplate(
    template=template,
    input_variables=["context", "question"]
)

# 🔁 RAG pipeline
def agent_message_node(messages) -> str:
    """
    Génère une réponse en tenant compte :
    - du thread complet (mémoire conversationnelle)
    - des documents RAG les plus pertinents
    """
    print("[DEBUG] agent_message_node reçoit le contexte complet :", messages)

    # 1️⃣ Thread formaté (mémoire conversation)
    thread_formatted = ""
    for m in messages:
        role = m.get("role") or m.get("sender") or "user"
        who = "Utilisateur" if role == "user" else "IA"
        thread_formatted += f"{who} : {m['content']}\n"

    # 2️⃣ On extrait la dernière question utilisateur pour le RAG
    last_user_message = next((m["content"] for m in reversed(messages) if (m.get("role") or m.get("sender")) == "user"), "")

    # 3️⃣ RAG — recherche de documents pertinents sur la dernière question
    retriever = get_message_retriever()
    docs = retriever.invoke(last_user_message)
    print(f"[DEBUG] {len(docs)} documents RAG trouvés")

    # Formatage des extraits docs
    context_rag = "\n---\n".join([doc.page_content for doc in docs])

    # 4️⃣ Construction du prompt final
    # -> On concatène les deux contextes dans 'context' pour le template
    full_context = (
        "Conversation précédente :\n"
        f"{thread_formatted}\n"
        "Sources pertinentes :\n"
        f"{context_rag}\n"
        "\nRéponds au dernier message utilisateur en tenant compte de la conversation et des sources ci-dessus."
    )
    question = ""  # Plus utile ici, mais conservé pour compatibilité template

    full_prompt = prompt.format(context=full_context, question=question)

    response = llm.invoke(full_prompt)
    print("[✅] Réponse contextuelle générée :")
    print(response.content)

    return response.content

