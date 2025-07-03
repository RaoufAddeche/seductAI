# 📄 agent_message.py
# Agent LangGraph : récupère les sources + génère une réponse via LLM Mistral (Ollama)

from model.retrievers.message_retriever import get_message_retriever
from langchain.prompts import PromptTemplate
from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="mistral")


# 📥 Chargement du prompt
with open("model/prompts/message_prompt.txt", "r") as f:
    template = f.read()

prompt = PromptTemplate(
    template=template,
    input_variables=["context", "question"]
)

# 🔁 RAG pipeline
def agent_message_node(question: str) -> str:
    print("[DEBUG] Requête posée à l'agent_message :", question)

    retriever = get_message_retriever()
    docs = retriever.invoke(question)
    print(f"[DEBUG] {len(docs)} documents trouvés")

    context = "\n---\n".join([doc.page_content for doc in docs])
    full_prompt = prompt.format(context=context, question=question)

    response = llm.invoke(full_prompt)
    print("[✅] Réponse générée :")
    print(response)

    return response
