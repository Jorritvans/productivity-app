import axios from 'axios';

// Create an Axios instance with the baseURL from environment variables
const api = axios.create({
  baseURL: process.env.REACT_APP_API_BASE_URL, // Uses the environment variable
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor to add the Authorization header to every request if a token exists
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