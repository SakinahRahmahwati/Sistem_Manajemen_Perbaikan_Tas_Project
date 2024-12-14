import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/views/LoginView.vue'
import DashboardView from '@/views/DashboardView.vue'
import Perbaikan from '@/views/perbaikan/PerbaikanView.vue'
import Material from '@/views/material/MaterialView.vue'
import MaterialInsert from '@/views/material/MaterialInsert.vue'
import MaterialUpdate from '@/views/material/MaterialUpdate.vue'
import Pelanggan from '@/views/pelanggan/PelangganView.vue'
import PelangganInsert from '@/views/pelanggan/PelangganInsert.vue'
import PelangganUpdate from '@/views/pelanggan/PelangganUpdate.vue'
import Pemasok from '@/views/pemasok/PemasokView.vue'
import PemasokInsert from '@/views/pemasok/PemasokInsert.vue'
import PemasokUpdate from '@/views/pemasok/PemasokUpdate.vue'
import Laporan from '@/views/laporankeuangan/LaporanUangMasuk.vue'
import Layanan from '@/views/layanan/LayananView.vue'
import LayananInsert from '@/views/layanan/LayananInsert.vue'
import LayananUpdate from '@/views/layanan/LayananUpdate.vue'
import PerbaikanInsert from '@/views/perbaikan/PerbaikanInsert.vue'
import PengeluaranInsert from '@/views/pengeluaran/PengeluaranInsert.vue'
import LaporanUangKeluar from '@/views/laporankeuangan/LaporanUangKeluar.vue'
import AkunView from '@/views/akun/AkunView.vue'
import AkunInsert from '@/views/akun/AkunInsert.vue'
import LandingPage from '@/views/LandingPage.vue'

const routes = [
  {
    path: '/',
    name: 'LandingPage',
    component: LandingPage
  },
  {
    path: '/login',
    name: 'login',
    component: Login
  },
  { path: '/daftarpengguna', 
    component: AkunView,
    meta: { requiresAuth: true, role: ['Admin'] },  
  },
  { path: '/kelola_akun', 
    component: AkunInsert,
    meta: { requiresAuth: true, role: ['Admin'] },   
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: DashboardView,
  },
  {
    path: '/perbaikan',
    name: 'perbaikan',
    component: Perbaikan
  },
  {
    path: '/perbaikan/insert',
    name: 'perbaikanInsert',
    component: PerbaikanInsert
  },
  {
    path: '/material',
    name: 'material',
    component: Material
  },
  {
    path: '/material/insert',
    name: 'materialInsert',
    component: MaterialInsert
  },
  {
    path: '/material/:id/edit',
    name: 'materialUpdate',
    component: MaterialUpdate
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
    component: Pemasok,
    meta: { requiresAuth: true, role: ['Admin', 'Kepala Toko'] }, 
  },
  {
    path: '/pemasok/insert',
    name: 'pemasokInsert',
    component: PemasokInsert,
    meta: { requiresAuth: true, role: ['Admin', 'Kepala Toko'] }, 
  },
  {
    path: '/pemasok/:id/edit',
    name: 'pemasokUpdate',
    component: PemasokUpdate,
    meta: { requiresAuth: true, role: ['Admin', 'Kepala Toko'] }, 
  },
  {
    path: '/laporankeuangan',
    name: 'laporankeuangan',
    component: Laporan,
    meta: { requiresAuth: true, role: ['Admin', 'Kepala Toko'] }, 
  },
  {
    path: '/jenislayanan',
    name: 'layanan',
    component: Layanan
  },
  {
    path: '/jenislayanan/insert',
    name: 'layananInsert',
    component: LayananInsert
  },
  {
    path: '/jenislayanan/:id/edit',
    name: 'layananUpdate',
    component: LayananUpdate
  },
  {
    path: '/pengeluaran',
    name: 'pengeluaran',
    component: LaporanUangKeluar,
    meta: { requiresAuth: true, role: ['Admin', 'Kepala Toko'] }, 
  },
  {
    path: '/pengeluaran/insert',
    name: 'pengeluaranInsert',
    component: PengeluaranInsert,
    meta: { requiresAuth: true, role: ['Admin', 'Kepala Toko'] }, 
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
});

router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('token');  // Cek apakah ada token
  const userRole = localStorage.getItem('role');          // Cek peran pengguna
  
  // Pengecualian untuk halaman login dan landing page
  if (to.name === 'login' || to.name === 'LandingPage') {
    return next();  // Tidak perlu otentikasi untuk halaman ini
  }

  // Jika halaman memerlukan otentikasi dan pengguna belum login
  if (!isAuthenticated) {
    return next({ name: 'login' }); // Redirect ke halaman login jika belum login
  }

  // Jika halaman memerlukan peran tertentu dan peran pengguna tidak sesuai
  if (to.meta.role && !to.meta.role.includes(userRole)) {
    return next({ name: 'LandingPage' }); // Redirect ke halaman landing jika role tidak sesuai
  }

  // Lanjutkan ke halaman yang diminta jika sudah memenuhi syarat
  next();
});

export default router;
