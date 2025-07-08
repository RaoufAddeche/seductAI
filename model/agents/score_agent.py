# 📄 score_agent.py
# Évalue une interaction sur 4 axes : confiance, clarté, empathie, assertivité

from langchain.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
import json

# 🔮 LLM de scoring
llm = OllamaLLM(model="mistral")

# 📄 Chargement du prompt
with open("model/prompts/score_prompt.txt", "r") as f:
    template = f.read()

prompt = PromptTemplate(
    template=template,
    input_variables=["question", "answer"]
)

def score_agent_node(question: str, answer: str) -> dict:
    print("[DEBUG] score_agent → Évaluation en cours")
    full_prompt = prompt.format(question=question, answer=answer)

    response = llm.invoke(full_prompt)
    print("[DEBUG] Réponse brute du LLM (scoring) :\n", response)

    try:
        scores = json.loads(response)
        assert all(k in scores for k in ["confiance", "clarte", "empathie", "assertivite"])
    except Exception as e:
        print("[❌] Erreur parsing JSON :", e)
        return {
            "confiance": 0.0,
            "clarte": 0.0,
            "empathie": 0.0,
            "assertivite": 0.0
        }

    print("[✅] Scores évalués :", scores)
    return scores
