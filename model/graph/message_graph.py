from typing import TypedDict
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from model.agents.agent_message import agent_message_node

# ✅ Définition explicite du schema de state
class MessageState(TypedDict):
    question: str
    response: str

# 🔁 Wrapper de ton agent
def agent_tool_node(state: MessageState) -> MessageState:
    question = state["question"]
    response = agent_message_node(question)
    return {"question": question, "response": response}

# 🔧 Création du graphe
graph_builder = StateGraph(MessageState)  # ✅ au lieu de dict
graph_builder.add_node("agent_message", agent_tool_node)
graph_builder.set_entry_point("agent_message")
graph_builder.set_finish_point("agent_message")

graph = graph_builder.compile()
