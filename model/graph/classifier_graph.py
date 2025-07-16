# 📄 classifier_graph.py
# Graphe LangGraph piloté par le classifier_agent

from typing import TypedDict
from langgraph.graph import StateGraph

from model.agents.agent_classifier import classifier_agent_node
from model.agents.agent_message import agent_message_node
from model.agents.agent_redflag import agent_redflag_node
from model.agents.agent_irl import agent_irl_node
from model.agents.agent_confiance import agent_confiance_node
from model.agents.agent_style import agent_style_node
from model.agents.score_agent import score_agent_node

from model.db.utils import save_interaction_to_db, save_message_to_db  # ✅ on utilise la version SQLAlchemy


# 🧠 État partagé entre les étapes du graphe
class ClassifierState(TypedDict):
    user_id: int
    question: str
    response: str
    final_answer: str
    scores: dict
    agents_used: list[str]
    interaction_id: int | None  # 👈 sera défini après scoring


# 🧠 Agents disponibles dans le graphe
AVAILABLE_AGENTS = {
    "agent_message": agent_message_node,
    "agent_redflag": agent_redflag_node,
    "agent_irl": agent_irl_node,
    "agent_confiance": agent_confiance_node,
    "agent_style": agent_style_node
}


# 🔁 Étape 1 : Classifier → sélection des agents et réponses
def classifier_node(state: ClassifierState) -> ClassifierState:
    question = state["question"]
    user_id = state["user_id"]

    print("[DEBUG] Question envoyée au classifier :", question)
    selected_agents = classifier_agent_node(question)
    print("[✅] Agents identifiés :", selected_agents)

    responses = []

    for agent_name in selected_agents:
        agent_func = AVAILABLE_AGENTS.get(agent_name)
        if agent_func:
            print(f"[⚙️] Appel de l'agent {agent_name}")
            response = agent_func(question)
            responses.append(f"[{agent_name}] {response}")

            # 💾 Sauvegarde de la réponse agent dans la base (pas encore d'interaction_id)
            try:
                save_message_to_db(
                    interaction_id=None,
                    sender=agent_name,
                    content=response,
                    user_id=user_id,
                    role="assistant"
                )
            except Exception as e:
                print(f"[❌] Erreur save_message_to_db pour {agent_name} :", e)
        else:
            print(f"[⚠️] Agent {agent_name} non trouvé.")

    return {
        "user_id": user_id,
        "question": question,
        "response": "\n\n".join(responses),
        "final_answer": "",
        "scores": {},
        "agents_used": selected_agents,
        "interaction_id": None
    }


# 🧠 Étape 2 : Fusionner toutes les réponses
def final_answer_node(state: ClassifierState) -> ClassifierState:
    print("[🧠] Fusion des réponses")
    state["final_answer"] = state["response"]
    return state


# ⚖️ Étape 3 : Scoring + Sauvegarde de l’interaction + message final
def scoring_node(state: ClassifierState) -> ClassifierState:
    question = state["question"]
    answer = state["final_answer"]
    user_id = state["user_id"]
    agents_used = state.get("agents_used", [])

    print("[⚖️] Lancement scoring")
    scores = score_agent_node(question, answer)
    print("[DEBUG] Scores générés :", scores)
    state["scores"] = scores

    # 💾 Sauvegarde de l’interaction complète
    try:
        interaction_id = save_interaction_to_db(
            user_id=user_id,
            question=question,
            final_answer=answer,
            scores=scores,
            agents_used=agents_used
        )
        state["interaction_id"] = interaction_id
        print("[✅] Interaction sauvegardée avec ID :", interaction_id)

        # 💬 Sauvegarde du message final (réponse fusionnée)
        save_message_to_db(
            interaction_id=interaction_id,
            sender="fusion",
            content=answer,
            user_id=user_id,
            role="assistant"
        )

    except Exception as e:
        print("[❌] Erreur sauvegarde interaction/message final :", e)

    return state


# 🛠️ Compilation du graphe LangGraph
graph_builder = StateGraph(ClassifierState)

graph_builder.add_node("classifier_router", classifier_node)
graph_builder.add_node("final_answer", final_answer_node)
graph_builder.add_node("score_agent", scoring_node)

graph_builder.set_entry_point("classifier_router")
graph_builder.add_edge("classifier_router", "final_answer")
graph_builder.add_edge("final_answer", "score_agent")
graph_builder.set_finish_point("score_agent")

graph = graph_builder.compile()
