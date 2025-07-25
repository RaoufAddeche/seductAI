# 📄 classifier_graph.py — Graphe LangGraph orchestré via classifier_agent

from typing import TypedDict
from datetime import datetime
from langgraph.graph import StateGraph #StateMessage?

# Agents IA
from model.agents.agent_classifier import classifier_agent_node
from model.agents.agent_message import agent_message_node
from model.agents.agent_redflag import agent_redflag_node
from model.agents.agent_irl import agent_irl_node
from model.agents.agent_confiance import agent_confiance_node
from model.agents.agent_style import agent_style_node
from model.agents.score_agent import score_agent_node

# Utils DB
from model.db.utils import (
    save_interaction_to_db,
    save_message_to_db,
    get_or_create_open_interaction
)

# 🧠 État partagé entre les étapes
class ClassifierState(TypedDict):
    user_id: int
    messages: list[dict]      # Toute la discussion !
    response: str
    final_answer: str
    scores: dict
    agents_used: list[str]
    interaction_id: int

# 🧠 Agents disponibles
AVAILABLE_AGENTS = {
    "agent_message": agent_message_node,
    "agent_redflag": agent_redflag_node,
    "agent_irl": agent_irl_node,
    "agent_confiance": agent_confiance_node,
    "agent_style": agent_style_node
}

# 🚪 Entrée du graphe — création ou récupération d’interaction
def classifier_node(state: ClassifierState) -> ClassifierState:
    messages = state["messages"]
    user_id = state["user_id"]

    print("[DEBUG] Historique complet transmis :", messages)

    # 👉 Dernier message utilisateur
    last_user_message = next(
        (m["content"] for m in reversed(messages) if m.get("role", "user") == "user"), None
    )
    if not last_user_message:
        raise RuntimeError("❌ Aucun message utilisateur trouvé pour classifieur.")

    # 🧠 Appel du classifieur (détecte les agents à activer)
    selected_agents = classifier_agent_node(last_user_message)
    print("[✅] Agents identifiés :", selected_agents)

    # 📦 Récupération ou création de l’interaction (ouverte depuis < 20 min)
    interaction = get_or_create_open_interaction(user_id)
    if not interaction:
        raise RuntimeError("❌ Impossible de créer ou récupérer une interaction valide.")
    interaction_id = interaction.id
    print(f"[✅] Interaction active : {interaction_id}")

    # 🤖 Appel des agents sélectionnés (PAS de sauvegarde des réponses agents dans le thread user)
    responses = []
    for agent_name in selected_agents:
        agent_func = AVAILABLE_AGENTS.get(agent_name)
        if agent_func:
            # Passe tout le thread (messages) à agent_message uniquement
            if agent_name == "agent_message":
                print(f"[DEBUG] Appel de {agent_name} avec contexte complet")
                response = agent_func(messages)
            else:
                print(f"[DEBUG] Appel de {agent_name} avec input : {last_user_message}")
                response = agent_func(last_user_message)
            responses.append(f"[{agent_name}] {response}")
        else:
            print(f"[⚠️] Agent {agent_name} non trouvé.")

    # On NE sauvegarde pas les réponses intermédiaires dans le chat ici
    # Uniquement la réponse finale/fusionnée plus loin

    return {
        "user_id": user_id,
        "messages": messages,
        "response": "\n\n".join(responses),
        "final_answer": "",
        "scores": {},
        "agents_used": selected_agents,
        "interaction_id": interaction_id
    }

def final_answer_node(state: ClassifierState) -> ClassifierState:
    print("[🧠] Fusion des réponses")
    state["final_answer"] = state["response"]
    return state

def scoring_node(state: ClassifierState) -> ClassifierState:
    messages = state["messages"]
    answer = state["final_answer"]
    user_id = state["user_id"]
    agents_used = state.get("agents_used", [])
    interaction_id = state["interaction_id"]

    # Dernier message utilisateur pour scoring
    last_user_message = next(
        (m["content"] for m in reversed(messages) if m.get("role", "user") == "user"), None
    )

    print("[⚖️] Lancement scoring")
    scores = score_agent_node(last_user_message, answer)
    print("[DEBUG] Scores générés :", scores)
    state["scores"] = scores

    # 💾 Mise à jour finale de l’interaction
    try:
        save_interaction_to_db(
            user_id=user_id,
            question=last_user_message,
            final_answer=answer,
            scores=scores,
            agents_used=agents_used,
            interaction_id=interaction_id
        )
        print("[✅] Interaction mise à jour avec ID :", interaction_id)

        # ✅ Seule la réponse FINALE/fusionnée est enregistrée dans le fil utilisateur
        save_message_to_db(
            interaction_id=interaction_id,
            sender="assistant",
            content=answer,
            user_id=user_id,
            role="assistant",
            timestamp=datetime.utcnow()
        )
    except Exception as e:
        print("[❌] Erreur sauvegarde interaction/message final :", e)

    return state

# 🧠 Compilation du graphe LangGraph
graph_builder = StateGraph(ClassifierState)

graph_builder.add_node("classifier_router", classifier_node)
graph_builder.add_node("final_answer", final_answer_node)
graph_builder.add_node("score_agent", scoring_node)

graph_builder.set_entry_point("classifier_router")
graph_builder.add_edge("classifier_router", "final_answer")
graph_builder.add_edge("final_answer", "score_agent")
graph_builder.set_finish_point("score_agent")

graph = graph_builder.compile()
