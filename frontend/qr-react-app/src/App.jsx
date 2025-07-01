import { Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import LoginRegister from './components/LoginRegister';
import MainPage from './components/MainPage';

function App() {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  // Проверяем токен при загрузке приложения
  useEffect(() => {
    const token = localStorage.getItem('jwtToken');
    if (token) {
      // Здесь можно добавить проверку токена на сервере
      // Для примера просто сохраняем минимальные данные
      setUser({ email: localStorage.getItem('userEmail') });
    }
  }, []);

  const handleLoginSuccess = (userData) => {
    setUser(userData);
    localStorage.setItem('userEmail', userData.email); // Сохраняем email
    navigate('/'); // Перенаправляем на главную
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