import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter as Router } from 'react-router-dom'
import App from './App.jsx'

// Initialize axios defaults (optional but recommended)
import axios from 'axios'
axios.defaults.baseURL = 'http://127.0.0.1:8000'
axios.defaults.withCredentials = true;

axios.interceptors.request.use((config) => {
  const token = localStorage.getItem("jwtToken");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Router>
      <App />
    </Router>
  </StrictMode>
)