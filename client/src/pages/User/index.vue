<template>
  <a-row justify="center">
    <a-descriptions id="userInfo" title="User Info" layout="vertical" bordered>
      <a-descriptions-item label="Username">{{ info.username }}</a-descriptions-item>
      <a-descriptions-item label="Email">{{ info.email }}</a-descriptions-item>
      <a-descriptions-item label="Transcript Time">{{ info.transcription_count }}</a-descriptions-item>
      <a-descriptions-item label="Register Time"
        >{{ info.registered_on }}</a-descriptions-item
      >
    </a-descriptions>
  </a-row>
  <a-row justify="center">
    <a-button type="primary" @click="logout">Logout</a-button>
  </a-row>
</template>

<style scoped>
#userInfo {
  width: 60%;
}
</style>

<script setup>
import { reactive } from "vue";
import request from "../../utils/request";
import { useRouter } from "vue-router";

const router = useRouter();

const logout = () => {
  sessionStorage.removeItem("token");
  router.push("/login");
};

const info = reactive({
  username: "",
  email: "",
  registered_on: "",
  transcription_count: "",
});

const fetchData = () => {
  // fetch data from server
  request.get("/user/profile").then((res) => {
    Object.assign(info, res)
  });
};

fetchData()

</script>
