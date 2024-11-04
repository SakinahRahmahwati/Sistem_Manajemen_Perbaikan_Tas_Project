import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '@/views/DashboardView.vue'
import PerbaikanTas from '@/views/PerbaikanTas.vue'
import Material from '@/views/MaterialView.vue'

const routes = [
  {
    path: '/',
    name: 'dashboard',
    component: DashboardView,
    alias: '/dashboard'
  },
  {
    path: '/perbaikantas',
    name: 'perbaikantas',
    component: PerbaikanTas
  },
  {
    path: '/material',
    name: 'material',
    component: Material
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
