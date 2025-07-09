// 📄 src/pages/Dashboard.jsx
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import ScoreBar from "../components/ScoreBar";
import SeductionClassCard from "../components/SeductionClassCard";

// 👉 Fonction qui supprime le token et redirige vers /login
function handleLogout() {
  localStorage.removeItem("token");
  window.location.href = "/login";
}

function Dashboard() {
  // 🧠 Données utilisateur
  const [userData, setUserData] = useState(null);

  // 🧠 Scores IA (confiance, clarté, etc.)
  const [lastScores, setLastScores] = useState(null);

  // 🔁 Redirection
  const navigate = useNavigate();

  // 🔁 useEffect au chargement : vérifie le token + appelle /me + /interactions/latest
  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token) {
      console.warn("🔒 Pas de token, redirection vers /login");
      navigate("/login");
      return;
    }

    // 👉 1. Récupérer les infos utilisateur
    fetch("http://localhost:8000/me", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((res) => {
        if (!res.ok) throw new Error("Token invalide");
        return res.json();
      })
      .then((data) => {
        console.log("✅ Données utilisateur :", data);
        setUserData(data);

        // 👉 2. Appel à /interactions/latest pour récupérer les scores IA
        return fetch("http://localhost:8000/interactions/latest", {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
      })
      .then((res) => res.json())
      .then((data) => {
        console.log("🧠 Derniers scores reçus :", data);
        setLastScores(data.scores);
      })
      .catch((err) => {
        console.error("❌ Erreur API ou token expiré :", err);
        navigate("/login");
      });
  }, [navigate]);

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Bienvenue sur ton Dashboard 🎯</h1>

      {/* ✅ Affichage infos utilisateur */}
      {userData ? (
        <div>
          <p><strong>Nom :</strong> {userData.username}</p>
          <p><strong>Email :</strong> {userData.email}</p>
        </div>
      ) : (
        <p>Chargement des infos utilisateur...</p>
      )}

      {/* ✅ Affichage scores IA */}
      {lastScores ? (
        <div style={{ marginTop: "2rem" }}>
        <h3>🧠 Progression relationnelle :</h3>
        <ScoreBar label="Confiance" value={lastScores.confiance} emoji="🔥" />
        <ScoreBar label="Clarté" value={lastScores["clarté"]} emoji="💬" />
        <ScoreBar label="Empathie" value={lastScores.empathie} emoji="💖" />
        <ScoreBar label="Assertivité" value={lastScores["assertivité"]} emoji="🎯" />
        <SeductionClassCard scores={lastScores} style={{ marginTop: "2rem" }} />
        </div>
      ) : (
        <p style={{ marginTop: "2rem" }}>Aucune interaction scorée pour le moment.</p>
      )}

      {/* 🔘 Bouton déconnexion */}
      <button
        onClick={handleLogout}
        style={{
          marginTop: "2rem",
          padding: "0.5rem 1rem",
          backgroundColor: "#e74c3c",
          color: "white",
          border: "none",
          borderRadius: "5px",
          cursor: "pointer"
        }}
      >
        Se déconnecter
      </button>
    </div>
  );
}

export default Dashboard;
