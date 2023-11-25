import { createRouter, createWebHistory } from 'vue-router'
import Ping from '../components/Ping.vue'
import Transcripts from '../components/Transcripts.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Transcripts',
      component: Transcripts,
    },
    {
      path: '/ping',
      name: 'ping',
      component: Ping
    },
  ]
})

export default router
