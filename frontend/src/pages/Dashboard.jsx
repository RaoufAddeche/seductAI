// 📄 src/pages/Dashboard.jsx
import React from "react";

function handleLogout() {
  localStorage.removeItem("token");
  window.location.href = "/login";
}

function Dashboard() {
  return (
    <div style={{ padding: "2rem" }}>
      <h1>Bienvenue sur ton Dashboard 🎯</h1>
      <p>Tu es connecté avec succès à SeductAI !</p>

      <button onClick={handleLogout} style={{
        marginTop: "1rem",
        padding: "0.5rem 1rem",
        backgroundColor: "#e74c3c",
        color: "white",
        border: "none",
        borderRadius: "5px",
        cursor: "pointer"
      }}>
        Se déconnecter
      </button>
    </div>
  );
}

export default Dashboard;
