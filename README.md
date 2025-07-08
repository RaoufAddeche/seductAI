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

## 🚀 Fonctionnalités principales

### ✅ Graphe IA multi-agent (LangGraph)
- Détection automatique du contexte avec `classifier_agent`
- Appel dynamique des agents spécialisés :
  - `agent_message` : rédaction / reformulation de messages
  - `agent_irl` : conseils face-à-face, dates, appels
  - `agent_confiance` : posture mentale, confiance, clarté intérieure
  - `agent_style` : style personnel, présentation, look
  - `agent_redflag` : détection signaux faibles / ambigus

### 🧠 Scoring IA sur 4 axes
À chaque interaction, l'IA attribue un score sur :
- **Confiance**
- **Clarté**
- **Empathie**
- **Assertivité**

### 💾 Sauvegarde des interactions
Toutes les interactions scorées sont enregistrées en base PostgreSQL :
```sql
interactions(question, final_answer, confiance, clarte, empathie, assertivite, created_at)

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
