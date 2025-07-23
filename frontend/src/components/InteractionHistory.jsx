import React, { useEffect, useState } from "react";

const InteractionHistory = ({
  token,
  fullMode,
  onSelectInteraction,
  onDelete,
  onReopen,
  refreshFlag,
}) => {
  const [interactions, setInteractions] = useState([]);
  const [openedId, setOpenedId] = useState(null);
  const [loadingActionId, setLoadingActionId] = useState(null);
  const [messagesDetail, setMessagesDetail] = useState({}); // {interactionId: [messages]}

  useEffect(() => {
    fetchInteractions();
    // eslint-disable-next-line
  }, [token, refreshFlag]);

  const fetchInteractions = async () => {
    try {
      const res = await fetch("http://localhost:8000/interactions", {
        headers: { Authorization: `Bearer ${token}` },
      });
      const data = await res.json();
      setInteractions(data.sort((a, b) => new Date(b.created_at) - new Date(a.created_at)));
    } catch (err) {
      console.error("Erreur interactions :", err);
    }
  };

  // Fetch les messages d'une interaction au clic (lazy loading)
  const handleShowThread = async (id) => {
    if (messagesDetail[id]) {
      // toggle masquage/affichage
      setMessagesDetail((prev) => ({ ...prev, [id]: undefined }));
      return;
    }
    try {
      const res = await fetch(`http://localhost:8000/messages/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const data = await res.json();
      setMessagesDetail((prev) => ({ ...prev, [id]: data }));
    } catch (err) {
      alert("Erreur lors du chargement du thread.");
      setMessagesDetail((prev) => ({ ...prev, [id]: undefined }));
    }
  };

  // Supprimer interaction
  const handleDeleteClick = async (id, e) => {
    e.stopPropagation();
    setLoadingActionId(id);
    await onDelete?.(id);
    setLoadingActionId(null);
  };

  // Rouvrir interaction
  const handleReopenClick = async (id, e) => {
    e.stopPropagation();
    setLoadingActionId(id);
    await onReopen?.(id);
    setLoadingActionId(null);
  };

  if (!interactions.length) return <p>📭 Aucune interaction enregistrée.</p>;

  return (
    <div style={{ marginTop: "2rem" }}>
      <h3>📜 Dernières interactions :</h3>
      {interactions.map((interaction) => (
        <div
          key={interaction.id}
          onClick={() => {
            if (fullMode) return;
            setOpenedId(interaction.id === openedId ? null : interaction.id);
            onSelectInteraction?.(interaction.id);
          }}
          style={{
            marginBottom: "1rem",
            padding: "1rem",
            backgroundColor: "#f9f9f9",
            borderRadius: "8px",
            cursor: fullMode ? "default" : "pointer",
            border: interaction.id === openedId ? "2px solid #007bff" : "1px solid #ccc",
            position: "relative",
            transition: "border .2s"
          }}
        >
          <p><strong>{new Date(interaction.created_at).toLocaleString()}</strong></p>
          <p>{interaction.question || <span style={{ color: "#bbb" }}>⏳ (Discussion sans question initiale)</span>}</p>
          <p>
            🔥 {interaction.confiance || 0}% | 💬 {interaction.clarte || 0}% | 💖 {interaction.empathie || 0}% | 🎯 {interaction.assertivite || 0}%<br/>
            🌿 {interaction.authenticite || 0}% | 🎨 {interaction.creativite || 0}%
          </p>
          <p>📌 <strong>Status :</strong> {interaction.status}</p>
          {(fullMode || openedId === interaction.id) && (
            <div
              style={{
                marginTop: "0.5rem",
                padding: "0.75rem",
                backgroundColor: "#eef4ff",
                borderRadius: "5px",
                whiteSpace: "pre-wrap",
              }}
            >
              💬 <strong>Réponse IA :</strong><br />
              {interaction.final_answer}
            </div>
          )}

          {/* Actions & Thread detail (only in fullMode) */}
          {fullMode && (
            <div style={{ position: "absolute", top: "10px", right: "10px", display: "flex", gap: "0.5rem" }}>
              {interaction.status !== "deleted" && (
                <button
                  onClick={(e) => handleDeleteClick(interaction.id, e)}
                  disabled={loadingActionId === interaction.id}
                  style={{
                    color: loadingActionId === interaction.id ? "#aaa" : "red",
                    background: "transparent",
                    border: "none",
                    cursor: loadingActionId === interaction.id ? "default" : "pointer",
                    fontSize: "1.2rem",
                  }}
                  title="Supprimer l'interaction"
                >
                  🗑️
                </button>
              )}

              {interaction.status === "closed" && (
                <button
                  onClick={(e) => handleReopenClick(interaction.id, e)}
                  disabled={loadingActionId === interaction.id}
                  style={{
                    color: loadingActionId === interaction.id ? "#aaa" : "blue",
                    background: "transparent",
                    border: "none",
                    cursor: loadingActionId === interaction.id ? "default" : "pointer",
                    fontSize: "1.2rem",
                  }}
                  title="Rouvrir l'interaction"
                >
                  ↩️
                </button>
              )}

              {/* Fil complet toggle */}
              <button
                onClick={(e) => { e.stopPropagation(); handleShowThread(interaction.id); }}
                style={{
                  color: "#2d8cff",
                  background: "transparent",
                  border: "none",
                  cursor: "pointer",
                  fontSize: "1.1rem",
                  marginLeft: "0.5rem"
                }}
                title={messagesDetail[interaction.id] ? "Masquer le fil" : "Voir le fil complet"}
              >
                {messagesDetail[interaction.id] ? "Masquer le fil" : "Voir le fil complet"}
              </button>
            </div>
          )}

          {/* Affichage thread complet si demandé */}
          {messagesDetail[interaction.id] && (
            <div style={{
              background: "#f6f8fa",
              marginTop: 10,
              borderRadius: 8,
              padding: 8,
              border: "1px solid #ccc"
            }}>
              <strong>🧵 Thread complet :</strong>
              {messagesDetail[interaction.id].length === 0
                ? <div style={{ color: "#aaa" }}>Aucun message dans ce thread.</div>
                : messagesDetail[interaction.id].map(msg =>
                  <div key={msg.id} style={{
                    marginBottom: 4,
                    background: msg.role === "user" ? "#d2eafc" : "#eee0fd",
                    borderRadius: 8,
                    padding: "5px 10px",
                    textAlign: msg.role === "user" ? "left" : "right",
                  }}>
                    <span style={{ fontWeight: 600, color: msg.role === "user" ? "#3498db" : "#8e44ad" }}>
                      {msg.role === "user" ? "🧑‍💬" : "🤖"} {msg.role}
                    </span>
                    <span style={{ color: "#666", marginLeft: 8, fontSize: "0.9em" }}>
                      {msg.timestamp ? new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : ""}
                    </span>
                    <div>{msg.content}</div>
                  </div>
                )
              }
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export default InteractionHistory;
