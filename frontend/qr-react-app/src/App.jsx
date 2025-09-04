// App.jsx
import { Routes, Route, Navigate, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import LoginRegister from "./components/LoginRegister";
import MainPage from "./components/MainPage";
// If you have the axios client with signOut helper:
// import { signOut } from "./lib/api";

function App() {
  const [user, setUser] = useState(null); // { email: string } | null
  const navigate = useNavigate();

  // On first load, restore session from localStorage
  useEffect(() => {
    const token = localStorage.getItem("jwtToken");
    const email = localStorage.getItem("userEmail");
    if (token && email) setUser({ email });
  }, []);

  // Optional: react to auth changes from other tabs
  useEffect(() => {
    const onStorage = (e) => {
      if (e.key === "jwtToken" && !e.newValue) {
        setUser(null);
        navigate("/login", { replace: true });
      }
    };
    window.addEventListener("storage", onStorage);
    return () => window.removeEventListener("storage", onStorage);
  }, [navigate]);

  const handleLoginSuccess = (email) => {
    // Your LoginRegister should already set localStorage.jwtToken
    localStorage.setItem("userEmail", email);
    setUser({ email });
    navigate("/", { replace: true });
  };

  const handleLogout = async () => {
    try {
      // If you exposed a logout endpoint:
      // await signOut(); // clears refresh cookie server-side
    } catch {/* ignore */}
    localStorage.removeItem("jwtToken");
    localStorage.removeItem("userEmail");
    setUser(null);
    navigate("/login", { replace: true });
  };

  return (
    <Routes>
      <Route
        path="/login"
        element={
          user ? (
            <Navigate to="/" replace />
          ) : (
            <LoginRegister onLoginSuccess={handleLoginSuccess} />
          )
        }
      />
      <Route
        path="/"
        element={
          user ? (
            <MainPage user={user} onLogout={handleLogout} />
          ) : (
            <Navigate to="/login" replace />
          )
        }
      />
      {/* Fallback */}
      <Route path="*" element={<Navigate to={user ? "/" : "/login"} replace />} />
    </Routes>
  );
}

export default App;
