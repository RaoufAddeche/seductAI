import React, { useEffect, useState } from "react";

const InteractionHistory = ({ token, fullMode, onSelectInteraction }) => {
  const [interactions, setInteractions] = useState([]);
  const [openedIndex, setOpenedIndex] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8000/interactions", {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => res.json())
      .then((data) => setInteractions(data.reverse())) // plus récent en haut
      .catch((err) => console.error("Erreur interactions :", err));
  }, [token]);

  if (!interactions.length) return <p>📭 Aucune interaction enregistrée.</p>;

  return (
    <div style={{ marginTop: "2rem" }}>
      <h3>📜 Dernières interactions :</h3>

      {interactions.map((interaction, index) => (
        <div
          key={interaction.id}
          onClick={() => {
            if (fullMode) return;
            setOpenedIndex(index === openedIndex ? null : index);
            if (onSelectInteraction) onSelectInteraction(interaction.id); // ✅ appel callback
          }}
          style={{
            marginBottom: "1rem",
            padding: "1rem",
            backgroundColor: "#f9f9f9",
            borderRadius: "8px",
            cursor: fullMode ? "default" : "pointer",
            border: index === openedIndex ? "2px solid #007bff" : "1px solid #ccc",
          }}
        >
          <p><strong>{new Date(interaction.created_at).toLocaleString()}</strong></p>
          <p>{interaction.question}</p>
          <p>
            🔥 {interaction.confiance || 0}% | 💬 {interaction.clarte || 0}% | 💖 {interaction.empathie || 0}% | 🎯 {interaction.assertivite || 0}%
          </p>

          {(fullMode || openedIndex === index) && (
            <div style={{
              marginTop: "0.5rem",
              padding: "0.75rem",
              backgroundColor: "#eef4ff",
              borderRadius: "5px",
              whiteSpace: "pre-wrap"
            }}>
              💬 <strong>Réponse IA :</strong><br />
              {interaction.final_answer}
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export default InteractionHistory;
