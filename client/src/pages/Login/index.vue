<template>
  <a-row id="login" justify="center" align="middle">
    <a-card :title="isSignup ? 'SignUp' : 'Login'">
      <a-form
        :model="formState"
        :label-col="{ span: 8 }"
        :wrapper-col="{ span: 16 }"
        @finish="onFinish"
      >
      <a-form-item
          v-if="isSignup"
          label="email"
          name="email"
          :rules="[{ required: true, validator: checkEmail, trigger: 'blur' }]"
        >
          <a-input v-model:value="formState.email" />
        </a-form-item>
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
          <a-input-password v-model:visible="visible" v-model:value="formState.password" />
        </a-form-item>

        <a-form-item
          v-if="isSignup"
          label="Confirm"
          name="confirm"
          :rules="[
            { required: true, validator: confirmPassword },
          ]"
        >
          <a-input-password v-model:visible="visible" v-model:value="formState.confirm" />
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
import { message } from "ant-design-vue";
import { useRouter } from "vue-router";
import request from "../../utils/request";

const router = useRouter();
const formState = reactive({
  email: "",
  username: "",
  password: "",
  confirm: "",
});
const visible = ref(false);
const isSignup = ref(false);

const switchMode = () => {
  isSignup.value = !isSignup.value;
};

const confirmPassword = async (rule, value) => {
  if (value !== formState.password) {
    throw new Error("The two passwords that you entered do not match!");
  }
};

const checkEmail = async (rule, value) => {
  if (!value) {
    throw new Error("Please input your email!");
  }
  // validate email
  const reg = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/;
  if (!reg.test(value)) {
    throw new Error("Please input a valid email!");
  }

  if (!isSignup.value) {
    return;
  }

  // check if email has been registered
  const res = await request.get("/user/checkEmail", { email: value });

  if (res.status === 'fail') {
    throw new Error("This email has been registered!");
  }
};

const onFinish = (values) => {
  if (isSignup.value) {
    request.post("/user/signup", values).then((res) => {
      sessionStorage.setItem("token", res.token);
      message.success("Signup successfully! Redirecting", 3);
      setTimeout(() => {
        router.push("/")
      }, 3000)
    });
  } else {
    request.post("/user/login", values).then((res) => {
      sessionStorage.setItem("token", res.token);
      message.success("Login successfully! Redirecting", 3);
      setTimeout(() => {
        router.push("/")
      }, 3000)
    });
  }
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
