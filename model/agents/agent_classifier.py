# 📄 agent_classifier.py
# Ce module détermine dynamiquement quels agents doivent être appelés via un prompt RAG

from langchain_ollama import OllamaLLM
import json

# 🧠 LLM local via Ollama (Mistral)
llm = OllamaLLM(model="mistral")

# 📥 Chargement du prompt depuis le fichier
with open("model/prompts/classifier_prompt.txt", "r") as f:
    template = f.read()

def classifier_agent_node(question: str) -> list[str]:
    print("[DEBUG] Question envoyée au classifier :", question)

    prompt = template.format(question=question)
    response = llm.invoke(prompt)

    print("[DEBUG] Réponse brute du classifier :", response)

    try:
        # ✅ Convertir la réponse en liste Python
        agents = json.loads(response)
        print("[✅] Agents identifiés :", agents)
        return agents
    except json.JSONDecodeError:
        print("[⚠️] Erreur : réponse non JSON")
        return []
