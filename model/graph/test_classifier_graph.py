# 📄 test_classifier_graph.py
# Lance une requête utilisateur et affiche les réponses générées via le classifier LangGraph

from classifier_graph import graph

if __name__ == "__main__":
    print("=== SeductAI — Graphe IA Multi-Agent ===")
    question = input("💬 Pose ta question à l'IA :\n> ")

    result = graph.invoke({"question": question})

    print("\n🧠 Réponse(s) combinée(s) :\n")
    print(result["response"])
