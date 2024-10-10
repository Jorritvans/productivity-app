import axios from 'axios';

// Create an Axios instance
const api = axios.create({
  baseURL: '/api/',  // Relative path since frontend and backend are served from the same domain
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor to add the Authorization header
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default api;
