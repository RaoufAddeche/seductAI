// 📄 src/components/ProgressionCard.jsx
import React from "react";

// 💡 Dictionnaire des styles IA
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
  authenticité: {
    title: "Sincère",
    emoji: "🌿",
    description: "Tu es naturel et aligné avec ce que tu dis et ressens.",
    color: "#2c3e50",
  },
  creativite: {
    title: "Inattendu",
    emoji: "🎨",
    description: "Tu surprends, tu joues avec les codes, tu vibres autrement.",
    color: "#9b59b6",
  }
};

function ProgressionCard({ scores, userClasse }) {
  if (!scores) return null;

  const topKey = Object.entries(scores).reduce((a, b) => (a[1] > b[1] ? a : b))[0];
  const profile = userClasse && userClasse !== "analyse_en_cours"
    ? classes[userClasse.toLowerCase()]
    : classes[topKey];

  if (!profile) {
    return <p>🔍 Aucun profil détecté pour le moment.</p>;
  }

  return (
    <div style={{
      marginTop: "2rem",
      padding: "1.5rem",
      borderRadius: "12px",
      backgroundColor: profile.color,
      color: "white",
      boxShadow: "0 4px 10px rgba(0,0,0,0.2)"
    }}>
      <h2>{profile.emoji} Profil {(userClasse && userClasse !== "analyse_en_cours") ? "(définitif)" : "(en cours)"} : {profile.title}</h2>
      <p>{profile.description}</p>
    </div>
  );
}

export default ProgressionCard;
