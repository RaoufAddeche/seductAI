import React, { useState } from "react";

/**
 * Formulaire pour démarrer ou continuer une interaction (thread)
 * - Crée le thread si besoin (si interactionId == null)
 * - Ajoute le 1er message si écrit
 * - Préviens le parent de l'ID du thread (onNewInteraction)
 */
function AskForm({ interactionId, onNewInteraction }) {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);

  // Permet submit avec Ctrl+Entrée
  const handleKeyDown = (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
      handleAsk();
    }
  };

  const handleAsk = async () => {
    if (loading) return;
    const token = localStorage.getItem("token");
    setLoading(true);

    let newInteractionId = interactionId; // Par défaut, continue le même chat

    try {
      // 1️⃣ Créer thread SI pas d'interaction courante (mode 'nouvelle conv')
      if (!newInteractionId) {
        console.log("[DEBUG AskForm] Création d'une nouvelle interaction");
        const res = await fetch("http://localhost:8000/interactions/start", {
          method: "POST",
          headers: { Authorization: `Bearer ${token}` }
        });
        if (!res.ok) throw new Error("Erreur lors de la création du thread");
        const data = await res.json();
        newInteractionId = data.id;
      }

      // 2️⃣ Ajout du message utilisateur
      if (question.trim()) {
        console.log(`[DEBUG AskForm] Ajout d'un message à interaction ${newInteractionId}`);
        const resMsg = await fetch("http://localhost:8000/messages", {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            interaction_id: newInteractionId,
            content: question.trim(),
            sender: "user",
            role: "user"
          }),
        });
        if (!resMsg.ok) throw new Error("Erreur enregistrement message");
        await resMsg.json();
      }

      setQuestion("");

      // 3️⃣ Toujours notifier le parent de l'ID utilisé (créé ou non)
      if (onNewInteraction) onNewInteraction(newInteractionId);

    } catch (error) {
      alert("[❌] Erreur AskForm : " + error.message);
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ marginTop: "2rem" }}>
      <textarea
        rows={3}
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Pose ta question ici... (facultatif)"
        style={{ width: "100%", padding: "1rem", borderRadius: "8px", resize: "none" }}
        disabled={loading}
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
          cursor: loading ? "not-allowed" : "pointer"
        }}
      >
        {loading ? "Envoi..." : "Envoyer"}
      </button>
    </div>
  );
}

export default AskForm;
