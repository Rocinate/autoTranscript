import axios from "axios";
import { message } from "ant-design-vue";

const request = axios.create({
  baseURL: "/api",
  timeout: 5000,
});

request.interceptors.response.use(
  (response) => {
    if (response.status !== 200) {
        message.error(response.data.msg)
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
