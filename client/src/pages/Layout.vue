<template>
  <a-layout :style="layoutStyle">
    <a-layout-header :style="headerStyle">
      <a-menu @click="handleMenuClick" v-model:selectedKeys="current" mode="horizontal" :items="items" />
    </a-layout-header>
    <a-layout-content :style="contentStyle">
      <router-view></router-view>
    </a-layout-content>
    <a-layout-footer :style="footerStyle">
      <a-row align="middle" justify="center" style="padding: 1rem;">
          <p style="margin:0;">Copy right <b>@Smart Transcript</b></p>
      </a-row>
    </a-layout-footer>
  </a-layout>
</template>

<script setup>
import { h, ref } from 'vue';
import { HomeOutlined, MessageOutlined, UserOutlined } from '@ant-design/icons-vue';
import { useRouter, useRoute } from 'vue-router';

const route = useRoute()
const router = useRouter()
const current = ref([route.name.toLocaleLowerCase()]);

// watch router change and update current menu
router.afterEach((to, from) => {
  current.value = [to.name.toLocaleLowerCase()]
})

const items = ref([
  {
    key: 'home',
    icon: () => h(HomeOutlined),
    label: 'Home',
    title: 'Home',
  },
  {
    key: 'history',
    icon: () => h(MessageOutlined),
    label: 'History',
    title: 'History',
  },
  {
    key: 'user',
    icon: () => h(UserOutlined),
    label: 'User',
    title: 'User',
  },
]);

const handleMenuClick = function(item) {
  router.push(item.key)
}

const layoutStyle = {
  minHeight: "100%"
}

const headerStyle = {
  backgroundColor: "#fff",
  boxShadow: "0 1px 2px 0 rgba(0, 0, 0, 0.03), 0 1px 6px -1px rgba(0, 0, 0, 0.02), 0 2px 4px 0 rgba(0, 0, 0, 0.02)",
};

const contentStyle = {
  backgroundColor: "#fff",
  flex: 1,
  padding: "1rem 50px",
  // paddingBottom: "200px"
};

const footerStyle = {
  textAlign: "center",
  color: "#fff",
  backgroundColor: "#1677ff",
};
</script>
