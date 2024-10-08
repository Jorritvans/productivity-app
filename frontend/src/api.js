import axios from 'axios';

const api = axios.create({
  baseURL: 'https://8000-jorritvans-productivity-my39hyagwgi.ws-eu116.gitpod.io/api',
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export default api;
