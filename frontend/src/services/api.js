// ✅ TOUS LES IMPORTS EN HAUT
import axios from "axios";

const BASE_URL = "http://localhost:8000";

// 👤 Inscription
export async function registerUser(userData) {
  try {
    const response = await fetch(`${BASE_URL}/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(userData),
    });

    if (!response.ok) throw new Error("Erreur lors de l'inscription");

    const data = await response.json();
    console.log("[✅] Utilisateur inscrit avec succès :", data);
    return data;
  } catch (error) {
    console.error("[❌] Erreur API registerUser :", error);
    throw error;
  }
}

// 🔐 Connexion
export async function loginUser(email, password) {
  try {
    const response = await fetch(`${BASE_URL}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({
        username: email,
        password: password,
      }),
    });

    if (!response.ok) throw new Error("Échec de la connexion");

    const data = await response.json();
    console.log("[✅] Connexion réussie :", data);
    return data;
  } catch (error) {
    console.error("[❌] Erreur loginUser :", error);
    throw error;
  }
}

// 📦 Appels API génériques via axios
const api = axios.create({
  baseURL: BASE_URL,
});

// 🔐 Ajout automatique du token dans les headers
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) config.headers.Authorization = `Bearer ${token}`;
    return config;
  },
  (error) => Promise.reject(error)
);

// ✅ Export global
export default api;
