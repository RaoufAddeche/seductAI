# 📄 test_score_agent.py
# Test console pour scorer une réponse manuellement

from model.agents.score_agent import score_agent_node

print("=== Test Scoring — SeductAI ===")
print("💬 Entre une question utilisateur :")
question = input("> ")

print("\n🧠 Copie-colle la réponse générée par l'IA :")
answer = input("> ")

scores = score_agent_node(question, answer)

print("\n🎯 Résultat du scoring :")
print(f"  🔹 Confiance     : {scores['confiance']:.2f}")
print(f"  🔹 Clarté        : {scores['clarte']:.2f}")
print(f"  🔹 Empathie      : {scores['empathie']:.2f}")
print(f"  🔹 Assertivité   : {scores['assertivite']:.2f}")
