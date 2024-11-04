import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/views/LoginView.vue'
import DashboardView from '@/views/DashboardView.vue'
import PerbaikanTas from '@/views/PerbaikanTas.vue'
import Material from '@/views/MaterialView.vue'
import Pelanggan from '@/views/PelangganView.vue'
import Pemasok from '@/views/PemasokView.vue'
import Laporan from '@/views/LaporanKeuangan.vue'
import Layanan from '@/views/LayananView.vue'

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
    path: '/login',
    name: 'login',
    component: Login
  },
  {
    path: '/material',
    name: 'material',
    component: Material
  },
  {
    path: '/pelanggan',
    name: 'pelanggan',
    component: Pelanggan
  },
  {
    path: '/pemasok',
    name: 'pemasok',
    component: Pemasok
  },
  {
    path: '/laporankeuangan',
    name: 'laporankeuangan',
    component: Laporan
  },
  {
    path: '/jenislayanan',
    name: 'layanan',
    component: Layanan
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
