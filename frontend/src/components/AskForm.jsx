// 📄 src/components/AskForm.jsx
import React, { useState } from "react";

function AskForm({ onNewInteraction }) {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    const token = localStorage.getItem("token");
    if (!question.trim()) return;

    setLoading(true);

    const res = await fetch("http://localhost:8000/ask", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ question })
    });

    const data = await res.json();
    console.log("[✅ ASK] Résultat IA :", data);

    setLoading(false);
    setQuestion("");

    // 🔄 Permet de recharger le dashboard après réponse
    if (onNewInteraction) onNewInteraction();
  };

  return (
    <div style={{ marginTop: "2rem" }}>
      <textarea
        rows="3"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Pose ta question à l'IA ici..."
        style={{ width: "100%", padding: "1rem", borderRadius: "8px", resize: "none" }}
      />
      <button
        onClick={handleAsk}
        disabled={loading}
        style={{
          marginTop: "0.5rem",
          padding: "0.5rem 1rem",
          backgroundColor: "#2ecc71",
          color: "white",
          border: "none",
          borderRadius: "5px",
          cursor: "pointer"
        }}
      >
        {loading ? "Envoi en cours..." : "Poser la question"}
      </button>
    </div>
  );
}

export default AskForm;
