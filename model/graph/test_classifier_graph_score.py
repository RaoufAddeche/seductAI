# 📄 test_classifier_graph_score.py
# Lance un test complet du graphe : classification → réponse → scoring

from model.graph.classifier_graph import graph

print("=== Test Classifier Graph avec Scoring ===")
question = input("💬 Entre ta question :\n> ")

inputs = {"question": question}

print("\n🚀 Lancement du graphe...")
final_state = graph.invoke(inputs)

# 🔎 Affichage des résultats
print("\n🧠 Réponse générée :")
print(final_state["final_answer"])

print("\n📊 Scores (0.0 à 1.0) :")
for k, v in final_state["scores"].items():
    print(f"  🔹 {k.capitalize():12} : {v:.2f}")
