<template>
    <div class="sidebar" data-color="white">
        <!--
         Tip 1: You can change the color of the sidebar using: data-color="purple | blue | green | orange | red"
 
         Tip 2: you can also add an image using data-image tag
     -->
        <div class="sidebar-wrapper">
            <div class="logo">
                <router-link to="" class="simple-text">
                    Dian Tas
                </router-link>
            </div>
            <ul class="nav">
                <li class="nav-item" :class="{ active: isActive('/dashboard') || isActive('/') }">
                    <router-link class="nav-link" to="/dashboard">
                        <i class="bi bi-house-door-fill"></i>
                        <p>Dashboard</p>
                    </router-link>
                </li>
                <li class="nav-item" :class="{ active: isActive('/perbaikantas') }">
                    <router-link class="nav-link" to="/perbaikantas">
                        <i class="bi bi-briefcase-fill"></i>
                        <p>Perbaikan Tas</p>
                    </router-link>
                </li>
                <li class="nav-item" :class="{ active: isActive('/jenislayanan') }">
                    <router-link class="nav-link" to="/jenislayanan">
                        <i class="bi bi-gear"></i>
                        <p>Jenis Layanan</p>
                    </router-link>
                </li>
                <li class="nav-item" :class="{ active: isActive('/material') }">
                    <router-link class="nav-link" to="/material">
                        <i class="bi bi-list-ul"></i>
                        <p>Material</p>
                    </router-link>
                </li>
                <li class="nav-item" :class="{ active: isActive('') }">
                    <router-link class="nav-link" to="/pelanggan">
                        <i class="bi bi-people-fill"></i>
                        <p>Pelanggan</p>
                    </router-link>
                </li>
                <li class="nav-item" :class="{ active: isActive('') }">
                    <router-link class="nav-link" to="/pemasok">
                        <i class="bi bi-boxes"></i>
                        <p>Pemasok</p>
                    </router-link>
                </li>
                <li class="nav-item" :class="{ active: isActive('') }">
                    <router-link class="nav-link" to="/laporankeuangan">
                        <i class="bi bi-cash-coin"></i>
                        <p>Laporan Keuangan</p>
                    </router-link>
                </li>
                <li class="nav-item" :class="{ active: isActive('') }">
                    <router-link class="nav-link" to="#">
                        <i class="bi bi-person-fill"></i>
                        <p>Akun</p>
                    </router-link>
                </li>
            </ul>
        </div>
    </div>
</template>

<script>
export default {
    methods: {
        isActive(route) {
            return this.$route.path === route;
        }
    }
}
</script>