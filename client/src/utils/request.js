import axios from "axios";
import { message } from "ant-design-vue";
import router from '../router/index'

const request = axios.create({
  baseURL: import.meta.env.MODE === "development" ? "http://localhost:5000/api" : "/api",
  timeout: 5000,
});

// Add a request interceptor
request.interceptors.request.use(
  (config) => {
    const token = sessionStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    message.error(error, 5)
    return Promise.reject(error);
  }
);

request.interceptors.response.use(
  (response) => {
    if (response.status !== 200) {
      const msg = response.data.msg || "Error";
        message.error(msg, 5)
        return Promise.reject(response.data.msg)
    } else {
        return Promise.resolve(response.data)
    }
  },
  (error) => {
    message.error(error.response.data.msg || error.message)

    if (error.response.status === 401) {
      sessionStorage.removeItem("token");
      setTimeout(() => {
        router.push("/login");
      }, 3000)
    }
    return Promise.reject(error.response.data.msg || error.message);
  }
);

export default request;
