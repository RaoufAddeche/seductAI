# 📄 test_classifier.py
# Teste le classifier_agent_node() et affiche les agents détectés

from agent_classifier import classifier_agent_node

if __name__ == "__main__":
    print("=== Test du classifier_agent ===")
    question = input("❓ Pose une question à l'IA :\n> ")

    agents = classifier_agent_node(question)

    print("\n📦 Agents suggérés par le classifier :")
    for a in agents:
        print("🔹", a)
