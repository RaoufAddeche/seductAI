// 📄 MessageThread.jsx — Affiche les messages d'une interaction
import React, { useEffect, useState } from "react";

function MessageThread({ interactionId, token }) {
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    if (!interactionId || !token) return;

    fetch(`http://localhost:8000/messages/${interactionId}`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => res.json())
      .then((data) => {
        setMessages(data);
      })
      .catch((err) => {
        console.error("[❌] Erreur récupération messages :", err);
      });
  }, [interactionId, token]);

  return (
    <div style={{ marginTop: "1rem", backgroundColor: "#f9f9f9", padding: "1rem", borderRadius: "8px" }}>
      <h4>💬 Fil de discussion</h4>
      {messages.map((msg, index) => (
        <div key={index} style={{
          textAlign: msg.sender === "user" ? "right" : "left",
          margin: "0.5rem 0"
        }}>
          <span style={{
            backgroundColor: msg.sender === "user" ? "#d1f0ff" : "#e6e6e6",
            padding: "0.5rem 1rem",
            borderRadius: "10px",
            display: "inline-block",
            maxWidth: "80%"
          }}>
            {msg.content}
          </span>
        </div>
      ))}
    </div>
  );
}

export default MessageThread;
