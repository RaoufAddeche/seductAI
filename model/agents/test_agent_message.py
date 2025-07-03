# 📄 test_agent_message.py
# Test simple du comportement de l'agent_message seul

from agent_message import agent_message_node


if __name__ == "__main__":
    print("=== TEST SeductAI: agent_message ===")
    question = input("🔹 Pose ta question à l'agent_message :\n> ")
    
    print("\n[🧠] Réponse de l'IA :\n")
    response = agent_message_node(question)
    print("\n🔚 Fin du test.")
