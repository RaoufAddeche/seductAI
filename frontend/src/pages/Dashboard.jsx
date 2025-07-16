import React, { useEffect, useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import ScoreBar from "../components/ScoreBar";
import ProgressionCard from "../components/ProgressionCard";
import InteractionHistory from "../components/InteractionHistory";
import AskForm from "../components/AskForm";
import MessageThread from "../components/MessageThread";

function handleLogout() {
  localStorage.removeItem("token");
  window.location.href = "/login";
}

function Dashboard() {
  const [userData, setUserData] = useState(null);
  const [lastScores, setLastScores] = useState(null);
  const [lastAnswer, setLastAnswer] = useState("");
  const [lastInteractionId, setLastInteractionId] = useState(null);
  const [showFullHistory, setShowFullHistory] = useState(false);
  const [classeIA, setClasseIA] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/login");
      return;
    }

    // 🔐 Infos utilisateur
    fetch("http://localhost:8000/me", {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => {
        if (!res.ok) throw new Error("Token invalide");
        return res.json();
      })
      .then((data) => {
        setUserData(data);
        return fetch("http://localhost:8000/interactions/latest", {
          headers: { Authorization: `Bearer ${token}` },
        });
      })
      .then((res) => res.json())
      .then((data) => {
        setLastScores(data.scores);
        setLastAnswer(data.final_answer || "");
        setLastInteractionId(data.id);
      })
      .catch((err) => {
        console.error("Erreur API :", err);
        navigate("/login");
      });

    // 🎭 Classe IA
    fetch("http://localhost:8000/me/progression", {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => res.json())
      .then((data) => setClasseIA(data.classe_actuelle || "analyse_en_cours"));
  }, [navigate]);

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Bienvenue sur ton Dashboard 🎯</h1>

      {/* 👤 Infos utilisateur */}
      {userData ? (
        <div>
          <p><strong>Nom :</strong> {userData.username}</p>
          <p><strong>Email :</strong> {userData.email}</p>
          <Link to="/edit-profile">
            <button style={styles.editButton}>✏️ Modifier mon profil</button>
          </Link>
        </div>
      ) : (
        <p>Chargement des infos utilisateur...</p>
      )}

      {/* 🔁 Toggle historique */}
      <button
        onClick={() => setShowFullHistory(!showFullHistory)}
        style={styles.toggleButton}
      >
        {showFullHistory ? "🔙 Revenir à une interaction simple" : "🧵 Voir toutes mes interactions"}
      </button>

      {/* 💬 Nouvelle interaction */}
      {!showFullHistory && (
        <>
          <h3 style={{ marginTop: "2rem" }}>🧠 Pose une nouvelle question :</h3>
          <AskForm onNewInteraction={() => window.location.reload()} />
        </>
      )}

      {/* 💡 Dernière réponse IA */}
      {!showFullHistory && lastAnswer && (
        <div style={{ marginTop: "2rem" }}>
          <h3>💡 Dernière réponse générée :</h3>
          <div style={styles.answerBox}>
            {lastAnswer}
          </div>
        </div>
      )}

      {/* 🧵 Fil de messages */}
      {!showFullHistory && lastInteractionId && (
        <MessageThread
          interactionId={lastInteractionId}
          token={localStorage.getItem("token")}
        />
      )}

      {/* 📊 Scores IA */}
      {!showFullHistory && lastScores && (
        <div style={{ marginTop: "2rem" }}>
          <h3>📊 Progression relationnelle :</h3>

          {/* ✅ 6 axes de progression */}
          <ScoreBar label="🔥 Confiance" value={lastScores.confiance} />
          <ScoreBar label="💬 Clarté" value={lastScores.clarté} />
          <ScoreBar label="💖 Empathie" value={lastScores.empathie} />
          <ScoreBar label="🎯 Assertivité" value={lastScores.assertivité} />
          <ScoreBar label="🌿 Authenticité" value={lastScores.authenticité} />
          <ScoreBar label="🎨 Créativité" value={lastScores.creativité} />

          <ProgressionCard scores={lastScores} userClasse={classeIA} />

          {/* 🎭 Classe IA */}
          <div style={{ marginTop: "2rem" }}>
            {classeIA === "analyse_en_cours" ? (
              <p>🧪 En cours d’analyse… L’IA affinera ton profil au fil des interactions.</p>
            ) : (
              <p><strong>🎭 Classe IA :</strong> {classeIA}</p>
            )}
          </div>
        </div>
      )}

      {/* 📜 Historique global */}
      <InteractionHistory
        token={localStorage.getItem("token")}
        fullMode={showFullHistory}
        onSelectInteraction={(id) => setLastInteractionId(id)}
      />

      {/* 🔓 Déconnexion */}
      <button onClick={handleLogout} style={styles.logoutButton}>
        Se déconnecter
      </button>
    </div>
  );
}

const styles = {
  editButton: {
    marginTop: "1rem",
    padding: "0.5rem 1rem",
    backgroundColor: "#2ecc71",
    color: "white",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
  },
  toggleButton: {
    marginTop: "2rem",
    padding: "0.5rem 1rem",
    backgroundColor: "#3498db",
    color: "white",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
  },
  logoutButton: {
    marginTop: "2rem",
    padding: "0.5rem 1rem",
    backgroundColor: "#e74c3c",
    color: "white",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
  },
  answerBox: {
    backgroundColor: "#f4f4f4",
    padding: "1rem",
    borderRadius: "8px",
    whiteSpace: "pre-wrap",
  },
};

export default Dashboard;
