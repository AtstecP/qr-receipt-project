import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || `http://${window.location.hostname}:8000`, 
  withCredentials: true,             // so refresh cookie is stored/sent
});

api.interceptors.request.use((config) => {
  const t = localStorage.getItem("jwtToken");
  if (t) config.headers.Authorization = `Bearer ${t}`;
  return config;
});

export default api;
