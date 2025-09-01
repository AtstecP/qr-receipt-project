// src/lib/api.js
import axios from "axios";

const BASE =
  import.meta.env.VITE_API_BASE_URL ||
  `http://${window.location.hostname}:8000`; // works on PC & phone

const api = axios.create({
  baseURL: BASE,
  withCredentials: true, // keep if you use cookies
  timeout: 20000,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("jwtToken");
  if (token) {
    config.headers = config.headers ?? {};
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
