// 📄 src/components/MessageThread.jsx

import React, { useEffect, useState, useRef } from "react";

/**
 * Affiche le thread de messages pour une interaction (chat).
 * Appelle onAfterIA() (si fourni) après chaque réponse IA,
 * pour permettre au parent (Dashboard) de refresh scores/stats.
 */
function MessageThread({ interactionId, token, onAfterIA }) {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  // 🟣 Auto-scroll à chaque update du thread
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  // 🔁 Récupère les messages du fil
  useEffect(() => {
    if (!interactionId) return;
    fetchMessages();
    // eslint-disable-next-line
  }, [interactionId, token]);

  // 👇 Fetch thread messages (réutilisable)
  const fetchMessages = async () => {
    if (!interactionId) return;
    try {
      const res = await fetch(`http://localhost:8000/messages/${interactionId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      const data = await res.json();
      console.log("MESSAGES FETCHED", data); // <--- ajoute ça !
      setMessages(data);
    } catch (err) {
      console.error("Erreur récupération messages:", err);
    }
  };

  // 🚀 Envoie message + IA + refresh + notify parent
  const handleSend = async () => {
    if (loading || !inputMessage.trim()) return;
    setLoading(true);
    try {
      // 1️⃣ Ajoute le message utilisateur
      const res = await fetch("http://localhost:8000/messages", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          interaction_id: interactionId,
          content: inputMessage,
          sender: "user",
          role: "user"
        })
      });
      if (!res.ok) throw new Error("Erreur ajout message");

      // 2️⃣ Appelle l’IA (génère la réponse et met à jour l'interaction)
      const askRes = await fetch(`http://localhost:8000/ask/${interactionId}`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ question: inputMessage })
      });
      if (!askRes.ok) throw new Error("Erreur appel IA");

      // 3️⃣ Refresh les messages
      await fetchMessages();

      // 4️⃣ Notifie le parent pour qu'il refresh scores/dashboard
      if (onAfterIA) onAfterIA();

      setInputMessage("");
    } catch (err) {
      console.error("Erreur dans le thread:", err);
      alert("Erreur lors de l’envoi. Réessaie.");
    } finally {
      setLoading(false);
    }
  };

  // 💡 Envoi avec Ctrl+Entrée (optionnel)
  const handleKeyDown = (e) => {
    if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
      handleSend();
    }
  };

  return (
    <div style={{ marginTop: "2rem" }}>
      <h3>🧵 Discussion :</h3>

      {/* 💬 Thread */}
      <div style={{
        backgroundColor: "#f9f9f9",
        padding: "1rem",
        borderRadius: "8px",
        minHeight: 120,
        maxHeight: 340,
        overflowY: "auto"
      }}>
        {messages.map((msg) => (
          <div
            key={msg.id}
            style={{
              marginBottom: "1rem",
              textAlign: msg.role === "user" ? "left" : "right",
              display: "flex",
              flexDirection: msg.role === "user" ? "row" : "row-reverse"
            }}
          >
            <div
              style={{
                backgroundColor: msg.role === "user" ? "#d2eafc" : "#eee0fd",
                color: "#222",
                padding: "0.7rem 1rem",
                borderRadius: "18px",
                maxWidth: "75%",
                minWidth: "60px",
                wordBreak: "break-word",
                boxShadow: "0 2px 4px #0001",
                position: "relative"
              }}
            >
              <div style={{ fontSize: "0.87em", color: "#666", marginBottom: "0.3em" }}>
                {msg.role === "user" ? "🧑‍💬 Toi" : "🤖 IA"}
                {" · "}
                {msg.timestamp
                  ? new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
                  : ""}
              </div>
              <div>{msg.content}</div>
            </div>
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      {/* ⏳ Loader IA animé */}
      {loading && (
        <div style={{
          marginTop: "1rem",
          color: "#8e44ad",
          fontWeight: "bold",
          display: "flex",
          alignItems: "center"
        }}>
          <span style={{
            display: "inline-block",
            width: "16px",
            height: "16px",
            marginRight: "8px",
            border: "3px solid #8e44ad",
            borderTop: "3px solid transparent",
            borderRadius: "50%",
            animation: "spin 1s linear infinite"
          }} />
          L'IA réfléchit...
          <style>
            {`
            @keyframes spin {
              0% { transform: rotate(0deg);}
              100% { transform: rotate(360deg);}
            }
            `}
          </style>
        </div>
      )}

      {/* 📝 Saisie + bouton */}
      <div style={{ marginTop: "1rem", display: "flex", alignItems: "flex-end" }}>
        <textarea
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          rows={2}
          placeholder="Écris ton message ici..."
          style={{
            width: "100%",
            padding: "0.5rem",
            borderRadius: "6px",
            border: "1px solid #ccc",
            resize: "none"
          }}
          disabled={loading}
        />
        <button
          onClick={handleSend}
          disabled={loading || !inputMessage.trim()}
          style={{
            marginLeft: "0.7rem",
            backgroundColor: "#3498db",
            color: "white",
            padding: "0.6rem 1.3rem",
            border: "none",
            borderRadius: "5px",
            cursor: loading ? "not-allowed" : "pointer",
            fontWeight: 600,
            fontSize: "1rem"
          }}
        >
          {loading ? "Envoi..." : "Envoyer"}
        </button>
      </div>
    </div>
  );
}

export default MessageThread;
