// 📄 src/components/SeductionClassCard.jsx
import React from "react";

// 💡 Dictionnaire de classes selon le score dominant
const classes = {
  confiance: {
    title: "Charismatique",
    emoji: "🦁",
    description: "Tu inspires confiance et assurance dès les premiers mots.",
    color: "#f39c12",
  },
  clarté: {
    title: "Direct",
    emoji: "⚡",
    description: "Tu vas droit au but, sans tourner autour du pot.",
    color: "#3498db",
  },
  empathie: {
    title: "Empathique",
    emoji: "💗",
    description: "Tu lis entre les lignes et connectes profondément.",
    color: "#e91e63",
  },
  assertivité: {
    title: "Leader doux",
    emoji: "🧠",
    description: "Tu poses ton cadre sans agressivité, avec justesse.",
    color: "#27ae60",
  },
};

function SeductionClassCard({ scores }) {
  if (!scores) return null;

  // 🔍 Trouve le score le plus élevé
  const topKey = Object.entries(scores).reduce((a, b) => (a[1] > b[1] ? a : b))[0];
  const profile = classes[topKey];

  return (
    <div style={{
      marginTop: "2rem",
      padding: "1.5rem",
      borderRadius: "12px",
      backgroundColor: profile.color,
      color: "white",
      boxShadow: "0 4px 10px rgba(0,0,0,0.2)"
    }}>
      <h2>{profile.emoji} Profil : {profile.title}</h2>
      <p>{profile.description}</p>
    </div>
  );
}

export default SeductionClassCard;
