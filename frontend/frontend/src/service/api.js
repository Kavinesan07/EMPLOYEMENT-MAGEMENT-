import axios from 'axios';

const api = axios.create({
  // Replace with your actual backend port (e.g., 5000, 8000, 8080)
  baseURL: 'http://localhost:5173/api', 
});

// Automatically attach the JWT token to every request if it exists
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
