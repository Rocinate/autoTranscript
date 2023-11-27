<template>
  <a-row id="login" justify="center" align="middle">
    <a-card :title="isSignup ? 'SignUp' : 'Login'">
      <a-form
        :model="formState"
        :label-col="{ span: 8 }"
        :wrapper-col="{ span: 16 }"
        @finish="onFinish"
        @finishFailed="onFinishFailed"
      >
        <a-form-item
          label="Username"
          name="username"
          :rules="[{ required: true, message: 'Please input your username!' }]"
        >
          <a-input v-model:value="formState.username" />
        </a-form-item>

        <a-form-item
          label="Password"
          name="password"
          :rules="[{ required: true, message: 'Please input your password!' }]"
        >
          <a-input-password v-model:value="formState.password" />
        </a-form-item>

        <a-form-item
          v-if="isSignup"
          label="Confirm"
          name="confirm"
          :rules="[
            { required: true, message: 'Please confirm your password!' },
          ]"
        >
          <a-input-password v-model:value="formState.confirm" />
        </a-form-item>

        <a-form-item :wrapper-col="{ offset: 8, span: 16 }">
          <a-button class="submit" type="primary" html-type="submit"
            >Submit</a-button
          >
          <a-button @click="switchMode">{{
            isSignup ? "Login" : "Signup"
          }}</a-button>
        </a-form-item>
      </a-form>
    </a-card>
  </a-row>
</template>

<script setup>
import { reactive, ref } from "vue";
const formState = reactive({
  username: "",
  password: "",
  confirm: ""
});

const isSignup = ref(false);

const switchMode = () => {
  isSignup.value = !isSignup.value;
};

const onFinish = (values) => {
  console.log("Success:", values);
};
const onFinishFailed = (errorInfo) => {
  console.log("Failed:", errorInfo);
};
</script>
<style scoped>
#login {
  height: 100%;
  width: 100%;
  background-color: #fff;
  flex: 1;
}

.submit {
  margin-right: 1rem;
}
</style>
