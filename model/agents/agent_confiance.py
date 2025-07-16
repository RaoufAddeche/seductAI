# 📄 agent_confiance.py
# Donne des conseils de posture mentale, clarté, confiance

from model.retrievers.confiance_retriever import get_confiance_retriever
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from model.agents.llm_loader import get_llm


llm = get_llm()

# Prompt
with open("model/prompts/confiance_prompt.txt", "r") as f:
    template = f.read()

prompt = PromptTemplate(
    template=template,
    input_variables=["context", "question"]
)

def agent_confiance_node(question: str) -> str:
    print("[DEBUG] agent_confiance → question :", question)

    retriever = get_confiance_retriever()
    docs = retriever.invoke(question)
    print(f"[DEBUG] {len(docs)} documents trouvés")

    context = "\n---\n".join([doc.page_content for doc in docs])
    full_prompt = prompt.format(context=context, question=question)

    response = llm.invoke(full_prompt)
    print("[✅] Réponse confiance générée :\n", response.content)

    return response.content
