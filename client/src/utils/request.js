import axios from "axios";
import { message } from "ant-design-vue";

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
        message.error(response.data.msg, 5)
        return Promise.reject(response.data.msg)
    } else {
        return Promise.resolve(response.data)
    }
  },
  (error) => {
    message.error(error)
    return Promise.reject(error);
  }
);

export default request;
