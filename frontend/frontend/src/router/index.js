import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/views/LoginView.vue'
import DashboardView from '@/views/DashboardView.vue'
import PerbaikanTas from '@/views/perbaikan/PerbaikanTas.vue'
import Material from '@/views/material/MaterialView.vue'
import Pelanggan from '@/views/pelanggan/PelangganView.vue'
import PelangganInsert from '@/views/pelanggan/PelangganInsert.vue'
import PelangganUpdate from '@/views/pelanggan/PelangganUpdate.vue'
import Pemasok from '@/views/pemasok/PemasokView.vue'
import PemasokInsert from '@/views/pemasok/PemasokInsert.vue'
import PemasokUpdate from '@/views/pemasok/PemasokUpdate.vue'
import Laporan from '@/views/laporankeuangan/LaporanKeuangan.vue'
import Layanan from '@/views/layanan/LayananView.vue'

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
    path: '/pelanggan/insert',
    name: 'pelangganInsert',
    component: PelangganInsert
  },
  {
    path: '/pelanggan/:id/edit',
    name: 'pelangganUpdate',
    component: PelangganUpdate
  },
  {
    path: '/pemasok',
    name: 'pemasok',
    component: Pemasok
  },
  {
    path: '/pemasok/insert',
    name: 'pemasokInsert',
    component: PemasokInsert
  },
  {
    path: '/pemasok/:id/edit',
    name: 'pemasokUpdate',
    component: PemasokUpdate
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
