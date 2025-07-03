import { Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import LoginRegister from './components/LoginRegister';
import MainPage from './components/MainPage';

function getCookie(name) {
  const matches = document.cookie.match(
    new RegExp(
      "(?:^|; )" +
        name.replace(/([$?*|{}\(\)\[\]\\\/\+^])/g, "\\$1") +
        "=([^;]*)"
    )
  );
  return matches ? decodeURIComponent(matches[1]) : undefined;
}

function App() {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const token = getCookie('token');
    if (token) {
      setUser({ email: localStorage.getItem('userEmail') });
    }
  }, []);

  const handleLoginSuccess = (email) => {
    setUser(email);
    localStorage.setItem('userEmail', email); 
    navigate('/'); 
  };

  const handleLogout = () => {
    localStorage.removeItem('jwtToken');
    localStorage.removeItem('userEmail');
    setUser(null);
    navigate('/login');
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
    </Routes>
  );
}

export default App;