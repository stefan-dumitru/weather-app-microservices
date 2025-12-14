import axios from "axios";

const baseURL = import.meta.env.VITE_API_BASE_URL;

console.log("API Base URL:", import.meta.env.VITE_API_BASE_URL);
console.log("API Base URL:", baseURL);

if (baseURL?.startsWith("http://") && import.meta.env.PROD) {
  throw new Error("🚨 Insecure API base URL in production");
}

const axiosClient = axios.create({ baseURL });

// Interceptor for JWT
axiosClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default axiosClient;