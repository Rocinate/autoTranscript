import { createRouter, createWebHistory } from "vue-router";
import NProgress from 'nprogress';
import 'nprogress/nprogress.css';

import Layout from "../pages/Layout.vue";
import Home from "../pages/Home/index.vue";
import History from "../pages/History/index.vue";
import User from "../pages/User/index.vue";
import Login from '../pages/Login/index.vue'

// import { pinia } from "../store"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      component: Layout,
      redirect: "/home",
      children: [
        {
          path: "/home",
          name: "Home",
          component: Home,
          meta: {
            requiresAuth: false
          }
        },
        {
          path: "/history",
          name: "History",
          component: History,
          meta: {
            // requiresAuth: true
            requiresAuth: false
          }
        },
        {
          path: "/user",
          name: "User",
          component: User,
          meta: {
            requiresAuth: true
          }
        },
      ],
    },
    {
      path: "/login",
      name: "Login",
      component: Login,
      meta: {
        requiresAuth: false
      }
    }
  ],
});

// add guard to routes
router.beforeEach(async (to, from) => {
  if (to.meta.requiresAuth && to.name !== 'Login') {

    // check if user is authenticated
    const isAuthenticated = sessionStorage.getItem('token')
    if (!isAuthenticated) {
      return { name: 'Login' }
    }
  }
  NProgress.start()
})

router.afterEach(async (to, from) => {
  NProgress.done()
})

export default router;
