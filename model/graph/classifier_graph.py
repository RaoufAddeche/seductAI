# 📄 classifier_graph.py
# Graphe LangGraph piloté par le classifier_agent qui appelle dynamiquement les bons agents

from typing import TypedDict
from langgraph.graph import StateGraph, END
from model.agents.agent_classifier import classifier_agent_node
from model.agents.agent_message import agent_message_node

# 🧠 Définir le type de state partagé entre les nodes
class ClassifierState(TypedDict):
    question: str
    response: str

# 🧩 Map d'agents disponibles dans ton système
AVAILABLE_AGENTS = {
    "agent_message": agent_message_node,
    # "agent_redflag": agent_redflag_node,
    # "agent_irl": agent_irl_node,
    # "agent_confiance": agent_confiance_node
}

# 🔁 Node de classification
def classifier_node(state: ClassifierState) -> ClassifierState:
    question = state["question"]
    selected = classifier_agent_node(question)

    responses = []

    for agent_name in selected:
        agent_func = AVAILABLE_AGENTS.get(agent_name)
        if agent_func:
            print(f"[⚙️] Appel de l'agent {agent_name}")
            response = agent_func(question)
            responses.append(f"[{agent_name}] {response}")
        else:
            print(f"[⚠️] Agent {agent_name} non implémenté. Ignoré.")

    return {
        "question": question,
        "response": "\n\n".join(responses)
    }

# 🛠️ Construction du graphe
graph_builder = StateGraph(ClassifierState)
graph_builder.add_node("classifier_router", classifier_node)
graph_builder.set_entry_point("classifier_router")
graph_builder.set_finish_point("classifier_router")

graph = graph_builder.compile()
