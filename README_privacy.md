# 🔐 Confidentialité & Sécurité — SeductAI

Ce projet contient des composants sensibles liés à l'intelligence artificielle, à la génération de langage naturel et à l'ingestion de documents propriétaires.

## 📁 Contenu exclu du versioning Git

Pour des raisons de confidentialité et de respect des droits d’auteur, les éléments suivants sont **exclus du dépôt Git** :

| Dossier / Fichier | Contenu | Raison d'exclusion |
|-------------------|---------|---------------------|
| `data/*.pdf` | Livres | ⚠️ Potentiellement soumis au droit d’auteur |
| `data/*.md` | Corpus textuels personnalisés | 🤫 Contenu stratégique de l’IA |
| `data/vectorstore/` | Index vectoriels générés par Chroma | 🔐 Données encodées confidentielles |
| `.env` | Clés de config, base de données, token secrets | 🔑 Sécurité |

---

## 🚫 Ce qui **ne doit jamais être pushé** :

- Données personnelles
- Corpus complet provenant d'ouvrages protégés
- Base vectorielle encodée (`Chroma`)
- Modèles entraînés spécifiques

---

## ✅ Bonnes pratiques recommandées

- Utiliser un fichier `.gitignore` strict pour tout fichier sensible
- Ajouter un `README_privacy.md` pour clarifier la politique de confidentialité du dépôt
- Versionner uniquement la structure, le code et les outils d’intégration

---

## 🔒 Objectif

Respecter les exigences du brief TechCorp :

- ✅ Protection des sources propriétaires
- ✅ Respect des droits de propriété intellectuelle
- ✅ Cloisonnement entre code et données confidentielles

---

> Ce dépôt est conçu pour être **clonable et réutilisable sans jamais exposer la connaissance centrale de l’IA SeductAI.**
