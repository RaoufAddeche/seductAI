# 📄 classifier_graph.py
# Graphe LangGraph piloté par le classifier_agent
# Appelle dynamiquement les agents pertinents, fusionne les réponses,
# évalue la réponse finale via scoring, et enregistre l’interaction en base

from typing import TypedDict
from langgraph.graph import StateGraph
from model.agents.agent_classifier import classifier_agent_node
from model.agents.agent_message import agent_message_node
from model.agents.agent_redflag import agent_redflag_node
from model.agents.agent_irl import agent_irl_node
from model.agents.agent_confiance import agent_confiance_node
from model.agents.agent_style import agent_style_node
from model.agents.score_agent import score_agent_node
from model.db.utils import save_interaction_to_db  # 💾 Fonction dédiée

# 🧠 State partagé entre les étapes du graphe
class ClassifierState(TypedDict):
    question: str
    response: str
    final_answer: str
    scores: dict

# 🔁 Liste des agents disponibles
AVAILABLE_AGENTS = {
    "agent_message": agent_message_node,
    "agent_redflag": agent_redflag_node,
    "agent_irl": agent_irl_node,
    "agent_confiance": agent_confiance_node,
    "agent_style": agent_style_node
}

# 🔀 Node de classification/routage
def classifier_node(state: ClassifierState) -> ClassifierState:
    question = state["question"]
    print("[DEBUG] Question envoyée au classifier :", question)

    selected_agents = classifier_agent_node(question)
    print("[DEBUG] Réponse brute du classifier :", selected_agents)
    print("[✅] Agents identifiés :", selected_agents)

    responses = []

    for agent_name in selected_agents:
        agent_func = AVAILABLE_AGENTS.get(agent_name)
        if agent_func:
            print(f"[⚙️] Appel de l'agent {agent_name}")
            response = agent_func(question)
            responses.append(f"[{agent_name}] {response}")
        else:
            print(f"[⚠️] Agent {agent_name} non implémenté.")

    return {
        "question": question,
        "response": "\n\n".join(responses),
        "final_answer": "",
        "scores": {}
    }

# 🧠 Fusion des réponses
def final_answer_node(state: ClassifierState) -> ClassifierState:
    print("[🧠] Fusion des réponses")
    state["final_answer"] = state["response"]
    return state

# ⚖️ Scoring + enregistrement
def scoring_node(state: ClassifierState) -> ClassifierState:
    question = state.get("question")
    answer = state.get("final_answer")

    print("[⚖️] Lancement scoring")
    scores = score_agent_node(question, answer)
    print("[DEBUG] Scores générés :", scores)

    state["scores"] = scores

    # 💾 Enregistrement BDD
    try:
        save_interaction_to_db(question, answer, scores)
    except Exception as e:
        print("[❌] Erreur lors de la sauvegarde :", e)

    return state

# 🛠️ Construction du graphe
graph_builder = StateGraph(ClassifierState)

graph_builder.add_node("classifier_router", classifier_node)
graph_builder.add_node("final_answer", final_answer_node)
graph_builder.add_node("score_agent", scoring_node)

graph_builder.set_entry_point("classifier_router")
graph_builder.add_edge("classifier_router", "final_answer")
graph_builder.add_edge("final_answer", "score_agent")
graph_builder.set_finish_point("score_agent")

graph = graph_builder.compile()
