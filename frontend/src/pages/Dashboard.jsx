import React, { useEffect, useState, useCallback } from "react";
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
  const [currentInteractionId, setCurrentInteractionId] = useState(null);
  const [currentInteractionStatus, setCurrentInteractionStatus] = useState("open"); // Ajouté
  const [showFullHistory, setShowFullHistory] = useState(false);
  const [classeIA, setClasseIA] = useState(null);
  const [refreshFlag, setRefreshFlag] = useState(false);
  const [refreshKey, setRefreshKey] = useState(0);

  const navigate = useNavigate();

  // 🔄 Récupère tout le détail de l'interaction courante
  const fetchCurrentInteraction = useCallback(() => {
    if (!currentInteractionId) return;
    const token = localStorage.getItem("token");
    fetch(`http://localhost:8000/interactions`, {
      headers: { Authorization: `Bearer ${token}` }
    })
      .then((res) => res.json())
      .then((data) => {
        const found = data.find(i => i.id === currentInteractionId);
        setCurrentInteractionStatus(found?.status || "open");
        // Harmonise scores
        if (found?.scores) setLastScores(found.scores);
        else if (found) setLastScores({
          confiance: found.confiance,
          clarte: found.clarte ?? found.clarté,
          empathie: found.empathie,
          assertivite: found.assertivite ?? found.assertivité,
          authenticite: found.authenticite ?? found.authenticité,
          creativite: found.creativite ?? found.créativité
        });
        else setLastScores(null);
      });
  }, [currentInteractionId]);

  // 1. Fetch user, latest interaction, progression au démarrage
  const fetchUserStats = useCallback(() => {
    const token = localStorage.getItem("token");
    Promise.all([
      fetch("http://localhost:8000/me", {
        headers: { Authorization: `Bearer ${token}` },
      }).then(res => {
        if (!res.ok) throw new Error("Token invalide");
        return res.json();
      }),
      fetch("http://localhost:8000/interactions/latest", {
        headers: { Authorization: `Bearer ${token}` },
      }).then(res => res.json()),
      fetch("http://localhost:8000/me/progression", {
        headers: { Authorization: `Bearer ${token}` },
      }).then(res => res.json())
    ])
      .then(([user, last, prog]) => {
        setUserData(user);
        setLastScores(last.scores);
        setCurrentInteractionId(last.id);
        setClasseIA(prog.classe_actuelle || "analyse_en_cours");
      })
      .catch((err) => {
        console.error("[DASHBOARD][fetchUserStats] Erreur API :", err);
        navigate("/login");
      });
  }, [navigate]);

  // 2. Fetch au montage/refresh
  useEffect(() => {
    fetchUserStats();
  }, [fetchUserStats, refreshKey]);

  // 3. À chaque changement d'interaction, fetch détail (status + scores)
  useEffect(() => {
    fetchCurrentInteraction();
    // eslint-disable-next-line
  }, [currentInteractionId, refreshKey, refreshFlag]);

  // ➕ Nouvelle conversation
  const handleNewConversation = () => {
    setCurrentInteractionId(null);
    setShowFullHistory(false);
    setLastScores(null);
    setCurrentInteractionStatus("open");
  };

  // Refresh dashboard après IA
  const handleAfterIA = () => {
    setRefreshKey(k => k + 1);
    setRefreshFlag(f => !f);
  };

  // Fermer conversation (PATCH /close)
  const handleCloseInteraction = async () => {
    try {
      const res = await fetch(`http://localhost:8000/interactions/${currentInteractionId}/close`, {
        method: "PATCH",
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
      });
      if (!res.ok) throw new Error("Erreur lors de la fermeture");
      setCurrentInteractionStatus("closed");
      setRefreshFlag(f => !f);
    } catch (e) {
      alert("Erreur lors de la fermeture du thread !");
    }
  };

  // 🗑️ Supprimer une interaction
  const handleDeleteInteraction = async (id) => {
    try {
      const res = await fetch(`http://localhost:8000/interactions/${id}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
      });
      if (!res.ok) throw new Error(`Erreur ${res.status}`);
      if (id === currentInteractionId) handleNewConversation();
      setRefreshFlag((f) => !f);
    } catch (err) {
      console.error("Erreur suppression interaction :", err);
    }
  };

  // ↩️ Rouvrir une interaction
  const handleReopenInteraction = async (id) => {
    try {
      const res = await fetch(`http://localhost:8000/interactions/${id}/reopen`, {
        method: "PATCH",
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
      });
      if (!res.ok) throw new Error(`Erreur ${res.status}`);
      setCurrentInteractionId(id);
      setShowFullHistory(false);
      setCurrentInteractionStatus("open");
      setRefreshFlag((f) => !f);
    } catch (err) {
      console.error("Erreur réouverture interaction :", err);
    }
  };

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

      {/* ➕ Nouvelle conversation */}
      <button
        onClick={handleNewConversation}
        style={{ ...styles.editButton, backgroundColor: "#9b59b6" }}
      >
        ➕ Nouvelle conversation
      </button>

      {/* 💬 Formulaire pour démarrer un nouveau fil */}
      {!showFullHistory && currentInteractionId === null && (
        <>
          <h3 style={{ marginTop: "2rem" }}>🧠 Pose une nouvelle question :</h3>
          <AskForm
            interactionId={null}
            onNewInteraction={(id) => setCurrentInteractionId(id)}
          />
        </>
      )}

      {/* 🧵 Thread de messages visible UNIQUEMENT si une interaction est active */}
      {!showFullHistory && currentInteractionId && (
        <>
          <MessageThread
            interactionId={currentInteractionId}
            token={localStorage.getItem("token")}
            onAfterIA={handleAfterIA}
          />
          {/* ⬇️ Bouton Fermer la conversation ⬇️ */}
          {currentInteractionStatus === "open" && (
            <button
              onClick={handleCloseInteraction}
              style={{
                ...styles.editButton,
                backgroundColor: "#FFA726",
                color: "#fff",
                marginTop: "1rem"
              }}
            >
              🔒 Fermer la conversation
            </button>
          )}
          {currentInteractionStatus === "closed" && (
            <p style={{ color: "#888", marginTop: "1rem" }}>
              Conversation clôturée. Tu peux la rouvrir via l’historique.
            </p>
          )}
        </>
      )}

      {/* 📊 Scores IA */}
      {!showFullHistory && lastScores && (
        <div style={{ marginTop: "2rem" }}>
          <h3>📊 Progression relationnelle :</h3>
          <ScoreBar label="🔥 Confiance" value={lastScores.confiance} />
          <ScoreBar label="💬 Clarté" value={lastScores.clarte ?? lastScores.clarté} />
          <ScoreBar label="💖 Empathie" value={lastScores.empathie} />
          <ScoreBar label="🎯 Assertivité" value={lastScores.assertivite ?? lastScores.assertivité} />
          <ScoreBar label="🌿 Authenticité" value={lastScores.authenticite ?? lastScores.authenticité} />
          <ScoreBar label="🎨 Créativité" value={lastScores.creativite ?? lastScores.créativité} />
          <ProgressionCard scores={lastScores} userClasse={classeIA} />
          <div style={{ marginTop: "2rem" }}>
            {classeIA === "analyse_en_cours" ? (
              <p>🧪 En cours d’analyse… L’IA affinera ton profil au fil des interactions.</p>
            ) : (
              <p><strong>🎭 Classe IA :</strong> {classeIA}</p>
            )}
          </div>
        </div>
      )}

      {/* 📜 Historique complet (toujours visible mais en mode "plein" si togglé) */}
      <InteractionHistory
        token={localStorage.getItem("token")}
        fullMode={showFullHistory}
        onSelectInteraction={(id) => setCurrentInteractionId(id)}
        onDelete={handleDeleteInteraction}
        onReopen={handleReopenInteraction}
        refreshFlag={refreshFlag}
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
};

export default Dashboard;
