import React, { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";

function EditProfile() {
  const navigate = useNavigate();
  const [profile, setProfile] = useState({
    username: "",
    email: "",
    age: "",
    gender: "",
    orientation: "",
    interests: [],
  });

  const [loading, setLoading] = useState(true);
  const token = localStorage.getItem("token");

  // Liste d’intérêts proposés
  const allInterests = [
    "dating",
    "confiance",
    "communication pro",
    "humour",
    "rendez-vous",
    "réseaux sociaux",
    "séduction IRL",
  ];

  useEffect(() => {
    if (!token) {
      navigate("/login");
      return;
    }

    fetch("http://localhost:8000/me", {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => res.json())
      .then((data) => {
        setProfile({
          username: data.username || "",
          email: data.email || "",
          age: data.age || "",
          gender: data.gender || "",
          orientation: data.orientation || "",
          interests: data.interests || [],
        });
        setLoading(false);
      })
      .catch((err) => {
        console.error("Erreur chargement profil:", err);
        navigate("/login");
      });
  }, [navigate, token]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setProfile((prev) => ({ ...prev, [name]: value }));
  };

  const toggleInterest = (interest) => {
    setProfile((prev) => {
      const alreadySelected = prev.interests.includes(interest);
      const updatedInterests = alreadySelected
        ? prev.interests.filter((i) => i !== interest)
        : [...prev.interests, interest];
      return { ...prev, interests: updatedInterests };
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    fetch("http://localhost:8000/me", {
      method: "PUT",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(profile),
    })
      .then((res) => {
        if (!res.ok) throw new Error("Erreur sauvegarde");
        return res.json();
      })
      .then(() => {
        alert("Profil mis à jour !");
        navigate("/dashboard");
      })
      .catch((err) => {
        console.error("Erreur MAJ profil:", err);
        alert("Erreur lors de la mise à jour.");
      });
  };

  if (loading) return <p>Chargement...</p>;

  return (
    <div style={{ padding: "2rem" }}>
      <h2>🛠 Modifier mon profil</h2>
      <form onSubmit={handleSubmit} style={{ maxWidth: "500px" }}>
        <label>Nom :</label>
        <input
          type="text"
          name="username"
          value={profile.username}
          onChange={handleChange}
          style={{ width: "100%", marginBottom: "1rem" }}
        />

        <label>Email :</label>
        <input
          type="email"
          name="email"
          value={profile.email}
          onChange={handleChange}
          style={{ width: "100%", marginBottom: "1rem" }}
        />

        <label>Âge :</label>
        <input
          type="number"
          name="age"
          value={profile.age}
          onChange={handleChange}
          style={{ width: "100%", marginBottom: "1rem" }}
        />

        <label>Genre :</label>
        <select
          name="gender"
          value={profile.gender}
          onChange={handleChange}
          style={{ width: "100%", marginBottom: "1rem" }}
        >
          <option value="">-- Choisir --</option>
          <option value="homme">Homme</option>
          <option value="femme">Femme</option>
          <option value="non-binaire">Non-binaire</option>
          <option value="autre">Autre</option>
        </select>

        <label>Orientation :</label>
        <select
          name="orientation"
          value={profile.orientation}
          onChange={handleChange}
          style={{ width: "100%", marginBottom: "1rem" }}
        >
          <option value="">-- Choisir --</option>
          <option value="hétérosexuel">Hétérosexuel</option>
          <option value="homosexuel">Homosexuel</option>
          <option value="bisexuel">Bisexuel</option>
          <option value="asexuel">Asexuel</option>
          <option value="autre">Autre</option>
        </select>

        <label>Style de communication préféré :</label>
        <select
            name="style"
            value={profile.style || ""}
            onChange={handleChange}
            style={{ width: "100%", marginBottom: "1rem" }}
        >
            <option value="">-- Choisir --</option>
            <option value="formel">Formel</option>
            <option value="jeune">Jeune</option>
            <option value="humour décalé">Humour décalé</option>
            <option value="poétique">Poétique</option>
            <option value="direct">Direct</option>
            <option value="mystérieux">Mystérieux</option>
            <option value="spontané">Spontané</option>
        </select>

        <label>Centres d'intérêt :</label>
        <div style={{ display: "flex", flexWrap: "wrap", marginBottom: "1rem" }}>
          {allInterests.map((interest) => (
            <button
              type="button"
              key={interest}
              onClick={() => toggleInterest(interest)}
              style={{
                margin: "4px",
                padding: "0.4rem 0.7rem",
                borderRadius: "5px",
                border: profile.interests.includes(interest)
                  ? "2px solid #2ecc71"
                  : "1px solid #ccc",
                backgroundColor: profile.interests.includes(interest)
                  ? "#2ecc71"
                  : "white",
                color: profile.interests.includes(interest) ? "white" : "black",
                cursor: "pointer",
              }}
            >
              {interest}
            </button>
          ))}
        </div>

        <button
          type="submit"
          style={{
            padding: "0.6rem 1.2rem",
            backgroundColor: "#3498db",
            color: "white",
            border: "none",
            borderRadius: "6px",
            cursor: "pointer",
          }}
        >
          💾 Sauvegarder
        </button>
      </form>

      {/* 🔙 Retour au Dashboard */}
      <div style={{ marginTop: "1.5rem" }}>
        <Link to="/dashboard">← Retour au Dashboard</Link>
      </div>
    </div>
  );
}

export default EditProfile;
