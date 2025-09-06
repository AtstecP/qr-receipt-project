// src/components/MainPage.jsx
import React, { useState, useEffect } from "react";
import LoginRegister from "./LoginRegister";
import Dashboard from "./Dashboard";
import api from "../lib/api"; // your axios instance with baseURL + cookies

export default function MainPage() {
  const [user, setUser] = useState(null);

  // fetch current user info from backend
  const fetchUser = async () => {
    try {
      const res = await api.get("/api/v1/me", { withCredentials: true });
      const u = res.data;
      // normalize to camelCase for the app
      setUser({
        email: u.email,
        companyName: u.company_name ?? u.companyName ?? "",
      });

      localStorage.setItem("userEmail", res.data.email);
    } catch {
      setUser(null);
    }
  };

  // on mount, try to restore session
  useEffect(() => {
    fetchUser();
  }, []);

  const handleLoginSuccess = async () => {
    await fetchUser();
  };

  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem("userEmail");
  };
  console.log(user)
  return (
    <div className="min-h-screen">
      {user ? (
        <Dashboard user={user} onLogout={handleLogout} />
      ) : (
        <LoginRegister onLoginSuccess={handleLoginSuccess} />
      )}
    </div>
  );
}
