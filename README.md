# 🧠 SeductAI — Coach IA en communication & séduction

SeductAI est un projet d'IA modulaire basé sur un graphe LangGraph, capable de coacher l'utilisateur dans différents contextes relationnels : messages, interactions IRL, confiance en soi, signaux d’alerte.

Le projet repose sur une architecture RAG (Retrieval-Augmented Generation) avec des agents IA spécialisés, chacun appuyé par une base de connaissances vectorisée issue de livres confidentiels.

---

## ⚙️ Stack technique

| Composant          | Tech utilisée               |
|--------------------|-----------------------------|
| LLM local          | Mistral (via Ollama)        |
| Base vectorielle   | Chroma                      |
| Embeddings         | HuggingFace MiniLM          |
| Backend            | FastAPI (non activé ici)    |
| Graphe IA          | LangGraph (LangChain)       |
| Monitoring         | LangChain (logs désactivés) |
| Sécurité des données | PDF renommés + gitignore   |

---

## 📦 Fonctionnalités actuelles

### ✅ Agents implémentés

- `agent_message` : aide à formuler ou analyser des messages, DMs, relances...
- `agent_confiance` : aide à se recentrer, gagner en assurance, clarifier ses intentions
- `classifier_agent` : analyse la question de l'utilisateur et route vers un ou plusieurs agents selon le contexte

### 🚀 Graphe LangGraph dynamique

- Routing basé sur un prompt intelligent
- Capable d'enchaîner plusieurs agents si besoin
- Réponses combinées automatiquement

---

## 🔐 Sécurité & confidentialité

- Aucun nom de livre n’est exposé
- Fichiers PDF renommés (`source_a1.pdf`, etc)
- `.txt` et vectorstore ignorés dans `.gitignore`
- Pas de push de données privées ou sous droits

---

## ✅ Setup rapide

```bash
git clone https://github.com/ton-repo/seductai.git
cd seductai
pip install -r requirements.txt
ollama run mistral  # Vérifie que le modèle est prêt

# Vectorisation (exemple)
python rag/vectorize_agent.py --agent agent_message --files data/pdf/source_a1.pdf

# Test simple
python model/graph/test_classifier_graph.py
