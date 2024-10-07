import axios from 'axios';

// Create an Axios instance
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL,  // Backend API URL
});

// Intercept requests and add the JWT token to the headers
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => Promise.reject(error)
);

export default api;
